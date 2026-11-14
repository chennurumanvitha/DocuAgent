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


def validate_documentation(documentation, project_info):
    """Validate generated documentation using Qwen."""

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
        "configuration": project_info["configuration"]
    }

    prompt = f"""
You are a technical documentation validation agent.

Review the generated documentation against the actual project information.

PROJECT INFORMATION:
{json.dumps(simplified_info, indent=2)}

GENERATED DOCUMENTATION:
{documentation}

Check:
1. Whether all required sections are present.
2. Whether important project files are documented.
3. Whether function names match the source code.
4. Whether unsupported features or claims are included.
5. Whether important information is missing.
6. Whether the documentation is clear and understandable.

Return ONLY valid JSON in this format:

{{
    "validation_status": "PASS or NEEDS IMPROVEMENT",
    "quality_score": 0,
    "checks": [
        {{
            "check": "Check name",
            "status": "PASS or FAIL",
            "observation": "Explanation"
        }}
    ],
    "missing_sections": [],
    "unsupported_claims": [],
    "suggestions": [],
    "final_observation": "Overall validation result"
}}

Be strict and evidence-based.
Do not invent problems.
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.1,
            "num_predict": 1500
        }
    }

    response = requests.post(
        OLLAMA_URL,
        json=payload,
        timeout=900
    )

    response.raise_for_status()

    result = response.json()
    validation = json.loads(result["response"])

    return validation


def save_validation_report(validation):
    """Save validation results as JSON."""

    output_directory = BASE_DIR / "outputs"
    output_directory.mkdir(parents=True, exist_ok=True)

    output_file = output_directory / "validation_report.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(validation, file, indent=4)

    return output_file


if __name__ == "__main__":

    print("\nDOCUAGENT - VALIDATION AGENT")
    print("=" * 50)

    try:
        documentation_file = (
            BASE_DIR / "outputs" / "technical_documentation.md"
        )

        if not documentation_file.exists():
            raise FileNotFoundError(
                "Technical documentation not found. Run generator.py first."
            )

        print("\nLoading generated documentation...")

        with open(documentation_file, "r", encoding="utf-8") as file:
            documentation = file.read()

        if not documentation.strip():
            raise ValueError("Generated documentation is empty.")

        print("Documentation loaded successfully.")

        print("\nExtracting project information...")

        sample_path = BASE_DIR / "sample_project"
        project_info = extract_project_info(sample_path)

        print("Project:", project_info["project_name"])

        print("\nSending documentation to Qwen...")
        print("Checking quality and accuracy...")
        print("Please wait. Validation may take several minutes.")

        validation = validate_documentation(
            documentation,
            project_info
        )

        output_file = save_validation_report(validation)

        print("\nVALIDATION COMPLETED")
        print("=" * 50)

        print(json.dumps(validation, indent=4))

        print("\nValidation report saved successfully!")
        print("Location:", output_file)

    except requests.exceptions.ConnectionError:
        print("\nERROR: Ollama is not running.")

    except requests.exceptions.Timeout:
        print("\nERROR: Model response timed out.")

    except (requests.exceptions.RequestException, ValueError, KeyError) as error:
        print("\nERROR:", error)

    except FileNotFoundError as error:
        print("\nERROR:", error)