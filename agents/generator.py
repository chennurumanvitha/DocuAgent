import json
import requests
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from agents.extractor import extract_project_info

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5-coder:7b"


def generate_documentation(project_info, documentation_plan):
    """Generate technical documentation using Qwen."""

    simplified_info = {
        "project_name": project_info["project_name"],
        "files": project_info["files"],
        "python_details": {
            name: {
                "functions": details.get("functions", []),
                "classes": details.get("classes", []),
                "imports": details.get("imports", [])
            }
            for name, details in project_info["python_details"].items()
        },
        "configuration": project_info["configuration"],
        "readme_content": project_info["readme_content"]
    }

    prompt = f"""
You are an expert technical documentation generation agent.

Generate complete and professional technical documentation
for the supplied software project.

PROJECT INFORMATION:
{json.dumps(simplified_info, indent=2)}

DOCUMENTATION PLAN:
{json.dumps(documentation_plan, indent=2)}

Write the documentation in Markdown format.

Include the following sections:

# Project Title

## 1. Project Overview
Explain the purpose of the application.

## 2. Features
Describe the features supported by the actual source code.

## 3. Technologies Used
List the programming languages and technologies identified.

## 4. Project Architecture
Explain how the files and components work together.

## 5. File Structure
Show the project folder structure.

## 6. Installation and Setup
Give the steps required to run the project.

## 7. Main Functions
Explain each important function and its purpose.

## 8. Configuration
Explain the available configuration files.

## 9. Usage Instructions
Provide practical instructions and examples.

## 10. Limitations
Mention limitations supported by the available project information.
Do not invent limitations.

## 11. Conclusion
Summarize the project.

IMPORTANT RULES:
- Use only the supplied project information.
- Do not invent functions, features, files or technologies.
- Explain the actual source code accurately.
- Use clear and simple technical language.
- Include relevant Python code examples only when supported
  by the supplied source code.
- Return Markdown documentation only.
- Do not return JSON.
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_predict": 3000
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=900
    )

    response.raise_for_status()

    result = response.json()
    documentation = result.get("response", "").strip()

    if not documentation:
        raise ValueError("The model returned empty documentation.")

    return documentation


def save_documentation(documentation):
    """Save generated documentation as a Markdown file."""

    output_directory = BASE_DIR / "outputs"
    output_directory.mkdir(parents=True, exist_ok=True)

    output_file = output_directory / "technical_documentation.md"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(documentation)

    return output_file


if __name__ == "__main__":

    print("\nDOCUAGENT - DOCUMENTATION GENERATION AGENT")
    print("=" * 55)

    try:
        print("\nExtracting project information...")

        sample_path = BASE_DIR / "sample_project"
        project_info = extract_project_info(sample_path)

        print("Project:", project_info["project_name"])
        print("Files detected:", len(project_info["files"]))

        plan_file = BASE_DIR / "outputs" / "documentation_plan.json"

        if not plan_file.exists():
            raise FileNotFoundError(
                "Documentation plan not found. Run planner.py first."
            )

        print("\nLoading documentation plan...")

        with open(plan_file, "r", encoding="utf-8") as file:
            documentation_plan = json.load(file)

        print("Plan loaded successfully.")

        print("\nSending information to Qwen...")
        print("Generating technical documentation...")
        print("Please wait. This may take several minutes.")

        documentation = generate_documentation(
            project_info,
            documentation_plan
        )

        output_file = save_documentation(documentation)

        print("\nDOCUMENTATION GENERATED SUCCESSFULLY")
        print("=" * 55)

        print("\nGenerated documentation preview:\n")
        print(documentation[:2000])

        print("\nFull documentation saved at:")
        print(output_file)

    except requests.exceptions.ConnectionError:
        print("\nERROR: Ollama is not running.")

    except requests.exceptions.Timeout:
        print("\nERROR: Model response timed out.")

    except (requests.exceptions.RequestException, ValueError, KeyError) as error:
        print("\nERROR:", error)

    except FileNotFoundError as error:
        print("\nERROR:", error)