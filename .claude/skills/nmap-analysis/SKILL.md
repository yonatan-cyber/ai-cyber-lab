---
name: nmap-analysis
description: Analyze nmap scan results, identify open ports, services, versions, and highlight potential security risks and misconfigurations when reviewing network scans or port scan outputs.
---

When analyzing nmap results:

1. Identify all open ports
   - List port number, protocol, and state
   - Example: 22/tcp open ssh

2. Identify running services and versions
   - Highlight outdated or uncommon versions
   - Mention if version detection is missing

3. Highlight risky or sensitive ports
   - SSH (22)
   - RDP (3389)
   - SMB (445)
   - FTP (21)
   - Telnet (23)
   - HTTP/HTTPS (80/443)

4. Look for potential security issues:
   - Open administrative services
   - Services exposed to the internet
   - Unencrypted protocols (FTP, Telnet)
   - Suspicious or unknown services

5. Suggest next steps:
   - Further scanning (e.g., `-sV`, `-A`, `--script`)
   - Service enumeration
   - Vulnerability scanning

6. Output format:

## Summary
Short explanation of what was found

## Open Ports
List of ports and services

## Risks
Bullet points of potential issues

## Recommendations
Next actions to take