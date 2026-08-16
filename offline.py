from flask import Flask, request, jsonify, render_template_string
import os
import requests

app = Flask(__name__)

HTML = r"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>OFFLINE AI</title>

<style>
*{box-sizing:border-box}

body{
    margin:0;
    height:100vh;
    overflow:hidden;
    font-family:Tahoma,Arial,sans-serif;
    background:
      radial-gradient(circle at 15% 20%,#403080 0,transparent 35%),
      radial-gradient(circle at 85% 80%,#164b70 0,transparent 35%),
      linear-gradient(135deg,#080b18,#10152b 55%,#07151f);
    color:white;
}

.app{
    width:100%;
    max-width:850px;
    height:100vh;
    margin:auto;
    display:flex;
    flex-direction:column;
    background:rgba(255,255,255,.055);
    backdrop-filter:blur(25px);
    -webkit-backdrop-filter:blur(25px);
    border-left:1px solid rgba(255,255,255,.08);
    border-right:1px solid rgba(255,255,255,.08);
}

header{
    height:72px;
    flex-shrink:0;
    display:flex;
    align-items:center;
    gap:12px;
    padding:12px 18px;
    background:rgba(255,255,255,.08);
    border-bottom:1px solid rgba(255,255,255,.1);
    backdrop-filter:blur(20px);
}

.logo{
    width:45px;
    height:45px;
    border-radius:15px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:23px;
    background:rgba(255,255,255,.12);
    border:1px solid rgba(255,255,255,.18);
    box-shadow:0 8px 25px rgba(0,0,0,.2);
}

.title{
    font-size:18px;
    font-weight:bold;
}

.status{
    font-size:11px;
    color:#83ffc1;
    margin-top:3px;
}

.chat{
    flex:1;
    overflow-y:auto;
    padding:20px 15px 25px;
    scroll-behavior:smooth;
}

.chat::-webkit-scrollbar{width:4px}
.chat::-webkit-scrollbar-thumb{
    background:rgba(255,255,255,.2);
    border-radius:10px;
}

.message{
    display:flex;
    margin:10px 0;
    animation:appear .25s ease;
}

@keyframes appear{
    from{opacity:0;transform:translateY(8px)}
    to{opacity:1;transform:translateY(0)}
}

.message.user{justify-content:flex-start}
.message.ai{justify-content:flex-end}

.bubble{
    max-width:78%;
    padding:12px 15px;
    border-radius:20px;
    line-height:1.8;
    font-size:14px;
    white-space:pre-wrap;
    box-shadow:0 8px 25px rgba(0,0,0,.15);
}

.user .bubble{
    background:rgba(100,170,255,.15);
    border:1px solid rgba(150,200,255,.22);
    border-bottom-right-radius:5px;
}

.ai .bubble{
    background:rgba(255,255,255,.095);
    border:1px solid rgba(255,255,255,.16);
    border-bottom-left-radius:5px;
}

.typing{
    display:none;
    width:max-content;
    padding:10px 16px;
    margin:8px 0 8px auto;
    border-radius:18px;
    background:rgba(255,255,255,.08);
    border:1px solid rgba(255,255,255,.12);
}

.dot{
    display:inline-block;
    width:6px;
    height:6px;
    margin:0 2px;
    border-radius:50%;
    background:#ddd;
    animation:bounce 1s infinite;
}

.dot:nth-child(2){animation-delay:.15s}
.dot:nth-child(3){animation-delay:.3s}

@keyframes bounce{
    0%,60%,100%{transform:translateY(0);opacity:.4}
    30%{transform:translateY(-5px);opacity:1}
}

.bottom{
    padding:12px;
    background:rgba(255,255,255,.055);
    border-top:1px solid rgba(255,255,255,.1);
    backdrop-filter:blur(20px);
}

.inputbox{
    display:flex;
    align-items:center;
    gap:8px;
    padding:7px;
    border-radius:22px;
    background:rgba(255,255,255,.09);
    border:1px solid rgba(255,255,255,.15);
    box-shadow:0 10px 30px rgba(0,0,0,.18);
}

textarea{
    flex:1;
    resize:none;
    height:42px;
    max-height:110px;
    border:0;
    outline:0;
    background:transparent;
    color:white;
    padding:10px 12px;
    font-family:inherit;
    font-size:14px;
}

textarea::placeholder{
    color:rgba(255,255,255,.5);
}

.send{
    width:43px;
    height:43px;
    border:0;
    border-radius:16px;
    cursor:pointer;
    color:white;
    font-size:18px;
    background:rgba(120,170,255,.2);
    border:1px solid rgba(180,210,255,.25);
    transition:.2s;
}

.send:hover{
    transform:scale(1.05);
    background:rgba(120,170,255,.3);
}

.send:active{transform:scale(.94)}

.welcome{
    text-align:center;
    margin:30px auto;
    max-width:500px;
}

.welcome h1{
    font-size:28px;
    margin-bottom:8px;
}

.welcome p{
    color:rgba(255,255,255,.65);
    line-height:1.8;
    font-size:13px;
}

@media(max-width:600px){
    .bubble{max-width:88%}
    header{height:65px}
    .chat{padding:15px 10px}
    .welcome h1{font-size:24px}
}
</style>
</head>

<body>

<div class="app">

<header>
    <div class="logo">🤖</div>
    <div>
        <div class="title">OFFLINE AI</div>
        <div class="status">● آمادهٔ گفتگو</div>
    </div>
</header>

<div class="chat" id="chat">

    <div class="welcome">
        <h1>سلام 👋</h1>
        <p>
            من OFFLINE AI هستم.<br>
            می‌تونی باهام گپ بزنی، سؤال بپرسی،
            شوخی کنی یا درباره موضوعات مختلف صحبت کنی.
        </p>
    </div>

    <div class="message ai">
        <div class="bubble">
            سلام! 😊 خوش آمدی.<br>
            بگو ببینم امروز درباره چی گپ بزنیم؟
        </div>
    </div>

    <div class="typing" id="typing">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
    </div>

</div>

<div class="bottom">
    <div class="inputbox">
        <textarea id="input" placeholder="پیامت را بنویس..." rows="1"></textarea>
        <button class="send" onclick="sendMessage()">➤</button>
    </div>
</div>

</div>

<script>
const input=document.getElementById("input");
const chat=document.getElementById("chat");
const typing=document.getElementById("typing");

input.addEventListener("keydown",function(e){
    if(e.key==="Enter" && !e.shiftKey){
        e.preventDefault();
        sendMessage();
    }
});

input.addEventListener("input",function(){
    this.style.height="42px";
    this.style.height=Math.min(this.scrollHeight,110)+"px";
});

function addMessage(text,type){
    const row=document.createElement("div");
    row.className="message "+type;

    const bubble=document.createElement("div");
    bubble.className="bubble";
    bubble.textContent=text;

    row.appendChild(bubble);
    chat.insertBefore(row,typing);

    chat.scrollTop=chat.scrollHeight;
}

async function sendMessage(){

    const text=input.value.trim();
    if(!text) return;

    addMessage(text,"user");

    input.value="";
    input.style.height="42px";

    typing.style.display="block";
    chat.scrollTop=chat.scrollHeight;

    try{
        const response=await fetch("/chat",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({message:text})
        });

        const data=await response.json();

        typing.style.display="none";
        addMessage(data.reply || "فعلاً نتوانستم پاسخ بدهم 😅","ai");

    }catch(error){

        typing.style.display="none";

        addMessage(
            "فعلاً اتصال هوش مصنوعی آماده نیست؛ اما صفحه چت درست کار می‌کند. 🤖",
            "ai"
        );
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
        return jsonify({"reply": "پیامی دریافت نکردم 🙂"})

    # پاسخ آزمایشی
    # بعداً این قسمت را به API هوش مصنوعی وصل می‌کنیم.
    reply = f"پیامت را دریافت کردم 😊\n\nگفتی: {message}"

    return jsonify({"reply": reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
