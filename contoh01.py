import requests

def ask_ai(prompt="", model="flash", url=""):
    if not url:
        return {
            "status": "error",
            "message": "URL API belum ditentukan"
        }

    full_url = url.rstrip("/") + "/api/ask"

    payload = {
        "prompt": prompt,
        "model": model
    }

    try:
        response = requests.post(
            full_url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=40,
            verify=False  # sama seperti CURLOPT_SSL_VERIFYPEER = false
        )

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Request Error: {str(e)}"
        }

    # Error HTTP
    if response.status_code != 200:
        return {
            "status": "error",
            "message": f"HTTP Error ({response.status_code})",
            "raw": response.text
        }

    # Decode JSON
    try:
        data = response.json()
    except ValueError:
        return {
            "status": "error",
            "message": "JSON Decode Error",
            "raw": response.text
        }

    # Return unified output
    return {
        "status": "ok",
        "agentID": data.get("agentID"),
        "agent": data.get("agent"),
        "model": data.get("model"),
        "response": data.get("response"),
        "error": data.get("error"),
        "timestamp": data.get("timestamp")
    }

isi = ask_ai(prompt="apa yang dimaksud dengan AI Model", model="flash", url="https://ai.ptov.my.id")
print(isi)