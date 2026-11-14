import sys
import streamlit as st
from pathlib import Path

# ==================================================
# 1. APPLICATION CONFIGURATION
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from workflow.graph import run_workflow

st.set_page_config(
    page_title="DocuAgent | AI Documentation",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==================================================
# 2. SESSION STATE
# ==================================================

if "workflow_result" not in st.session_state:
    st.session_state.workflow_result = None

if "final_documentation" not in st.session_state:
    st.session_state.final_documentation = ""

if "project_path" not in st.session_state:
    st.session_state.project_path = str(BASE_DIR / "sample_project")


# ==================================================
# 3. PROFESSIONAL BLACK THEME
# ==================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #080808;
    color: #f5f5f5;
}

[data-testid="stHeader"] {
    background: #080808;
}

[data-testid="stAppViewContainer"] {
    background: #080808;
}

[data-testid="stSidebar"] {
    background: #101010;
    border-right: 1px solid #262626;
}

[data-testid="stSidebar"] * {
    color: #e5e5e5;
}

[data-testid="stSidebar"] hr {
    border-color: #292929;
}

/* Main headings */

.main-title {
    font-size: 36px;
    font-weight: 800;
    letter-spacing: -1.2px;
    color: #ffffff;
    margin-bottom: 5px;
}

.gradient-text {
    background: linear-gradient(90deg, #60a5fa, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    font-size: 14px;
    color: #929292;
    margin-bottom: 28px;
    line-height: 1.7;
}

.section-heading {
    color: #ffffff;
    font-size: 21px;
    font-weight: 700;
    margin-top: 14px;
    margin-bottom: 15px;
}

/* Containers */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #111111;
    border: 1px solid #292929;
    border-radius: 13px;
}

div[data-testid="stMetric"] {
    background: #111111;
    border: 1px solid #292929;
    padding: 18px;
    border-radius: 12px;
}

[data-testid="stMetricLabel"] {
    color: #a3a3a3 !important;
}

[data-testid="stMetricValue"] {
    color: #ffffff !important;
    font-weight: 700;
}

/* Agent cards */

.agent-card {
    background: #111111;
    border: 1px solid #292929;
    border-radius: 12px;
    padding: 19px;
    min-height: 145px;
    transition: 0.2s ease;
}

.agent-card:hover {
    border-color: #3b82f6;
    background: #151515;
}

.agent-number {
    font-size: 12px;
    font-weight: 700;
    color: #60a5fa;
    margin-bottom: 12px;
}

.agent-title {
    color: #ffffff;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 9px;
}

.agent-description {
    color: #999999;
    font-size: 12px;
    line-height: 1.7;
}

/* Buttons */

.stButton > button {
    background: #2563eb;
    color: #ffffff;
    border: 1px solid #2563eb;
    border-radius: 9px;
    min-height: 43px;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #1d4ed8;
    border-color: #3b82f6;
    color: #ffffff;
}

.stDownloadButton > button {
    background: #171717;
    color: #ffffff;
    border: 1px solid #404040;
    border-radius: 9px;
    min-height: 43px;
    font-weight: 600;
}

.stDownloadButton > button:hover {
    background: #262626;
    color: #ffffff;
    border-color: #60a5fa;
}

/* Input fields */

.stTextInput input,
.stTextArea textarea {
    background: #171717 !important;
    color: #ffffff !important;
    border: 1px solid #353535 !important;
    border-radius: 8px !important;
}

.stTextInput label,
.stTextArea label {
    color: #d4d4d4 !important;
    font-weight: 600;
}

.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #3b82f6 !important;
}

/* Tabs */

.stTabs [data-baseweb="tab-list"] {
    background: #111111;
    border-bottom: 1px solid #292929;
    gap: 12px;
}

.stTabs [data-baseweb="tab"] {
    color: #a3a3a3;
    font-weight: 600;
}

.stTabs [aria-selected="true"] {
    color: #60a5fa !important;
}

/* Expanders */

[data-testid="stExpander"] {
    background: #111111;
    border: 1px solid #292929;
    border-radius: 9px;
}

[data-testid="stExpander"] summary {
    color: #ffffff;
}

/* Text */

p, li, label {
    color: #d4d4d4;
}

.stCaption {
    color: #888888;
}

hr {
    border-color: #292929;
}

/* Footer */

.footer {
    text-align: center;
    color: #737373;
    font-size: 12px;
    line-height: 1.9;
    padding: 25px 0 12px 0;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 4. SIDEBAR
# ==================================================

with st.sidebar:

    st.markdown(
        """
        <div style="padding:10px 0 5px 0;">
            <div style="font-size:27px;font-weight:800;color:white;">
                📘 DocuAgent
            </div>
            <div style="font-size:11px;color:#777;margin-top:5px;">
                INTELLIGENT DOCUMENTATION PLATFORM
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### WORKSPACE")

    st.markdown("🏠  Dashboard")
    st.markdown("📋  Documentation Plan")
    st.markdown("📝  Documentation Editor")
    st.markdown("🔍  Validation Report")

    st.divider()

    st.markdown("### AI TECHNOLOGY STACK")

    st.markdown("""
    **Core Language**

    Python

    **AI Model**

    Qwen 2.5 Coder 7B

    **Local Model API**

    Ollama

    **Agent Framework**

    LangGraph

    **User Interface**

    Streamlit
    """)

    st.divider()

    st.markdown("### WORKFLOW")

    st.markdown("""
    <div style="font-size:13px;line-height:2.3;color:#b5b5b5;">
        <span style="color:#60a5fa;">01</span> Information Extraction<br>
        <span style="color:#60a5fa;">02</span> Documentation Planning<br>
        <span style="color:#60a5fa;">03</span> Documentation Generation<br>
        <span style="color:#60a5fa;">04</span> Documentation Validation
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown(
        """
        <div style="color:#737373;font-size:11px;">
            DOCUAGENT · VERSION 1.0.0<br>
            AI-POWERED DOCUMENTATION
        </div>
        """,
        unsafe_allow_html=True
    )


# ==================================================
# 5. MAIN HEADER
# ==================================================

st.markdown(
    """
    <div class="main-title">
        Intelligent <span class="gradient-text">Documentation</span>
    </div>
    <div class="subtitle">
        An agentic AI platform that transforms software source code
        into structured, accurate and validated technical documentation.
    </div>
    """,
    unsafe_allow_html=True
)


# ==================================================
# 6. PROJECT CONFIGURATION
# ==================================================

st.markdown(
    '<div class="section-heading">01 / Project Configuration</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    st.markdown("#### Source Project")

    project_path = st.text_input(
        "Project Folder Path",
        value=st.session_state.project_path,
        placeholder="Enter your project folder path"
    )

    st.caption(
        "Provide the complete local folder path containing your "
        "source code, configuration files and README."
    )

    generate_clicked = st.button(
        "🚀  Generate Technical Documentation",
        type="primary",
        use_container_width=True
    )


# ==================================================
# 7. EXECUTE AGENTIC WORKFLOW
# ==================================================

if generate_clicked:

    source_path = Path(project_path.strip()).expanduser()

    if not source_path.exists() or not source_path.is_dir():

        st.error("Invalid folder path. Please enter an existing project folder.")

    else:

        st.session_state.project_path = str(source_path)

        try:

            with st.status(
                "DocuAgent is executing the AI workflow...",
                expanded=True
            ) as status:

                st.write("01 · Extracting source code information")
                st.write("02 · Planning technical documentation")
                st.write("03 · Generating documentation with Qwen")
                st.write("04 · Validating documentation quality")

                result = run_workflow(source_path)

                st.session_state.workflow_result = result
                st.session_state.final_documentation = (
                    result.get("documentation", "")
                )

                status.update(
                    label="AI workflow completed successfully",
                    state="complete",
                    expanded=False
                )

            st.success(
                "Technical documentation has been generated successfully."
            )

        except Exception as error:

            st.error(f"Workflow execution failed: {error}")


# ==================================================
# 8. DISPLAY GENERATED RESULTS
# ==================================================

if st.session_state.workflow_result is not None:

    result = st.session_state.workflow_result

    plan = result.get("documentation_plan", {})
    documentation = result.get("documentation", "")
    validation = result.get("validation_report", {})

    if not st.session_state.final_documentation:
        st.session_state.final_documentation = documentation

    st.divider()

    st.markdown(
        '<div class="section-heading">02 / Project Analytics</div>',
        unsafe_allow_html=True
    )

    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            "PROJECT",
            plan.get("project_title", "Software Project")
        )

    with metric2:
        st.metric(
            "FILES ANALYZED",
            len(result.get("project_info", {}).get("files", []))
        )

    with metric3:
        st.metric(
            "DOCUMENTATION SECTIONS",
            len(plan.get("documentation_sections", []))
        )

    with metric4:
        st.metric(
            "VALIDATION",
            validation.get("validation_status", "N/A")
        )

    # ----------------------------------------------
    # AGENT WORKFLOW CARDS
    # ----------------------------------------------

    st.markdown(
        '<div class="section-heading">03 / Multi-Agent Architecture</div>',
        unsafe_allow_html=True
    )

    agents = [
        (
            "01",
            "Information Extraction",
            "Analyzes source files and extracts functions, classes, imports and configurations."
        ),
        (
            "02",
            "Documentation Planning",
            "Creates a structured documentation plan based on extracted project information."
        ),
        (
            "03",
            "Documentation Generation",
            "Uses the local Qwen model to generate technical documentation."
        ),
        (
            "04",
            "Documentation Validation",
            "Checks documentation quality, missing sections and unsupported claims."
        )
    ]

    columns = st.columns(4)

    for column, agent in zip(columns, agents):

        with column:

            st.markdown(
                f"""
                <div class="agent-card">
                    <div class="agent-number">AGENT {agent[0]}</div>
                    <div class="agent-title">{agent[1]}</div>
                    <div class="agent-description">{agent[2]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.divider()

    # ----------------------------------------------
    # RESULT TABS
    # ----------------------------------------------

    tab1, tab2, tab3 = st.tabs([
        "📋  Documentation Plan",
        "📝  Documentation Editor",
        "🔍  Validation Report"
    ])


    # ==============================================
    # TAB 1 - PLAN
    # ==============================================

    with tab1:

        st.markdown("### Documentation Planning")

        st.write(
            plan.get(
                "project_description",
                "No project description available."
            )
        )

        st.divider()

        st.markdown("#### Planned Sections")

        sections = plan.get("documentation_sections", [])

        if sections:

            for index, section in enumerate(sections, 1):

                with st.expander(
                    f"{index:02d}  ·  {section.get('section', 'Section')}"
                ):

                    st.write(
                        section.get("purpose", "No purpose specified.")
                    )

        else:
            st.info("No documentation sections were returned.")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("#### Technologies Used")

            for technology in plan.get("technologies", []):
                st.markdown(f"- {technology}")

        with col2:

            st.markdown("#### Important Features")

            for feature in plan.get("important_features", []):
                st.markdown(f"- {feature}")

        st.markdown("#### Files to Document")

        for file_name in plan.get("files_to_document", []):
            st.markdown(f"- `{file_name}`")


    # ==============================================
    # TAB 2 - EDITOR
    # ==============================================

    with tab2:

        st.markdown("### Technical Documentation Editor")

        st.caption(
            "Review, modify, save and download the AI-generated document."
        )

        edited_documentation = st.text_area(
            "Documentation Content",
            value=st.session_state.final_documentation,
            height=500,
            key="documentation_editor"
        )

        st.session_state.final_documentation = edited_documentation

        save_col, download_col = st.columns(2)

        with save_col:

            if st.button(
                "💾 Save Final Documentation",
                type="primary",
                use_container_width=True
            ):

                final_file = OUTPUT_DIR / "final_documentation.md"

                with open(
                    final_file,
                    "w",
                    encoding="utf-8"
                ) as file:

                    file.write(edited_documentation)

                st.success("Final documentation saved successfully.")

        with download_col:

            st.download_button(
                "⬇️ Download Documentation",
                data=edited_documentation,
                file_name="final_documentation.md",
                mime="text/markdown",
                use_container_width=True
            )

        with st.expander("Preview Formatted Document"):

            st.markdown(edited_documentation)


    # ==============================================
    # TAB 3 - VALIDATION
    # ==============================================

    with tab3:

        st.markdown("### Documentation Quality Assessment")

        status_value = validation.get(
            "validation_status",
            "Unavailable"
        )

        score_value = validation.get(
            "quality_score",
            "N/A"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.metric("QUALITY SCORE", score_value)

        with col2:
            st.metric("VALIDATION STATUS", status_value)

        st.divider()

        st.markdown("#### Validation Checks")

        checks = validation.get("checks", [])

        if checks:

            for check in checks:

                name = check.get("check", "Validation Check")
                check_status = check.get("status", "UNKNOWN")
                observation = check.get("observation", "")

                if check_status.upper() == "PASS":

                    st.success(f"**{name}**\n\n{observation}")

                else:

                    st.warning(f"**{name}**\n\n{observation}")

        else:

            st.info("No validation checks are available.")

        st.divider()

        st.markdown("#### Missing Sections")

        missing = validation.get("missing_sections", [])

        if missing:

            for item in missing:
                st.warning(str(item))

        else:

            st.success("No missing sections were reported.")

        st.markdown("#### Unsupported Claims")

        unsupported = validation.get("unsupported_claims", [])

        if unsupported:

            for item in unsupported:
                st.warning(str(item))

        else:

            st.success("No unsupported claims were reported.")

        st.markdown("#### Improvement Suggestions")

        suggestions = validation.get("suggestions", [])

        if suggestions:

            for item in suggestions:
                st.markdown(f"- {item}")

        else:

            st.info("No suggestions were returned.")

        st.markdown("#### Final Observation")

        st.info(
            validation.get(
                "final_observation",
                "No final observation available."
            )
        )


# ==================================================
# 9. INITIAL DASHBOARD
# ==================================================

else:

    st.divider()

    st.markdown(
        '<div class="section-heading">How DocuAgent Works</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown("### 🔎 Analyze")

        st.write(
            "Automatically examine project files and identify "
            "the structure, functions, classes and configurations."
        )

    with col2:

        st.markdown("### 🧠 Generate")

        st.write(
            "Create a documentation plan and generate detailed "
            "technical content using a local AI model."
        )

    with col3:

        st.markdown("### ✓ Validate")

        st.write(
            "Evaluate the generated document and identify "
            "missing information and unsupported claims."
        )


# ==================================================
# 10. FOOTER
# ==================================================

st.markdown(
    """
    <div class="footer">
        <strong style="color:#d4d4d4;">DOCUAGENT</strong>
        <br>
        Agentic AI System for Automated Technical Documentation
        <br>
        Powered by Python · LangGraph · Ollama · Qwen 2.5 Coder 7B · Streamlit
    </div>
    """,
    unsafe_allow_html=True
)