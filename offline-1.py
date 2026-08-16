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
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#f4f8fc">
<title>OFFLINE AI</title>
<style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}
html,body{margin:0;width:100%;height:100%;overflow:hidden}
body{
font-family:Tahoma,Arial,sans-serif;color:#172638;
background:
radial-gradient(circle at 90% -5%,#d9ecff 0,transparent 32%),
radial-gradient(circle at -5% 100%,#e9f5ff 0,transparent 34%),#f6f9fc
}
button,textarea{font-family:inherit}
.app{width:100%;max-width:820px;height:100dvh;margin:auto;display:flex;flex-direction:column}
.header{
height:70px;flex-shrink:0;display:flex;align-items:center;justify-content:space-between;
padding:9px 14px;background:rgba(255,255,255,.92);border-bottom:1px solid #e2e9f0;
backdrop-filter:blur(18px);z-index:5
}
.brand{display:flex;align-items:center;gap:11px}
.logo,.hero{
display:flex;align-items:center;justify-content:center;
background:linear-gradient(145deg,#173654,#4385bb);
box-shadow:0 12px 30px rgba(35,94,145,.20)
}
.logo{width:48px;height:48px;border-radius:16px}
.logo svg{width:34px;height:34px}
.brand-title{font-size:17px;font-weight:900}
.brand-sub{margin-top:4px;color:#718094;font-size:9px}
.dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#20b979;margin-left:4px;box-shadow:0 0 7px #20b979}
.clear{
width:42px;height:42px;border:1px solid #dfe7ef;border-radius:13px;background:#fff;color:#506174;font-size:18px
}
.welcome{text-align:center;padding:24px 18px 10px}
.hero{width:88px;height:88px;margin:auto;border-radius:27px}
.hero svg{width:64px;height:64px}
.welcome h1{margin:14px 0 7px;font-size:23px;font-weight:900}
.welcome p{margin:0;color:#758398;font-size:11px}
.messages{flex:1;overflow-y:auto;padding:8px 13px 12px;scroll-behavior:smooth}
.messages::-webkit-scrollbar{width:3px}.messages::-webkit-scrollbar-thumb{background:#c7d2de;border-radius:10px}
.message{display:flex;gap:8px;margin:13px 0;animation:show .18s ease-out}
.message.user{flex-direction:row-reverse}
@keyframes show{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
.profile-wrap{width:38px;min-width:38px}
.profile{
width:38px;height:38px;border-radius:13px;display:flex;align-items:center;justify-content:center;
color:#fff;font-size:8px;font-weight:900;background:linear-gradient(145deg,#173654,#4385bb)
}
.user .profile{background:linear-gradient(145deg,#435364,#718398)}
.profile-name{margin-top:4px;text-align:center;color:#718094;font-size:7px;white-space:nowrap}
.content{max-width:83%}
.bubble{
padding:11px 14px;border-radius:18px;line-height:1.9;font-size:13px;
white-space:pre-wrap;word-break:break-word;overflow-wrap:anywhere;unicode-bidi:plaintext
}
.ai .bubble{background:#fff;border:1px solid #dfe7ef;border-top-right-radius:5px;box-shadow:0 5px 18px rgba(40,65,90,.06)}
.user .bubble{background:#e5f2ff;border:1px solid #cfe3f6;border-top-left-radius:5px}
.typing{display:flex;gap:4px;align-items:center;height:18px;direction:ltr}
.typing i{display:block;width:5px;height:5px;border-radius:50%;background:#6f8499;animation:blink 1s infinite}
.typing i:nth-child(2){animation-delay:.15s}.typing i:nth-child(3){animation-delay:.3s}
@keyframes blink{0%,100%{opacity:.25;transform:none}50%{opacity:1;transform:translateY(-3px)}}
.suggestions{display:flex;gap:7px;overflow-x:auto;padding:5px 12px 9px;scrollbar-width:none}
.suggestions::-webkit-scrollbar{display:none}
.suggestion{
flex-shrink:0;padding:8px 13px;border-radius:18px;border:1px solid #dce5ee;
background:rgba(255,255,255,.92);color:#526579;font-size:10px
}
.input-area{
flex-shrink:0;padding:8px 12px calc(10px + env(safe-area-inset-bottom));
background:rgba(255,255,255,.95);border-top:1px solid #e2e9f0;backdrop-filter:blur(18px)
}
.input-box{
display:flex;align-items:flex-end;gap:7px;padding:5px;border:1px solid #d8e3ed;
border-radius:20px;background:#f8fbfe;box-shadow:0 4px 18px rgba(30,70,110,.05)
}
textarea{
flex:1;min-width:0;height:43px;max-height:115px;resize:none;outline:0;border:0;
background:transparent;color:#172638;font-size:13px;padding:12px 8px;line-height:1.5
}
textarea::placeholder{color:#8b99a8}
.send{
width:43px;height:43px;border:0;border-radius:14px;background:linear-gradient(145deg,#214e76,#4385bb);
color:#fff;font-size:17px;cursor:pointer
}
.send:disabled{opacity:.5}
.footer{text-align:center;margin-top:6px;color:#8794a3;font-size:7px}
@media(max-width:480px){
.header{height:64px;padding:8px 12px}.logo{width:42px;height:42px}
.welcome{padding-top:19px}.hero{width:78px;height:78px;border-radius:23px}.hero svg{width:55px;height:55px}
.welcome h1{font-size:21px}.bubble{font-size:12.5px}.content{max-width:84%}
}
</style>
</head>
<body>
<div class="app">

<header class="header">
<div class="brand">
<div class="logo">
<svg viewBox="0 0 100 100" fill="none" aria-hidden="true">
<path d="M22 29C22 23 27 18 33 18H67C73 18 78 23 78 29V58C78 64 73 69 67 69H51L39 82V69H33C27 69 22 64 22 58V29Z" stroke="#9BD5FF" stroke-width="5" stroke-linejoin="round"/>
<path d="M35 43H65" stroke="white" stroke-width="5" stroke-linecap="round"/>
<path d="M42 54H58" stroke="#9BD5FF" stroke-width="5" stroke-linecap="round"/>
<circle cx="76" cy="24" r="8" fill="white"/>
</svg>
</div>
<div>
<div class="brand-title">OFFLINE AI</div>
<div class="brand-sub"><span class="dot"></span>آماده پاسخ‌گویی</div>
</div>
</div>
<button class="clear" onclick="clearChat()" aria-label="پاک کردن چت">⌫</button>
</header>

<section class="welcome" id="welcome">
<div class="hero">
<svg viewBox="0 0 100 100" fill="none" aria-hidden="true">
<path d="M22 29C22 23 27 18 33 18H67C73 18 78 23 78 29V58C78 64 73 69 67 69H51L39 82V69H33C27 69 22 64 22 58V29Z" stroke="#9BD5FF" stroke-width="5" stroke-linejoin="round"/>
<path d="M35 43H65" stroke="white" stroke-width="5" stroke-linecap="round"/>
<path d="M42 54H58" stroke="#9BD5FF" stroke-width="5" stroke-linecap="round"/>
<circle cx="76" cy="24" r="8" fill="white"/>
</svg>
</div>
<h1>خوش آمدی به OFFLINE AI</h1>
<p>سریع، هوشمند و آماده گفت‌وگو</p>
</section>

<main class="messages" id="messages"></main>

<div class="suggestions">
<button class="suggestion" onclick="quickAsk('سلام، خودت را معرفی کن')">معرفی OFFLINE AI</button>
<button class="suggestion" onclick="quickAsk('سازنده تو کیست؟')">سازنده</button>
<button class="suggestion" onclick="quickAsk('برای یادگیری برنامه نویسی کمکم کن')">برنامه‌نویسی</button>
<button class="suggestion" onclick="quickAsk('یک ایده جالب بهم بده')">ایده</button>
</div>

<div class="input-area">
<div class="input-box">
<textarea id="input" placeholder="پیامت را بنویس..." oninput="resizeInput(this)" onkeydown="handleKey(event)"></textarea>
<button id="send" class="send" onclick="sendMessage()" aria-label="ارسال">➤</button>
</div>
<div class="footer">OFFLINE AI • ساخته‌شده توسط ریس آفلاین کندزی</div>
</div>

</div>

<script>
const input=document.getElementById("input");
const messages=document.getElementById("messages");
const welcome=document.getElementById("welcome");
const send=document.getElementById("send");

function scrollBottom(){
requestAnimationFrame(()=>{messages.scrollTop=messages.scrollHeight;});
}

function addMessage(text,type){
welcome.style.display="none";
const row=document.createElement("div");
row.className="message "+type;

const profileWrap=document.createElement("div");
profileWrap.className="profile-wrap";

const profile=document.createElement("div");
profile.className="profile";
profile.textContent=type==="user"?"OFF":"AI";

const name=document.createElement("div");
name.className="profile-name";
name.textContent=type==="user"?"آفلاین":"OFFLINE AI";

profileWrap.appendChild(profile);
profileWrap.appendChild(name);

const content=document.createElement("div");
content.className="content";

const bubble=document.createElement("div");
bubble.className="bubble";
bubble.dir="auto";
bubble.textContent=text||"";

content.appendChild(bubble);
row.appendChild(profileWrap);
row.appendChild(content);
messages.appendChild(row);
scrollBottom();
return bubble;
}

function addTyping(){
const bubble=addMessage("","ai");
bubble.innerHTML='<div class="typing"><i></i><i></i><i></i></div>';
return bubble;
}

function quickAsk(text){
input.value=text;
resizeInput(input);
sendMessage();
}

function handleKey(event){
if(event.key==="Enter"&&!event.shiftKey){
event.preventDefault();
sendMessage();
}
}

function resizeInput(el){
el.style.height="43px";
el.style.height=Math.min(el.scrollHeight,115)+"px";
}

async function sendMessage(){
const text=input.value.trim();
if(!text||send.disabled)return;

addMessage(text,"user");
input.value="";
input.style.height="43px";
send.disabled=true;

const aiBubble=addTyping();

try{
const response=await fetch("/chat",{
method:"POST",
headers:{"Content-Type":"application/json; charset=UTF-8","Accept":"application/json"},
body:JSON.stringify({message:text})
});

let data={};
try{data=await response.json();}catch(e){}

if(!response.ok){
aiBubble.textContent=data.error||"خطایی در پاسخ‌گویی رخ داد.";
return;
}

aiBubble.textContent=data.reply||"پاسخی دریافت نشد.";
aiBubble.dir="auto";
scrollBottom();

}catch(error){
aiBubble.textContent="ارتباط با سرور برقرار نشد. دوباره تلاش کن.";
}finally{
send.disabled=false;
input.focus();
}
}

function clearChat(){
messages.innerHTML="";
welcome.style.display="block";
input.focus();
}
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
