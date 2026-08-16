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
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>OFFLINE AI</title>
<style>
:root{--bg:#080b10;--panel:#10151d;--line:#273140;--text:#f5f7fb;--muted:#8e9aaa;--accent:#6c63ff;--user:#202938;--ai:#111c1a}
*{box-sizing:border-box}body{margin:0;background:radial-gradient(circle at 50% -10%,#1c2140 0,#0b0e14 38%,var(--bg) 75%);color:var(--text);font-family:Arial,Tahoma,sans-serif;min-height:100vh}
.app{min-height:100vh;display:flex;flex-direction:column;max-width:980px;margin:auto}
header{position:sticky;top:0;z-index:5;display:flex;align-items:center;justify-content:space-between;padding:14px 16px;background:rgba(8,11,16,.84);backdrop-filter:blur(16px);border-bottom:1px solid rgba(255,255,255,.06)}
.brand{display:flex;align-items:center;gap:11px}.logo{width:42px;height:42px;border-radius:14px;display:grid;place-items:center;background:linear-gradient(135deg,var(--accent),#2dd4bf);box-shadow:0 8px 25px rgba(108,99,255,.3);font-size:22px}
.brand b{font-size:18px}.status{font-size:11px;color:#65e6a2;margin-top:3px}.actions button{width:38px;height:38px;border:1px solid var(--line);background:var(--panel);color:var(--text);border-radius:12px;font-size:17px}
#chat{flex:1;overflow-y:auto;padding:24px 14px 125px}.empty{text-align:center;padding:12vh 18px 0;color:var(--muted)}.empty .hero{font-size:54px;margin-bottom:10px}.empty h1{color:var(--text);margin:0 0 8px;font-size:27px}.empty p{margin:0 auto;max-width:470px;line-height:1.9}
.msg{position:relative;width:fit-content;max-width:min(86%,720px);padding:12px 15px;margin:12px 0;border:1px solid var(--line);border-radius:18px;line-height:1.85;white-space:pre-wrap;word-wrap:break-word;box-shadow:0 7px 25px rgba(0,0,0,.12);animation:pop .18s ease-out}.user{margin-right:0;background:linear-gradient(135deg,#273247,#1c2532);border-bottom-right-radius:5px}.ai{margin-left:0;background:linear-gradient(135deg,#13201d,#11181a);border-bottom-left-radius:5px}
form{position:fixed;z-index:6;bottom:0;left:50%;transform:translateX(-50%);width:min(980px,100%);padding:10px 12px calc(10px + env(safe-area-inset-bottom));background:linear-gradient(transparent,rgba(8,11,16,.98) 28%);display:flex}.composer{display:flex;align-items:center;gap:8px;width:100%;padding:7px;background:rgba(16,21,29,.96);border:1px solid var(--line);border-radius:18px;box-shadow:0 18px 50px rgba(0,0,0,.35)}
input{flex:1;min-width:0;padding:12px;border:0;outline:0;background:transparent;color:var(--text);font-size:15px;direction:rtl}input::placeholder{color:#6f7a89}button.send{border:0;min-width:48px;height:44px;border-radius:14px;background:linear-gradient(135deg,var(--accent),#8b84ff);color:white;font-size:18px;font-weight:bold}
.typing{display:flex;gap:5px;align-items:center;padding:15px 18px}.dot{width:6px;height:6px;background:#9aa5b5;border-radius:50%;animation:bounce 1s infinite}.dot:nth-child(2){animation-delay:.15s}.dot:nth-child(3){animation-delay:.3s}
.toast{position:fixed;top:72px;left:50%;transform:translateX(-50%) translateY(-15px);opacity:0;pointer-events:none;background:#171d27;border:1px solid var(--line);padding:9px 14px;border-radius:12px;color:#fff;transition:.25s;z-index:20;font-size:13px}.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
@keyframes pop{from{opacity:0;transform:translateY(5px)}to{opacity:1;transform:none}}@keyframes bounce{0%,80%,100%{transform:translateY(0);opacity:.45}40%{transform:translateY(-5px);opacity:1}}
@media(max-width:600px){header{padding:12px}.msg{max-width:91%}.empty{padding-top:10vh}.empty h1{font-size:24px}}
</style>
</head>
<body><div class="app">
<header><div class="brand"><div class="logo">🤖</div><div><b>OFFLINE AI</b><div class="status">● آنلاین و آماده پاسخ‌گویی</div></div></div><div class="actions"><button id="clear" title="پاک کردن چت">⌫</button></div></header>
<div id="chat"><div class="empty" id="empty"><div class="hero">✨</div><h1>سلام! من OFFLINE AI هستم</h1><p>سؤالت را بنویس و با هوش مصنوعی گفتگو کن. طراحی شده برای یک تجربه سریع، ساده و زیبا.</p></div></div>
<form id="form"><div class="composer"><input id="message" placeholder="پیامت را بنویس..." autocomplete="off"><button class="send" type="submit" aria-label="ارسال">➤</button></div></form><div class="toast" id="toast"></div>
<script>
const form=document.getElementById("form"),input=document.getElementById("message"),chat=document.getElementById("chat"),empty=document.getElementById("empty"),toast=document.getElementById("toast");
function addMessage(text,cls){if(document.getElementById("empty"))document.getElementById("empty").remove();const d=document.createElement("div");d.className="msg "+cls;d.textContent=text;chat.appendChild(d);chat.scrollTop=chat.scrollHeight;return d}
function showToast(t){toast.textContent=t;toast.classList.add("show");setTimeout(()=>toast.classList.remove("show"),1800)}
form.addEventListener("submit",async e=>{e.preventDefault();const text=input.value.trim();if(!text)return;addMessage(text,"user");input.value="";input.focus();const typing=addMessage("","ai");typing.classList.add("typing");typing.innerHTML='<span class="dot"></span><span class="dot"></span><span class="dot"></span>';try{const r=await fetch("/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({message:text})});const d=await r.json();typing.remove();addMessage(d.reply||d.error||"خطایی رخ داد.","ai")}catch(e){typing.remove();addMessage("اتصال به سرور مشکل دارد.","ai")}});
document.getElementById("clear").addEventListener("click",()=>{chat.innerHTML='<div class="empty" id="empty"><div class="hero">✨</div><h1>گفتگو پاک شد</h1><p>هر وقت آماده بودی، پیام جدیدت را بنویس.</p></div>';showToast("گفتگو پاک شد")});
input.addEventListener("keydown",e=>{if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();form.requestSubmit()}});
</script></div></body></html>
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
