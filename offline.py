from flask import Flask, request, jsonify, Response
import os
import requests
import json

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "").strip()
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

HTML = r"""<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#f4f8ff">
<title>OFFLINE AI</title>
<style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;width:100%;height:100%;overflow:hidden}
body{
font-family:Tahoma,Arial,sans-serif;color:#142235;
background:
radial-gradient(circle at 85% -10%,rgba(100,181,246,.28),transparent 30%),
radial-gradient(circle at -10% 95%,rgba(143,211,255,.22),transparent 32%),
linear-gradient(135deg,#f8fbff,#edf5fc);
}
.app{height:100dvh;width:100%;max-width:860px;margin:auto;display:flex;flex-direction:column}
.header{
height:74px;flex-shrink:0;padding:10px 15px;display:flex;align-items:center;justify-content:space-between;
background:rgba(255,255,255,.78);border-bottom:1px solid rgba(110,145,180,.16);
backdrop-filter:blur(22px);box-shadow:0 4px 22px rgba(42,78,112,.06);z-index:5
}
.brand{display:flex;align-items:center;gap:11px}
.logo{
width:50px;height:50px;border-radius:17px;display:flex;align-items:center;justify-content:center;
background:linear-gradient(145deg,#123b60,#5da7df);box-shadow:0 9px 28px rgba(45,119,177,.25);
border:1px solid rgba(255,255,255,.7)
}
.logo svg{width:35px;height:35px}
.brand-title{font-size:17px;font-weight:900;letter-spacing:.2px}
.brand-sub{font-size:9px;color:#718299;margin-top:4px}
.dot{display:inline-block;width:7px;height:7px;border-radius:50%;background:#22bd7c;margin-left:5px;box-shadow:0 0 9px rgba(34,189,124,.65)}
.clear{
width:43px;height:43px;border-radius:14px;border:1px solid #dce6ef;background:rgba(255,255,255,.8);
color:#60748a;font-size:18px;box-shadow:0 5px 16px rgba(40,70,100,.07)
}
.welcome{text-align:center;padding:27px 18px 12px}
.hero{
width:104px;height:104px;margin:auto;border-radius:31px;display:flex;align-items:center;justify-content:center;
background:linear-gradient(145deg,#123b60,#65afe5);box-shadow:0 22px 48px rgba(41,116,174,.24);
border:1px solid rgba(255,255,255,.85)
}
.hero svg{width:70px;height:70px}
.welcome h1{
margin:16px 0 8px;font-size:24px;font-weight:900;
background:linear-gradient(90deg,#123b60,#4386b9);-webkit-background-clip:text;color:transparent
}
.welcome p{margin:0;color:#75869a;font-size:11px}
.messages{flex:1;overflow-y:auto;padding:8px 14px 15px;scroll-behavior:smooth}
.messages::-webkit-scrollbar{width:3px}.messages::-webkit-scrollbar-thumb{background:#c5d5e4;border-radius:20px}
.message{display:flex;gap:9px;margin:14px 0;animation:up .2s ease-out}
.message.user{flex-direction:row-reverse}
@keyframes up{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.profile-wrap{width:40px;min-width:40px}
.profile{
width:40px;height:40px;border-radius:14px;display:flex;align-items:center;justify-content:center;
font-size:8px;font-weight:900;color:#fff;background:linear-gradient(145deg,#153d61,#5ba6de);
box-shadow:0 7px 18px rgba(35,100,150,.16)
}
.user .profile{background:linear-gradient(145deg,#536579,#8798a9);box-shadow:none}
.profile-name{text-align:center;margin-top:4px;font-size:7px;color:#74859a;white-space:nowrap}
.content{max-width:84%}
.bubble{
padding:12px 15px;border-radius:19px;font-size:13px;line-height:2;
white-space:pre-wrap;word-break:break-word;overflow-wrap:anywhere;unicode-bidi:plaintext
}
.ai .bubble{
background:rgba(255,255,255,.92);border:1px solid rgba(211,224,236,.9);
border-top-right-radius:6px;box-shadow:0 7px 22px rgba(44,75,105,.07)
}
.user .bubble{
background:linear-gradient(145deg,#e9f5ff,#dceeff);border:1px solid #cfe4f5;
border-top-left-radius:6px;box-shadow:0 5px 16px rgba(48,104,148,.07)
}
.typing{display:flex;gap:4px;height:18px;align-items:center;direction:ltr}
.typing i{width:5px;height:5px;border-radius:50%;background:#66829b;animation:b 1s infinite}
.typing i:nth-child(2){animation-delay:.15s}.typing i:nth-child(3){animation-delay:.3s}
@keyframes b{0%,100%{opacity:.25;transform:none}50%{opacity:1;transform:translateY(-3px)}}
.suggestions{display:flex;gap:8px;overflow-x:auto;padding:5px 13px 10px;scrollbar-width:none}
.suggestions::-webkit-scrollbar{display:none}
.suggestion{
flex-shrink:0;padding:9px 14px;border-radius:20px;border:1px solid #dbe6ef;
background:rgba(255,255,255,.84);color:#4e657c;font-size:10px;
box-shadow:0 5px 14px rgba(40,72,102,.05)
}
.suggestion:active{transform:scale(.97)}
.input-area{
padding:9px 13px calc(10px + env(safe-area-inset-bottom));
background:rgba(255,255,255,.82);border-top:1px solid rgba(110,145,180,.14);
backdrop-filter:blur(22px)
}
.input-box{
display:flex;align-items:flex-end;gap:7px;padding:5px;border-radius:21px;
background:#f8fbff;border:1px solid #d5e2ed;box-shadow:0 7px 22px rgba(40,72,105,.08)
}
textarea{
flex:1;min-width:0;height:43px;max-height:115px;resize:none;outline:0;border:0;
background:transparent;color:#162638;font-size:13px;line-height:1.55;padding:12px 8px
}
textarea::placeholder{color:#8a99a9}
.send{
width:44px;height:44px;border:0;border-radius:15px;background:linear-gradient(145deg,#173f63,#58a2da);
color:#fff;font-size:18px;box-shadow:0 7px 17px rgba(40,112,170,.24)
}
.send:disabled{opacity:.48}
.footer{text-align:center;margin-top:6px;color:#8292a4;font-size:7px}
@media(max-width:480px){
.header{height:65px;padding:8px 12px}.logo{width:43px;height:43px}.logo svg{width:31px;height:31px}
.welcome{padding-top:20px}.hero{width:82px;height:82px;border-radius:25px}.hero svg{width:57px;height:57px}
.welcome h1{font-size:21px}.bubble{font-size:12.5px;line-height:1.9}.content{max-width:85%}
}
</style>
</head>
<body>
<div class="app">
<header class="header">
<div class="brand">
<div class="logo">
<svg viewBox="0 0 100 100" fill="none">
<path d="M22 29C22 23 27 18 33 18H67C73 18 78 23 78 29V58C78 64 73 69 67 69H51L39 82V69H33C27 69 22 64 22 58V29Z" stroke="#a9ddff" stroke-width="5" stroke-linejoin="round"/>
<path d="M35 43H65" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
<path d="M42 54H58" stroke="#a9ddff" stroke-width="5" stroke-linecap="round"/>
<circle cx="76" cy="24" r="8" fill="#fff"/>
</svg>
</div>
<div><div class="brand-title">OFFLINE AI</div><div class="brand-sub"><span class="dot"></span>آماده پاسخ‌گویی</div></div>
</div>
<button class="clear" onclick="clearChat()">⌫</button>
</header>

<section class="welcome" id="welcome">
<div class="hero">
<svg viewBox="0 0 100 100" fill="none">
<path d="M22 29C22 23 27 18 33 18H67C73 18 78 23 78 29V58C78 64 73 69 67 69H51L39 82V69H33C27 69 22 64 22 58V29Z" stroke="#a9ddff" stroke-width="5" stroke-linejoin="round"/>
<path d="M35 43H65" stroke="#fff" stroke-width="5" stroke-linecap="round"/>
<path d="M42 54H58" stroke="#a9ddff" stroke-width="5" stroke-linecap="round"/>
<circle cx="76" cy="24" r="8" fill="#fff"/>
</svg>
</div>
<h1>خوش آمدی به OFFLINE AI</h1>
<p>یک تجربه ساده، سریع و هوشمند برای گفت‌وگو</p>
</section>

<main class="messages" id="messages"></main>

<div class="suggestions">
<button class="suggestion" onclick="quickAsk('سلام، خودت را معرفی کن')">🤖 معرفی OFFLINE AI</button>
<button class="suggestion" onclick="quickAsk('سازنده تو کیست؟')">👤 سازنده</button>
<button class="suggestion" onclick="quickAsk('برای یادگیری برنامه نویسی کمکم کن')">💻 برنامه‌نویسی</button>
<button class="suggestion" onclick="quickAsk('یک ایده جالب بهم بده')">💡 ایده</button>
</div>

<div class="input-area">
<div class="input-box">
<textarea id="input" placeholder="پیامت را بنویس..." oninput="resizeInput(this)" onkeydown="handleKey(event)"></textarea>
<button id="send" class="send" onclick="sendMessage()">➤</button>
</div>
<div class="footer">OFFLINE AI • ساخته‌شده توسط ریس آفلاین کندزی</div>
</div>
</div>

<script>
const input=document.getElementById("input");
const messages=document.getElementById("messages");
const welcome=document.getElementById("welcome");
const send=document.getElementById("send");

function scrollBottom(){requestAnimationFrame(()=>messages.scrollTop=messages.scrollHeight)}

function addMessage(text,type){
welcome.style.display="none";
const row=document.createElement("div"); row.className="message "+type;
const pw=document.createElement("div"); pw.className="profile-wrap";
const p=document.createElement("div"); p.className="profile"; p.textContent=type==="user"?"OFF":"AI";
const n=document.createElement("div"); n.className="profile-name"; n.textContent=type==="user"?"آفلاین":"OFFLINE AI";
pw.appendChild(p); pw.appendChild(n);
const content=document.createElement("div"); content.className="content";
const bubble=document.createElement("div"); bubble.className="bubble"; bubble.dir="auto"; bubble.textContent=text||"";
content.appendChild(bubble); row.appendChild(pw); row.appendChild(content); messages.appendChild(row); scrollBottom();
return bubble;
}
function addTyping(){const b=addMessage("","ai");b.innerHTML='<div class="typing"><i></i><i></i><i></i></div>';return b}
function quickAsk(t){input.value=t;resizeInput(input);sendMessage()}
function handleKey(e){if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();sendMessage()}}
function resizeInput(el){el.style.height="43px";el.style.height=Math.min(el.scrollHeight,115)+"px"}

async function sendMessage(){
const text=input.value.trim(); if(!text||send.disabled)return;
addMessage(text,"user"); input.value=""; input.style.height="43px"; send.disabled=true;
const bubble=addTyping();
try{
const r=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json; charset=UTF-8","Accept":"application/json"},body:JSON.stringify({message:text})});
let data={}; try{data=await r.json()}catch(e){}
if(!r.ok){bubble.textContent=data.error||"خطایی رخ داد.";return}
bubble.textContent=data.reply||"پاسخی دریافت نشد.";bubble.dir="auto";scrollBottom();
}catch(e){bubble.textContent="ارتباط با سرور برقرار نشد. دوباره تلاش کن."}
finally{send.disabled=false;input.focus()}
}
function clearChat(){messages.innerHTML="";welcome.style.display="block";input.focus()}
</script>
</body>
</html>"""

SYSTEM_PROMPT = """
تو OFFLINE AI هستی؛ یک دستیار هوش مصنوعی مدرن و دوستانه.

نام محصول: OFFLINE AI
سازنده و بنیان‌گذار: ریس آفلاین کندزی

اگر کاربر درباره سازنده، بنیان‌گذار یا خالق پرسید، بگو:
«سازنده و بنیان‌گذار من ریس آفلاین کندزی است؛ خالق پروژه OFFLINE AI.»

اگر کاربر پرسید تو کی هستی، بگو:
«من OFFLINE AI هستم؛ یک دستیار هوش مصنوعی مدرن که برای گفت‌وگوی سریع و مفید ساخته شده‌ام. سازنده و بنیان‌گذار من ریس آفلاین کندزی است.»

قوانین:
- اگر کاربر فارسی یا دری صحبت کرد، فارسی/دری روان و خوانا جواب بده.
- هرگز متن فارسی را با encoding خراب یا حروف لاتین عجیب تولید نکن.
- پاسخ طبیعی، واضح و تا حد لازم کوتاه باشد.
- اطلاعاتی درباره سازنده یا پروژه که در این دستور مشخص نشده، از خودت اختراع نکن.
"""

@app.route("/")
def home():
    return Response(
        HTML.encode("utf-8"),
        status=200,
        mimetype="text/html; charset=utf-8"
    )

@app.route("/health")
def health():
    return jsonify({"status":"ok","service":"OFFLINE AI"})

@app.route("/chat", methods=["POST"])
def chat():
    data=request.get_json(silent=True) or {}
    message=str(data.get("message","")).strip()

    if not message:
        return Response(
            json.dumps({"error":"پیام خالی است."},ensure_ascii=False),
            status=400,
            content_type="application/json; charset=utf-8"
        )

    if not GROQ_API_KEY:
        return Response(
            json.dumps({"error":"GROQ_API_KEY در Render تنظیم نشده است."},ensure_ascii=False),
            status=500,
            content_type="application/json; charset=utf-8"
        )

    try:
        r=requests.post(
            GROQ_URL,
            headers={
                "Authorization":"Bearer "+GROQ_API_KEY,
                "Content-Type":"application/json",
                "Accept":"application/json"
            },
            json={
                "model":"llama-3.1-8b-instant",
                "messages":[
                    {"role":"system","content":SYSTEM_PROMPT},
                    {"role":"user","content":message}
                ],
                "temperature":0.5,
                "max_tokens":700,
                "stream":False
            },
            timeout=30
        )

        if r.status_code != 200:
            try:
                err=r.json().get("error",{}).get("message","خطا در سرویس هوش مصنوعی.")
            except Exception:
                err="خطا در سرویس هوش مصنوعی."
            return Response(
                json.dumps({"error":err},ensure_ascii=False),
                status=502,
                content_type="application/json; charset=utf-8"
            )

        result=r.json()
        choices=result.get("choices",[])
        reply=""

        if choices:
            reply=choices[0].get("message",{}).get("content","")

        if not reply:
            reply="پاسخی دریافت نشد."

        return Response(
            json.dumps({"reply":reply},ensure_ascii=False),
            status=200,
            content_type="application/json; charset=utf-8",
            headers={"Cache-Control":"no-cache"}
        )

    except requests.exceptions.Timeout:
        return Response(
            json.dumps({"error":"زمان پاسخ‌گویی تمام شد. دوباره تلاش کن."},ensure_ascii=False),
            status=504,
            content_type="application/json; charset=utf-8"
        )
    except requests.exceptions.RequestException:
        return Response(
            json.dumps({"error":"ارتباط با سرویس هوش مصنوعی برقرار نشد."},ensure_ascii=False),
            status=502,
            content_type="application/json; charset=utf-8"
        )
    except Exception:
        return Response(
            json.dumps({"error":"خطایی در سرور رخ داد."},ensure_ascii=False),
            status=500,
            content_type="application/json; charset=utf-8"
        )

if __name__=="__main__":
    port=int(os.environ.get("PORT","5000"))
    app.run(host="0.0.0.0",port=port,debug=False)
