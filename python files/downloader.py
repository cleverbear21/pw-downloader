import os
import subprocess
import sys


def get_base_dir():
    """Returns the executable folder path when compiled, or script folder path when uncompiled."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def run_downloader():
    base_dir = get_base_dir()

    # Locate keypair.txt in the same directory as the executable
    keypair_path = os.path.join(base_dir, "keypair.txt")

    if not os.path.exists(keypair_path):
        print(f"Error: Could not find '{keypair_path}'.")
        print("Please run your key extractor executable first to generate keypair.txt.")
        return

    # Read key pair from keypair.txt
    with open(keypair_path, "r", encoding="utf-8") as f:
        keys = [line.strip() for line in f if line.strip()]

    if not keys:
        print(f"Error: '{keypair_path}' is empty.")
        return

    key_pair = keys[0]
    print(f"Loaded Key Pair: {key_pair}")

    stream_url = input("\nPaste MPD URL: ").strip()
    if not stream_url:
        print("Error: No URL provided.")
        return

    # Path to N_m3u8DL-RE.exe located in the same directory
    downloader_exe = os.path.join(base_dir, "N_m3u8DL-RE.exe")

    if not os.path.exists(downloader_exe):
        print(f"\nError: '{downloader_exe}' was not found.")
        print("Ensure N_m3u8DL-RE.exe is placed in the same directory as this tool.")
        return

    cmd = [
        downloader_exe,
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

    print("\nStarting download...\n")
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"\nDownload failed with exit code: {e.returncode}")


if __name__ == "__main__":
    run_downloader()