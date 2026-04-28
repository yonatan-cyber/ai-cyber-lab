import subprocess
from datetime import datetime
from pathlib import Path

def main():
    target = input("Enter target IP or domain: ").strip()

    if not target:
        print("No target provided.")
        return

    output_dir = Path("labs/nmap")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_file = output_dir / f"nmap_scan_{target}_{timestamp}.txt"

    command = [
        "nmap",
        "-sV",
        "-Pn",
        target
    ]

    print(f"[+] Running: {' '.join(command)}")
    print(f"[+] Saving results to: {output_file}")

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=False
        )

        output_file.write_text(result.stdout + "\n" + result.stderr, encoding="utf-8")

        print("\n===== NMAP RESULT =====\n")
        print(result.stdout)

        if result.stderr:
            print("\n===== ERRORS / WARNINGS =====\n")
            print(result.stderr)

    except FileNotFoundError:
        print("Nmap is not installed or not in PATH.")
        print("Install it from: https://nmap.org/download.html")

if __name__ == "__main__":
    main()