from agents import Agent, Runner
from pydantic import BaseModel, Field
from typing import List, Literal
import markdown
import asyncio
import os
# ==============================================================================
# 📥 Input Model: Result from ad compliance audit
# ==============================================================================

class AdCheckOutput(BaseModel):
    report: str
    matched_requirements: List[str]
    issues_found: List[str]
    final_verdict: Literal["Compliant", "Non-compliant"]

# ==============================================================================
# 📤 Output Model: structured report
# ==============================================================================

class ComplianceReportOutput(BaseModel):
    structured_report: str = Field(
        description="Generated report with analysis and recommendations"
    )

# ==============================================================================
# 🤖 Agent: Generates structured report and recommendations
# ==============================================================================

compliance_report_agent = Agent(
    name="Compliance Report Generator Agent",
    model="gpt-4o-mini",
    output_type=ComplianceReportOutput,
    instructions="""
You are an assistant that takes the result of an outdoor ad compliance audit and generates:
- A structured report
- A list of actionable recommendations based on issues found

Your report should include:
1. Final verdict
2. List of matched requirements
3. List of issues found
4. Summary
5. Recommendations

Be concise and use bullet points for clarity. Avoid unnecessary repetition.
"""
)

# ==============================================================================
# 🚀 Main Function: Run the agent and generate the report
# ==============================================================================

async def generate_compliance_report(ad_check_result: AdCheckOutput) -> ComplianceReportOutput:
    result = await Runner.run(
       
        compliance_report_agent,
        f"""
Create a compliance report from the following audit data:

Verdict: {ad_check_result.final_verdict}
Matched: {ad_check_result.matched_requirements}
Issues: {ad_check_result.issues_found}
Summary: {ad_check_result.report}
"""
    )
    return result.final_output

# ==============================================================================
# 🧪 Example Run
# ==============================================================================

if __name__ == "__main__":
    example_data = AdCheckOutput(
        report="The store name, menu, and interior meet the requirements. "
               "However, the street sign is placed too low on the façade, violating the guideline.",
        matched_requirements=[
            "Café name placed at the top center",
            "Menu on the left side, legible",
            "Clean and attractive interior"
        ],
        issues_found=[
            "Street sign appears on the façade below the second floor"
        ],
        final_verdict="Non-compliant"
    )

    final_report = asyncio.run(generate_compliance_report(example_data))

    print("📝 Report:\n")
    print(final_report.structured_report)

