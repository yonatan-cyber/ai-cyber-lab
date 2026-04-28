import subprocess
from datetime import datetime
from pathlib import Path
import re

RISKY_PORTS = {
    "21": "FTP - Unencrypted. Check for anonymous login.",
    "22": "SSH - Check version, weak passwords, brute-force protection.",
    "23": "Telnet - Unencrypted and high risk.",
    "80": "HTTP - Check for web vulnerabilities.",
    "135": "MSRPC - Internal Windows service. Avoid internet exposure.",
    "139": "NetBIOS - Related to Windows file sharing.",
    "445": "SMB - Sensitive. Review shares and permissions.",
    "3389": "RDP - High risk if exposed to the internet.",
    "5900": "VNC - Remote access. Check authentication settings.",
}

SCAN_MODES = {
    "1": {
        "name": "Quick Scan",
        "args": ["-sV", "-Pn"],
    },
    "2": {
        "name": "Default Scripts Scan",
        "args": ["-sV", "-sC", "-Pn"],
    },
    "3": {
        "name": "Aggressive Scan",
        "args": ["-A", "-Pn"],
    },
}

def safe_filename(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_.-]", "_", value)

def analyze_open_ports(output: str):
    findings = []

    for line in output.splitlines():
        match = re.match(r"^(\d+)/tcp\s+open\s+(\S+)\s*(.*)$", line)
        if not match:
            continue

        port, service, version = match.groups()

        if port in RISKY_PORTS:
            findings.append(f"- {port}/tcp {service}: {RISKY_PORTS[port]}")

        if version and "?" in version:
            findings.append(f"- {port}/tcp {service}: Service detection uncertain. Manual verification recommended.")

    return findings

def choose_scan_mode():
    print("\nChoose scan mode:")
    for key, mode in SCAN_MODES.items():
        print(f"{key}. {mode['name']}")

    choice = input("Mode: ").strip()
    return SCAN_MODES.get(choice, SCAN_MODES["1"])

def main():
    target = input("Enter target IP or domain: ").strip()

    if not target:
        print("No target provided.")
        return

    mode = choose_scan_mode()

    output_dir = Path("labs/nmap")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    clean_target = safe_filename(target)

    txt_file = output_dir / f"nmap_{clean_target}_{timestamp}.txt"
    xml_file = output_dir / f"nmap_{clean_target}_{timestamp}.xml"

    command = [
        "nmap",
        *mode["args"],
        "-oX",
        str(xml_file),
        target,
    ]

    print(f"\n[+] Selected mode: {mode['name']}")
    print(f"[+] Running: {' '.join(command)}")
    print(f"[+] TXT output: {txt_file}")
    print(f"[+] XML output: {xml_file}")

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )

        full_output = result.stdout + "\n" + result.stderr
        txt_file.write_text(full_output, encoding="utf-8")

        print("\n===== NMAP RESULT =====\n")
        print(result.stdout)

        findings = analyze_open_ports(result.stdout)

        print("\n===== BASIC SECURITY ANALYSIS =====\n")
        if findings:
            for item in findings:
                print(item)
        else:
            print("No high-risk ports from the built-in list were detected.")

        if result.stderr:
            print("\n===== ERRORS / WARNINGS =====\n")
            print(result.stderr)

    except FileNotFoundError:
        print("Nmap is not installed or not in PATH.")
        print("Install it from: https://nmap.org/download.html")

if __name__ == "__main__":
    main()