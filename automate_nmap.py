#!/usr/bin/env python3

import argparse
import subprocess
import os
import shlex
import shutil
from pathlib import Path
from typing import List, Generator

# Third-party libraries
try:
    from ctransformers import AutoModelForCausalLM
    from transformers import AutoTokenizer
    from colorama import Fore, Style, init
except ImportError:
    print("Error: Required libraries are not installed. Please run 'pip install ctransformers transformers colorama' to install them.")
    exit(1)

# --- Constants ---
CONTEXT_LENGTH = 4096
MAX_NEW_TOKENS = 2048
# The maximum number of characters from the nmap output to feed into the model.
# This prevents exceeding the context window. Adjust as needed.
MAX_OUTPUT_LENGTH = 3500 
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
    """Constructs the full prompt to be sent to the language model."""
    
    if len(scan_output) > MAX_OUTPUT_LENGTH:
        print_warning(f"Scan output is very long. Truncating to {MAX_OUTPUT_LENGTH} characters to fit context window.")
        scan_output = scan_output[:MAX_OUTPUT_LENGTH]

    return f"""
Analyze the following output from nmapAutomator. Extract key vulnerabilities, open services, and potential misconfigurations. 
Based on your analysis, generate a ready-to-use Bash or Python script for the next steps in exploitation or enumeration.

--- BEGIN NMAPAUTOMATOR OUTPUT ---
{scan_output}
--- END NMAPAUTOMATOR OUTPUT ---
"""

def stream_generation(model: AutoModelForCausalLM, token_ids: List[int]) -> Generator[str, None, None]:
    """Streams the model's output token by token."""
    for token in model.generate(token_ids):
        yield model.detokenize(token)

# --- Main Execution ---

def main():
    """Main function to run the PentestAI script."""
    initialize_colors()
    
    parser = argparse.ArgumentParser(
        description="PentestAI: Analyze nmapAutomator output with a local LLM.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("ip_address", help="The IP address of the target machine.")
    parser.add_argument("--model-path", required=True, help="Path to the GGUF model file.")
    parser.add_argument("--gpu-layers", type=int, default=50, help="Number of layers to offload to GPU. Set to 0 for CPU-only.")
    parser.add_argument("--threads", type=int, default=os.cpu_count(), help="Number of CPU threads to use for inference.")
    
    args = parser.parse_args()

    model_path = Path(args.model_path)
    if not model_path.is_file():
        print_error(f"Model file not found at: {args.model_path}")
        
    # 1. Check for dependencies
    check_and_install_nmapAutomator()

    # 2. Load Model and Tokenizer
    print_info("Loading model and tokenizer... This may take a moment.")
    try:
        tokenizer = AutoTokenizer.from_pretrained("ArmurAI/Pentest_AI")
        model = AutoModelForCausalLM.from_pretrained(
            str(model_path),
            model_type="llama", # Adjust if you use a different model type
            gpu_layers=args.gpu_layers,
            threads=args.threads,
            context_length=CONTEXT_LENGTH,
            max_new_tokens=MAX_NEW_TOKENS,
        )
        print_success("Model and tokenizer loaded.")
    except Exception as e:
        print_error(f"Failed to load the model. Please check the path and file integrity.\nDetails: {e}")

    # 3. Run nmapAutomator Scan
    command = f"nmapAutomator.sh {args.ip_address} All"
    scan_output = run_command(command)
    print_success("nmapAutomator scan completed.")
    print(f"{Fore.WHITE}{Style.DIM}{'-'*50}\n{scan_output.strip()}\n{'-'*50}{Style.RESET_ALL}")
    
    # 4. Prepare prompt and tokens for the LLM
    print_info("Preparing prompt for AI analysis.")
    # The 'system' role or a prefixed instruction helps guide the model better.
    # The exact format depends on the model's training. This is a common one.
    system_prompt = f"<s>[INST] {ASSISTANT_PERSONA} [/INST]</s>"
    user_prompt = f"<s>[INST] {build_prompt(scan_output)} [/INST]"
    
    # Note: Some models work better without the system prompt, or with different tags.
    # Check your model's documentation for the correct prompt format.
    full_prompt = f"{system_prompt}\n{user_prompt}"

    tokens = tokenizer.encode(full_prompt)

    # 5. Generate and Stream Response
    print_info("PentestAI is analyzing the output and generating suggestions...")
    print(f"\n{Fore.CYAN}{Style.BRIGHT}--- PENTESTAI ANALYSIS ---{Style.RESET_ALL}\n")
    
    try:
        for char in stream_generation(model, tokens):
            print(char, end="", flush=True)
    except Exception as e:
        print_error(f"An error occurred during model generation: {e}")

    print(f"\n\n{Fore.CYAN}{Style.BRIGHT}--- ANALYSIS COMPLETE ---{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
