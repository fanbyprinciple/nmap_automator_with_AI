#!/usr/bin/env python3

import argparse
import subprocess
import os
import shlex
import shutil
from pathlib import Path
from typing import Generator

# Third-party libraries
try:
    import google.generativeai as genai
    from colorama import Fore, Style, init
except ImportError:
    print("Error: Required libraries are not installed. Please run 'pip install google-generativeai colorama' to install them.")
    exit(1)

# --- Constants ---
# The maximum number of characters from the nmap output to feed into the model.
# This prevents exceeding the context window. Adjust as needed.
MAX_OUTPUT_LENGTH = 3800 
ASSISTANT_PERSONA = (
    "You are PentestAI, an expert assistant designed to analyze outputs from the nmapAutomator tool. "
    "Your job is to meticulously extract vulnerabilities, identify running services, flag known CVEs, "
    "and suggest clear, actionable follow-up exploitation scripts or commands. When given output "
    "from nmapAutomator, provide a concise summary of the most critical findings and then generate a "
    "Bash or Python script to proceed with exploitation or deeper enumeration."
)

# --- Utility Functions ---

def initialize_colors():
    """Initializes Colorama for cross-platform colored output."""
    init(autoreset=True)

def print_info(message: str):
    """Prints an informational message."""
    print(f"{Fore.CYAN}{Style.BRIGHT}INFO:{Style.RESET_ALL} {message}")

def print_success(message: str):
    """Prints a success message."""
    print(f"{Fore.GREEN}{Style.BRIGHT}SUCCESS:{Style.RESET_ALL} {message}")

def print_warning(message: str):
    """Prints a warning message."""
    print(f"{Fore.YELLOW}{Style.BRIGHT}WARNING:{Style.RESET_ALL} {message}")

def print_error(message: str):
    """Prints an error message and exits."""
    print(f"{Fore.RED}{Style.BRIGHT}ERROR:{Style.RESET_ALL} {message}")
    exit(1)

def get_google_api_key() -> str:
    """Retrieves the Google API key from environment variables."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print_error("The GOOGLE_API_KEY environment variable is not set. Please obtain an API key from Google AI Studio and set it.")
    return api_key

def check_and_install_nmapAutomator():
    """
    Checks if nmapAutomator.sh is in the system's PATH. 
    If not, provides secure instructions for the user to install it.
    """
    tool_name = "nmapAutomator.sh"
    if shutil.which(tool_name):
        print_success(f"'{tool_name}' is already installed and in your PATH.")
        return

    print_warning(f"'{tool_name}' not found in your PATH.")
    print_info("To install it, please follow these steps:")
    
    url = "https://raw.githubusercontent.com/21y4d/nmapAutomator/master/nmapAutomator.sh"
    download_path = Path.home() / tool_name

    print("\n1. Download the script (no sudo required):")
    print(Fore.LIGHTBLACK_EX + f"   wget {url} -O {download_path}")
    
    print("\n2. Make it executable:")
    print(Fore.LIGHTBLACK_EX + f"   chmod +x {download_path}")

    print("\n3. Move it to a directory in your system's PATH (sudo is required for this step):")
    print(Fore.LIGHTBLACK_EX + f"   sudo mv {download_path} /usr/local/bin/{tool_name}")
    
    print_error("Please install the tool and run this script again.")

def run_command(command: str) -> str:
    """
    Runs a shell command safely and returns its output.
    Exits the script if the command fails.
    """
    print_info(f"Running command: {command}")
    try:
        # Use a longer timeout for potentially long-running scans
        result = subprocess.run(
            shlex.split(command), 
            capture_output=True, 
            text=True, 
            timeout=1800, # 30 minutes
            check=True  # Raises CalledProcessError if return code is non-zero
        )
        return result.stdout
    except FileNotFoundError:
        print_error(f"Command not found: '{shlex.split(command)[0]}'. Is it installed and in your PATH?")
    except subprocess.TimeoutExpired:
        print_error("The command timed out after 30 minutes.")
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed with exit code {e.returncode}:\n{e.stderr}")
    except Exception as e:
        print_error(f"An unexpected error occurred while running the command: {e}")

# --- Core AI and Pentest Logic ---

def build_prompt(scan_output: str) -> str:
    """Constructs the full prompt to be sent to the Gemini model."""
    
    if len(scan_output) > MAX_OUTPUT_LENGTH:
        print_warning(f"Scan output is very long. Truncating to {MAX_OUTPUT_LENGTH} characters to fit context window.")
        scan_output = scan_output[:MAX_OUTPUT_LENGTH]

    # The persona is now part of the main instruction.
    return f"""
{ASSISTANT_PERSONA}

Analyze the following output from nmapAutomator. Extract key vulnerabilities, open services, and potential misconfigurations. 
Based on your analysis, generate a ready-to-use Bash or Python script for the next steps in exploitation or enumeration.

--- BEGIN NMAPAUTOMATOR OUTPUT ---
{scan_output}
--- END NMAPAUTOMATOR OUTPUT ---
"""

# --- Main Execution ---

def main():
    """Main function to run the PentestAI script."""
    initialize_colors()
    
    parser = argparse.ArgumentParser(
        description="PentestAI: Analyze nmapAutomator output with Google's Generative AI.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("ip_address", help="The IP address of the target machine.")
    
    args = parser.parse_args()

    # 1. Get API Key and configure the model
    api_key = get_google_api_key()
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    # 2. Check for dependencies
    check_and_install_nmapAutomator()

    # 3. Run nmapAutomator Scan
    command = f"nmapAutomator.sh {args.ip_address} All"
    scan_output = run_command(command)
    print_success("nmapAutomator scan completed.")
    print(f"{Fore.WHITE}{Style.DIM}{'-'*50}\n{scan_output.strip()}\n{'-'*50}{Style.RESET_ALL}")
    
    # 4. Prepare prompt for the AI
    print_info("Preparing prompt for AI analysis.")
    prompt = build_prompt(scan_output)

    # 5. Generate Response
    print_info("PentestAI is analyzing the output and generating suggestions...")
    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- PENTESTAI ANALYSIS ---{Style.RESET_ALL}\n")
    
    try:
        # Using stream=True to get response as it's generated
        response_stream = model.generate_content(prompt, stream=True)
        for chunk in response_stream:
            print(chunk.text, end="", flush=True)
            
    except Exception as e:
        print_error(f"An error occurred during model generation: {e}")

    print(f"\n\n{Fore.CYAN}{Style.BRIGHT}--- ANALYSIS COMPLETE ---{Style.RESET_ALL}")

if __name__ == "__main__":
    main()