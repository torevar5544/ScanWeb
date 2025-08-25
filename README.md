🔍 Advanced Website Security Scanner
https://img.shields.io/badge/Python-3.8%252B-blue?logo=python
https://img.shields.io/badge/Platform-Windows%2520%257C%2520Linux-lightgrey
https://img.shields.io/badge/License-MIT-green

A comprehensive, GUI-based security scanning tool that performs in-depth analysis of websites and network infrastructure with detailed reporting capabilities.

✨ Features
🛡️ Comprehensive Security Analysis
Port Scanning: Complete port mapping with service detection

Network Diagnostics: Real-time MTR tracing for route analysis

DNS Enumeration: Complete DNS record analysis (A, AAAA, MX, NS, TXT)

Subdomain Discovery: Automated discovery of common subdomains

📊 Advanced Reporting
Dual Format Reports: Automatically generates both HTML and TXT reports

Visual Interface: Clean, dark-themed GUI with real-time logging

Export Ready: Professional formatting for security assessments

🌐 Network Intelligence
WHOIS Integration: Complete domain registration information

GeoIP Location: IP geolocation with ISP and network details

Infrastructure Mapping: Comprehensive network service discovery

🚀 Quick Start
Prerequisites
Python 3.8 or higher

Nmap installed on your system

MTR (Linux) or WinMTR (Windows)

Installation
bash
# Clone the repository
git clone https://github.com/yourusername/website-security-scanner.git
cd website-security-scanner

# Install Python dependencies
pip install -r requirements.txt
Usage
bash
# Run the scanner
python web_security_scanner.py
Enter a domain or IP address in the input field

Click "Start Scan" to begin the security assessment

Monitor real-time progress in the logging panel

Access generated reports in the reports/ directory

📋 Scan Capabilities
Feature	Description
Full Port Scan	Comprehensive -p- scan identifying all open ports
Service Detection	Version detection for running services
OS Fingerprinting	Remote operating system identification
Network Tracing	MTR integration for route analysis
DNS Analysis	Complete DNS record enumeration
Subdomain Discovery	Automated subdomain enumeration
WHOIS Lookup	Domain registration information
GeoIP Location	Geographic IP location data
📁 Report Sample
Generated reports include:

Executive summary of findings

Detailed technical analysis

Network mapping results

Security recommendations

Timestamped documentation

Example report structure:

text
reports/
├── report_example.com_2024-01-15_14-30-25.html
└── report_example.com_2024-01-15_14-30-25.txt
🛠️ Technical Details
Built With
Python 3.8+ - Core programming language

Tkinter - GUI framework

Nmap - Network discovery and security auditing

DNS Python - DNS toolkit for Python

MTR - Network diagnostic tool

System Requirements
Windows: Nmap, WinMTR

Linux: nmap, mtr-tiny

macOS: nmap, mtr

🤝 Contributing
We welcome contributions! Please feel free to submit pull requests, report bugs, or suggest new features.

Fork the repository

Create your feature branch (git checkout -b feature/AmazingFeature)

Commit your changes (git commit -m 'Add some AmazingFeature')

Push to the branch (git push origin feature/AmazingFeature)

Open a Pull Request

⚠️ Legal Disclaimer
This tool is intended for educational purposes and authorized security testing only.

🚫 Do not use on networks or systems without explicit permission

🔒 Ensure you have proper authorization before scanning any target

📜 The developers are not responsible for misuse of this tool

Always comply with local laws and regulations regarding network scanning and security testing.

📞 Support
If you have any questions or need help with the scanner:

Open an Issue

Check the Wiki for documentation

Email: your.email@example.com

📜 License
This project is licensed under the MIT License - see the LICENSE.md file for details.

🏆 Acknowledgments
Nmap Project for the incredible scanning engine

Python community for excellent libraries

Security researchers worldwide for their contributions

Note: Always practice responsible disclosure and ethical security testing. Happy scanning! 🔍
