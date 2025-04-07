from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner, set_default_openai_key, enable_verbose_stdout_logging
from pydantic import BaseModel, Field
import asyncio
from typing import List, Optional
from report_agent import compliance_report_agent
from image_analyzer import ad_check_agent
import os
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()

# Verify API key is loaded
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

# Set the default OpenAI API key
set_default_openai_key(api_key)

requirements_description = """
Outdoor Advertising Requirements (Café Front Window)
1. The café name must be placed at the top of the façade, centered, and written in the brand's signature font style.
2. The menu must be placed on the left side of the window, clearly legible and styled with good contrast.
3. The interior visible through the window must appear tidy and visually appealing.
4. The window must include a promotional poster or special offer displayed at the bottom-right corner of the window.
5. The street name sign must not appear on the shopfront or façade below the second floor.
"""
image_url = "https://i.pinimg.com/736x/4e/9a/03/4e9a031c196ed3335f5f4a9b3b277950.jpg"

audit_agent = Agent(
    name="Audit Agent",
    model="gpt-4o",   
    handoffs=[ad_check_agent, compliance_report_agent],
    instructions="""
    You are an audit coordinator that manages the process of checking advertisement compliance.
    
    Your workflow should be:
    1. First, use the ad_check_agent to analyze the image against the requirements
    2. Then, use the compliance_report_agent to generate a detailed report based on the analysis
    
    Make sure to:
    - Pass the complete requirements and image URL to the ad_check_agent
    - Pass the full analysis results to the compliance_report_agent
    - Handle any errors or issues that arise during the process
    """
)

async def main():
    try:
        # First run: Check the advertisement
        input_text = f"""
        Please analyze this advertisement image against the following requirements:
        
        Image URL: {image_url}
        
        Requirements:
        {requirements_description}
        """
        
        result = await Runner.run(audit_agent, input_text)
        print("Initial Analysis Result:", result)
        
        # Second run: Generate report
        report_result = await Runner.run(
            audit_agent,
            f"Generate a detailed compliance report from the following analysis: {result} as string"
        )
        print("Report:", report_result)
        print("Final Report:", report_result.final_output.structured_report)
        
    except Exception as e:
        print(f"Error during audit process: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())