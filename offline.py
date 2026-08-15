from flask import Flask, request, jsonify, render_template_string
import requests
import os

app = Flask(__name__)

API_KEY = os.getenv("GROQ_API_KEY")

HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>OFFLINE AI</title>
<style>
body{
    margin:0;
    font-family:Arial,sans-serif;
    background:#101010;
    color:white;
}
header{
    padding:18px;
    text-align:center;
    background:#181818;
    font-size:24px;
    font-weight:bold;
}
#chat{
    height:75vh;
    overflow-y:auto;
    padding:15px;
}
.msg{
    padding:12px;
    margin:10px 0;
    border-radius:12px;
    max-width:85%;
    line-height:1.7;
}
.user{
    background:#333;
    margin-right:auto;
}
.ai{
    background:#1d5c3a;
    margin-left:auto;
}
form{
    display:flex;
    padding:10px;
    background:#181818;
    position:fixed;
    bottom:0;
    width:100%;
    box-sizing:border-box;
}
input{
    flex:1;
    padding:13px;
    border:0;
    border-radius:10px;
    font-size:16px;
}
button{
    margin-right:8px;
    padding:12px 18px;
    border:0;
    border-radius:10px;
    background:#20c77a;
    color:white;
    font-size:16px;
}
</style>
</head>

<body>

<header>🤖 OFFLINE AI</header>

<div id="chat"></div>

<form id="form">
<input id="message" placeholder="پیامت را بنویس..." autocomplete="off">
<button type="submit">ارسال</button>
</form>

<script>
const form = document.getElementById("form");
const input = document.getElementById("message");
const chat = document.getElementById("chat");

function addMessage(text, cls){
    const div = document.createElement("div");
    div.className = "msg " + cls;
    div.textContent = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

form.addEventListener("submit", async (e)=>{
    e.preventDefault();

    const text = input.value.trim();
    if(!text) return;

    addMessage(text, "user");
    input.value = "";

    addMessage("در حال فکر کردن...","ai");

    try{
        const response = await fetch("/chat",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({message:text})
        });

        const data = await response.json();

        chat.lastChild.remove();

        addMessage(
            data.reply || data.error || "خطایی رخ داد.",
            "ai"
        );

    }catch(error){
        chat.lastChild.remove();
        addMessage("اتصال به سرور مشکل دارد.","ai");
    }
});
</script>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "پیام خالی است."})

    if not API_KEY:
        return jsonify({
            "error": "کلید API تنظیم نشده است."
        })

    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.1-8b-instant",
                "messages": [{"role": "user", "content": message}]
            },
            timeout=60
        )

        result = response.json()

        if response.status_code != 200:
            return jsonify({
                "error": result.get("error", {}).get(
                    "message",
                    "خطا در API"
                )
            })

        answer = result.get("choices", [{}])[0].get("message", {}).get("content", "")


        return jsonify({
            "reply": answer or "پاسخی دریافت نشد."
        })

    except Exception as e:
        return jsonify({
            "error": "SERVER_ERROR: " + type(e).__name__
        })


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
