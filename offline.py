from flask import Flask, request, jsonify, render_template_string, Response
import os
import json
import requests

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

HTML = r"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="theme-color" content="#070b12">
<title>OFFLINE AI</title>

<style>
*{
    box-sizing:border-box;
    -webkit-tap-highlight-color:transparent;
}

html,body{
    margin:0;
    width:100%;
    height:100%;
    overflow:hidden;
}

body{
    font-family:Tahoma,Arial,sans-serif;
    color:#eef3f8;
    background:
        radial-gradient(circle at 80% -10%,rgba(36,104,180,.28),transparent 32%),
        radial-gradient(circle at -10% 90%,rgba(21,67,120,.24),transparent 32%),
        #070b12;
}

.app{
    width:100%;
    max-width:760px;
    height:100dvh;
    margin:auto;
    display:flex;
    flex-direction:column;
    overflow:hidden;
}

/* HEADER */

.header{
    height:70px;
    flex-shrink:0;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:9px 14px;
    background:rgba(6,10,16,.93);
    border-bottom:1px solid rgba(255,255,255,.07);
    backdrop-filter:blur(22px);
    z-index:10;
}

.brand{
    display:flex;
    align-items:center;
    gap:11px;
}

.logo{
    width:47px;
    height:47px;
    border-radius:15px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(145deg,#18283c,#0b111a);
    border:1px solid rgba(107,181,255,.28);
    box-shadow:
        0 0 24px rgba(40,130,220,.18),
        inset 0 1px rgba(255,255,255,.12);
}

.logo svg{
    width:35px;
    height:35px;
}

.brand-title{
    font-size:16px;
    font-weight:900;
    letter-spacing:.3px;
}

.brand-sub{
    margin-top:4px;
    color:#7e8b9b;
    font-size:9px;
}

.green-dot{
    display:inline-block;
    width:6px;
    height:6px;
    margin-left:4px;
    border-radius:50%;
    background:#36d68c;
    box-shadow:0 0 8px rgba(54,214,140,.8);
}

.clear{
    width:41px;
    height:41px;
    border-radius:13px;
    border:1px solid rgba(255,255,255,.08);
    background:rgba(255,255,255,.045);
    color:#bdc7d3;
    font-size:18px;
}

/* WELCOME */

.welcome{
    padding:28px 18px 13px;
    text-align:center;
}

.hero-logo{
    width:94px;
    height:94px;
    margin:auto;
    border-radius:28px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(145deg,#162538,#090f17);
    border:1px solid rgba(105,180,255,.23);
    box-shadow:
        0 20px 50px rgba(0,0,0,.42),
        0 0 45px rgba(38,126,210,.15),
        inset 0 1px rgba(255,255,255,.13);
}

.hero-logo svg{
    width:68px;
    height:68px;
}

.welcome h1{
    margin:15px 0 7px;
    font-size:23px;
    font-weight:900;
    background:linear-gradient(90deg,#fff,#aebed1);
    -webkit-background-clip:text;
    color:transparent;
}

.welcome p{
    margin:0;
    color:#697789;
    font-size:11px;
}

/* MESSAGES */

.messages{
    flex:1;
    overflow-y:auto;
    padding:7px 12px 14px;
    scroll-behavior:smooth;
}

.messages::-webkit-scrollbar{
    width:3px;
}

.messages::-webkit-scrollbar-thumb{
    background:#273342;
    border-radius:20px;
}

.message{
    display:flex;
    gap:8px;
    margin:13px 0;
    animation:appear .2s ease-out;
}

.message.user{
    flex-direction:row-reverse;
}

@keyframes appear{
    from{
        opacity:0;
        transform:translateY(5px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}

/* PROFILE */

.profile-wrap{
    width:38px;
    min-width:38px;
}

.profile{
    width:38px;
    height:38px;
    border-radius:12px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:8px;
    font-weight:900;
    color:#e9f3ff;
    background:linear-gradient(145deg,#1c2c3f,#0d141d);
    border:1px solid rgba(101,176,255,.22);
    box-shadow:0 6px 17px rgba(0,0,0,.35);
}

.profile-name{
    margin-top:4px;
    text-align:center;
    font-size:7px;
    color:#6e7c8c;
    white-space:nowrap;
}

/* BUBBLES */

.content{
    max-width:83%;
}

.bubble{
    padding:11px 14px;
    border-radius:17px;
    font-size:13px;
    line-height:1.9;
    white-space:pre-wrap;
    word-break:break-word;
}

.ai .bubble{
    background:
        linear-gradient(
            145deg,
            rgba(255,255,255,.075),
            rgba(255,255,255,.028)
        );
    border:1px solid rgba(255,255,255,.08);
    border-top-right-radius:5px;
    color:#e8edf3;
}

.user .bubble{
    background:
        linear-gradient(
            145deg,
            #1d2a39,
            #131b25
        );
    border:1px solid rgba(104,170,230,.12);
    border-top-left-radius:5px;
    color:#f0f4f8;
}

/* TYPING */

.typing{
    display:flex;
    align-items:center;
    gap:4px;
    height:18px;
}

.typing span{
    width:5px;
    height:5px;
    border-radius:50%;
    background:#91a4ba;
    animation:typing 1s infinite;
}

.typing span:nth-child(2){
    animation-delay:.15s;
}

.typing span:nth-child(3){
    animation-delay:.30s;
}

@keyframes typing{
    0%,100%{
        opacity:.25;
        transform:translateY(0);
    }
    50%{
        opacity:1;
        transform:translateY(-3px);
    }
}

/* SUGGESTIONS */

.suggestions{
    display:flex;
    gap:7px;
    overflow-x:auto;
    padding:5px 12px 9px;
}

.suggestions::-webkit-scrollbar{
    display:none;
}

.suggestion{
    flex-shrink:0;
    padding:8px 12px;
    border-radius:18px;
    border:1px solid rgba(255,255,255,.08);
    background:rgba(255,255,255,.045);
    color:#aab6c5;
    font-family:inherit;
    font-size:10px;
}

/* INPUT */

.input-area{
    flex-shrink:0;
    padding:8px 12px calc(10px + env(safe-area-inset-bottom));
    background:rgba(5,8,13,.95);
    border-top:1px solid rgba(255,255,255,.07);
    backdrop-filter:blur(22px);
}

.input-box{
    display:flex;
    align-items:flex-end;
    gap:7px;
    padding:5px;
    border-radius:19px;
    background:#101720;
    border:1px solid rgba(255,255,255,.09);
}

textarea{
    flex:1;
    min-width:0;
    height:43px;
    max-height:115px;
    resize:none;
    outline:none;
    border:0;
    background:transparent;
    color:#f4f7fa;
    font-family:inherit;
    font-size:13px;
    padding:12px 8px;
}

textarea::placeholder{
    color:#606d7c;
}

.send{
    width:43px;
    height:43px;
    border:1px solid rgba(109,181,255,.17);
    border-radius:14px;
    color:#fff;
    background:linear-gradient(145deg,#25435f,#172637);
    font-size:17px;
}

.send:disabled{
    opacity:.45;
}

.footer{
    text-align:center;
    margin-top:6px;
    color:#465362;
    font-size:7px;
}

@media(max-width:480px){

    .header{
        height:64px;
        padding:8px 12px;
    }

    .logo{
        width:42px;
        height:42px;
    }

    .welcome{
        padding-top:20px;
    }

    .hero-logo{
        width:78px;
        height:78px;
        border-radius:23px;
    }

    .hero-logo svg{
        width:56px;
        height:56px;
    }

    .welcome h1{
        font-size:21px;
    }

    .content{
        max-width:84%;
    }

    .bubble{
        font-size:12.5px;
    }
}
</style>
</head>

<body>

<div class="app">

<header class="header">

<div class="brand">

<div class="logo">

<svg viewBox="0 0 100 100" fill="none">
<path
d="M22 29C22 23 27 18 33 18H67C73 18 78 23 78 29V58C78 64 73 69 67 69H51L39 82V69H33C27 69 22 64 22 58V29Z"
stroke="#70B8FF"
stroke-width="5"
stroke-linejoin="round"/>

<path
d="M35 43H65"
stroke="#DCEEFF"
stroke-width="5"
stroke-linecap="round"/>

<path
d="M42 54H58"
stroke="#70B8FF"
stroke-width="5"
stroke-linecap="round"/>

<circle
cx="76"
cy="24"
r="8"
fill="#70B8FF"/>
</svg>

</div>

<div>

<div class="brand-title">
OFFLINE AI
</div>

<div class="brand-sub">
<span class="green-dot"></span>
آماده پاسخ‌گویی
</div>

</div>

</div>

<button class="clear" onclick="clearChat()">
⌫
</button>

</header>

<section class="welcome" id="welcome">

<div class="hero-logo">

<svg viewBox="0 0 100 100" fill="none">

<path
d="M22 29C22 23 27 18 33 18H67C73 18 78 23 78 29V58C78 64 73 69 67 69H51L39 82V69H33C27 69 22 64 22 58V29Z"
stroke="#70B8FF"
stroke-width="5"
stroke-linejoin="round"/>

<path
d="M35 43H65"
stroke="#DCEEFF"
stroke-width="5"
stroke-linecap="round"/>

<path
d="M42 54H58"
stroke="#70B8FF"
stroke-width="5"
stroke-linecap="round"/>

<circle
cx="76"
cy="24"
r="8"
fill="#70B8FF"/>

</svg>

</div>

<h1>
خوش آمدی به OFFLINE AI
</h1>

<p>
سریع، هوشمند و آماده گفت‌وگو
</p>

</section>

<main class="messages" id="messages"></main>

<div class="suggestions">

<button class="suggestion"
onclick="quickAsk('سلام، خودت را معرفی کن')">
معرفی OFFLINE AI
</button>

<button class="suggestion"
onclick="quickAsk('سازنده تو کیست؟')">
سازنده
</button>

<button class="suggestion"
onclick="quickAsk('برای یادگیری برنامه نویسی کمکم کن')">
برنامه‌نویسی
</button>

<button class="suggestion"
onclick="quickAsk('یک ایده جالب بهم بده')">
ایده
</button>

</div>

<div class="input-area">

<div class="input-box">

<textarea
id="input"
placeholder="پیامت را بنویس..."
oninput="resizeInput(this)"
onkeydown="handleKey(event)"
></textarea>

<button
id="send"
class="send"
onclick="sendMessage()">
➤
</button>

</div>

<div class="footer">
OFFLINE AI • ساخته‌شده توسط ریس آفلاین کندزی
</div>

</div>

</div>

<script>

const input = document.getElementById("input");
const messages = document.getElementById("messages");
const welcome = document.getElementById("welcome");
const send = document.getElementById("send");

function scrollBottom(){
    requestAnimationFrame(() => {
        messages.scrollTop = messages.scrollHeight;
    });
}

function addMessage(text, type){

    welcome.style.display = "none";

    const row = document.createElement("div");
    row.className = "message " + type;

    const profileWrap = document.createElement("div");
    profileWrap.className = "profile-wrap";

    const profile = document.createElement("div");
    profile.className = "profile";
    profile.textContent = type === "user" ? "OFF" : "AI";

    const profileName = document.createElement("div");
    profileName.className = "profile-name";
    profileName.textContent =
        type === "user" ? "آفلاین" : "OFFLINE AI";

    profileWrap.appendChild(profile);
    profileWrap.appendChild(profileName);

    const content = document.createElement("div");
    content.className = "content";

    const bubble = document.createElement("div");
    bubble.className = "bubble";
    bubble.textContent = text || "";

    content.appendChild(bubble);

    row.appendChild(profileWrap);
    row.appendChild(content);

    messages.appendChild(row);

    scrollBottom();

    return bubble;
}

function addTyping(){

    welcome.style.display = "none";

    const row = document.createElement("div");
    row.className = "message ai";

    const profileWrap = document.createElement("div");
    profileWrap.className = "profile-wrap";

    const profile = document.createElement("div");
    profile.className = "profile";
    profile.textContent = "AI";

    const profileName = document.createElement("div");
    profileName.className = "profile-name";
    profileName.textContent = "OFFLINE AI";

    profileWrap.appendChild(profile);
    profileWrap.appendChild(profileName);

    const content = document.createElement("div");
    content.className = "content";

    const bubble = document.createElement("div");
    bubble.className = "bubble";

    bubble.innerHTML = `
        <div class="typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    content.appendChild(bubble);

    row.appendChild(profileWrap);
    row.appendChild(content);

    messages.appendChild(row);

    scrollBottom();

    return row;
}

function quickAsk(text){
    input.value = text;
    resizeInput(input);
    sendMessage();
}

function handleKey(event){

    if(event.key === "Enter" && !event.shiftKey){
        event.preventDefault();
        sendMessage();
    }
}

function resizeInput(el){

    el.style.height = "43px";

    el.style.height =
        Math.min(el.scrollHeight, 115) + "px";
}

async function sendMessage(){

    const text = input.value.trim();

    if(!text || send.disabled){
        return;
    }

    addMessage(text, "user");

    input.value = "";
    input.style.height = "43px";

    send.disabled = true;

    const typing = addTyping();

    try{

        const response = await fetch("/chat", {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                message:text
            })
        });

        if(!response.ok){

            let errorMessage = "خطا در پاسخ‌گویی.";

            try{
                const error = await response.json();
                errorMessage = error.error || errorMessage;
            }catch(e){}

            typing.remove();
            addMessage(errorMessage, "ai");
            return;
        }

        typing.remove();

        const bubble = addMessage("", "ai");

        if(!response.body){
            bubble.textContent = "پاسخی دریافت نشد.";
            return;
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let fullText = "";

        let buffer = "";

        while(true){

            const result = await reader.read();

            if(result.done){
                break;
            }

            buffer += decoder.decode(
                result.value,
                {stream:true}
            );

            const parts = buffer.split("\n");

            buffer = parts.pop() || "";

            for(const line of parts){

                if(!line.startsWith("data:")){
                    continue;
                }

                const data = line.slice(5).trim();

                if(!data || data === "[DONE]"){
                    continue;
                }

                try{

                    const obj = JSON.parse(data);

                    if(obj.error){
                        fullText += obj.error;
                    }else{
                        fullText += obj.text || "";
                    }

                    bubble.textContent = fullText;

                    scrollBottom();

                }catch(e){}
            }
        }

        if(!fullText){
            bubble.textContent = "پاسخی دریافت نشد.";
        }

    }catch(error){

        typing.remove();

        addMessage(
            "ارتباط با سرور برقرار نشد. دوباره تلاش کن.",
            "ai"
        );

    }finally{

        send.disabled = false;
        input.focus();
    }
}

function clearChat(){

    messages.innerHTML = "";

    welcome.style.display = "block";

    input.focus();
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

    message = str(data.get("message", "")).strip()

    if not message:
        return jsonify({
            "error": "پیام خالی است."
        }), 400

    if not GROQ_API_KEY:
        return jsonify({
            "error": "GROQ_API_KEY در Render تنظیم نشده است."
        }), 500

    system_prompt = """
تو OFFLINE AI هستی؛ یک دستیار هوش مصنوعی مدرن.

نام محصول:
OFFLINE AI

سازنده و بنیان‌گذار:
ریس آفلاین کندزی

اگر کاربر درباره سازنده، بنیان‌گذار یا خالق OFFLINE AI پرسید، پاسخ بده:

«سازنده و بنیان‌گذار من ریس آفلاین کندزی است؛ خالق پروژه OFFLINE AI.»

اگر کاربر پرسید تو کی هستی، بگو:

«من OFFLINE AI هستم؛ یک دستیار هوش مصنوعی مدرن که با هدف ارائه تجربه‌ای هوشمند، زیبا و متفاوت ساخته شده‌ام. سازنده و بنیان‌گذار من ریس آفلاین کندزی است.»

با کاربر به زبان خودش صحبت کن.
پاسخ‌ها طبیعی، واضح، کوتاه و مفید باشند.
اطلاعاتی درباره سازنده که مشخص نشده را از خودت اختراع نکن.
"""

    try:

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",

            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },

            json={
                "model": "llama-3.1-8b-instant",

                "messages":[
                    {
                        "role":"system",
                        "content":system_prompt
                    },
                    {
                        "role":"user",
                        "content":message
                    }
                ],

                "temperature":0.6,
                "max_tokens":1000,
                "stream":True
            },

            stream=True,
            timeout=60
        )

        if response.status_code != 200:

            try:
                result = response.json()

                error = (
                    result.get("error", {}).get(
                        "message",
                        "خطا در سرویس هوش مصنوعی."
                    )
                )

            except Exception:
                error = "خطا در سرویس هوش مصنوعی."

            return jsonify({
                "error": error
            }), 500

        def generate():

            try:

                for line in response.iter_lines(
                    decode_unicode=True
                ):

                    if not line:
                        continue

                    if not line.startswith("data:"):
                        continue

                    data = line[5:].strip()

                    if data == "[DONE]":
                        break

                    try:

                        obj = json.loads(data)

                        choices = obj.get("choices", [])

                        if not choices:
                            continue

                        delta = choices[0].get("delta", {})

                        text = delta.get("content", "")

                        if text:

                            payload = {
                                "text": text
                            }

                            yield (
                                "data: "
                                + json.dumps(
                                    payload,
                                    ensure_ascii=False
                                )
                                + "\n\n"
                            )

                    except Exception:
                        continue

                yield "data: [DONE]\n\n"

            except Exception:

                payload = {
                    "error": "ارتباط با سرویس قطع شد."
                }

                yield (
                    "data: "
                    + json.dumps(
                        payload,
                        ensure_ascii=False
                    )
                    + "\n\n"
                )

        return Response(
            generate(),
            mimetype="text/event-stream",
            headers={
                "Cache-Control":"no-cache",
                "X-Accel-Buffering":"no",
                "Connection":"keep-alive"
            }
        )

    except requests.exceptions.Timeout:

        return jsonify({
            "error": "زمان پاسخ‌گویی تمام شد."
        }), 504

    except Exception:

        return jsonify({
            "error": "خطایی در ارتباط با سرور رخ داد."
        }), 500


if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host="0.0.0.0",
        port=port
                            )
