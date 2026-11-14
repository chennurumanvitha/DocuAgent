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


def create_documentation_plan(project_info):
    """Use Qwen to create a structured documentation plan."""

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
You are a professional technical documentation planning agent.

Analyze the supplied project information.

PROJECT INFORMATION:
{json.dumps(simplified_info, indent=2)}

Create a clear and concise technical documentation plan.

Include these sections:
1. Project Overview
2. Features
3. Technologies Used
4. Project Architecture
5. File Structure
6. Installation and Setup
7. Main Functions
8. Configuration
9. Usage Instructions
10. Limitations
11. Conclusion

Return ONLY valid JSON in this format:

{{
    "project_title": "Project title",
    "project_description": "Short project description",
    "documentation_sections": [
        {{
            "section": "Section name",
            "purpose": "What this section explains"
        }}
    ],
    "important_features": [],
    "technologies": [],
    "files_to_document": []
}}

Important rules:
- Use only the supplied project information.
- Do not invent features or functions.
- Keep descriptions concise.
- Return valid JSON only.
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.2,
            "num_predict": 1200
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=900
    )

    response.raise_for_status()

    result = response.json()
    plan = json.loads(result["response"])

    return plan


def save_documentation_plan(plan):
    """Save the generated documentation plan."""

    output_directory = BASE_DIR / "outputs"
    output_directory.mkdir(parents=True, exist_ok=True)

    output_file = output_directory / "documentation_plan.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(plan, file, indent=4)

    return output_file


if __name__ == "__main__":

    print("\nDOCUAGENT - PLANNING AGENT")
    print("=" * 50)

    print("\nExtracting project information...")

    sample_path = BASE_DIR / "sample_project"
    project_info = extract_project_info(sample_path)

    print("Project:", project_info["project_name"])
    print("Total files:", len(project_info["files"]))

    print("\nSending information to Qwen...")
    print("Creating documentation plan...")
    print("Please wait. The local AI model may take several minutes.")

    try:
        plan = create_documentation_plan(project_info)

        output_file = save_documentation_plan(plan)

        print("\nDOCUMENTATION PLAN GENERATED")
        print("=" * 50)

        print(json.dumps(plan, indent=4))

        print("\nPlan saved successfully!")
        print("Location:", output_file)

    except requests.exceptions.ConnectionError:
        print("\nERROR: Ollama is not running.")
        print("Please make sure Ollama is running.")

    except requests.exceptions.Timeout:
        print("\nERROR: Model response timed out.")
        print("Try again after closing other applications using system memory.")

    except (requests.exceptions.RequestException, ValueError, KeyError) as error:
        print("\nERROR:", error)