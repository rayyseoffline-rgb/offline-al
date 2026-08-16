from flask import Flask, request, jsonify, Response
import os
import requests

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

HTML = r"""
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">

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
}

body{
    font-family:Tahoma,Arial,sans-serif;
    background:
        radial-gradient(circle at 90% 0%,#dceeff,transparent 35%),
        radial-gradient(circle at 0% 100%,#eaf5ff,transparent 35%),
        #f5f8fc;
    color:#182536;
}

.app{
    width:100%;
    max-width:820px;
    height:100dvh;
    margin:auto;
    display:flex;
    flex-direction:column;
}

/* HEADER */

.header{
    height:70px;
    flex-shrink:0;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:9px 14px;
    background:rgba(255,255,255,.9);
    border-bottom:1px solid #e3e9f0;
    backdrop-filter:blur(18px);
}

.brand{
    display:flex;
    align-items:center;
    gap:11px;
}

.logo{
    width:48px;
    height:48px;
    border-radius:16px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(145deg,#18324f,#3b79ad);
    box-shadow:0 8px 25px rgba(40,100,155,.22);
}

.logo svg{
    width:34px;
    height:34px;
}

.brand-title{
    font-size:17px;
    font-weight:900;
}

.brand-sub{
    margin-top:4px;
    color:#728197;
    font-size:9px;
}

.dot{
    display:inline-block;
    width:6px;
    height:6px;
    border-radius:50%;
    background:#21b879;
    margin-left:4px;
}

.clear{
    width:42px;
    height:42px;
    border:1px solid #dfe6ed;
    border-radius:13px;
    background:white;
    color:#536274;
    font-size:18px;
}

/* WELCOME */

.welcome{
    text-align:center;
    padding:25px 18px 12px;
}

.hero{
    width:90px;
    height:90px;
    margin:auto;
    border-radius:28px;
    display:flex;
    align-items:center;
    justify-content:center;
    background:linear-gradient(145deg,#18334f,#3977aa);
    box-shadow:0 18px 45px rgba(40,100,155,.22);
}

.hero svg{
    width:65px;
    height:65px;
}

.welcome h1{
    margin:14px 0 7px;
    font-size:23px;
}

.welcome p{
    margin:0;
    color:#758397;
    font-size:11px;
}

/* CHAT */

.messages{
    flex:1;
    overflow-y:auto;
    padding:8px 13px 15px;
}

.message{
    display:flex;
    gap:8px;
    margin:13px 0;
}

.message.user{
    flex-direction:row-reverse;
}

.profile-wrap{
    width:38px;
    min-width:38px;
}

.profile{
    width:38px;
    height:38px;
    border-radius:13px;
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size:8px;
    font-weight:900;
    background:linear-gradient(145deg,#18324f,#3978ac);
}

.user .profile{
    background:linear-gradient(145deg,#344456,#68798a);
}

.profile-name{
    margin-top:4px;
    text-align:center;
    color:#718095;
    font-size:7px;
    white-space:nowrap;
}

.content{
    max-width:83%;
}

.bubble{
    padding:11px 14px;
    border-radius:18px;
    line-height:1.9;
    font-size:13px;
    white-space:pre-wrap;
    word-break:break-word;
    unicode-bidi:plaintext;
}

.ai .bubble{
    background:white;
    border:1px solid #e0e7ef;
    border-top-right-radius:5px;
    box-shadow:0 5px 18px rgba(40,65,90,.06);
}

.user .bubble{
    background:#e4f1ff;
    border:1px solid #cfe2f5;
    border-top-left-radius:5px;
}

/* SUGGESTIONS */

.suggestions{
    display:flex;
    gap:7px;
    overflow-x:auto;
    padding:5px 12px 9px;
}

.suggestion{
    flex-shrink:0;
    padding:8px 13px;
    border-radius:18px;
    border:1px solid #dfe7ef;
    background:white;
    color:#536579;
    font-family:inherit;
}

/* INPUT */

.input-area{
    padding:8px 12px calc(10px + env(safe-area-inset-bottom));
    background:rgba(255,255,255,.94);
    border-top:1px solid #e3e9f0;
}

.input-box{
    display:flex;
    align-items:flex-end;
    gap:7px;
    padding:5px;
    border:1px solid #dce5ee;
    border-radius:20px;
    background:#f8fbfe;
}

textarea{
    flex:1;
    min-width:0;
    height:43px;
    max-height:115px;
    resize:none;
    border:0;
    outline:0;
    background:transparent;
    color:#172638;
    font-family:inherit;
    font-size:13px;
    padding:12px 8px;
}

textarea::placeholder{
    color:#8997a7;
}

.send{
    width:43px;
    height:43px;
    border:0;
    border-radius:14px;
    background:linear-gradient(145deg,#214d75,#3979ad);
    color:white;
    font-size:17px;
}

.send:disabled{
    opacity:.5;
}

.footer{
    text-align:center;
    margin-top:6px;
    color:#8794a3;
    font-size:7px;
}

@media(max-width:480px){

    .header{
        height:64px;
    }

    .logo{
        width:42px;
        height:42px;
    }

    .hero{
        width:78px;
        height:78px;
    }

    .hero svg{
        width:55px;
        height:55px;
    }

    .welcome h1{
        font-size:21px;
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
stroke="#9BD5FF"
stroke-width="5"
stroke-linejoin="round"/>

<path
d="M35 43H65"
stroke="white"
stroke-width="5"
stroke-linecap="round"/>

<path
d="M42 54H58"
stroke="#9BD5FF"
stroke-width="5"
stroke-linecap="round"/>

<circle
cx="76"
cy="24"
r="8"
fill="white"/>

</svg>

</div>

<div>

<div class="brand-title">
OFFLINE AI
</div>

<div class="brand-sub">
<span class="dot"></span>
آماده پاسخ‌گویی
</div>

</div>

</div>

<button class="clear" onclick="clearChat()">⌫</button>

</header>


<section class="welcome" id="welcome">

<div class="hero">

<svg viewBox="0 0 100 100" fill="none">

<path
d="M22 29C22 23 27 18 33 18H67C73 18 78 23 78 29V58C78 64 73 69 67 69H51L39 82V69H33C27 69 22 64 22 58V29Z"
stroke="#9BD5FF"
stroke-width="5"
stroke-linejoin="round"/>

<path
d="M35 43H65"
stroke="white"
stroke-width="5"
stroke-linecap="round"/>

<path
d="M42 54H58"
stroke="#9BD5FF"
stroke-width="5"
stroke-linecap="round"/>

<circle
cx="76"
cy="24"
r="8"
fill="white"/>

</svg>

</div>

<h1>خوش آمدی به OFFLINE AI</h1>

<p>سریع، هوشمند و آماده گفت‌وگو</p>

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

const input =
document.getElementById("input");

const messages =
document.getElementById("messages");

const welcome =
document.getElementById("welcome");

const send =
document.getElementById("send");


function scrollBottom(){

requestAnimationFrame(function(){
    messages.scrollTop =
    messages.scrollHeight;
});

}


function addMessage(text,type){

welcome.style.display="none";

const row =
document.createElement("div");

row.className =
"message " + type;


const profileWrap =
document.createElement("div");

profileWrap.className =
"profile-wrap";


const profile =
document.createElement("div");

profile.className =
"profile";

profile.textContent =
type === "user"
? "OFF"
: "AI";


const profileName =
document.createElement("div");

profileName.className =
"profile-name";

profileName.textContent =
type === "user"
? "آفلاین"
: "OFFLINE AI";


profileWrap.appendChild(profile);
profileWrap.appendChild(profileName);


const content =
document.createElement("div");

content.className =
"content";


const bubble =
document.createElement("div");

bubble.className =
"bubble";

bubble.dir="auto";

bubble.textContent =
text;


content.appendChild(bubble);

row.appendChild(profileWrap);
row.appendChild(content);

messages.appendChild(row);

scrollBottom();

return bubble;

}


function quickAsk(text){

input.value=text;

resizeInput(input);

sendMessage();

}


function handleKey(event){

if(
event.key === "Enter" &&
!event.shiftKey
){

event.preventDefault();

sendMessage();

}

}


function resizeInput(el){

el.style.height="43px";

el.style.height =
Math.min(
el.scrollHeight,
115
) + "px";

}


async function sendMessage(){

const text =
input.value.trim();

if(!text || send.disabled)
return;


addMessage(
text,
"user"
);

input.value="";

input.style.height="43px";

send.disabled=true;


const aiBubble =
addMessage(
"در حال پاسخ‌گویی...",
"ai"
);


try{

const response =
await fetch(
"/chat",
{
method:"POST",

headers:{
"Content-Type":
"application/json"
},

body:JSON.stringify({
message:text
})
}
);


const data =
await response.json();


if(!response.ok){

aiBubble.textContent =
data.error ||
"خطایی رخ داد.";

return;

}


aiBubble.textContent =
data.reply ||
"پاسخی دریافت نشد.";

aiBubble.dir="auto";

scrollBottom();


}catch(error){

aiBubble.textContent =
"ارتباط با سرور برقرار نشد. دوباره تلاش کن.";

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
</html>
"""


@app.route("/")
def home():
    return Response(
        HTML,
        status=200,
        headers={
            "Content-Type":
            "text/html; charset=utf-8"
        }
    )


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json(
        silent=True
    ) or {}

    message = str(
        data.get("message", "")
    ).strip()

    if not message:

        return Response(
            '{"error":"پیام خالی است."}',
            status=400,
            headers={
                "Content-Type":
                "application/json; charset=utf-8"
            }
        )


    if not GROQ_API_KEY:

        return Response(
            '{"error":"GROQ_API_KEY در Render تنظیم نشده است."}',
            status=500,
            headers={
                "Content-Type":
                "application/json; charset=utf-8"
            }
        )


    system_prompt = """
تو OFFLINE AI هستی؛ یک دستیار هوش مصنوعی مدرن.

نام:
OFFLINE AI

سازنده و بنیان‌گذار:
ریس آفلاین کندزی

اگر کاربر پرسید «سازنده تو کیست؟»، پاسخ بده:
«سازنده و بنیان‌گذار من ریس آفلاین کندزی است؛ خالق پروژه OFFLINE AI.»

اگر کاربر پرسید «تو کی هستی؟»، پاسخ بده:
«من OFFLINE AI هستم؛ یک دستیار هوش مصنوعی مدرن. سازنده و بنیان‌گذار من ریس آفلاین کندزی است.»

قوانین:
- اگر کاربر فارسی یا دری صحبت کرد، کاملاً فارسی یا دری پاسخ بده.
- متن را با حروف فارسی و خوانا بنویس.
- پاسخ‌ها طبیعی، واضح و مفید باشند.
- اطلاعاتی درباره سازنده که داده نشده اختراع نکن.
"""


    try:

        response = requests.post(

            "https://api.groq.com/openai/v1/chat/completions",

            headers={
                "Authorization":
                "Bearer " + GROQ_API_KEY,

                "Content-Type":
                "application/json"
            },

            json={

                "model":
                "llama-3.1-8b-instant",

                "messages":[

                    {
                        "role":
                        "system",

                        "content":
                        system_prompt
                    },

                    {
                        "role":
                        "user",

                        "content":
                        message
                    }

                ],

                "temperature":
                0.6,

                "max_tokens":
                1000,

                "stream":
                False
            },

            timeout=45
        )


        if response.status_code != 200:

            try:

                error_data =
                    response.json()

                error_message =
                    error_data.get(
                        "error",
                        {}
                    ).get(
                        "message",
                        "خطا در سرویس هوش مصنوعی."
                    )

            except Exception:

                error_message =
                    "خطا در سرویس هوش مصنوعی."

            return Response(

                json.dumps(
                    {
                        "error":
                        error_message
                    },
                    ensure_ascii=False
                ),

                status=500,

                headers={
                    "Content-Type":
                    "application/json; charset=utf-8"
                }
            )


        result =
            response.json()


        reply = ""

        choices =
            result.get(
                "choices",
                []
            )

        if choices:

            reply =
                choices[0].get(
                    "message",
                    {}
                ).get(
                    "content",
                    ""
                )


        if not reply:

            reply =
                "پاسخی دریافت نشد."


        return Response(

            json.dumps(
                {
                    "reply":
                    reply
                },
                ensure_ascii=False
            ),

            status=200,

            headers={
                "Content-Type":
                "application/json; charset=utf-8",

                "Cache-Control":
                "no-cache"
            }
        )


    except requests.exceptions.Timeout:

        return Response(

            json.dumps(
                {
                    "error":
                    "زمان پاسخ‌گویی تمام شد. دوباره تلاش کن."
                },
                ensure_ascii=False
            ),

            status=504,

            headers={
                "Content-Type":
                "application/json; charset=utf-8"
            }
        )


    except Exception as error:

        return Response(

            json.dumps(
                {
                    "error":
                    "خطایی در ارتباط با سرور رخ داد."
                },
                ensure_ascii=False
            ),

            status=500,

            headers={
                "Content-Type":
                "application/json; charset=utf-8"
            }
        )


if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
