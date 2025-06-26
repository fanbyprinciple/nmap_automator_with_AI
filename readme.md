# PentestAI: nmapAutomator with AI-Powered Analysis

This script automates running the `nmapAutomator.sh` tool and then uses Google's Generative AI to analyze the scan results, providing you with actionable insights and suggested next steps for your penetration test.

## Features

-   **Automated Scans**: Runs the comprehensive `nmapAutomator.sh` "All" scan on a target.
-   **AI-Powered Analysis**: Sends the scan output to the Gemini API to identify key vulnerabilities, services, and misconfigurations.
-   **Actionable Suggestions**: The AI generates a summary of findings and a ready-to-use Bash or Python script for exploitation or further enumeration.
-   **Streamlined Workflow**: Saves you time by combining scanning and analysis into a single, efficient process.

## Prerequisites

1.  **Python 3**: Make sure you have Python 3 installed.
2.  **nmapAutomator**: The script will check if `nmapAutomator.sh` is in your PATH and guide you through the installation if it's not.
3.  **Google AI API Key**: You need an API key from Google AI Studio to use the analysis feature.

## Setup

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/PentestAI.git
    cd PentestAI
    ```

2.  **Install Python dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your Google AI API Key:**

    You need to set your API key as an environment variable. This is a secure way to handle your key without hardcoding it into the script.

    -   **For Linux/macOS:**

        ```bash
        export GOOGLE_API_KEY='YOUR_API_KEY'
        ```

        To make this permanent, add the line to your `~/.bashrc`, `~/.zshrc`, or shell configuration file.

    -   **For Windows:**

        ```powershell
        $Env:GOOGLE_API_KEY='YOUR_API_KEY'
        ```

        To set it permanently, use the System Properties menu.

## Usage

Run the script with the IP address of your target machine:

```bash
python automate_nmap.py <TARGET_IP>
```

**Example:**

```bash
python automate_nmap.py 10.10.11.123
```

The script will:

1.  Verify that `nmapAutomator.sh` is installed.
2.  Run the scan against the target IP.
3.  Print the raw `nmapAutomator` output.
4.  Send the output to the Gemini API for analysis.
5.  Stream and display the AI-generated report and suggested script.

## How It Works

The script leverages the `google-generativeai` library to communicate with the Gemini API. It constructs a detailed prompt that includes the `nmapAutomator` output and a persona for the AI, instructing it to act as a pentesting expert. The model's response is then streamed to your console in real-time.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.