from flask import Flask, request, jsonify, Response
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
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#07111f">

<title>OFFLINE AI</title>

<style>
*{
    box-sizing:border-box;
    -webkit-tap-highlight-color:transparent;
}

:root{
    --bg:#07111f;
    --bg2:#0b1728;
    --glass:rgba(255,255,255,.075);
    --glass2:rgba(255,255,255,.11);
    --border:rgba(255,255,255,.13);
    --text:#f2f7ff;
    --muted:#91a4ba;
    --blue:#56b8ff;
    --purple:#8c68ff;
    --green:#35e59a;
}

body.light{
    --bg:#eef5fc;
    --bg2:#ffffff;
    --glass:rgba(255,255,255,.70);
    --glass2:rgba(255,255,255,.90);
    --border:rgba(20,50,80,.12);
    --text:#132238;
    --muted:#64758a;
}

html,
body{
    margin:0;
    width:100%;
    height:100%;
    overflow:hidden;
}

body{
    font-family:
        Tahoma,
        Arial,
        sans-serif;

    color:var(--text);

    background:
        radial-gradient(
            circle at 85% -10%,
            #236aa5 0,
            transparent 34%
        ),
        radial-gradient(
            circle at -10% 100%,
            #39266d 0,
            transparent 35%
        ),
        linear-gradient(
            135deg,
            var(--bg),
            var(--bg2)
        );
}

button,
textarea,
input{
    font-family:inherit;
}

.app{
    width:100%;
    max-width:900px;
    height:100dvh;
    margin:auto;
    display:flex;
    flex-direction:column;
}

/* HEADER */

.header{
    height:74px;
    flex-shrink:0;

    display:flex;
    align-items:center;
    justify-content:space-between;

    padding:9px 14px;

    background:rgba(5,12,23,.64);
    backdrop-filter:blur(25px);

    border-bottom:1px solid var(--border);

    z-index:10;
}

body.light .header{
    background:rgba(255,255,255,.70);
}

.brand{
    display:flex;
    align-items:center;
    gap:11px;
}

.logo{
    width:51px;
    height:51px;

    border-radius:18px;

    display:flex;
    align-items:center;
    justify-content:center;

    background:
        linear-gradient(
            145deg,
            #123c64,
            #7657ff
        );

    border:1px solid rgba(255,255,255,.15);

    box-shadow:
        0 10px 35px rgba(0,0,0,.35),
        0 0 35px rgba(70,160,255,.25);
}

.logo svg{
    width:38px;
    height:38px;
}

.brand-title{
    font-size:17px;
    font-weight:900;
    letter-spacing:.3px;
}

.brand-sub{
    margin-top:4px;
    font-size:9px;
    color:var(--muted);
}

.online-dot{
    display:inline-block;
    width:7px;
    height:7px;
    margin-left:4px;

    border-radius:50%;

    background:var(--green);

    box-shadow:
        0 0 10px var(--green);
}

.header-actions{
    display:flex;
    gap:7px;
}

.icon-btn{
    width:43px;
    height:43px;

    border:1px solid var(--border);
    border-radius:14px;

    background:var(--glass);

    color:var(--text);

    font-size:18px;

    backdrop-filter:blur(15px);
}

/* WELCOME */

.welcome{
    text-align:center;
    padding:22px 15px 8px;
}

.hero{
    width:102px;
    height:102px;

    margin:auto;

    border-radius:32px;

    display:flex;
    align-items:center;
    justify-content:center;

    background:
        linear-gradient(
            145deg,
            #103b64,
            #7655ff
        );

    border:1px solid rgba(255,255,255,.15);

    box-shadow:
        0 20px 60px rgba(0,0,0,.4),
        0 0 50px rgba(70,150,255,.22);
}

.hero svg{
    width:72px;
    height:72px;
}

.welcome h1{
    margin:14px 0 7px;
    font-size:24px;
    font-weight:900;
}

.welcome p{
    margin:0;
    color:var(--muted);
    font-size:11px;
}

/* MESSAGES */

.messages{
    flex:1;
    overflow-y:auto;

    padding:
        6px
        12px
        12px;

    scroll-behavior:smooth;
}

.messages::-webkit-scrollbar{
    width:3px;
}

.messages::-webkit-scrollbar-thumb{
    background:#50647c;
    border-radius:20px;
}

.message{
    display:flex;
    gap:9px;

    margin:14px 0;

    animation:
        messageIn
        .22s
        ease;
}

@keyframes messageIn{
    from{
        opacity:0;
        transform:translateY(7px);
    }

    to{
        opacity:1;
        transform:translateY(0);
    }
}

.message.user{
    flex-direction:row-reverse;
}

.avatar-wrap{
    width:41px;
    min-width:41px;
    text-align:center;
}

.avatar{
    width:41px;
    height:41px;

    border-radius:14px;

    display:flex;
    align-items:center;
    justify-content:center;

    font-size:9px;
    font-weight:900;

    color:white;

    background:
        linear-gradient(
            145deg,
            #173f66,
            #7959ff
        );

    border:1px solid rgba(255,255,255,.15);

    box-shadow:
        0 8px 25px rgba(0,0,0,.35);
}

.user .avatar{
    background:
        linear-gradient(
            145deg,
            #293b4e,
            #657c91
        );
}

.avatar-name{
    margin-top:4px;

    color:var(--muted);

    font-size:7px;

    white-space:nowrap;
}

.content{
    max-width:82%;
}

.bubble{
    padding:12px 15px;

    border-radius:20px;

    border:1px solid var(--border);

    background:
        linear-gradient(
            135deg,
            rgba(255,255,255,.10),
            rgba(255,255,255,.035)
        );

    backdrop-filter:blur(20px);

    box-shadow:
        0 8px 30px rgba(0,0,0,.16);

    color:var(--text);

    font-size:13px;
    line-height:1.95;

    white-space:pre-wrap;
    word-break:break-word;

    unicode-bidi:plaintext;
}

.ai .bubble{
    border-top-right-radius:5px;
}

.user .bubble{
    border-top-left-radius:5px;

    background:
        linear-gradient(
            135deg,
            rgba(40,145,220,.20),
            rgba(120,80,255,.15)
        );
}

.typing{
    display:flex;
    gap:5px;
    height:18px;
    align-items:center;
}

.typing span{
    width:6px;
    height:6px;

    border-radius:50%;

    background:var(--blue);

    animation:
        typing
        1s
        infinite;
}

.typing span:nth-child(2){
    animation-delay:.15s;
}

.typing span:nth-child(3){
    animation-delay:.30s;
}

@keyframes typing{
    0%,100%{
        opacity:.3;
        transform:translateY(0);
    }

    50%{
        opacity:1;
        transform:translateY(-4px);
    }
}

/* QUICK BUTTONS */

.quick{
    display:flex;
    gap:7px;

    overflow-x:auto;

    padding:
        5px
        12px
        9px;
}

.quick::-webkit-scrollbar{
    display:none;
}

.quick-btn{
    flex-shrink:0;

    padding:
        9px
        13px;

    border-radius:20px;

    border:1px solid var(--border);

    background:var(--glass);

    color:var(--text);

    font-size:10px;

    backdrop-filter:blur(15px);
}

/* INPUT */

.input-area{
    flex-shrink:0;

    padding:
        8px
        12px
        calc(
            10px +
            env(safe-area-inset-bottom)
        );

    background:
        rgba(4,10,18,.67);

    backdrop-filter:blur(25px);

    border-top:1px solid var(--border);
}

body.light .input-area{
    background:rgba(255,255,255,.72);
}

.input-box{
    display:flex;
    align-items:flex-end;

    gap:7px;

    padding:5px;

    border:
        1px solid
        var(--border);

    border-radius:21px;

    background:var(--glass);

    backdrop-filter:blur(20px);
}

textarea{
    flex:1;
    min-width:0;

    height:44px;
    max-height:120px;

    resize:none;

    border:0;
    outline:0;

    background:transparent;

    color:var(--text);

    font-size:13px;

    padding:12px 8px;
}

textarea::placeholder{
    color:var(--muted);
}

.send{
    width:44px;
    height:44px;

    border:0;
    border-radius:15px;

    color:white;

    font-size:18px;

    background:
        linear-gradient(
            145deg,
            #198ed1,
            #7655ff
        );

    box-shadow:
        0 7px 20px
        rgba(50,120,255,.25);
}

.send:disabled{
    opacity:.45;
}

.footer{
    text-align:center;

    color:var(--muted);

    font-size:7px;

    margin-top:5px;
}

/* DRAWER */

.drawer{
    position:fixed;
    inset:0;

    display:none;

    background:rgba(0,0,0,.70);

    z-index:50;
}

.drawer.open{
    display:block;
}

.panel{
    position:absolute;

    right:0;
    top:0;

    width:min(
        350px,
        90vw
    );

    height:100%;

    padding:18px;

    overflow-y:auto;

    background:
        rgba(8,18,32,.97);

    backdrop-filter:blur(30px);

    border-left:
        1px solid
        var(--border);

    color:var(--text);
}

body.light .panel{
    background:
        rgba(244,249,255,.97);
}

.panel-title{
    font-size:21px;
    font-weight:900;

    margin:
        18px
        0;
}

.setting{
    display:flex;
    align-items:center;
    justify-content:space-between;

    padding:
        14px 4px;

    border-bottom:
        1px solid
        var(--border);
}

.setting button{
    padding:
        8px 12px;

    border:
        1px solid
        var(--border);

    border-radius:12px;

    background:var(--glass);

    color:var(--text);
}

.contact{
    margin-top:18px;

    padding:16px;

    border:
        1px solid
        var(--border);

    border-radius:19px;

    background:var(--glass);

    line-height:2;

    font-size:12px;
}

.contact a{
    color:#65c5ff;
    text-decoration:none;
}

/* PHOTO */

.photo-panel{
    position:fixed;

    left:50%;
    bottom:90px;

    transform:
        translateX(-50%);

    display:none;

    width:min(
        94vw,
        550px
    );

    max-height:75vh;

    overflow-y:auto;

    padding:15px;

    border:
        1px solid
        var(--border);

    border-radius:22px;

    background:
        rgba(7,17,31,.96);

    backdrop-filter:blur(25px);

    z-index:40;

    box-shadow:
        0 20px 70px
        rgba(0,0,0,.5);
}

.photo-panel.open{
    display:block;
}

.photo-preview{
    width:100%;

    max-height:300px;

    object-fit:contain;

    margin-top:10px;

    border-radius:16px;

    display:none;

    background:#02060b;
}

.photo-tools{
    display:flex;
    flex-wrap:wrap;

    gap:7px;

    margin-top:10px;
}

.photo-tools button{
    padding:9px 11px;

    border:
        1px solid
        var(--border);

    border-radius:12px;

    background:var(--glass);

    color:white;
}

/* MOBILE */

@media(max-width:480px){

    .header{
        height:66px;
        padding:8px 11px;
    }

    .logo{
        width:44px;
        height:44px;
    }

    .logo svg{
        width:32px;
    }

    .brand-title{
        font-size:15px;
    }

    .hero{
        width:82px;
        height:82px;
        border-radius:26px;
    }

    .hero svg{
        width:58px;
    }

    .welcome h1{
        font-size:21px;
    }

    .bubble{
        font-size:12.5px;
    }

    .content{
        max-width:84%;
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
stroke="#B9E6FF"
stroke-width="5"
stroke-linejoin="round"/>

<path
d="M35 43H65"
stroke="white"
stroke-width="5"
stroke-linecap="round"/>

<path
d="M42 54H58"
stroke="#B9E6FF"
stroke-width="5"
stroke-linecap="round"/>

<circle
cx="76"
cy="24"
r="8"
fill="#B9E6FF"/>

</svg>

</div>

<div>

<div class="brand-title">
OFFLINE AI
</div>

<div class="brand-sub">
<span class="online-dot"></span>
هوش مصنوعی ریس آفلاین
</div>

</div>

</div>

<div class="header-actions">

<button
class="icon-btn"
onclick="openPhoto()">
🖼️
</button>

<button
class="icon-btn"
onclick="openSettings()">
☰
</button>

</div>

</header>


<section
class="welcome"
id="welcome">

<div class="hero">

<svg viewBox="0 0 100 100" fill="none">

<path
d="M22 29C22 23 27 18 33 18H67C73 18 78 23 78 29V58C78 64 73 69 67 69H51L39 82V69H33C27 69 22 64 22 58V29Z"
stroke="#B9E6FF"
stroke-width="5"
stroke-linejoin="round"/>

<path
d="M35 43H65"
stroke="white"
stroke-width="5"
stroke-linecap="round"/>

<path
d="M42 54H58"
stroke="#B9E6FF"
stroke-width="5"
stroke-linecap="round"/>

<circle
cx="76"
cy="24"
r="8"
fill="#B9E6FF"/>

</svg>

</div>

<h1>
خوش آمدی به OFFLINE AI
</h1>

<p>
چت هوشمند • کدنویسی • اطلاعات • ابزار عکس
</p>

</section>


<main
class="messages"
id="messages">
</main>


<div class="quick">

<button
class="quick-btn"
onclick="quickAsk('خودت را معرفی کن')">
🤖 معرفی
</button>

<button
class="quick-btn"
onclick="quickAsk('برای یادگیری برنامه نویسی یک برنامه بده')">
💻 کدنویسی
</button>

<button
class="quick-btn"
onclick="openPhoto()">
🖼️ ویرایش عکس
</button>

<button
class="quick-btn"
onclick="quickAsk('یک ایده خلاقانه بهم بده')">
💡 ایده
</button>

<button
class="quick-btn"
onclick="quickAsk('با من دوستانه صحبت کن')">
💬 گفتگو
</button>

</div>


<div class="input-area">

<div class="input-box">

<textarea
id="input"
placeholder="پیامت را بنویس..."
oninput="resizeInput(this)"
onkeydown="handleKey(event)">
</textarea>

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


<!-- SETTINGS -->

<div
class="drawer"
id="drawer"
onclick="drawerClick(event)">

<div class="panel">

<button
class="icon-btn"
onclick="closeSettings()">
×
</button>

<div class="panel-title">
⚙️ تنظیمات
</div>


<div class="setting">

<span>
🌙 حالت تاریک
</span>

<button
onclick="setTheme('dark')">
فعال
</button>

</div>


<div class="setting">

<span>
☀️ حالت روشن
</span>

<button
onclick="setTheme('light')">
فعال
</button>

</div>


<div class="setting">

<span>
🗑️ پاک کردن گفتگو
</span>

<button
onclick="clearChat()">
پاک کن
</button>

</div>


<div class="contact">

<b>
📞 ارتباط با ریس آفلاین
</b>

<br>

WhatsApp:

<a
href="https://wa.me/93700446505"
target="_blank">
+93 700 446 505
</a>

<br>

Telegram:

<a
href="https://t.me/RAYYSE_OFFLINE"
target="_blank">
@RAYYSE_OFFLINE
</a>

</div>

</div>

</div>


<!-- PHOTO -->

<div
class="photo-panel"
id="photoPanel">

<button
class="icon-btn"
onclick="closePhoto()">
×
</button>

<h3>
🖼️ ویرایش عکس
</h3>

<input
type="file"
id="photoInput"
accept="image/*"
onchange="previewImage(event)">

<img
id="photoPreview"
class="photo-preview">

<div class="photo-tools">

<button
onclick="rotateImage()">
↻ چرخش
</button>

<button
onclick="photoFilter('grayscale(1)')">
سیاه‌وسفید
</button>

<button
onclick="photoFilter('brightness(1.25)')">
روشن‌تر
</button>

<button
onclick="photoFilter('contrast(1.3)')">
کنتراست
</button>

<button
onclick="photoFilter('blur(2px)')">
تاری
</button>

<button
onclick="resetPhoto()">
اصلی
</button>

</div>

<p
style="
color:#91a4ba;
font-size:10px;
line-height:1.8;
">

ویرایش‌های پایه عکس مستقیماً داخل مرورگر انجام می‌شود.
برای ویرایش مولد هوش مصنوعی باید API تصویری به برنامه متصل شود.

</p>

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

requestAnimationFrame(
function(){

messages.scrollTop =
messages.scrollHeight;

});

}


function addMessage(
text,
type
){

welcome.style.display =
"none";


const row =
document.createElement(
"div"
);

row.className =
"message " + type;


const avatarWrap =
document.createElement(
"div"
);

avatarWrap.className =
"avatar-wrap";


const avatar =
document.createElement(
"div"
);

avatar.className =
"avatar";

avatar.textContent =
type === "user"
? "YOU"
: "AI";


const name =
document.createElement(
"div"
);

name.className =
"avatar-name";

name.textContent =
type === "user"
? "آفلاین"
: "OFFLINE AI";


avatarWrap.appendChild(
avatar
);

avatarWrap.appendChild(
name
);


const content =
document.createElement(
"div"
);

content.className =
"content";


const bubble =
document.createElement(
"div"
);

bubble.className =
"bubble";

bubble.dir =
"auto";

bubble.textContent =
text || "";


content.appendChild(
bubble
);


row.appendChild(
avatarWrap
);

row.appendChild(
content
);

messages.appendChild(
row
);

scrollBottom();

return bubble;

}


function addTyping(){

welcome.style.display =
"none";


const row =
document.createElement(
"div"
);

row.className =
"message ai";


const avatarWrap =
document.createElement(
"div"
);

avatarWrap.className =
"avatar-wrap";


avatarWrap.innerHTML =

'<div class="avatar">AI</div>' +
'<div class="avatar-name">OFFLINE AI</div>';


const content =
document.createElement(
"div"
);

content.className =
"content";


const bubble =
document.createElement(
"div"
);

bubble.className =
"bubble";


bubble.innerHTML =

'<div class="typing">' +
'<span></span>' +
'<span></span>' +
'<span></span>' +
'</div>';


content.appendChild(
bubble
);

row.appendChild(
avatarWrap
);

row.appendChild(
content
);

messages.appendChild(
row
);

scrollBottom();

return row;

}


function quickAsk(text){

input.value =
text;

resizeInput(
input
);

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

el.style.height =
"44px";

el.style.height =
Math.min(
el.scrollHeight,
120
) + "px";

}


async function sendMessage(){

const text =
input.value.trim();


if(
!text ||
send.disabled
){

return;

}


addMessage(
text,
"user"
);


input.value =
"";

resizeInput(
input
);

send.disabled =
true;


const typing =
addTyping();


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

body:
JSON.stringify({
message:text
})

}
);


let data;

try{

data =
await response.json();

}catch(e){

data = {};

}


typing.remove();


if(!response.ok){

addMessage(
data.error ||
"خطایی رخ داد.",
"ai"
);

return;

}


addMessage(
data.reply ||
"پاسخی دریافت نشد.",
"ai"
);


}catch(error){

typing.remove();

addMessage(
"ارتباط با سرور برقرار نشد. دوباره تلاش کن.",
"ai"
);

}finally{

send.disabled =
false;

input.focus();

scrollBottom();

}

}


/* SETTINGS */

function openSettings(){

document
.getElementById("drawer")
.classList
.add("open");

}


function closeSettings(){

document
.getElementById("drawer")
.classList
.remove("open");

}


function drawerClick(event){

if(
event.target.id ===
"drawer"
){

closeSettings();

}

}


function setTheme(theme){

if(
theme === "light"
){

document.body.classList.add(
"light"
);

}else{

document.body.classList.remove(
"light"
);

}

localStorage.setItem(
"offline_theme",
theme
);

}


const savedTheme =
localStorage.getItem(
"offline_theme"
);

if(savedTheme){

setTheme(
savedTheme
);

}


/* CLEAR */

function clearChat(){

messages.innerHTML =
"";

welcome.style.display =
"block";

closeSettings();

input.focus();

}


/* PHOTO */

let rotation = 0;


function openPhoto(){

document
.getElementById("photoPanel")
.classList
.add("open");

}


function closePhoto(){

document
.getElementById("photoPanel")
.classList
.remove("open");

}


function previewImage(event){

const file =
event.target.files[0];

if(!file){

return;

}


const image =
document.getElementById(
"photoPreview"
);

image.src =
URL.createObjectURL(
file
);

image.style.display =
"block";

rotation =
0;

image.style.transform =
"rotate(0deg)";

image.style.filter =
"none";

}


function rotateImage(){

rotation +=
90;

document
.getElementById(
"photoPreview"
)
.style
.transform =
"rotate(" +
rotation +
"deg)";

}


function photoFilter(filter){

document
.getElementById(
"photoPreview"
)
.style
.filter =
filter;

}


function resetPhoto(){

const image =
document.getElementById(
"photoPreview"
);

rotation =
0;

image.style.transform =
"rotate(0deg)";

image.style.filter =
"none";

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


@app.route(
    "/chat",
    methods=["POST"]
)
def chat():

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )


    message = str(
        data.get(
            "message",
            ""
        )
    ).strip()


    if not message:

        return jsonify(
            error="پیام خالی است."
        ), 400


    if not GROQ_API_KEY:

        return jsonify(
            error=
            "GROQ_API_KEY در Render تنظیم نشده است."
        ), 500


    system_prompt = """
تو OFFLINE AI هستی؛ یک دستیار هوش مصنوعی مدرن برای پروژه ریس آفلاین کندزی.

نام:
OFFLINE AI

سازنده و بنیان‌گذار:
ریس آفلاین کندزی

اگر کاربر درباره سازنده یا بنیان‌گذار پرسید، بگو:

«سازنده و بنیان‌گذار من ریس آفلاین کندزی است؛ خالق پروژه OFFLINE AI.»

اگر کاربر پرسید تو کی هستی، بگو:

«من OFFLINE AI هستم؛ یک دستیار هوش مصنوعی مدرن که توسط ریس آفلاین کندزی ساخته شده‌ام.»

قوانین:

1. اگر کاربر فارسی یا دری صحبت کرد، کاملاً با حروف فارسی پاسخ بده.

2. اگر کاربر انگلیسی صحبت کرد، می‌توانی انگلیسی پاسخ بده.

3. پاسخ‌ها طبیعی، واضح و مفید باشند.

4. برای برنامه‌نویسی می‌توانی کد Python، HTML، CSS، JavaScript،
Flask و کد ربات تولید کنی.

5. هنگام تولید کد، کد را کامل و قابل استفاده ارائه کن.

6. اطلاعاتی درباره ریس آفلاین کندزی که داده نشده است، از خودت اختراع نکن.

7. اگر کاربر درد دل کرد، با مهربانی و بدون قضاوت پاسخ بده.
خودت را انسان یا درمانگر معرفی نکن.

8. درباره موضوعات مختلف اطلاعات عمومی و آموزشی ارائه کن.

9. اگر چیزی را نمی‌دانی، صادقانه بگو که مطمئن نیستی.

10. پاسخ‌ها را تا حد ممکن سریع، مرتب و قابل فهم نگه دار.
"""


    try:

        response = requests.post(

            "https://api.groq.com/openai/v1/chat/completions",

            headers={

                "Authorization":
                "Bearer " +
                GROQ_API_KEY,

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
                1200,

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


            return jsonify(
                error=error_message
            ), 500


        result =
            response.json()


        choices =
            result.get(
                "choices",
                []
            )


        reply = ""


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

        return jsonify(
            error=
            "زمان پاسخ‌گویی تمام شد. دوباره تلاش کن."
        ), 504


    except Exception:

        return jsonify(
            error=
            "خطایی در ارتباط با سرور رخ داد."
        ), 500


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
