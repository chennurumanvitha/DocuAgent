import sys
from pathlib import Path
from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

BASE_DIR = Path(__file__).resolve().parent.parent

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from agents.extractor import extract_project_info
from agents.planner import (
    create_documentation_plan,
    save_documentation_plan
)
from agents.generator import (
    generate_documentation,
    save_documentation
)
from agents.validator import (
    validate_documentation,
    save_validation_report
)


class WorkflowState(TypedDict, total=False):
    project_path: str
    project_info: dict
    documentation_plan: dict
    documentation: str
    validation_report: dict
    status: str


def extraction_node(state: WorkflowState):
    """Extract information from the source project."""

    print("\n[1/4] INFORMATION EXTRACTION AGENT")
    print("-" * 45)

    project_info = extract_project_info(state["project_path"])

    print("Project:", project_info["project_name"])
    print("Files detected:", len(project_info["files"]))
    print("Extraction completed.")

    return {"project_info": project_info}


def planning_node(state: WorkflowState):
    """Create a documentation plan."""

    print("\n[2/4] DOCUMENTATION PLANNING AGENT")
    print("-" * 45)

    plan = create_documentation_plan(state["project_info"])

    output_file = save_documentation_plan(plan)

    print("Documentation plan created.")
    print("Saved:", output_file)

    return {"documentation_plan": plan}


def generation_node(state: WorkflowState):
    """Generate technical documentation."""

    print("\n[3/4] DOCUMENTATION GENERATION AGENT")
    print("-" * 45)

    documentation = generate_documentation(
        state["project_info"],
        state["documentation_plan"]
    )

    output_file = save_documentation(documentation)

    print("Technical documentation generated.")
    print("Saved:", output_file)

    return {"documentation": documentation}


def validation_node(state: WorkflowState):
    """Validate the generated documentation."""

    print("\n[4/4] DOCUMENTATION VALIDATION AGENT")
    print("-" * 45)

    validation = validate_documentation(
        state["documentation"],
        state["project_info"]
    )

    output_file = save_validation_report(validation)

    print("Validation completed.")
    print("Status:", validation.get("validation_status"))
    print("Saved:", output_file)

    return {
        "validation_report": validation,
        "status": "COMPLETED"
    }


def build_workflow():
    """Build and compile the LangGraph workflow."""

    workflow = StateGraph(WorkflowState)

    workflow.add_node("extractor", extraction_node)
    workflow.add_node("planner", planning_node)
    workflow.add_node("generator", generation_node)
    workflow.add_node("validator", validation_node)

    workflow.add_edge(START, "extractor")
    workflow.add_edge("extractor", "planner")
    workflow.add_edge("planner", "generator")
    workflow.add_edge("generator", "validator")
    workflow.add_edge("validator", END)

    return workflow.compile()


def run_workflow(project_path):
    """Execute the complete documentation workflow."""

    app = build_workflow()

    initial_state = {
        "project_path": str(project_path),
        "status": "RUNNING"
    }

    result = app.invoke(initial_state)

    return result


if __name__ == "__main__":

    print("\nDOCUAGENT - LANGGRAPH WORKFLOW")
    print("=" * 55)

    sample_project = BASE_DIR / "sample_project"

    try:
        result = run_workflow(sample_project)

        print("\nWORKFLOW EXECUTION COMPLETED")
        print("=" * 55)

        print("Status:", result.get("status"))
        print(
            "Validation:",
            result.get("validation_report", {}).get(
                "validation_status",
                "Not available"
            )
        )

        print("\nGenerated files:")
        print("1. outputs/documentation_plan.json")
        print("2. outputs/technical_documentation.md")
        print("3. outputs/validation_report.json")

    except Exception as error:
        print("\nWORKFLOW EXECUTION FAILED")
        print("Error:", error)
        raise