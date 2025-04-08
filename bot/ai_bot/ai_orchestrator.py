from agents import Runner
from .agent_data.main_agent import audit_agent



async def run_compliance_pipeline(image_url: str, requirements: str):
    input_text = f"""
        Please analyze this advertisement image against the following requirements:
        
        Image URL: {image_url}
        
        Requirements:
        {requirements}
        """

    result = await Runner.run(audit_agent, input_text)
    print("Initial Analysis Result:", result)

    # Second run: Generate report
    report_result = await Runner.run(
        audit_agent,
        f"Generate a detailed compliance report from the following analysis: {result} as string"
    )
    return report_result.final_output.structured_report
