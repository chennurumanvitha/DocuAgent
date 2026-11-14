import ast
import json
from pathlib import Path


def extract_python_details(file_path):
    """Extract functions, classes and imports from Python files."""

    with open(file_path, "r", encoding="utf-8") as file:
        source_code = file.read()

    try:
        tree = ast.parse(source_code)
    except SyntaxError:
        return {
            "functions": [],
            "classes": [],
            "imports": [],
            "source_code": source_code,
            "error": "Unable to parse Python file"
        }

    functions = []
    classes = []
    imports = []

    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append(node.name)

        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)

        elif isinstance(node, ast.Import):
            for item in node.names:
                imports.append(item.name)

        elif isinstance(node, ast.ImportFrom):
            imports.append(node.module or "")

    return {
        "functions": sorted(set(functions)),
        "classes": sorted(set(classes)),
        "imports": sorted(set(imports)),
        "source_code": source_code
    }


def extract_project_info(project_directory):
    """Extract technical information from the project directory."""

    project_path = Path(project_directory).resolve()

    project_info = {
        "project_name": project_path.name,
        "project_path": str(project_path),
        "files": [],
        "python_details": {},
        "configuration": {},
        "readme_content": ""
    }

    supported_extensions = {".py", ".json", ".md"}

    if not project_path.exists():
        raise FileNotFoundError(
            f"Project directory not found: {project_path}"
        )

    for file_path in sorted(project_path.rglob("*")):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in supported_extensions:
            continue

        if any(part.startswith(".") for part in file_path.relative_to(project_path).parts):
            continue

        if file_path.stat().st_size > 500_000:
            continue

        relative_path = str(file_path.relative_to(project_path))

        project_info["files"].append(relative_path)

        if file_path.suffix.lower() == ".py":

            details = extract_python_details(file_path)

            project_info["python_details"][relative_path] = details

        elif file_path.suffix.lower() == ".json":

            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    project_info["configuration"][relative_path] = json.load(file)

            except (json.JSONDecodeError, OSError):
                project_info["configuration"][relative_path] = (
                    "Invalid or unreadable JSON"
                )

        elif file_path.name.lower() == "readme.md":

            with open(file_path, "r", encoding="utf-8") as file:
                project_info["readme_content"] = file.read()

    return project_info


if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent

    SAMPLE_PROJECT = BASE_DIR / "sample_project"

    result = extract_project_info(SAMPLE_PROJECT)

    print("\nINFORMATION EXTRACTION RESULT")
    print("=" * 50)

    print(json.dumps(result, indent=4))

    print("\nEXTRACTION SUMMARY")
    print("=" * 50)
    print("Project:", result["project_name"])
    print("Total files:", len(result["files"]))

    for file_name, details in result["python_details"].items():
        print("\nPython file:", file_name)
        print("Functions:", details["functions"])
        print("Classes:", details["classes"])
        print("Imports:", details["imports"])

    print("\nExtraction completed successfully!")