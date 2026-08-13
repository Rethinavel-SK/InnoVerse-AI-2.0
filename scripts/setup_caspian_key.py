"""
InnoVerse AI 2.0 — Caspian CLI Key Generator & Device Login
===========================================================
This script initiates device authentication with Caspian API,
waits for browser verification, extracts your Caspian API Key,
and automatically updates your .env file!
"""

import os
import sys
import time
import httpx

DOTENV_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")


def update_env_file(key_name: str, value: str):
    """Update or append key=value in .env file."""
    lines = []
    found = False
    if os.path.exists(DOTENV_PATH):
        with open(DOTENV_PATH, "r", encoding="utf-8") as f:
            lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.strip().startswith(f"{key_name}="):
            new_lines.append(f"{key_name}={value}\n")
            found = True
        else:
            new_lines.append(line)

    if not found:
        new_lines.append(f"\n{key_name}={value}\n")

    with open(DOTENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(new_lines)


def setup_caspian_key():
    print("\n=======================================================")
    print("🔑 InnoVerse AI 2.0 — Caspian Device Key Generator")
    print("=======================================================\n")

    try:
        res = httpx.post("https://api.trycaspianai.com/v1/auth/device/start", json={})
        if res.status_code != 200:
            print(f"❌ Failed to start device login. Status: {res.status_code}")
            print(res.text)
            return

        data = res.json()
        device_code = data.get("device_code")
        user_code = data.get("user_code")
        verify_url = data.get("verification_uri_complete") or data.get("verification_uri")
        interval = data.get("interval", 5)

        print("👉 STEP 1: Open this authorization link in your browser:")
        print(f"\n    \033[1;36m{verify_url}\033[0m\n")
        if user_code and "code=" not in verify_url:
            print(f"   (Enter User Code: {user_code})")

        print("👉 STEP 2: Waiting for browser authorization (polling)...")

        deadline = time.monotonic() + 300
        while time.monotonic() < deadline:
            time.sleep(interval)
            t_res = httpx.post(
                "https://api.trycaspianai.com/v1/auth/device/token",
                json={"device_code": device_code}
            )
            if t_res.status_code == 200:
                t_data = t_res.json()
                status = t_data.get("status")
                if status == "approved":
                    api_key = t_data.get("api_key") or t_data.get("access_token")
                    print("\n✅ Authorization Approved!")
                    if api_key:
                        print(f"🔑 Received Caspian API Key: {api_key[:8]}...{api_key[-4:]}")
                        update_env_file("CASPIAN_API_KEY", api_key)
                        print("💾 Saved CASPIAN_API_KEY to .env successfully!")
                    else:
                        print("ℹ️ Device approved! Details:", t_data)
                    return
                elif status in ("expired", "not_found"):
                    print(f"\n❌ Login session {status}. Please re-run the script.")
                    return
                else:
                    sys.stdout.write(".")
                    sys.stdout.flush()
            else:
                sys.stdout.write(".")
                sys.stdout.flush()

        print("\n⏱️ Device login timed out after 5 minutes.")

    except Exception as e:
        print(f"\n❌ Error during setup: {e}")


if __name__ == "__main__":
    setup_caspian_key()
