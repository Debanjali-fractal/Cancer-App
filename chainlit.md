# Cancer Data Analysis Chatbot

## Overview
The **Cancer Data Analysis Chatbot** is an AI-powered assistant designed to analyze and provide insights from cancer-related datasets. Built using Python, Pandas, Google Gemini AI, LangChain, and Chainlit, this chatbot offers seamless query-based interaction, enabling users to extract meaningful data, generate visualizations, and receive detailed analysis in natural language.

---

## Features

### 1. **AI-Powered Query Resolution**
   - Handles user queries related to cancer datasets.
   - Provides answers in natural language, supported by data-driven insights.
   - Executes Python code dynamically to compute and extract required information.

### 2. **Data Visualization**
   - Automatically generates charts and graphs for distribution-related questions.
   - Visual aids enhance understanding of trends and patterns.

### 3. **Comprehensive Data Analysis**
   - Summarizes distributions, trends, and outliers from the dataset.
   - Offers actionable insights for further exploration.

### 4. **Conversation History Management**
   - Displays conversation history on request.
   - Allows clearing the history for a fresh start.

### 5. **Error Handling**
   - Provides clear error messages and suggestions for fixes.
   - Ensures user-friendly interaction, even for non-technical users.

---

## Technologies Used

### **Core Libraries and Frameworks**
- **Python**: Primary programming language for data analysis.
- **Pandas**: For data manipulation and analysis.
- **Matplotlib & Seaborn**: For generating visualizations.
- **LangChain**: Manages prompt engineering and LLM interactions.
- **Google Gemini AI**: Powers intelligent query responses and code generation.
- **Chainlit**: Provides the chatbot interface.

### **Additional Tools**
- **Jupyter Notebook**: Used for testing and prototyping.
- **VS Code**: Development environment.

---

## Setup and Installation

### Prerequisites
- Python 3.9+
- Pip package manager
- Required libraries (see below)

### Installation Steps
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install Required Libraries**:
   ```bash
   pip install pandas matplotlib seaborn langchain chainlit
   ```

3. **Download Dataset**:
   - Place the dataset in the appropriate directory (e.g., `data/`).

4. **Run the Chatbot**:
   ```bash
   chainlit run app.py
   ```

---

## Dataset Description
This project uses a cancer dataset with the following columns:

| Column Name                  | Description                                                                 |
|------------------------------|-----------------------------------------------------------------------------|
| `patientID`                  | Unique identifier for each patient.                                         |
| `encounterID`                | Unique identifier for each hospital encounter.                             |
| `diagnosisCodeDescription`   | Description of the diagnosis code for the cancer type.                     |
| `Cancer Diagnosis Category`  | Category of the cancer diagnosis.                                          |
| `Specialty`                  | Medical specialty handling the case.                                       |
| `Encounter Type`             | Type of hospital encounter (e.g., outpatient, inpatient).                  |
| `encounterAdmitDateTime`     | Date and time of patient admission.                                        |
| `encounterDischargeDateTime` | Date and time of patient discharge.                                        |
| `Facility Code`              | Identifier for the medical facility.                                       |
| `ageAtEncounter`             | Age of the patient at the time of the encounter.                           |
| `ageGroup`                   | Age group of the patient.                                                  |
| `LOS(hours)`                 | Length of stay in hours.                                                   |
| `readmission`                | Whether the patient was readmitted (Yes/No).                               |
| `YearQuarter`                | Quarter and year of the encounter.                                         |
| `gender`                     | Gender of the patient.                                                     |
| `nationality`                | Nationality of the patient.                                                |
| `national`                   | Additional national information (if applicable).                          |

---

## Example Queries
- "What is the distribution of cancer cases by type?"
- "Which age group has the highest number of malignant cancer cases?"
- "Show the average length of stay by cancer category."
- "Generate a visualization of readmission rates by age group."

---

## Contribution Guidelines
1. Fork the repository and create a new branch for your changes.
2. Commit changes with meaningful messages.
3. Submit a pull request for review.

---

## Troubleshooting
- **Dataset Not Found**: Ensure the dataset is placed in the correct directory and the file path is updated in the code.
- **Python Errors**: Verify all dependencies are installed.
- **Visualization Issues**: Ensure Matplotlib and Seaborn are properly installed.

---

## Future Enhancements
- Integrate more advanced visualization libraries (e.g., Plotly).
- Add support for larger datasets using Dask.
- Expand natural language capabilities for more complex queries.
- Implement a dashboard for visual analysis.

---

## License
This project is licensed under the MIT License.

---

## Contact
For questions or issues, please contact:
- **Name**: Debanjali Goswami
- **Email**: debanjali.goswami@fractal.ai
- **GitHub**: [Your GitHub Profile Here]

