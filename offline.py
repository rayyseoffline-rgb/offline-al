from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>OFFLINE AI</title>

<style>
*{box-sizing:border-box}

body{
    margin:0;
    height:100vh;
    font-family:Tahoma,Arial,sans-serif;
    color:white;
    background:
      radial-gradient(circle at 10% 10%,#553c9a,transparent 35%),
      radial-gradient(circle at 90% 90%,#176080,transparent 35%),
      #080b18;
}

.app{
    max-width:900px;
    height:100vh;
    margin:auto;
    display:flex;
    flex-direction:column;
    background:rgba(255,255,255,.06);
    backdrop-filter:blur(25px);
}

header{
    display:flex;
    align-items:center;
    gap:12px;
    padding:14px 18px;
    border-bottom:1px solid rgba(255,255,255,.12);
    background:rgba(255,255,255,.08);
}

.logo{
    width:46px;
    height:46px;
    display:grid;
    place-items:center;
    border-radius:16px;
    font-size:23px;
    background:rgba(255,255,255,.12);
    border:1px solid rgba(255,255,255,.2);
}

.title{
    font-size:18px;
    font-weight:bold;
}

.status{
    color:#78ffc0;
    font-size:11px;
    margin-top:4px;
}

.chat{
    flex:1;
    overflow-y:auto;
    padding:20px 14px;
}

.message{
    display:flex;
    margin:11px 0;
}

.user{
    justify-content:flex-start;
}

.ai{
    justify-content:flex-end;
}

.bubble{
    max-width:82%;
    padding:13px 16px;
    border-radius:20px;
    line-height:1.9;
    font-size:14px;
    white-space:pre-wrap;

    background:rgba(255,255,255,.09);
    border:1px solid rgba(255,255,255,.18);
    backdrop-filter:blur(20px);

    box-shadow:0 8px 30px rgba(0,0,0,.18);
}

.user .bubble{
    background:rgba(80,150,255,.16);
    border-bottom-right-radius:5px;
}

.ai .bubble{
    border-bottom-left-radius:5px;
}

.typing{
    display:none;
    width:max-content;
    margin:8px 0 8px auto;
    padding:9px 15px;
    border-radius:18px;
    background:rgba(255,255,255,.09);
    border:1px solid rgba(255,255,255,.15);
}

.dot{
    display:inline-block;
    width:6px;
    height:6px;
    margin:0 2px;
    border-radius:50%;
    background:white;
    animation:bounce 1s infinite;
}

.dot:nth-child(2){animation-delay:.15s}
.dot:nth-child(3){animation-delay:.3s}

@keyframes bounce{
    0%,60%,100%{
        transform:translateY(0);
        opacity:.4
    }
    30%{
        transform:translateY(-5px);
        opacity:1
    }
}

.bottom{
    padding:12px;
    border-top:1px solid rgba(255,255,255,.12);
    background:rgba(255,255,255,.06);
}

.input-box{
    display:flex;
    gap:8px;
    align-items:center;
    padding:7px;
    border-radius:24px;

    background:rgba(255,255,255,.09);
    border:1px solid rgba(255,255,255,.18);
    backdrop-filter:blur(20px);
}

textarea{
    flex:1;
    height:44px;
    resize:none;
    border:0;
    outline:0;
    background:transparent;
    color:white;
    padding:11px;
    font-family:Tahoma;
    font-size:14px;
}

textarea::placeholder{
    color:rgba(255,255,255,.5);
}

.send{
    width:45px;
    height:45px;
    border:0;
    border-radius:16px;
    cursor:pointer;
    color:white;
    font-size:19px;
    background:rgba(100,160,255,.25);
    border:1px solid rgba(255,255,255,.2);
}

.send:active{
    transform:scale(.94);
}

@media(max-width:600px){
    .bubble{
        max-width:90%;
    }
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

<div id="chat" class="chat">

    <div class="message ai">
        <div class="bubble">
سلام 👋
من OFFLINE AI هستم.

هر چیزی خواستی بگو؛
می‌تونیم گپ بزنیم، شوخی کنیم،
داستان بسازیم یا درباره موضوعات مختلف صحبت کنیم 😊
        </div>
    </div>

    <div id="typing" class="typing">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
    </div>

</div>

<div class="bottom">
    <div class="input-box">
        <textarea id="message"
        placeholder="پیامت را بنویس..."></textarea>

        <button class="send"
        onclick="sendMessage()">➤</button>
    </div>
</div>

</div>

<script>

const input =
document.getElementById("message");

const chat =
document.getElementById("chat");

const typing =
document.getElementById("typing");

input.addEventListener("keydown", function(e){

    if(e.key === "Enter" && !e.shiftKey){

        e.preventDefault();

        sendMessage();

    }

});

function addMessage(text,type){

    const row =
    document.createElement("div");

    row.className =
    "message " + type;

    const bubble =
    document.createElement("div");

    bubble.className =
    "bubble";

    bubble.textContent =
    text;

    row.appendChild(bubble);

    chat.insertBefore(row,typing);

    chat.scrollTop =
    chat.scrollHeight;
}

async function sendMessage(){

    const text =
    input.value.trim();

    if(!text)return;

    addMessage(text,"user");

    input.value="";

    typing.style.display="block";

    chat.scrollTop =
    chat.scrollHeight;

    try{

        const response =
        await fetch("/chat",{

            method:"POST",

            headers:{
                "Content-Type":
                "application/json"
            },

            body:JSON.stringify({
                message:text
            })

        });

        const data =
        await response.json();

        typing.style.display="none";

        addMessage(
            data.reply ||
            "پاسخی دریافت نشد.",
            "ai"
        );

    }catch(error){

        typing.style.display="none";

        addMessage(
            "اتصال به هوش مصنوعی برقرار نشد.",
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

    message = str(
        data.get("message","")
    ).strip()

    if not message:

        return jsonify(
            reply="پیامی دریافت نکردم 🙂"
        )

    api_key = os.environ.get(
        "OPENAI_API_KEY"
    )

    if not api_key:

        return jsonify(
            reply="کلید OPENAI_API_KEY در Render تنظیم نشده است."
        )

    try:

        client = OpenAI(
            api_key=api_key
        )

        response = client.responses.create(

            model=os.environ.get(
                "OPENAI_MODEL",
                "gpt-5.6"
            ),

            instructions="""
تو OFFLINE AI هستی.

یک دستیار فارسی‌زبان دوستانه،
باهوش، محترم و خوش‌صحبت باش.

با کاربر طبیعی و صمیمی صحبت کن،
اما وارد نقش‌آفرینی عاشقانه نشو.

می‌توانی:
- گپ بزنی
- شوخی سالم کنی
- داستان بسازی
- به سؤال‌ها پاسخ بدهی
- موضوعات آموزشی را توضیح بدهی
- وقتی کاربر ناراحت است با مهربانی پاسخ بدهی

پاسخ‌ها را واضح و متناسب با سؤال کاربر بده.
""",

            input=message
        )

        return jsonify(
            reply=response.output_text
        )

    except Exception as error:

        print(error)

        return jsonify(
            reply="فعلاً در اتصال به هوش مصنوعی مشکلی پیش آمده."
        ),500


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port
    )
