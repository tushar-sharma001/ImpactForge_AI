import streamlit as st
import json
import re
from typing import List, Optional
from pydantic import BaseModel
from google import genai

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="ImpactForge AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.main{
    background:#f7f9fc;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

.title{
    text-align:center;
    font-size:48px;
    font-weight:800;
    color:#1e293b;
}

.subtitle{
    text-align:center;
    color:#64748b;
    font-size:20px;
    margin-bottom:20px;
}

.card{
    background:white;
    padding:18px;
    border-radius:12px;
    border:1px solid #e5e7eb;
    margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# TITLE
# ==========================================================

st.markdown(
"""
<div class="title">
🌍 ImpactForge AI
</div>
""",
unsafe_allow_html=True
)

st.markdown(
"""
<div class="subtitle">
Multi-Agent Social Impact Project Designer powered by Google Gemini
</div>
""",
unsafe_allow_html=True
)

st.divider()

# ==========================================================
# GEMINI API
# ==========================================================

try:

    api_key = st.secrets["GEMINI_API_KEY"]

except Exception:

    st.sidebar.warning("Using Manual API Key")

    api_key = st.sidebar.text_input(
        "Gemini API Key",
        type="password"
    )

if not api_key:

    st.info("Please enter your Gemini API Key.")
    st.stop()

client = genai.Client(
    api_key=api_key
)

# ==========================================================
# JSON PARSER
# ==========================================================

def parse_json(text):

    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    start = text.find("{")
    end = text.rfind("}") + 1

    if start == -1 or end == 0:
        raise ValueError("No JSON found.")

    return json.loads(text[start:end])

# ==========================================================
# GEMINI HELPER
# ==========================================================

def run_gemini(system_prompt, user_prompt):

    prompt = f"""

{system_prompt}

----------------------------------

{user_prompt}

Return ONLY valid JSON.

"""

    try:

        response = client.models.generate_content(

            model="gemini-2.5-flash",

            contents=prompt

        )

        return parse_json(response.text)

    except Exception as e:

        st.error(e)

        st.stop()

# ==========================================================
# INPUT MODEL
# ==========================================================

class ProjectIdea(BaseModel):
    problem: str
    location: str
    target_population: str
    budget: str


# ==========================================================
# RESEARCH OUTPUT
# ==========================================================

class ResearchOutput(BaseModel):
    summary: str
    root_causes: List[str]
    stakeholders: List[str]
    existing_solutions: List[str]
    challenges: List[str]


# ==========================================================
# SDG OUTPUT
# ==========================================================

class SDG(BaseModel):
    number: int
    title: str
    reason: str


class SDGOutput(BaseModel):
    sdgs: List[SDG]


# ==========================================================
# PROJECT PLANNING
# ==========================================================

class Objective(BaseModel):
    id: str
    description: str
    sdg_alignment: List[str]


class Activity(BaseModel):
    id: str
    objective: str
    description: str
    timeline: str


class Timeline(BaseModel):
    phase: str
    duration: str


class PlanningOutput(BaseModel):
    objectives: List[Objective]
    activities: List[Activity]
    timeline: List[Timeline]


# ==========================================================
# METRICS
# ==========================================================

class KPI(BaseModel):
    name: str
    target: str


class MetricsOutput(BaseModel):
    kpis: List[KPI]
    success_metrics: List[str]


# ==========================================================
# RISK
# ==========================================================

class Risk(BaseModel):
    risk: str
    impact: str
    probability: str
    mitigation: str


class RiskOutput(BaseModel):
    risks: List[Risk]


# ==========================================================
# FUNDING
# ==========================================================

class FundingSource(BaseModel):
    organization: str
    funding_type: str
    reason: str
    estimated_amount: str


class FundingOutput(BaseModel):
    funding_sources: List[FundingSource]


# ==========================================================
# EVALUATION
# ==========================================================

class EvaluationOutput(BaseModel):
    innovation_score: int
    feasibility_score: int
    impact_score: int
    sustainability_score: int
    overall_score: int
    feedback: str


# ==========================================================
# FINAL REPORT
# ==========================================================

class ReportOutput(BaseModel):
    executive_summary: str
    implementation_strategy: str
    expected_impact: str
    recommendations: str


# ==========================================================
# SHARED AGENT STATE
# ==========================================================

class AgentState(BaseModel):

    project: ProjectIdea

    research: Optional[ResearchOutput] = None

    sdg: Optional[SDGOutput] = None

    planning: Optional[PlanningOutput] = None

    metrics: Optional[MetricsOutput] = None

    risks: Optional[RiskOutput] = None

    funding: Optional[FundingOutput] = None

    evaluation: Optional[EvaluationOutput] = None

    report: Optional[ReportOutput] = None

# ==========================================================
# RESEARCH PROMPT
# ==========================================================

RESEARCH_PROMPT = """
You are a Senior Social Impact Research Analyst.

Your task is to analyse the given social problem.

Return ONLY valid JSON.

{
    "summary":"",
    "root_causes":[
        "string"
    ],
    "stakeholders":[
        "string"
    ],
    "existing_solutions":[
        "string"
    ],
    "challenges":[
        "string"
    ]
}
"""


# ==========================================================
# SDG PROMPT
# ==========================================================

SDG_PROMPT = """
You are an expert in the United Nations Sustainable Development Goals.

Identify the three most relevant SDGs for the given problem.

Return ONLY valid JSON.

{
    "sdgs":[
        {
            "number":2,
            "title":"Zero Hunger",
            "reason":"Reason"
        }
    ]
}
"""


# ==========================================================
# PLANNING PROMPT
# ==========================================================

PLAN_PROMPT = """
You are a Professional Social Impact Project Manager.

Create an implementation plan.

Return ONLY valid JSON.

{
    "objectives":[
        {
            "id":"OBJ1",
            "description":"",
            "sdg_alignment":[
                "SDG 2"
            ]
        }
    ],

    "activities":[
        {
            "id":"ACT1",
            "objective":"OBJ1",
            "description":"",
            "timeline":"Month 1"
        }
    ],

    "timeline":[
        {
            "phase":"Planning",
            "duration":"Month 1"
        }
    ]
}
"""


# ==========================================================
# KPI PROMPT
# ==========================================================

METRICS_PROMPT = """
You are a Monitoring & Evaluation Expert.

Generate measurable KPIs.

Return ONLY valid JSON.

{
    "kpis":[
        {
            "name":"",
            "target":""
        }
    ],

    "success_metrics":[
        "string"
    ]
}
"""


# ==========================================================
# RISK PROMPT
# ==========================================================

RISK_PROMPT = """
You are a Risk Management Consultant.

Identify implementation risks.

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


# ==========================================================
# FUNDING PROMPT
# ==========================================================

FUNDING_PROMPT = """
You are a CSR and Grant Consultant.

Recommend suitable funding organisations.

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


# ==========================================================
# EVALUATION PROMPT
# ==========================================================

EVALUATION_PROMPT = """
You are an International Hackathon Judge.

Evaluate the project objectively.

Return ONLY valid JSON.

{
    "innovation_score":90,
    "feasibility_score":90,
    "impact_score":90,
    "sustainability_score":90,
    "overall_score":90,
    "feedback":""
}
"""


# ==========================================================
# REPORT PROMPT
# ==========================================================

REPORT_PROMPT = """
You are an Expert Proposal Writer.

Generate a professional final report.

Return ONLY valid JSON.

{
    "executive_summary":"",
    "implementation_strategy":"",
    "expected_impact":"",
    "recommendations":""
}
"""

# ==========================================================
# RESEARCH AGENT
# ==========================================================

def research_agent(state: AgentState):

    user_prompt = f"""
Problem:
{state.project.problem}

Location:
{state.project.location}

Target Population:
{state.project.target_population}

Budget:
{state.project.budget}
"""

    data = run_gemini(
        RESEARCH_PROMPT,
        user_prompt
    )

    state.research = ResearchOutput(**data)

    return state


# ==========================================================
# SDG AGENT
# ==========================================================

def sdg_agent(state: AgentState):

    user_prompt = f"""
Problem:
{state.project.problem}

Research Summary:
{state.research.summary}

Root Causes:
{", ".join(state.research.root_causes)}
"""

    data = run_gemini(
        SDG_PROMPT,
        user_prompt
    )

    state.sdg = SDGOutput(**data)

    return state


# ==========================================================
# PLANNING AGENT
# ==========================================================

def planning_agent(state: AgentState):

    sdgs = ", ".join(
        [
            f"SDG {s.number}: {s.title}"
            for s in state.sdg.sdgs
        ]
    )

    user_prompt = f"""
Problem:
{state.project.problem}

Research Summary:
{state.research.summary}

Relevant SDGs:
{sdgs}

Generate a practical implementation plan.
"""

    data = run_gemini(
        PLAN_PROMPT,
        user_prompt
    )

    state.planning = PlanningOutput(**data)

    return state


# ==========================================================
# COORDINATOR (PART 1)
# ==========================================================

def coordinator(state: AgentState):

    progress = st.progress(0)

    status = st.empty()

    status.info("🔎 Running Research Agent...")
    progress.progress(20)

    state = research_agent(state)

    status.info("🌍 Running SDG Agent...")
    progress.progress(40)

    state = sdg_agent(state)

    status.info("📋 Running Planning Agent...")
    progress.progress(60)

    state = planning_agent(state)

    return state

# ==========================================================
# METRICS AGENT
# ==========================================================

def metrics_agent(state: AgentState):

    objectives = "\n".join(
        [
            f"- {obj.description}"
            for obj in state.planning.objectives
        ]
    )

    user_prompt = f"""
Problem:
{state.project.problem}

Objectives:
{objectives}

Generate measurable KPIs and success metrics.
"""

    data = run_gemini(
        METRICS_PROMPT,
        user_prompt
    )

    state.metrics = MetricsOutput(**data)

    return state


# ==========================================================
# RISK AGENT
# ==========================================================

def risk_agent(state: AgentState):

    activities = "\n".join(
        [
            f"- {act.description}"
            for act in state.planning.activities
        ]
    )

    user_prompt = f"""
Problem:
{state.project.problem}

Activities:
{activities}

Identify the major implementation risks.
"""

    data = run_gemini(
        RISK_PROMPT,
        user_prompt
    )

    state.risks = RiskOutput(**data)

    return state


# ==========================================================
# FUNDING AGENT
# ==========================================================

def funding_agent(state: AgentState):

    sdgs = ", ".join(
        [
            sdg.title
            for sdg in state.sdg.sdgs
        ]
    )

    user_prompt = f"""
Problem:
{state.project.problem}

Location:
{state.project.location}

Budget:
{state.project.budget}

Relevant SDGs:
{sdgs}

Suggest grants, CSR programs and funding opportunities.
"""

    data = run_gemini(
        FUNDING_PROMPT,
        user_prompt
    )

    state.funding = FundingOutput(**data)

    return state


# ==========================================================
# COORDINATOR UPDATE
# ==========================================================

def coordinator(state: AgentState):

    progress = st.progress(0)

    status = st.empty()

    # -------------------------

    status.info("🔍 Research Agent")
    progress.progress(10)

    state = research_agent(state)

    # -------------------------

    status.info("🌍 SDG Agent")
    progress.progress(25)

    state = sdg_agent(state)

    # -------------------------

    status.info("📋 Planning Agent")
    progress.progress(45)

    state = planning_agent(state)

    # -------------------------

    status.info("📈 Metrics Agent")
    progress.progress(60)

    state = metrics_agent(state)

    # -------------------------

    status.info("⚠ Risk Agent")
    progress.progress(75)

    state = risk_agent(state)

    # -------------------------

    status.info("💰 Funding Agent")
    progress.progress(90)

    state = funding_agent(state)

    progress.progress(100)

    status.success("Completed Successfully!")

    return state

# ==========================================================
# EVALUATION AGENT
# ==========================================================

def evaluation_agent(state: AgentState):

    objectives = "\n".join(
        [obj.description for obj in state.planning.objectives]
    )

    kpis = "\n".join(
        [f"{kpi.name} - {kpi.target}" for kpi in state.metrics.kpis]
    )

    user_prompt = f"""
Problem:
{state.project.problem}

Objectives:
{objectives}

KPIs:
{kpis}

Evaluate this project.
"""

    data = run_gemini(
        EVALUATION_PROMPT,
        user_prompt
    )

    state.evaluation = EvaluationOutput(**data)

    return state


# ==========================================================
# REPORT AGENT
# ==========================================================

def report_agent(state: AgentState):

    objectives = "\n".join(
        [obj.description for obj in state.planning.objectives]
    )

    funding = "\n".join(
        [f.organization for f in state.funding.funding_sources]
    )

    user_prompt = f"""
Problem:
{state.project.problem}

Research Summary:
{state.research.summary}

Objectives:
{objectives}

Funding Sources:
{funding}

Generate a professional final report.
"""

    data = run_gemini(
        REPORT_PROMPT,
        user_prompt
    )

    state.report = ReportOutput(**data)

    return state


# ==========================================================
# COMPLETE COORDINATOR
# ==========================================================

def coordinator(state: AgentState):

    progress = st.progress(0)

    status = st.empty()

    # --------------------------------------------

    status.info("🔍 Research Agent Running...")
    progress.progress(10)

    state = research_agent(state)

    # --------------------------------------------

    status.info("🌍 SDG Mapping Agent Running...")
    progress.progress(25)

    state = sdg_agent(state)

    # --------------------------------------------

    status.info("📋 Planning Agent Running...")
    progress.progress(40)

    state = planning_agent(state)

    # --------------------------------------------

    status.info("📊 Metrics Agent Running...")
    progress.progress(55)

    state = metrics_agent(state)

    # --------------------------------------------

    status.info("⚠ Risk Agent Running...")
    progress.progress(70)

    state = risk_agent(state)

    # --------------------------------------------

    status.info("💰 Funding Agent Running...")
    progress.progress(82)

    state = funding_agent(state)

    # --------------------------------------------

    status.info("⭐ Evaluation Agent Running...")
    progress.progress(92)

    state = evaluation_agent(state)

    # --------------------------------------------

    status.info("📝 Report Agent Running...")
    progress.progress(98)

    state = report_agent(state)

    progress.progress(100)

    status.success("✅ Project Generated Successfully!")

    return state


# ==========================================================
# REPORT GENERATOR
# ==========================================================

def generate_markdown_report(state: AgentState):

    report = f"""
# 🌍 ImpactForge AI Report

## Problem
{state.project.problem}

---

## Research Summary

{state.research.summary}

---

## SDGs
"""

    for sdg in state.sdg.sdgs:

        report += f"\n- SDG {sdg.number}: {sdg.title}"

    report += "\n\n## Objectives\n"

    for obj in state.planning.objectives:

        report += f"- {obj.description}\n"

    report += "\n## Activities\n"

    for act in state.planning.activities:

        report += f"- {act.description}\n"

    report += "\n## KPIs\n"

    for kpi in state.metrics.kpis:

        report += f"- {kpi.name} ({kpi.target})\n"

    report += "\n## Risks\n"

    for risk in state.risks.risks:

        report += f"- {risk.risk}\n"

    report += "\n## Funding\n"

    for fund in state.funding.funding_sources:

        report += f"- {fund.organization}\n"

    report += "\n## Evaluation Score\n"

    report += f"{state.evaluation.overall_score}/100\n"

    report += "\n## Executive Summary\n"

    report += state.report.executive_summary

    report += "\n\n## Implementation Strategy\n"

    report += state.report.implementation_strategy

    report += "\n\n## Expected Impact\n"

    report += state.report.expected_impact

    report += "\n\n## Recommendations\n"

    report += state.report.recommendations

    return report

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("📌 Project Details")

problem = st.sidebar.text_area(
    "Social Problem",
    placeholder="e.g. Reduce food waste in Delhi schools"
)

location = st.sidebar.text_input(
    "Location",
    value="Delhi"
)

target_population = st.sidebar.text_input(
    "Target Population",
    value="School Students"
)

budget = st.sidebar.text_input(
    "Estimated Budget",
    value="50000 INR"
)

st.sidebar.divider()

generate = st.sidebar.button(
    "🚀 Generate Project",
    use_container_width=True
)

st.sidebar.divider()

st.sidebar.markdown("""
### About

ImpactForge AI converts any social problem into a complete
implementation-ready project using multiple AI Agents.

Powered by **Google Gemini**.
""")

# ==========================================================
# MAIN APP
# ==========================================================

if generate:

    if problem.strip() == "":

        st.warning("Please enter a problem statement.")

        st.stop()

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

    st.success("✅ Project Generated Successfully!")

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "SDGs",
            len(state.sdg.sdgs)
        )

    with col2:

        st.metric(
            "Objectives",
            len(state.planning.objectives)
        )

    with col3:

        st.metric(
            "Activities",
            len(state.planning.activities)
        )

    with col4:

        st.metric(
            "Overall Score",
            f"{state.evaluation.overall_score}/100"
        )

    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "🔍 Research",
            "📋 Planning",
            "📈 Execution",
            "⭐ Evaluation",
            "📄 Report"
        ]
    )

    # ======================================================
    # TAB 1
    # ======================================================

    with tab1:

        st.subheader("Research Summary")

        st.write(state.research.summary)

        st.divider()

        c1, c2 = st.columns(2)

        with c1:

            st.subheader("Root Causes")

            for cause in state.research.root_causes:

                st.write("•", cause)

        with c2:

            st.subheader("Challenges")

            for challenge in state.research.challenges:

                st.write("•", challenge)

        st.divider()

        st.subheader("Stakeholders")

        for stakeholder in state.research.stakeholders:

            st.success(stakeholder)

        st.divider()

        st.subheader("Existing Solutions")

        for solution in state.research.existing_solutions:

            st.write("•", solution)

        st.divider()

        st.subheader("Relevant SDGs")

        for sdg in state.sdg.sdgs:

            with st.expander(f"SDG {sdg.number} - {sdg.title}"):

                st.write(sdg.reason)




    # ======================================================
    # TAB 2 : PLANNING
    # ======================================================

    with tab2:

        st.subheader("Objectives")

        for obj in state.planning.objectives:

            with st.container(border=True):

                st.markdown(f"### {obj.id}")

                st.write(obj.description)

                st.caption(
                    "Aligned with: " +
                    ", ".join(obj.sdg_alignment)
                )

        st.divider()

        st.subheader("Activities")

        for act in state.planning.activities:

            with st.container(border=True):

                st.markdown(f"### {act.id}")

                st.write(act.description)

                st.caption(
                    f"Objective: {act.objective}"
                )

                st.caption(
                    f"Timeline: {act.timeline}"
                )

        st.divider()

        st.subheader("Timeline")

        for phase in state.planning.timeline:

            st.info(
                f"**{phase.phase}** — {phase.duration}"
            )



    # ======================================================
    # TAB 3 : EXECUTION
    # ======================================================

    with tab3:

        left, right = st.columns(2)

        with left:

            st.subheader("KPIs")

            for kpi in state.metrics.kpis:

                with st.container(border=True):

                    st.markdown(
                        f"**{kpi.name}**"
                    )

                    st.caption(
                        f"Target : {kpi.target}"
                    )

        with right:

            st.subheader("Success Metrics")

            for metric in state.metrics.success_metrics:

                st.success(metric)

        st.divider()

        st.subheader("Risk Assessment")

        for risk in state.risks.risks:

            with st.expander(risk.risk):

                st.write(
                    f"**Impact:** {risk.impact}"
                )

                st.write(
                    f"**Probability:** {risk.probability}"
                )

                st.write(
                    f"**Mitigation:** {risk.mitigation}"
                )

        st.divider()

        st.subheader("Funding Opportunities")

        for fund in state.funding.funding_sources:

            with st.container(border=True):

                st.markdown(
                    f"### {fund.organization}"
                )

                st.write(fund.reason)

                st.caption(
                    f"Funding Type: {fund.funding_type}"
                )

                st.caption(
                    f"Estimated Amount: {fund.estimated_amount}"
                )



    # ======================================================
    # TAB 4 : EVALUATION
    # ======================================================

    with tab4:

        a,b,c,d,e = st.columns(5)

        a.metric(
            "Innovation",
            state.evaluation.innovation_score
        )

        b.metric(
            "Feasibility",
            state.evaluation.feasibility_score
        )

        c.metric(
            "Impact",
            state.evaluation.impact_score
        )

        d.metric(
            "Sustainability",
            state.evaluation.sustainability_score
        )

        e.metric(
            "Overall",
            state.evaluation.overall_score
        )

        st.divider()

        st.subheader("Judge Feedback")

        st.info(
            state.evaluation.feedback
        )



    # ======================================================
    # TAB 5 : REPORT
    # ======================================================

    with tab5:

        st.subheader("Executive Summary")

        st.write(
            state.report.executive_summary
        )

        st.divider()

        st.subheader(
            "Implementation Strategy"
        )

        st.write(
            state.report.implementation_strategy
        )

        st.divider()

        st.subheader("Expected Impact")

        st.write(
            state.report.expected_impact
        )

        st.divider()

        st.subheader("Recommendations")

        st.write(
            state.report.recommendations
        )

        report = generate_markdown_report(
            state
        )

        st.download_button(

            label="📥 Download Report",

            data=report,

            file_name="ImpactForge_AI_Report.md",

            mime="text/markdown"

        )



# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(
"""
<center>

### 🌍 ImpactForge AI

AI-Powered Social Impact Project Generator

Built using **Google Gemini • Streamlit • Pydantic**

</center>
""",
unsafe_allow_html=True
)
