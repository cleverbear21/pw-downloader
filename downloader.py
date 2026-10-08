import os
import subprocess


def run_downloader():
    # 1. Locate keypair.txt in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    keypair_path = os.path.join(script_dir, "keypair.txt")

    if not os.path.exists(keypair_path):
        print(f"Error: Could not find '{keypair_path}'.")
        print("Please run your key extractor script first to generate keypair.txt.")
        return

    # 2. Read key pair from keypair.txt
    with open(keypair_path, "r", encoding="utf-8") as f:
        keys = [line.strip() for line in f if line.strip()]

    if not keys:
        print(f"Error: '{keypair_path}' is empty.")
        return

    key_pair = keys[0]  # Uses the first key pair found in keypair.txt
    print(f"Loaded Key Pair: {key_pair}")

    # 3. Prompt user for MPD URL
    stream_url = input("\nPaste MPD URL: ").strip()
    if not stream_url:
        print("Error: No URL provided.")
        return

    # 4. Construct command explicitly using .\N_m3u8DL-RE.exe
    cmd = [
        r".\N_m3u8DL-RE.exe",
        stream_url,
        "-H", "Accept: */*",
        "-H", "DNT: 1",
        "-H", "Origin: https://www.pw.live",
        "-H", "Referer: https://www.pw.live/",
        "-H", "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/154.0.0.0 Safari/537.36",
        "--append-url-params",
        "--key", key_pair,
        "--use-shaka-packager",
        "-M", "format=mkv",
    ]

    # 5. Execute command
    print("\nStarting download...\n")
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print("\nError: '.\\N_m3u8DL-RE.exe' was not found in the current folder.")
        print("Ensure N_m3u8DL-RE.exe is placed directly in the same directory as this script.")
    except subprocess.CalledProcessError as e:
        print(f"\nDownload failed with exit code: {e.returncode}")


if __name__ == "__main__":
    run_downloader()