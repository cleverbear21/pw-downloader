import base64
import json
import os
import re
import sys


def base64url_decode(input_str):
    """Adds padding if missing and decodes base64url string."""
    rem = len(input_str) % 4
    if rem > 0:
        input_str += "=" * (4 - rem)
    return base64.urlsafe_b64decode(input_str)


def extract_and_save_keys(log_text):
    # Determine the current directory where this script file is stored
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, "keypair.txt")

    # Fixed Regex: Escaped the hyphen (\-) inside the character set
    pattern = r"MediaKeySession\.update\(Uint8Array instance \[\s*([A-Za-z0-9_=\-\s]+?)\s*\]\)"
    matches = re.findall(pattern, log_text, re.S)

    if not matches:
        print("\nNo ClearKey update payloads found in the log.")
        return

    key_pairs = []

    for raw_payload in matches:
        # Strip all newlines and spaces inside the base64 string
        b64_payload = re.sub(r"\s+", "", raw_payload)

        try:
            raw_json = base64url_decode(b64_payload).decode("utf-8")
            data = json.loads(raw_json)

            for key_obj in data.get("keys", []):
                kid_b64 = key_obj.get("kid")
                k_b64 = key_obj.get("k")

                if kid_b64 and k_b64:
                    kid_hex = base64url_decode(kid_b64).hex()
                    k_hex = base64url_decode(k_b64).hex()
                    key_pairs.append(f"{kid_hex}:{k_hex}")

        except Exception as e:
            print(f"Error parsing match: {e}")

    if not key_pairs:
        print("\nNo valid keys could be decoded.")
        return

    # Write output directly to keypair.txt in the script's folder
    with open(output_file, "w", encoding="utf-8") as f:
        for pair in key_pairs:
            f.write(f"{pair}\n")

    print(f"\nSuccessfully extracted {len(key_pairs)} key pair(s) and saved to:\n{output_file}\n")
    for pair in key_pairs:
        print(f"  {pair}")


if __name__ == "__main__":
    print("=== Paste your EME Log text below ===")
    print("When finished pasting, press Ctrl+Z then Enter (Windows) or Ctrl+D (Mac/Linux):\n")

    log_content = sys.stdin.read()

    if log_content.strip():
        extract_and_save_keys(log_content)
    else:
        print("No log content provided. Exiting.")