import pandas as pd
import google.generativeai as genai
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import os
import warnings
import chainlit as cl

warnings.filterwarnings('ignore')

# Set your Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyBeM3p8WXFVQ6x19aJX252tpWkHm11ckXg"  # Replace with your actual key
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Load the CSV data
try:
    df = pd.read_csv(r'C:\Users\debanjali.goswami\Downloads\DEBANJALI\Cancer-Data-Structured\data_Cancer_v2_Merged Data 2.csv')
    df.rename(columns={"YQ (YearQuarter)": "YQ"}, inplace=True)
except FileNotFoundError:
    print("Error: Dataset not found. Ensure the correct path.")
    exit()
except pd.errors.ParserError:
    print("Error: Could not parse the dataset.")
    exit()

# Initialize the Gemini LLM
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)

# Conversation memory for Chainlit
memory = ConversationBufferMemory(memory_key="conversation_history", input_key="query")

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=["query", "dataframe_head", "conversation_history"],
    template=(
         '''
         You are a Python expert working with Pandas DataFrames.  
Here is the head of the DataFrame:  
{dataframe_head}  

Conversation so far:  
{conversation_history}  

You are also an expert in English, hence you can read and understand what the given question asks for.  
Write Python pandas code to answer the question. The code should:  
- Use appropriate aggregations, groupings, and filters.  
- Carefully interpret the query and identify relevant columns.  
- Read the dataset using the provided CSV path:  
  (r'C:\\Users\debanjali.goswami\Downloads\DEBANJALI\Cancer-Data-Structured\data_Cancer_v2_Merged Data 2.csv') (use this path when loading data into a DataFrame).  
- Ensure the code references the exact column names provided:  
  - patientID  
  - encounterID  
  - diagnosisCodeDescription  
  - Cancer Diagnosis Category  
  - Specialty  
  - Encounter Type  
  - encounterAdmitDateTime  
  - encounterDischargeDateTime  
  - Facility Code  (tip: use this column when asked for cancer providers specifically.)
  - ageAtEncounter  
  - ageGroup  
  - LOS(hours)  
  - readmission  
  - YearQuarter  
  - gender  
  - nationality  
  - national  

- Handle textual and categorical filtering with proper techniques:  
  - Use case-insensitive filtering for text columns when needed (`case=False`).  
  - Exclude rows with missing values appropriately (`na=False`).  
  - Use `diagnosisCodeDescription` for descriptive filtering, and `Cancer Diagnosis Category` for categorical analysis. For example:  
    - For malignant tumors, check if `'Malignant'` is present in `Cancer Diagnosis Category`.  
    - For non-malignant tumors, ensure `'Malignant'` is not present in `Cancer Diagnosis Category`.  

- Handle date and time columns carefully:  
  - Always use proper datetime parsing when working with dates.  
  - Avoid using `.unique()` unless explicitly required in the query.  
  - Generate **all relevant discharge and admit dates** grouped as per query requirements.  

- Ensure correctness and completeness:  
  - Use concise, readable variable names for intermediate steps.  
  - Provide well-structured Pandas expressions.  
  - Include appropriate column references in every step.  
  - Always output both category/label and corresponding value when finding the highest or lowest value.  
  - Name result columns clearly when performing calculations (e.g., averages, counts).  
  - Sort results appropriately (e.g., descending for counts or numerical data).  
- When identifying the highest or lowest value, include both the category/label and its corresponding value in the output.
- If performing calculations (e.g., averages, counts), name the result columns accordingly.
- Write code that is executable without syntax errors:  
  - Begin the code with `import pandas as pd`.  
  - Ensure the code does not contain extra trailing text.
  ##- You should also explain what you are analysing from the dataset, while answering the question.  
'''
"""Task: Write the full Python Pandas code to answer the following query:  
{query}"""

"Please write the complete code starting with `import pandas as pd` and ending with a line that outputs the final result."  
    ),
)

# Create the LLM Chain
llm_chain = LLMChain(llm=llm, prompt=prompt_template, memory=memory)

# Create the Pandas agent
pandas_agent = create_pandas_dataframe_agent(
       llm, df, verbose=False, allow_dangerous_code=True, handle_parsing_errors=True,
       prefix=(
        "You are an expert in Python and Pandas DataFrame operations.\n"
        "Your task is to execute the Python code accurately on the given DataFrame.\n"
        "Please execute the given code correctly, read it carefully, I don't want 'I dont know' as an answer."
        "Ensure correctness, and return only the result of the execution. Do not provide explanations or extra output."
    )
)

last_query = None
# Chainlit App
@cl.on_chat_start
async def start():
    await cl.Message(
        content=(
            "Welcome to the Cancer Data Analysis Chatbot! 🎉\n\n"
            "This application allows you to explore and analyze a dataset about cancer cases. "
            "You can ask questions like:\n"
            "- What is the distribution of cancer cases by type?\n"
            "- Which category has the highest number of cases?\n"
            "- Show discharge dates for various groups.\n\n"
            "Feel free to ask your questions!"
        )
    ).send()

@cl.on_message
async def handle_message(message):
    global last_query
    user_input = message.content.strip().lower()
    if "wrong answer" in user_input or "incorrect" in user_input or "rectify" in user_input:
        if last_query:
            await cl.Message(content="Apologies! Let me recheck and correct the response. Please wait a moment.").send()
            try:
                # Reanalyze the last query
                response = llm_chain.run({
                    "query": last_query,
                    "dataframe_head": str(df.head())
                })
                pandas_code = response.strip('`').replace("```python", "").replace("```", "").strip()

                # Display the corrected code
                await cl.Message(content=f"Corrected Pandas Code:\n```python\n{pandas_code}\n```").send()

                # Execute the corrected code
                result = pandas_agent.run(pandas_code)
                await cl.Message(content=f"Corrected Result:\n{result}").send()
            except Exception as e:
                await cl.Message(content=f"Error during correction: {e}").send()
        else:
            await cl.Message(content="I don't have a previous query to reanalyze. Please provide a new query.").send()
        return

    # Regular query processing
    try:
        last_query = message.content  # Store the query
        response = llm_chain.run({
            "query": last_query,
            "dataframe_head": str(df.head())
        })
        pandas_code = response.strip('`').replace("```python", "").replace("```", "").strip()

        # Display the generated code
        await cl.Message(content=f"Generated Pandas Code:\n```python\n{pandas_code}\n```").send()

        # Execute the code using the Pandas Agent
        result = pandas_agent.run(pandas_code)

        # Display the execution result
        await cl.Message(content=f"Execution Result:\n{result}").send()
    except Exception as e:
        await cl.Message(content=f"Error: {e}").send()