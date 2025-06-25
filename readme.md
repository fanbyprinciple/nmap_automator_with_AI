# 🚀 Nmap Automator with AI

<div align="center">

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macos-lightgrey.svg)
![AI Powered](https://img.shields.io/badge/AI-Powered-ff6b6b.svg)

**An intelligent network reconnaissance tool that combines the power of nmapAutomator with AI-driven vulnerability analysis**

[Features](#-features) • [Installation](#-installation) • [Usage](#-usage) • [Examples](#-examples) • [Contributing](#-contributing)

</div>

---

## 🌟 Overview

Nmap Automator with AI is a cutting-edge penetration testing tool that automates network reconnaissance using nmapAutomator and enhances the results with AI-powered vulnerability analysis. The tool leverages local Large Language Models (LLMs) to provide intelligent insights, identify potential attack vectors, and generate actionable exploitation scripts.

### 🎯 Key Benefits

- **🤖 AI-Powered Analysis**: Leverages local LLMs for intelligent vulnerability assessment
- **🔍 Comprehensive Scanning**: Automated nmap scanning with nmapAutomator integration
- **📊 Smart Reporting**: Generates actionable insights and exploitation scripts
- **🔒 Privacy-First**: Runs completely offline with local AI models
- **⚡ Streamlined Workflow**: One command from reconnaissance to exploitation planning

## 🚀 Features

### Core Functionality
- **Automated Network Scanning**: Seamless integration with nmapAutomator for comprehensive target analysis
- **AI Vulnerability Analysis**: Local LLM processing for identifying security weaknesses
- **Intelligent Script Generation**: Auto-generates bash/python scripts for next-phase exploitation
- **Colorized Output**: Enhanced terminal experience with clear, color-coded results
- **Streaming Response**: Real-time AI analysis output for immediate insights

### Technical Features
- **Multi-threading Support**: Configurable CPU thread utilization
- **GPU Acceleration**: Optional GPU offloading for faster AI processing
- **Timeout Protection**: Built-in safeguards against long-running operations
- **Error Handling**: Comprehensive error management and user guidance
- **Context-Aware Processing**: Smart truncation to fit LLM context windows

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows
- **Memory**: Minimum 8GB RAM (16GB recommended for larger models)
- **Storage**: 2-10GB free space (depending on model size)

### Dependencies
- **nmapAutomator**: Network scanning automation
- **nmap**: Network discovery and security auditing
- **Local LLM Model**: GGUF format model (e.g., from Hugging Face)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/nmap_automator_with_AI.git
cd nmap_automator_with_AI
```

### 2. Install Python Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Or install manually
pip install ctransformers transformers colorama
```

### 3. Install nmapAutomator
The script will guide you through the installation if nmapAutomator is not found:

```bash
# Download nmapAutomator
wget https://raw.githubusercontent.com/21y4d/nmapAutomator/master/nmapAutomator.sh -O ~/nmapAutomator.sh

# Make executable
chmod +x ~/nmapAutomator.sh

# Move to system PATH (requires sudo)
sudo mv ~/nmapAutomator.sh /usr/local/bin/nmapAutomator.sh
```

### 4. Download AI Model
Download a compatible GGUF model (recommended: PentestAI models):

```bash
# Example: Download a lightweight model
wget https://huggingface.co/ArmurAI/Pentest_AI/resolve/main/model.gguf
```

## 🎮 Usage

### Basic Usage
```bash
python automate_nmap.py <TARGET_IP> --model-path /path/to/your/model.gguf
```

### Advanced Options
```bash
python automate_nmap.py <TARGET_IP> \
    --model-path /path/to/model.gguf \
    --gpu-layers 32 \
    --threads 8
```

### Command Line Arguments

| Argument | Description | Default | Required |
|----------|-------------|---------|----------|
| `ip_address` | Target IP address for scanning | - | ✅ |
| `--model-path` | Path to GGUF model file | - | ✅ |
| `--gpu-layers` | Number of layers to offload to GPU | 50 | ❌ |
| `--threads` | CPU threads for inference | CPU count | ❌ |

## 📖 Examples

### Example 1: Basic Scan
```bash
python automate_nmap.py 192.168.1.100 --model-path ./models/pentest-ai.gguf
```

### Example 2: GPU-Accelerated Analysis
```bash
python automate_nmap.py 10.0.0.50 \
    --model-path ./models/large-model.gguf \
    --gpu-layers 40 \
    --threads 16
```

### Example 3: CPU-Only Processing
```bash
python automate_nmap.py 172.16.1.10 \
    --model-path ./models/cpu-optimized.gguf \
    --gpu-layers 0 \
    --threads 4
```

## 📊 Sample Output

```
INFO: Loading model and tokenizer... This may take a moment.
SUCCESS: Model and tokenizer loaded.
INFO: Running command: nmapAutomator.sh 192.168.1.100 All
SUCCESS: nmapAutomator scan completed.

--- PENTESTAI ANALYSIS ---

🎯 CRITICAL FINDINGS:
1. SSH service (port 22) - Potential for brute force attacks
2. HTTP service (port 80) - Web application enumeration required
3. SMB service (port 445) - Anonymous access possible

🔧 RECOMMENDED EXPLOITATION SCRIPT:
#!/bin/bash
# Generated exploitation script
hydra -L users.txt -P passwords.txt ssh://192.168.1.100
gobuster dir -u http://192.168.1.100 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt
smbclient -L 192.168.1.100 -N

--- ANALYSIS COMPLETE ---
```

## 🔧 Configuration

### Model Selection
Choose models based on your hardware capabilities:

- **Lightweight (2-4GB)**: Fast processing, basic analysis
- **Medium (4-8GB)**: Balanced performance and accuracy
- **Large (8GB+)**: Comprehensive analysis, detailed insights

### Performance Tuning
- **GPU Layers**: Increase for faster processing (if GPU available)
- **Threads**: Set to your CPU core count for optimal performance
- **Context Length**: Adjust based on scan output size

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Clone and setup development environment
git clone https://github.com/yourusername/nmap_automator_with_AI.git
cd nmap_automator_with_AI
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Areas for Contribution
- 🐛 Bug fixes and improvements
- 🚀 New AI model integrations
- 📚 Documentation enhancements
- 🎨 UI/UX improvements
- 🧪 Test coverage expansion

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

**IMPORTANT**: This tool is intended for authorized penetration testing and educational purposes only. Users are responsible for ensuring they have proper authorization before scanning any networks or systems. Unauthorized access to computer systems is illegal and unethical.

## 🆘 Support

- 📖 **Documentation**: Check our [Wiki](https://github.com/yourusername/nmap_automator_with_AI/wiki)
- 🐛 **Issues**: Report bugs on [GitHub Issues](https://github.com/yourusername/nmap_automator_with_AI/issues)
- 💬 **Discussions**: Join our [GitHub Discussions](https://github.com/yourusername/nmap_automator_with_AI/discussions)

## 🙏 Acknowledgments

- [nmapAutomator](https://github.com/21y4d/nmapAutomator) - Excellent nmap automation framework
- [Hugging Face](https://huggingface.co/) - AI model hosting and transformers library
- [ctransformers](https://github.com/marella/ctransformers) - Efficient local LLM inference

---

<div align="center">

**Made with ❤️ for the cybersecurity community**

⭐ Star this repo if you find it useful!

</div>
