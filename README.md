# 🤖 AI Generative Client (Python)

Client Python sederhana untuk mengakses API AI Generative:

```
https://ai.ptov.my.id/api/ask
```

Project ini merupakan konversi dari fungsi PHP cURL ke Python menggunakan `requests`.

---

## 📦 Fitur

* POST request ke `/api/ask`
* Timeout 40 detik
* Support custom model
* Handle error:

  * Request error
  * HTTP error
  * JSON decode error
* Output response sudah dalam format unified

---

## 🛠 Requirements

* Python 3.8+
* requests

Install dependency:

```bash
pip install requests
```

---

## 📂 Struktur Project

```
ai-client/
│
├── ai_client.py
├── app.py (optional Flask example)
└── README.md
```

---

## 🧠 Function: ask_ai()

### File: `ai_client.py`

```python
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
            verify=False
        )
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": f"Request Error: {str(e)}"
        }

    if response.status_code != 200:
        return {
            "status": "error",
            "message": f"HTTP Error ({response.status_code})",
            "raw": response.text
        }

    try:
        data = response.json()
    except ValueError:
        return {
            "status": "error",
            "message": "JSON Decode Error",
            "raw": response.text
        }

    return {
        "status": "ok",
        "agentID": data.get("agentID"),
        "agent": data.get("agent"),
        "model": data.get("model"),
        "response": data.get("response"),
        "error": data.get("error"),
        "timestamp": data.get("timestamp")
    }
```

---

## 🚀 Cara Menggunakan

### Contoh Sederhana

```python
from ai_client import ask_ai

result = ask_ai(
    prompt="Buatkan puisi tentang AI",
    model="flash",
    url="https://ai.ptov.my.id/"
)

print(result)
```

---

## 🌐 Integrasi Dengan Flask

### File: `app.py`

```python
from flask import Flask, request, jsonify
from ai_client import ask_ai

app = Flask(__name__)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    
    result = ask_ai(
        prompt=data.get("prompt"),
        model=data.get("model", "flash"),
        url="https://ai.ptov.my.id/"
    )

    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

Test dengan:

```bash
curl -X POST http://localhost:5000/ask \
-H "Content-Type: application/json" \
-d '{"prompt":"Halo AI","model":"flash"}'
```

---

## 🔐 SSL Note

Saat ini menggunakan:

```python
verify=False
```

Artinya SSL certificate tidak diverifikasi.

Untuk production environment sebaiknya gunakan:

```python
verify=True
```

atau pasang SSL certificate valid pada server.

---

## 🧾 Contoh Response Sukses

```json
{
  "status": "ok",
  "agentID": "123",
  "agent": "Qwen",
  "model": "flash",
  "response": "Halo! Ada yang bisa saya bantu?",
  "error": null,
  "timestamp": "2026-02-20T12:00:00"
}
```

---

## 🧨 Contoh Error Response

```json
{
  "status": "error",
  "message": "HTTP Error (500)"
}
```

---

## 🖥 Deployment di Ubuntu (Optional)

Jalankan sebagai service menggunakan:

* systemd
* pm2 (python interpreter)
* supervisor

Jika ingin dibuatkan file service systemd, beri tahu.

---

## 📄 License

Free to use for internal project.

---

