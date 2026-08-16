from flask import Flask, request, jsonify, Response
import os, requests, json

app=Flask(__name__)
KEY=os.environ.get("GROQ_API_KEY")

HTML=r"""<!doctype html><html lang="fa" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>OFFLINE AI</title><style>
*{box-sizing:border-box;-webkit-tap-highlight-color:transparent}html,body{margin:0;width:100%;height:100%;overflow:hidden}
body{font-family:Tahoma,Arial,sans-serif;color:#eef8ff;background:radial-gradient(circle at 50% -10%,#174d72 0,transparent 35%),radial-gradient(circle at 0 80%,#07344b 0,transparent 28%),#050b13}
.app{height:100dvh;max-width:860px;margin:auto;display:flex;flex-direction:column;position:relative;overflow:hidden}
.header{height:74px;flex-shrink:0;display:flex;align-items:center;justify-content:space-between;padding:9px 14px;background:rgba(4,11,19,.82);border-bottom:1px solid #1b3448;backdrop-filter:blur(22px);z-index:3}
.brand{display:flex;align-items:center;gap:11px}.logo,.heroIcon{display:grid;place-items:center;background:linear-gradient(145deg,#124a6c,#081b2b);border:1px solid #2b9bd0;box-shadow:0 0 28px #0878a822,inset 0 1px #ffffff22}
.logo{width:48px;height:48px;border-radius:16px}.logo svg{width:34px}.title{font-size:17px;font-weight:900}.sub{font-size:9px;color:#7894a9;margin-top:4px}.dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#35e89b;box-shadow:0 0 10px #35e89b;margin-left:5px}
.clear{width:42px;height:42px;border:1px solid #234052;border-radius:14px;background:#ffffff08;color:#a8c0d2;font-size:18px}
.welcome{text-align:center;padding:25px 15px 12px}.heroIcon{width:100px;height:100px;margin:auto;border-radius:30px;box-shadow:0 20px 55px #0007,0 0 45px #168bd022}.heroIcon svg{width:68px}.welcome h1{font-size:24px;margin:15px 0 7px;background:linear-gradient(90deg,#fff,#72d3ff);-webkit-background-clip:text;color:transparent}.welcome p{margin:0;color:#7891a5;font-size:11px}.chips{display:flex;justify-content:center;gap:7px;margin-top:12px;flex-wrap:wrap}.chip{font-size:9px;color:#8fb4c9;border:1px solid #2a5368;background:#ffffff07;padding:6px 10px;border-radius:20px}
.messages{flex:1;overflow-y:auto;padding:6px 12px 14px;scroll-behavior:smooth}.messages::-webkit-scrollbar{width:3px}.messages::-webkit-scrollbar-thumb{background:#28516a;border-radius:9px}
.message{display:flex;gap:8px;margin:13px 0;animation:show .2s ease}.message.user{flex-direction:row-reverse}@keyframes show{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}
.profileWrap{width:38px;min-width:38px}.profile{width:38px;height:38px;border-radius:13px;display:grid;place-items:center;font-size:8px;font-weight:900;background:linear-gradient(145deg,#17618c,#0b273d);border:1px solid #328bb6}.user .profile{background:linear-gradient(145deg,#475a6a,#25323d);border-color:#526a7b}.profileName{text-align:center;margin-top:4px;font-size:7px;color:#678195;white-space:nowrap}.content{max-width:84%}.bubble{padding:11px 14px;border-radius:18px;font-size:13px;line-height:1.95;white-space:pre-wrap;word-break:break-word;unicode-bidi:plaintext}.ai .bubble{background:linear-gradient(145deg,#ffffff0d,#ffffff05);border:1px solid #77c8ed18;border-top-right-radius:5px}.user .bubble{background:linear-gradient(145deg,#123c58,#0d263a);border:1px solid #3d91bd2a;border-top-left-radius:5px}
.typing{display:flex;gap:5px;height:20px;align-items:center}.typing i{width:5px;height:5px;border-radius:50%;background:#76d1ff;animation:b 1s infinite}.typing i:nth-child(2){animation-delay:.15s}.typing i:nth-child(3){animation-delay:.3s}@keyframes b{50%{opacity:1;transform:translateY(-4px)}0%,100%{opacity:.25}}
.suggestions{display:flex;gap:7px;overflow-x:auto;padding:5px 12px 9px}.suggestions::-webkit-scrollbar{display:none}.suggestion{flex-shrink:0;padding:8px 12px;border-radius:19px;border:1px solid #315266;background:#ffffff08;color:#91aec0;font:10px Tahoma}
.inputArea{padding:8px 12px calc(10px + env(safe-area-inset-bottom));background:#040b13e8;border-top:1px solid #193345;backdrop-filter:blur(22px)}.inputBox{display:flex;align-items:flex-end;gap:7px;padding:5px;border:1px solid #27485c;border-radius:21px;background:#0a1723}.inputBox textarea{flex:1;min-width:0;height:43px;max-height:115px;resize:none;outline:0;border:0;background:transparent;color:#f2f8fc;font:13px Tahoma;padding:12px 8px}.inputBox textarea::placeholder{color:#5e778a}.send{width:43px;height:43px;border:0;border-radius:15px;background:linear-gradient(145deg,#238fce,#124d77);color:white;font-size:18px}.send:disabled{opacity:.45}.footer{text-align:center;margin-top:6px;color:#4d697d;font-size:7px}
@media(max-width:480px){.header{height:65px}.logo{width:43px;height:43px}.heroIcon{width:82px;height:82px;border-radius:25px}.heroIcon svg{width:56px}.welcome h1{font-size:21px}.bubble{font-size:12.5px}}
</style></head><body><div class="app">
<header class="header"><div class="brand"><div class="logo"><svg viewBox="0 0 100 100" fill="none"><path d="M22 29C22 23 27 18 33 18H67C73 18 78 23 78 29V58C78 64 73 69 67 69H51L39 82V69H33C27 69 22 64 22 58V29Z" stroke="#72d5ff" stroke-width="5"/><path d="M35 43H65M42 54H58" stroke="white" stroke-width="5" stroke-linecap="round"/><circle cx="76" cy="24" r="8" fill="#72d5ff"/></svg></div><div><div class="title">OFFLINE AI</div><div class="sub"><span class="dot"></span>آماده پاسخ‌گویی</div></div></div><button class="clear" onclick="clearChat()">⌫</button></header>
<section class="welcome" id="welcome"><div class="heroIcon"><svg viewBox="0 0 100 100" fill="none"><path d="M22 29C22 23 27 18 33 18H67C73 18 78 23 78 29V58C78 64 73 69 67 69H51L39 82V69H33C27 69 22 64 22 58V29Z" stroke="#72d5ff" stroke-width="5"/><path d="M35 43H65M42 54H58" stroke="white" stroke-width="5" stroke-linecap="round"/><circle cx="76" cy="24" r="8" fill="#72d5ff"/></svg></div><h1>خوش آمدی به OFFLINE AI</h1><p>هوشمند، سریع و آماده گفت‌وگو</p><div class="chips"><span class="chip">🤖 هوش مصنوعی</span><span class="chip">⚡ پاسخ سریع</span><span class="chip">💬 فارسی</span></div></section>
<main class="messages" id="messages"></main>
<div class="suggestions"><button class="suggestion" onclick="ask('سلام، خودت را معرفی کن')">معرفی OFFLINE AI</button><button class="suggestion" onclick="ask('سازنده تو کیست؟')">سازنده</button><button class="suggestion" onclick="ask('برای یادگیری برنامه نویسی کمکم کن')">برنامه‌نویسی</button><button class="suggestion" onclick="ask('یک ایده جالب بهم بده')">ایده</button></div>
<div class="inputArea"><div class="inputBox"><textarea id="input" placeholder="پیامت را بنویس..." oninput="resizeMe(this)" onkeydown="key(event)"></textarea><button id="send" class="send" onclick="sendMessage()">➤</button></div><div class="footer">OFFLINE AI • ساخته‌شده توسط ریس آفلاین کندزی</div></div></div>
<script>
const input=document.getElementById("input"),messages=document.getElementById("messages"),welcome=document.getElementById("welcome"),send=document.getElementById("send");
function bottom(){requestAnimationFrame(()=>messages.scrollTop=messages.scrollHeight)}
function add(text,type){welcome.style.display="none";let row=document.createElement("div");row.className="message "+type;let pw=document.createElement("div");pw.className="profileWrap";let p=document.createElement("div");p.className="profile";p.textContent=type==="user"?"OFF":"AI";let n=document.createElement("div");n.className="profileName";n.textContent=type==="user"?"آفلاین":"OFFLINE AI";pw.append(p,n);let c=document.createElement("div");c.className="content";let b=document.createElement("div");b.className="bubble";b.dir="auto";b.textContent=text;c.appendChild(b);row.append(pw,c);messages.appendChild(row);bottom();return b}
function ask(t){input.value=t;resizeMe(input);sendMessage()}
function key(e){if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();sendMessage()}}
function resizeMe(e){e.style.height="43px";e.style.height=Math.min(e.scrollHeight,115)+"px"}
async function sendMessage(){let text=input.value.trim();if(!text||send.disabled)return;add(text,"user");input.value="";input.style.height="43px";send.disabled=true;let b=add("","ai");b.innerHTML='<div class="typing"><i></i><i></i><i></i></div>';try{let r=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:text})});let d=await r.json();b.textContent=r.ok?(d.reply||"پاسخی دریافت نشد."):d.error||"خطایی رخ داد."}catch(e){b.textContent="ارتباط با سرور برقرار نشد. دوباره تلاش کن."}finally{send.disabled=false;input.focus();bottom()}}
function clearChat(){messages.innerHTML="";welcome.style.display="block";input.focus()}
</script></body></html>"""

@app.route("/")
def home(): return Response(HTML,200,{"Content-Type":"text/html; charset=utf-8"})

@app.route("/chat",methods=["POST"])
def chat():
    data=request.get_json(silent=True) or {}; msg=str(data.get("message","")).strip()
    if not msg:return jsonify(error="پیام خالی است."),400
    if not KEY:return jsonify(error="GROQ_API_KEY در Render تنظیم نشده است."),500
    system="""تو OFFLINE AI هستی؛ یک دستیار هوش مصنوعی مدرن.
سازنده و بنیان‌گذار: ریس آفلاین کندزی.
اگر درباره سازنده پرسیدند بگو: «سازنده و بنیان‌گذار من ریس آفلاین کندزی است؛ خالق پروژه OFFLINE AI.»
اگر درباره هویتت پرسیدند بگو: «من OFFLINE AI هستم؛ یک دستیار هوش مصنوعی مدرن.»
اگر کاربر فارسی یا دری نوشت، کاملاً فارسی/دری و خوانا پاسخ بده. طبیعی، دقیق و مفید باش. اطلاعاتی که داده نشده را اختراع نکن."""
    try:
        r=requests.post("https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization":"Bearer "+KEY,"Content-Type":"application/json"},
        json={"model":"llama-3.1-8b-instant","messages":[{"role":"system","content":system},{"role":"user","content":msg}],"temperature":.55,"max_tokens":900},timeout=35)
        if r.status_code!=200:
            try:e=r.json().get("error",{}).get("message","خطا در سرویس هوش مصنوعی.")
            except Exception:e="خطا در سرویس هوش مصنوعی."
            return jsonify(error=e),500
        ch=r.json().get("choices",[]); reply=ch[0].get("message",{}).get("content","") if ch else ""
        return Response(json.dumps({"reply":reply or "پاسخی دریافت نشد."},ensure_ascii=False),200,{"Content-Type":"application/json; charset=utf-8"})
    except requests.exceptions.Timeout:return jsonify(error="زمان پاسخ‌گویی تمام شد. دوباره تلاش کن."),504
    except Exception:return jsonify(error="خطایی در ارتباط با سرور رخ داد."),500

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)),debug=False)
