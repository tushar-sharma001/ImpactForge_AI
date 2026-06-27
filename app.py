import streamlit as st
import json
import re
import os

from typing import List, Optional
from pydantic import BaseModel

from google import genai

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="ImpactForge AI",
    page_icon="🌍",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>

.main{
    background:#f8fafc;
}

.block-container{
    padding-top:2rem;
}

.title{
    text-align:center;
    font-size:45px;
    font-weight:800;
    color:#1f2937;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:20px;
}

.card{
    background:white;
    padding:20px;
    border-radius:15px;
    box-shadow:0px 0px 10px rgba(0,0,0,0.08);
    margin-bottom:20px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("<div class='title'>🌍 ImpactForge AI</div>", unsafe_allow_html=True)

st.markdown(
"<div class='subtitle'>Multi-Agent Social Impact Project Designer powered by Google Gemini</div>",
unsafe_allow_html=True
)

st.divider()

# -----------------------------
# GEMINI
# -----------------------------

api_key = st.sidebar.text_input(
    "Gemini API Key",
    type="password"
)

if api_key == "":
    st.warning("Enter your Gemini API key.")
    st.stop()

client = genai.Client(api_key=api_key)

# -----------------------------
# JSON PARSER
# -----------------------------

def parse_json(text):

    text = re.sub(r"```json","",text)
    text = re.sub(r"```","",text)

    return json.loads(text.strip())

# -----------------------------
# GEMINI HELPER
# -----------------------------

def run_gemini(system_prompt,user_prompt):

    prompt=f"""

{system_prompt}

{user_prompt}

"""

    response=client.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt

    )

    return parse_json(response.text)

# -----------------------------
# MODELS
# -----------------------------

class ProjectIdea(BaseModel):

    problem:str
    location:str
    target_population:str
    budget:str

class ResearchOutput(BaseModel):

    summary:str
    root_causes:List[str]
    stakeholders:List[str]
    existing_solutions:List[str]
    challenges:List[str]

class SDG(BaseModel):

    number:int
    title:str
    reason:str

class SDGOutput(BaseModel):

    sdgs:List[SDG]

class Objective(BaseModel):

    id:str
    description:str
    sdg_alignment:List[str]

class Activity(BaseModel):

    id:str
    objective:str
    description:str
    timeline:str

class PlanningOutput(BaseModel):

    objectives:List[Objective]
    activities:List[Activity]
    timeline:List[dict]

class MetricsOutput(BaseModel):

    kpis:List[str]
    success_metrics:List[str]

class Risk(BaseModel):

    risk:str
    impact:str
    probability:str
    mitigation:str

class RiskOutput(BaseModel):

    risks:List[Risk]

class FundingSource(BaseModel):

    organization:str
    funding_type:str
    reason:str
    estimated_amount:str

class FundingOutput(BaseModel):

    funding_sources:List[FundingSource]

class EvaluationOutput(BaseModel):

    innovation_score:int
    feasibility_score:int
    impact_score:int
    sustainability_score:int
    overall_score:int
    feedback:str

class ReportOutput(BaseModel):

    executive_summary:str
    implementation_strategy:str
    expected_impact:str
    recommendations:str

class AgentState(BaseModel):

    project:ProjectIdea

    research:Optional[ResearchOutput]=None
    sdg:Optional[SDGOutput]=None
    planning:Optional[PlanningOutput]=None
    metrics:Optional[MetricsOutput]=None
    risks:Optional[RiskOutput]=None
    funding:Optional[FundingOutput]=None
    evaluation:Optional[EvaluationOutput]=None
    report:Optional[ReportOutput]=None


# ============================================================
# PROMPTS
# ============================================================

RESEARCH_PROMPT = """
You are a Senior Social Impact Research Analyst.

Analyse the given social problem.

Return ONLY valid JSON.

{
"summary":"",
"root_causes":[],
"stakeholders":[],
"existing_solutions":[],
"challenges":[]
}
"""

SDG_PROMPT = """
You are an expert in the United Nations Sustainable Development Goals.

Identify the most relevant SDGs for the problem.

Return ONLY valid JSON.

{
"sdgs":[
{
"number":1,
"title":"",
"reason":""
}
]
}
"""

PLAN_PROMPT = """
You are an experienced Social Impact Project Manager.

Create a complete implementation plan.

Return ONLY valid JSON.

{
"objectives":[
{
"id":"",
"description":"",
"sdg_alignment":[]
}
],
"activities":[
{
"id":"",
"objective":"",
"description":"",
"timeline":""
}
],
"timeline":[]
}
"""

METRICS_PROMPT = """
You are a Monitoring and Evaluation Expert.

Generate measurable KPIs.

Return ONLY valid JSON.

{
"kpis":[],
"success_metrics":[]
}
"""

RISK_PROMPT = """
You are a Risk Assessment Consultant.

Identify project risks.

Return ONLY valid JSON.

{
"risks":[
{
"risk":"",
"impact":"",
"probability":"",
"mitigation":""
}
]
}
"""

FUNDING_PROMPT = """
You are a Funding Consultant.

Recommend grants, CSR programmes and funding organisations.

Return ONLY valid JSON.

{
"funding_sources":[
{
"organization":"",
"funding_type":"",
"reason":"",
"estimated_amount":""
}
]
}
"""

EVALUATION_PROMPT = """
You are an International Hackathon Judge.

Evaluate the proposed project.

Return ONLY valid JSON.

{
"innovation_score":0,
"feasibility_score":0,
"impact_score":0,
"sustainability_score":0,
"overall_score":0,
"feedback":""
}
"""

REPORT_PROMPT = """
You are a Professional Proposal Writer.

Generate the final executive report.

Return ONLY valid JSON.

{
"executive_summary":"",
"implementation_strategy":"",
"expected_impact":"",
"recommendations":""
}
"""

# ============================================================
# RESEARCH AGENT
# ============================================================

def research_agent(state):

    user_prompt = f"""
Problem:
{state.project.problem}

Location:
{state.project.location}

Target Population:
{state.project.target_population}
"""

    data = run_gemini(
        RESEARCH_PROMPT,
        user_prompt
    )

    state.research = ResearchOutput(**data)

    return state


# ============================================================
# SDG AGENT
# ============================================================

def sdg_agent(state):

    user_prompt = f"""
Problem:
{state.project.problem}

Research Summary:
{state.research.summary}
"""

    data = run_gemini(
        SDG_PROMPT,
        user_prompt
    )

    state.sdg = SDGOutput(**data)

    return state


# ============================================================
# PLANNING AGENT
# ============================================================

def planning_agent(state):

    user_prompt = f"""
Problem:
{state.project.problem}

Research Summary:
{state.research.summary}

Relevant SDGs:
{", ".join([sdg.title for sdg in state.sdg.sdgs])}
"""

    data = run_gemini(
        PLAN_PROMPT,
        user_prompt
    )

    state.planning = PlanningOutput(**data)

    return state


# ============================================================
# METRICS AGENT
# ============================================================

def metrics_agent(state):

    user_prompt = f"""
Problem:
{state.project.problem}

Objectives:
{[o.description for o in state.planning.objectives]}
"""

    data = run_gemini(
        METRICS_PROMPT,
        user_prompt
    )

    state.metrics = MetricsOutput(**data)

    return state


# ============================================================
# RISK AGENT
# ============================================================

def risk_agent(state):

    user_prompt = f"""
Problem:
{state.project.problem}

Activities:
{[a.description for a in state.planning.activities]}
"""

    data = run_gemini(
        RISK_PROMPT,
        user_prompt
    )

    state.risks = RiskOutput(**data)

    return state


# ============================================================
# FUNDING AGENT
# ============================================================

def funding_agent(state):

    user_prompt = f"""
Problem:
{state.project.problem}

Budget:
{state.project.budget}

Location:
{state.project.location}
"""

    data = run_gemini(
        FUNDING_PROMPT,
        user_prompt
    )

    state.funding = FundingOutput(**data)

    return state


# ============================================================
# EVALUATION AGENT
# ============================================================

def evaluation_agent(state):

    user_prompt = f"""
Problem:
{state.project.problem}

Objectives:
{[o.description for o in state.planning.objectives]}

KPIs:
{state.metrics.kpis}
"""

    data = run_gemini(
        EVALUATION_PROMPT,
        user_prompt
    )

    state.evaluation = EvaluationOutput(**data)

    return state


# ============================================================
# REPORT AGENT
# ============================================================

def report_agent(state):

    user_prompt = f"""
Problem:
{state.project.problem}

Research:
{state.research.summary}

Objectives:
{[o.description for o in state.planning.objectives]}

KPIs:
{state.metrics.kpis}

Funding:
{[f.organization for f in state.funding.funding_sources]}
"""

    data = run_gemini(
        REPORT_PROMPT,
        user_prompt
    )

    state.report = ReportOutput(**data)

    return state

# ============================================================
# COORDINATOR
# ============================================================

def coordinator(state):

    progress = st.progress(0)

    progress.progress(10)

    state = research_agent(state)

    progress.progress(20)

    state = sdg_agent(state)

    progress.progress(35)

    state = planning_agent(state)

    progress.progress(50)

    state = metrics_agent(state)

    progress.progress(65)

    state = risk_agent(state)

    progress.progress(80)

    state = funding_agent(state)

    progress.progress(90)

    state = evaluation_agent(state)

    progress.progress(95)

    state = report_agent(state)

    progress.progress(100)

    return state


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("⚙ Project Details")

problem = st.sidebar.text_area(
    "Social Problem",
    "Reduce food waste in Delhi schools"
)

location = st.sidebar.text_input(
    "Location",
    "Delhi"
)

target_population = st.sidebar.text_input(
    "Target Population",
    "School Students"
)

budget = st.sidebar.text_input(
    "Budget",
    "50000 INR"
)

generate = st.sidebar.button(
    "🚀 Generate Project"
)

# ============================================================
# MAIN
# ============================================================

if generate:

    project = ProjectIdea(

        problem=problem,

        location=location,

        target_population=target_population,

        budget=budget

    )

    state = AgentState(

        project=project

    )

    with st.spinner("Running AI Agents..."):

        state = coordinator(state)

    st.success("Project Generated Successfully!")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "Research",
            "Planning",
            "Execution",
            "Evaluation",
            "Final Report"
        ]
    )

    # -----------------------------------------------------

    with tab1:

        st.header("Research Summary")

        st.write(state.research.summary)

        st.subheader("Root Causes")

        for cause in state.research.root_causes:

            st.write("•", cause)

        st.subheader("Stakeholders")

        for s in state.research.stakeholders:

            st.write("•", s)

        st.subheader("Relevant SDGs")

        for sdg in state.sdg.sdgs:

            st.success(
                f"SDG {sdg.number}: {sdg.title}"
            )

    # -----------------------------------------------------

    with tab2:

        st.header("Objectives")

        for obj in state.planning.objectives:

            st.info(obj.description)

        st.header("Activities")

        for act in state.planning.activities:

            st.write("•", act.description)

    # -----------------------------------------------------

    with tab3:

        col1,col2=st.columns(2)

        with col1:

            st.subheader("KPIs")

            for k in state.metrics.kpis:

                st.write("•",k)

        with col2:

            st.subheader("Success Metrics")

            for s in state.metrics.success_metrics:

                st.write("•",s)

        st.divider()

        st.subheader("Risks")

        for r in state.risks.risks:

            with st.expander(r.risk):

                st.write("Impact:",r.impact)

                st.write("Probability:",r.probability)

                st.write("Mitigation:",r.mitigation)

        st.divider()

        st.subheader("Funding")

        for f in state.funding.funding_sources:

            st.success(f.organization)

            st.write(f.reason)

            st.caption(f.estimated_amount)

    # -----------------------------------------------------

    with tab4:

        c1,c2,c3,c4,c5=st.columns(5)

        c1.metric(
            "Innovation",
            state.evaluation.innovation_score
        )

        c2.metric(
            "Feasibility",
            state.evaluation.feasibility_score
        )

        c3.metric(
            "Impact",
            state.evaluation.impact_score
        )

        c4.metric(
            "Sustainability",
            state.evaluation.sustainability_score
        )

        c5.metric(
            "Overall",
            state.evaluation.overall_score
        )

        st.divider()

        st.write(state.evaluation.feedback)

    # -----------------------------------------------------

    with tab5:

        st.header("Executive Summary")

        st.write(
            state.report.executive_summary
        )

        st.header("Implementation Strategy")

        st.write(
            state.report.implementation_strategy
        )

        st.header("Expected Impact")

        st.write(
            state.report.expected_impact
        )

        st.header("Recommendations")

        st.write(
            state.report.recommendations
        )


# ============================================================
# EXPORT REPORT
# ============================================================

        report = f"""
# ImpactForge AI Report

## Problem
{state.project.problem}

## Research Summary
{state.research.summary}

## SDGs
"""

        for sdg in state.sdg.sdgs:
            report += f"\n- SDG {sdg.number}: {sdg.title}"

        report += "\n\n## Objectives\n"

        for obj in state.planning.objectives:
            report += f"- {obj.description}\n"

        report += "\n## KPIs\n"

        for kpi in state.metrics.kpis:
            report += f"- {kpi}\n"

        report += "\n## Risks\n"

        for risk in state.risks.risks:
            report += f"- {risk.risk} | Mitigation: {risk.mitigation}\n"

        report += "\n## Funding Sources\n"

        for fund in state.funding.funding_sources:
            report += f"- {fund.organization}\n"

        report += "\n## Overall Evaluation\n"

        report += f"{state.evaluation.overall_score}/100\n\n"

        report += state.evaluation.feedback

        report += "\n\n## Executive Summary\n"

        report += state.report.executive_summary

        st.download_button(
            "📄 Download Report",
            report,
            file_name="ImpactForge_Report.md",
            mime="text/markdown"
        )

# ============================================================
# SIDEBAR INFO
# ============================================================

st.sidebar.markdown("---")

st.sidebar.success("ImpactForge AI")

st.sidebar.write(
    """
**Version:** 1.0

Google Gemini Powered

Multi-Agent AI System
"""
)

# ============================================================
# ABOUT
# ============================================================

with st.expander("ℹ About ImpactForge AI"):

    st.write("""
ImpactForge AI is a Multi-Agent AI system that transforms a social problem
into a complete implementation-ready project proposal.

Agents Included

• Research Agent

• SDG Mapping Agent

• Planning Agent

• Metrics Agent

• Risk Assessment Agent

• Funding Recommendation Agent

• Evaluation Agent

• Report Generation Agent

Built using:

- Google Gemini
- Streamlit
- Pydantic
- Python
""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
"""
<div style='text-align:center;color:gray;'>

### 🌍 ImpactForge AI

Multi-Agent Social Impact Project Designer

Built with ❤️ using Google Gemini & Streamlit

</div>
""",
unsafe_allow_html=True
)
