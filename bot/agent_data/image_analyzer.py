from agents import Agent, InputGuardrail, GuardrailFunctionOutput, Runner
from pydantic import BaseModel, Field
import asyncio
from typing import List, Literal


class AdCheckOutput(BaseModel):
    """Output model for advertisement compliance check results."""
    report: str = Field(description="Brief summary of how the image matches the requirements")
    matched_requirements: List[str] = Field(description="List of requirements that are correctly met")
    issues_found: List[str] = Field(description="List of missing or incorrectly implemented elements")
    final_verdict: Literal["Compliant", "Non-compliant"] = Field(description="Final judgment on compliance")


ad_check_agent = Agent(
    name="Ad Visual Compliance Checker",
    model="gpt-4o",
    output_type=AdCheckOutput,
    instructions="""
    You are an outdoor advertising inspector. Your task is to analyze an advertisement image and check whether it matches a given set of requirements (brief or spec).

    You will be given:
    - An image
    - A description of the expected elements and layout (the requirements)

    Your responsibilities:
    1. Review the image and compare it to the listed requirements.
    2. Identify which requirements are correctly implemented.
    3. Identify any issues: missing elements, incorrect positions, or visual problems.
    4. Provide a clear, short report.
    5. Conclude with a final verdict:
       - "Compliant" if all requirements are met
       - "Non-compliant" if there are any issues

    Stay objective. Do not make assumptions outside of the provided brief.
    """
)


async def check_ad_image(image_path: str, requirements_description: str) -> AdCheckOutput:
    """Run an advertisement compliance check on the given image.
    
    Args:
        image_path: Path or URL to the advertisement image
        requirements_description: Description of the requirements to check against
        
    Returns:
        AdCheckOutput containing the compliance check results
    """
    return await Runner.run(
        ad_check_agent,
        f"Check this advertisement image against the following requirements: {requirements_description}. Image: {image_path}"
    )


if __name__ == "__main__":
    requirements_description = """
    Outdoor Advertising Requirements (Café Front Window)
    1. The café name must be placed at the top of the façade, centered, and written in the brand's signature font style.
    2. The menu must be placed on the left side of the window, clearly legible and styled with good contrast.
    3. The interior visible through the window must appear tidy and visually appealing.
    4. The window must include a promotional poster or special offer displayed at the bottom-right corner of the window.
    5. The street name sign must not appear on the shopfront or façade below the second floor.
    """
    image_url = "https://i.pinimg.com/736x/4e/9a/03/4e9a031c196ed3335f5f4a9b3b277950.jpg"

    result = asyncio.run(check_ad_image(image_url, requirements_description))

    print("=== Ad Compliance Report ===")
    print("Report:", result.final_output.report)
    print("Matched:", result.final_output.matched_requirements)
    print("Issues:", result.final_output.issues_found)
    print("Final Verdict:", result.final_output.final_verdict)

    

