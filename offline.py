from flask import Flask, request, jsonify, render_template_string
import os
import requests

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

HTML = r"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="theme-color" content="#090611">
<title>OFFLINE AI</title>

<style>
* {
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}

html, body {
    margin: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

body {
    font-family: Tahoma, Arial, sans-serif;
    color: #fff;
    background:
        radial-gradient(circle at 15% 15%, rgba(255, 70, 170, .16), transparent 28%),
        radial-gradient(circle at 85% 20%, rgba(120, 70, 255, .18), transparent 30%),
        radial-gradient(circle at 50% 100%, rgba(255, 30, 130, .12), transparent 35%),
        #08050d;
}

/* Background lights */
body::before,
body::after {
    content: "";
    position: fixed;
    width: 260px;
    height: 260px;
    border-radius: 50%;
    filter: blur(80px);
    pointer-events: none;
    opacity: .35;
    animation: floatLight 8s ease-in-out infinite alternate;
}

body::before {
    background: #ff2f9d;
    top: -100px;
    right: -80px;
}

body::after {
    background: #684cff;
    bottom: -120px;
    left: -100px;
    animation-delay: 2s;
}

@keyframes floatLight {
    from { transform: translate(0,0) scale(1); }
    to { transform: translate(35px,25px) scale(1.15); }
}

.app {
    position: relative;
    width: 100%;
    max-width: 720px;
    height: 100dvh;
    margin: auto;
    display: flex;
    flex-direction: column;
    overflow: hidden;
}

/* Header */
.header {
    position: relative;
    z-index: 5;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 17px;
    background: rgba(10, 6, 18, .72);
    border-bottom: 1px solid rgba(255,255,255,.08);
    backdrop-filter: blur(20px);
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo {
    position: relative;
    width: 48px;
    height: 48px;
    border-radius: 17px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    font-size: 13px;
    letter-spacing: -1px;
    color: #fff;
    background: linear-gradient(135deg, #ff4baa, #743cff);
    box-shadow:
        0 0 20px rgba(255, 65, 170, .35),
        inset 0 1px 1px rgba(255,255,255,.4);
}

.logo::after {
    content: "♥";
    position: absolute;
    font-size: 9px;
    bottom: 5px;
    left: 6px;
    opacity: .9;
}

.brand-title {
    font-size: 17px;
    font-weight: 800;
}

.brand-subtitle {
    margin-top: 4px;
    font-size: 10px;
    color: #c4afc9;
}

.online {
    color: #ff80c4;
}

.dot {
    display: inline-block;
    width: 6px;
    height: 6px;
    margin-left: 4px;
    border-radius: 50%;
    background: #ff55ad;
    box-shadow: 0 0 9px #ff55ad;
}

.clear-btn {
    width: 42px;
    height: 42px;
    border: 1px solid rgba(255,255,255,.09);
    border-radius: 14px;
    background: rgba(255,255,255,.05);
    color: #fff;
    font-size: 19px;
}

/* Welcome */
.welcome {
    position: relative;
    text-align: center;
    padding: 27px 20px 10px;
    z-index: 2;
    transition: .4s ease;
}

.hero {
    position: relative;
    width: 92px;
    height: 92px;
    margin: 0 auto 16px;
    border-radius: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    background:
        linear-gradient(145deg, rgba(255,255,255,.15), rgba(255,255,255,.03));
    border: 1px solid rgba(255,255,255,.13);
    box-shadow:
        0 0 45px rgba(255, 55, 169, .18),
        inset 0 1px 1px rgba(255,255,255,.2);
    backdrop-filter: blur(20px);
    animation: heroFloat 4s ease-in-out infinite;
}

.hero::before {
    content: "";
    position: absolute;
    inset: -8px;
    border-radius: 35px;
    border: 1px solid rgba(255,70,180,.18);
    animation: pulse 2.5s ease-in-out infinite;
}

.hero-heart {
    font-size: 43px;
    color: #ff55b0;
    text-shadow:
        0 0 12px #ff55b0,
        0 0 35px rgba(255,55,170,.7);
}

@keyframes heroFloat {
    0%,100% { transform: translateY(0); }
    50% { transform: translateY(-7px); }
}

@keyframes pulse {
    0%,100% { transform: scale(.98); opacity: .4; }
    50% { transform: scale(1.06); opacity: 1; }
}

.welcome h1 {
    margin: 0;
    font-size: 25px;
    background: linear-gradient(90deg, #fff, #ffb4dd, #b9a7ff);
    -webkit-background-clip: text;
    color: transparent;
}

.welcome p {
    margin: 9px 0 0;
    color: #a99baa;
    font-size: 12px;
}

/* Chat */
.messages {
    flex: 1;
    overflow-y: auto;
    padding: 12px 16px 14px;
    scroll-behavior: smooth;
    z-index: 2;
}

.messages::-webkit-scrollbar {
    width: 3px;
}

.messages::-webkit-scrollbar-thumb {
    background: rgba(255,90,180,.35);
    border-radius: 20px;
}

.message {
    display: flex;
    margin: 12px 0;
    animation: messageIn .3s ease;
}

@keyframes messageIn {
    from {
        opacity: 0;
        transform: translateY(8px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.message.user {
    justify-content: flex-start;
}

.message.ai {
    justify-content: flex-end;
}

.bubble {
    max-width: 86%;
    padding: 13px 16px;
    font-size: 14px;
    line-height: 1.9;
    white-space: pre-wrap;
    word-wrap: break-word;
    border-radius: 21px;
}

.user .bubble {
    background:
        linear-gradient(135deg, rgba(255,66,166,.18), rgba(116,61,255,.16));
    border: 1px solid rgba(255,100,190,.15);
    border-bottom-right-radius: 6px;
    color: #f9edf6;
    box-shadow: 0 8px 25px rgba(0,0,0,.15);
}

.ai .bubble {
    color: #fff;
    background:
        linear-gradient(135deg, rgba(255,255,255,.105), rgba(255,255,255,.045));
    border: 1px solid rgba(255,255,255,.11);
    border-bottom-left-radius: 6px;
    box-shadow: 0 8px 25px rgba(0,0,0,.18);
    backdrop-filter: blur(15px);
}

/* Typing */
.typing {
    display: flex;
    gap: 5px;
    align-items: center;
    height: 20px;
}

.typing span {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #ff6eb9;
    animation: typing 1.1s infinite;
}

.typing span:nth-child(2) {
    animation-delay: .15s;
}

.typing span:nth-child(3) {
    animation-delay: .3s;
}

@keyframes typing {
    0%,60%,100% { transform: translateY(0); opacity: .35; }
    30% { transform: translateY(-5px); opacity: 1; }
}

/* Suggestions */
.suggestions {
    position: relative;
    z-index: 4;
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 6px 15px 10px;
}

.suggestions::-webkit-scrollbar {
    display: none;
}

.suggestions button {
    flex-shrink: 0;
    border: 1px solid rgba(255,100,190,.14);
    border-radius: 20px;
    padding: 9px 13px;
    color: #d9c8d9;
    background: rgba(255,255,255,.045);
    font-family: inherit;
    font-size: 11px;
    backdrop-filter: blur(10px);
}

.suggestions button:active {
    transform: scale(.96);
}

/* Input */
.input-area {
    position: relative;
    z-index: 5;
    padding: 9px 13px 13px;
    background: rgba(8,5,13,.82);
    border-top: 1px solid rgba(255,255,255,.07);
    backdrop-filter: blur(22px);
}

.input-box {
    display: flex;
    align-items: flex-end;
    gap: 7px;
    padding: 6px;
    border-radius: 23px;
    background: rgba(255,255,255,.055);
    border: 1px solid rgba(255,100,190,.14);
    box-shadow: 0 8px 30px rgba(0,0,0,.25);
}

textarea {
    flex: 1;
    height: 44px;
    max-height: 110px;
    resize: none;
    border: 0;
    outline: 0;
    color: #fff;
    background: transparent;
    font-family: inherit;
    font-size: 14px;
    padding: 12px 8px;
}

textarea::placeholder {
    color: #776b79;
}

.send {
    width: 44px;
    height: 44px;
    flex-shrink: 0;
    border: 0;
    border-radius: 16px;
    color: #fff;
    font-size: 18px;
    background: linear-gradient(135deg, #ff4baa, #7040ff);
    box-shadow:
        0 0 18px rgba(255,65,170,.3),
        inset 0 1px 1px rgba(255,255,255,.3);
}

.send:active {
    transform: scale(.92);
}

.footer {
    text-align: center;
    margin-top: 7px;
    font-size: 8px;
    color: #5f5362;
}

/* Mobile */
@media (max-width: 480px) {
    .header {
        padding: 13px 14px;
    }

    .welcome {
        padding-top: 23px;
    }

    .hero {
        width: 78px;
        height: 78px;
        border-radius: 25px;
    }

    .hero-heart {
        font-size: 36px;
    }

    .welcome h1 {
        font-size: 22px;
    }

    .bubble {
        font-size: 13px;
        max-width: 89%;
    }
}
</style>
</head>

<body>

<div class="app">

    <header class="header">
        <div class="brand">
            <div class="logo">OFF</div>

            <div>
                <div class="brand-title">OFFLINE AI</div>
                <div class="brand-subtitle">
                    <span class="dot"></span>
                    <span class="online">همیشه آماده گفت‌وگو</span>
                </div>
            </div>
        </div>

        <button class="clear-btn" onclick="clearChat()">⋮</button>
    </header>

    <section class="welcome" id="welcome">

        <div class="hero">
            <div class="hero-heart">♥</div>
        </div>

        <h1>به دنیای OFFLINE خوش آمدی</h1>

        <p>
            یک گفت‌وگوی متفاوت، آرام و هوشمندانه ✨
        </p>

    </section>

    <main class="messages" id="messages"></main>

    <div class="suggestions">
        <button onclick="quickAsk('سلام، خودت را معرفی کن')">
            ✨ معرفی خودت
        </button>

        <button onclick="quickAsk('برای یادگیری برنامه نویسی راهنمایی‌ام کن')">
            💻 برنامه‌نویسی
        </button>

        <button onclick="quickAsk('یک متن زیبا و احساسی برایم بنویس')">
            💜 متن زیبا
        </button>

        <button onclick="quickAsk('امروز چه چیز جدیدی می‌توانم یاد بگیرم؟')">
            🌙 ایده جدید
        </button>
    </div>

    <div class="input-area">

        <div class="input-box">

            <textarea
                id="input"
                placeholder="حرف دلت را بنویس..."
                oninput="autoResize(this)"
                onkeydown="handleKey(event)"
            ></textarea>

            <button class="send" onclick="sendMessage()">
                ➤
            </button>

        </div>

        <div class="footer">
            OFFLINE AI • ساخته شده برای گفت‌وگوی هوشمند
        </div>

    </div>

</div>

<script>

const input = document.getElementById("input");
const messages = document.getElementById("messages");
const welcome = document.getElementById("welcome");

function addMessage(text, type) {

    welcome.style.display = "none";

    const row = document.createElement("div");
    row.className = "message " + type;

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    bubble.textContent = text;

    row.appendChild(bubble);
    messages.appendChild(row);

    messages.scrollTop = messages.scrollHeight;

    return bubble;
}

function addTyping() {

    welcome.style.display = "none";

    const row = document.createElement("div");
    row.className = "message ai";

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    bubble.innerHTML = `
        <div class="typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    row.appendChild(bubble);
    messages.appendChild(row);

    messages.scrollTop = messages.scrollHeight;

    return row;
}

function quickAsk(text) {

    input.value = text;
    autoResize(input);
    sendMessage();

}

function handleKey(event) {

    if (event.key === "Enter" && !event.shiftKey) {

        event.preventDefault();
        sendMessage();

    }

}

function autoResize(element) {

    element.style.height = "44px";

    element.style.height =
        Math.min(element.scrollHeight, 110) + "px";

}

async function sendMessage() {

    const text = input.value.trim();

    if (!text) return;

    addMessage(text, "user");

    input.value = "";
    input.style.height = "44px";

    const typing = addTyping();

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: text
            })

        });

        const data = await response.json();

        typing.remove();

        if (data.reply) {

            addMessage(data.reply, "ai");

        } else {

            addMessage(
                data.error || "یک خطای ناشناخته رخ داد.",
                "ai"
            );

        }

    } catch (error) {

        typing.remove();

        addMessage(
            "ارتباط با سرور برقرار نشد. دوباره تلاش کن.",
            "ai"
        );

    }

}

function clearChat() {

    if (confirm("گفت‌وگو پاک شود؟")) {

        messages.innerHTML = "";

        welcome.style.display = "block";

    }

}

</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True) or {}

    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "error": "پیام خالی است."
        }), 400

    if not GROQ_API_KEY:
        return jsonify({
            "error": "کلید GROQ_API_KEY در Render تنظیم نشده است."
        }), 500

    try:

        response = requests.post(

            "https://api.groq.com/openai/v1/chat/completions",

            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },

            json={

                "model": "llama-3.3-70b-versatile",

                "messages": [

                    {
                        "role": "system",
                        "content":
                        "تو دستیار هوشمند OFFLINE AI هستی. "
                        "با کاربر به زبان خودش صحبت کن. "
                        "پاسخ‌ها واضح، دوستانه، مفید و محترمانه باشند."
                    },

                    {
                        "role": "user",
                        "content": message
                    }

                ],

                "temperature": 0.7,

                "max_tokens": 1500

            },

            timeout=60

        )

        result = response.json()

        if response.status_code != 200:

            error_message = (
                result
                .get("error", {})
                .get(
                    "message",
                    "خطا در ارتباط با سرویس هوش مصنوعی."
                )
            )

            return jsonify({
                "error": error_message
            }), 500

        reply = (
            result["choices"][0]["message"]["content"]
        )

        return jsonify({
            "reply": reply
        })

    except requests.exceptions.Timeout:

        return jsonify({
            "error": "زمان پاسخ‌گویی تمام شد. دوباره تلاش کن."
        }), 504

    except Exception:

        return jsonify({
            "error": "خطایی در سرور رخ داد."
        }), 500


if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
