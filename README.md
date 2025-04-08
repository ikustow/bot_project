# Advertisement Compliance Audit Bot

This project implements an AI-powered bot that audits advertisement images for compliance with a given set of requirements. It uses a multi-agent system to first analyze the image against the rules and then generate a detailed compliance report.

## Features

- Analyzes advertisement images based on provided requirements.
- Uses OpenAI's GPT models for analysis and report generation.
- Employs a multi-agent workflow (Audit Agent -> Ad Check Agent -> Compliance Report Agent).
- Loads configuration (like OpenAI API key) from a `.env` file.

## Project Structure

```
bot_project/
│
├── bot/
│   ├── ai_bot/
│   │   ├── agent_data/
│   │   │   ├── main_agent.py       # Main script to run the audit process
│   │   │   ├── report_agent.py     # Agent responsible for generating reports
│   │   │   └── image_analyzer.py   # Agent responsible for analyzing images
│   │   └── ... (other potential agent files)
│   └── ... (other bot components)
│
├── .env                    # Environment variables (needs to be created)
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd bot_project
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the project root directory (`bot_project/`) and add your OpenAI API key:
    ```dotenv
    OPENAI_API_KEY='your_openai_api_key_here'
    ```

## Usage

Modify the `requirements_description` and `image_url` variables within `bot/ai_bot/agent_data/main_agent.py` according to your needs.

Then, run the main script:

```bash
python bot/ai_bot/agent_data/main_agent.py
```

The script will:
1.  Use the `Ad Check Agent` to analyze the image based on the requirements.
2.  Use the `Compliance Report Agent` to generate a report from the analysis.
3.  Print the initial analysis results and the final structured report to the console.

## How it Works

The `main_agent.py` script orchestrates the process:
- It defines an `Audit Agent` that coordinates the workflow.
- The `Audit Agent` first hands off the task (image URL and requirements) to the `Ad Check Agent` (defined in `image_analyzer.py`).
- The `Ad Check Agent` analyzes the image and returns its findings.
- The `Audit Agent` then passes these findings to the `Compliance Report Agent` (defined in `report_agent.py`).
- The `Compliance Report Agent` generates a structured compliance report.
- The final report is printed.

## Dependencies


- [python-dotenv](https://github.com/theskumar/python-dotenv): For loading environment variables from a `.env` file.
- [openai](https://github.com/openai/openai-python): OpenAI Python client library.
- `agents`: (Assumed local/custom library for agent framework) 