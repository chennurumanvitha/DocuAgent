# DocuAgent – Agentic AI System for Automated Technical Documentation

## 1. Project Overview

DocuAgent is an Agentic AI-based system that automates the process of generating technical documentation for software projects.

It uses multiple specialized AI agents that collaborate through a LangGraph workflow. The system extracts project information, plans documentation, generates technical content, and validates the final output.

The project uses Ollama with the Qwen 2.5 Coder 7B model to perform local AI processing.

## 2. Objectives

- Automate technical documentation generation.
- Extract information from source code and project files.
- Create structured documentation using AI.
- Validate documentation for completeness and accuracy.
- Demonstrate collaboration between multiple AI agents.

## 3. Technologies Used

- **Python:** Main programming language.
- **Streamlit:** Interactive web application.
- **LangGraph:** Multi-agent workflow orchestration.
- **Ollama:** Local large language model execution.
- **Qwen 2.5 Coder 7B:** AI model used for documentation tasks.
- **AST:** Python source-code analysis.
- **JSON and Markdown:** Structured data and documentation formats.

## 4. System Architecture

The system consists of four specialized agents:

1. **Information Extraction Agent:** Extracts functions, classes, imports, and project details.
2. **Documentation Planning Agent:** Creates a structured documentation plan.
3. **Documentation Generation Agent:** Generates technical documentation using the local AI model.
4. **Documentation Validation Agent:** Checks documentation completeness and identifies unsupported claims or missing information.

The agents execute sequentially through a LangGraph workflow and are accessed through a Streamlit interface.

## 5. Project Structure

```text
DocuAgent/
│
├── agents/
│   ├── extractor.py
│   ├── planner.py
│   ├── generator.py
│   └── validator.py
│
├── workflow/
│   └── graph.py
│
├── sample_project/
│   ├── main.py
│   ├── config.json
│   ├── README.md
│   └── tasks.json
│
├── outputs/
├── screenshots/
├── diagrams/
│   ├── architecture.mmd
│   └── architecture.md
│
├── app.py
├── main.py
├── requirements.txt
└── README.md
```

## 6. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd DocuAgent
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 3: Activate the Environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 4: Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### Step 5: Install and Start Ollama

Install Ollama and download the required model:

```bash
ollama pull qwen2.5-coder:7b
```

Make sure the Ollama service is running.

## 7. Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

Open the local application in your browser:

```text
http://localhost:8501
```

Select the project directory and start the documentation workflow.

## 8. Generated Outputs

The system generates the following files:

- `documentation_plan.json` – Structured documentation plan.
- `technical_documentation.md` – Generated technical documentation.
- `validation_report.json` – Documentation validation results.
- `final_documentation.md` – Final documentation available through the application.

## 9. Sample Implementation and Testing

The system was tested using a sample Task Management System project.

The workflow successfully executed all four agents:

- Information extraction completed.
- Documentation planning completed.
- Documentation generation completed.
- Documentation validation completed.

The validation output reported **PASS** for the sample execution.

## 10. Limitations

- Documentation quality depends on the available source-code information.
- Local model performance depends on system hardware and available resources.
- Complex projects may require additional processing time.
- AI-generated documentation should be reviewed before production use.
- Validation results do not guarantee that every generated statement is correct.

## 11. Future Enhancements

- Support for additional programming languages.
- Automatic documentation updates when source code changes.
- Improved validation and code-documentation consistency checks.
- Export documentation into PDF and HTML formats.
- Integration with GitHub repositories.

## 12. Conclusion

DocuAgent demonstrates how Agentic AI and multi-agent collaboration can automate technical documentation. By combining Python, LangGraph, Streamlit, Ollama, and Qwen 2.5 Coder, the project provides a local AI-powered workflow for extracting, planning, generating, and validating software documentation.