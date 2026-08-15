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
<meta name="viewport" content="width=device-width,initial-scale=1.0,viewport-fit=cover">
<meta name="theme-color" content="#080a0f">

<title>OFFLINE AI</title>

<style>
*{
    box-sizing:border-box;
    -webkit-tap-highlight-color:transparent;
}

html,body{
    width:100%;
    height:100%;
    margin:0;
    overflow:hidden;
}

body{
    font-family:
        Tahoma,
        Arial,
        sans-serif;
    background:
        radial-gradient(
            circle at 80% 0%,
            rgba(70,90,130,.20),
            transparent 30%
        ),
        radial-gradient(
            circle at 0% 100%,
            rgba(30,60,100,.16),
            transparent 32%
        ),
        #080a0f;
    color:#f3f5f8;
}

.app{
    width:100%;
    max-width:760px;
    height:100dvh;
    margin:auto;
    display:flex;
    flex-direction:column;
    position:relative;
    overflow:hidden;
}

/* HEADER */

.header{
    height:70px;
    flex-shrink:0;
    display:flex;
    align-items:center;
    justify-content:space-between;
    padding:10px 15px;
    background:rgba(8,10,15,.88);
    border-bottom:1px solid rgba(255,255,255,.07);
    backdrop-filter:blur(22px);
    z-index:10;
}

.brand{
    display:flex;
    align-items:center;
    gap:11px;
}

.main-avatar{
    width:46px;
    height:46px;
    border-radius:14px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-weight:900;
    font-size:12px;
    letter-spacing:-.5px;
    color:white;
    background:
        linear-gradient(
            145deg,
            #202735,
            #10141c
        );
    border:1px solid rgba(255,255,255,.12);
    box-shadow:
        0 8px 25px rgba(0,0,0,.35),
        inset 0 1px rgba(255,255,255,.12);
}

.brand-name{
    font-size:16px;
    font-weight:800;
    letter-spacing:.2px;
}

.brand-status{
    margin-top:4px;
    font-size:9px;
    color:#8993a3;
}

.status-dot{
    display:inline-block;
    width:6px;
    height:6px;
    border-radius:50%;
    background:#35d58a;
    box-shadow:0 0 8px rgba(53,213,138,.8);
    margin-left:4px;
}

.header-btn{
    width:40px;
    height:40px;
    border-radius:12px;
    border:1px solid rgba(255,255,255,.08);
    background:rgba(255,255,255,.045);
    color:#d9dee7;
    font-size:18px;
}

/* WELCOME */

.welcome{
    padding:28px 18px 14px;
    text-align:center;
}

.welcome-avatar{
    width:84px;
    height:84px;
    margin:auto;
    border-radius:25px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:23px;
    font-weight:900;
    background:
        linear-gradient(
            145deg,
            #242b38,
            #0f131b
        );
    border:1px solid rgba(255,255,255,.12);
    box-shadow:
        0 18px 45px rgba(0,0,0,.38),
        0 0 35px rgba(70,100,150,.13),
        inset 0 1px rgba(255,255,255,.13);
}

.welcome h1{
    margin:15px 0 7px;
    font-size:24px;
    font-weight:900;
    background:
        linear-gradient(
            90deg,
            #ffffff,
            #b9c5d7
        );
    -webkit-background-clip:text;
    color:transparent;
}

.welcome p{
    margin:0;
    color:#737d8d;
    font-size:11px;
}

/* MESSAGES */

.messages{
    flex:1;
    overflow-y:auto;
    padding:8px 13px 15px;
    scroll-behavior:smooth;
}

.messages::-webkit-scrollbar{
    width:3px;
}

.messages::-webkit-scrollbar-thumb{
    background:#29313d;
    border-radius:20px;
}

.message{
    display:flex;
    gap:9px;
    margin:13px 0;
    animation:messageIn .22s ease-out;
}

@keyframes messageIn{
    from{
        opacity:0;
        transform:translateY(5px);
    }
    to{
        opacity:1;
        transform:translateY(0);
    }
}

.message.user{
    flex-direction:row-reverse;
}

.profile{
    width:34px;
    height:34px;
    min-width:34px;
    border-radius:11px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:8px;
    font-weight:900;
    color:#fff;
    background:
        linear-gradient(
            145deg,
            #202733,
            #10141b
        );
    border:1px solid rgba(255,255,255,.10);
    box-shadow:0 5px 15px rgba(0,0,0,.3);
}

.user .profile{
    background:
        linear-gradient(
            145deg,
            #293342,
            #151a22
        );
}

.message-content{
    max-width:82%;
}

.profile-name{
    font-size:9px;
    color:#707b8c;
    margin:1px 4px 5px;
}

.user .profile-name{
    text-align:right;
}

.bubble{
    padding:11px 14px;
    border-radius:16px;
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
            rgba(255,255,255,.035)
        );
    border:1px solid rgba(255,255,255,.08);
    border-top-right-radius:5px;
    color:#e9edf3;
}

.user .bubble{
    background:
        linear-gradient(
            145deg,
            #202733,
            #171c25
        );
    border:1px solid rgba(255,255,255,.08);
    border-top-left-radius:5px;
    color:#f4f6f9;
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
    background:#aeb8c8;
    animation:typing 1s infinite;
}

.typing span:nth-child(2){
    animation-delay:.13s;
}

.typing span:nth-child(3){
    animation-delay:.26s;
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
    padding:5px 13px 9px;
}

.suggestions::-webkit-scrollbar{
    display:none;
}

.suggestion{
    flex-shrink:0;
    border:1px solid rgba(255,255,255,.08);
    background:rgba(255,255,255,.045);
    color:#aeb7c5;
    padding:8px 12px;
    border-radius:18px;
    font-family:inherit;
    font-size:10px;
}

.suggestion:active{
    transform:scale(.96);
}

/* INPUT */

.input-area{
    flex-shrink:0;
    padding:
        8px
        12px
        calc(10px + env(safe-area-inset-bottom));
    background:rgba(7,9,13,.94);
    border-top:1px solid rgba(255,255,255,.07);
    backdrop-filter:blur(22px);
}

.input-box{
    display:flex;
    align-items:flex-end;
    gap:7px;
    padding:5px;
    border-radius:18px;
    background:#11151c;
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
    color:#f5f7fa;
    font-family:inherit;
    font-size:13px;
    padding:12px 8px;
}

textarea::placeholder{
    color:#626c7b;
}

.send{
    width:43px;
    height:43px;
    border:0;
    border-radius:14px;
    color:#fff;
    background:
        linear-gradient(
            145deg,
            #3a4658,
            #202733
        );
    border:1px solid rgba(255,255,255,.10);
    font-size:17px;
    transition:.15s;
}

.send:active{
    transform:scale(.91);
}

.send.loading{
    opacity:.55;
}

.footer{
    text-align:center;
    color:#4e5867;
    font-size:7px;
    margin-top:6px;
}

@media(max-width:480px){

    .header{
        height:64px;
        padding:8px 12px;
    }

    .main-avatar{
        width:42px;
        height:42px;
    }

    .welcome{
        padding-top:21px;
    }

    .welcome-avatar{
        width:72px;
        height:72px;
        border-radius:22px;
        font-size:20px;
    }

    .welcome h1{
        font-size:21px;
    }

    .message-content{
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

        <div class="main-avatar">
            OFF
        </div>

        <div>
            <div class="brand-name">
                OFFLINE AI
            </div>

            <div class="brand-status">
                <span class="status-dot"></span>
                آماده پاسخ‌گویی
            </div>
        </div>

    </div>

    <button
        class="header-btn"
        onclick="clearChat()">
        ⌫
    </button>

</header>


<section
    class="welcome"
    id="welcome">

    <div class="welcome-avatar">
        OFF
    </div>

    <h1>
        خوش آمدی به OFFLINE AI
    </h1>

    <p>
        سریع، هوشمند و همیشه آماده گفت‌وگو
    </p>

</section>


<main
    class="messages"
    id="messages">
</main>


<div class="suggestions">

    <button
        class="suggestion"
        onclick="quickAsk('سلام، خودت را معرفی کن')">
        معرفی OFFLINE AI
    </button>

    <button
        class="suggestion"
        onclick="quickAsk('سازنده تو کیست؟')">
        سازنده
    </button>

    <button
        class="suggestion"
        onclick="quickAsk('برای یادگیری برنامه نویسی کمکم کن')">
        برنامه‌نویسی
    </button>

    <button
        class="suggestion"
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

const sendButton =
    document.getElementById("send");


function scrollBottom(){

    requestAnimationFrame(() => {
        messages.scrollTop =
            messages.scrollHeight;
    });
}


function addMessage(
    text,
    type,
    streaming = false
){

    welcome.style.display = "none";

    const row =
        document.createElement("div");

    row.className =
        "message " + type;

    const profile =
        document.createElement("div");

    profile.className =
        "profile";

    profile.textContent =
        type === "user"
            ? "OFF"
            : "AI";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    const name =
        document.createElement("div");

    name.className =
        "profile-name";

    name.textContent =
        type === "user"
            ? "OFFLINE"
            : "OFFLINE AI";


    const bubble =
        document.createElement("div");

    bubble.className =
        "bubble";

    bubble.textContent =
        text || "";


    content.appendChild(name);
    content.appendChild(bubble);

    row.appendChild(profile);
    row.appendChild(content);

    messages.appendChild(row);

    scrollBottom();

    return bubble;
}


function addTyping(){

    welcome.style.display = "none";

    const row =
        document.createElement("div");

    row.className =
        "message ai";

    const profile =
        document.createElement("div");

    profile.className =
        "profile";

    profile.textContent = "AI";


    const content =
        document.createElement("div");

    content.className =
        "message-content";


    const name =
        document.createElement("div");

    name.className =
        "profile-name";

    name.textContent =
        "OFFLINE AI";


    const bubble =
        document.createElement("div");

    bubble.className =
        "bubble";

    bubble.innerHTML = `
        <div class="typing">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;


    content.appendChild(name);
    content.appendChild(bubble);

    row.appendChild(profile);
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

    if(
        event.key === "Enter" &&
        !event.shiftKey
    ){

        event.preventDefault();

        sendMessage();
    }
}


function resizeInput(element){

    element.style.height = "43px";

    element.style.height =
        Math.min(
            element.scrollHeight,
            115
        ) + "px";
}


async function sendMessage(){

    const text =
        input.value.trim();

    if(!text) return;

    addMessage(
        text,
        "user"
    );

    input.value = "";

    input.style.height = "43px";

    sendButton.classList.add("loading");

    sendButton.disabled = true;

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

                    body:JSON.stringify({
                        message:text
                    })
                }
            );


        if(!response.ok){

            const error =
                await response.json();

            typing.remove();

            addMessage(
                error.error ||
                "خطا در ارتباط با هوش مصنوعی.",
                "ai"
            );

            return;
        }


        typing.remove();


        const bubble =
            addMessage(
                "",
                "ai"
            );


        const reader =
            response.body.getReader();

        const decoder =
            new TextDecoder();

        let fullText = "";


        while(true){

            const {
                value,
                done
            } =
                await reader.read();

            if(done) break;


            const chunk =
                decoder.decode(
                    value,
                    {
                        stream:true
                    }
                );


            const lines =
                chunk.split("\n");


            for(
                const line of lines
            ){

                if(
                    !line.startsWith("data:")
                ){
                    continue;
                }


                const data =
                    line.slice(5).trim();


                if(
                    !data ||
                    data === "[DONE]"
                ){
                    continue;
                }


                try{

                    const parsed =
                        JSON.parse(data);


                    if(parsed.error){

                        fullText +=
                            parsed.error;

                    }else{

                        fullText +=
                            parsed.text || "";
                    }


                    bubble.textContent =
                        fullText;

                    scrollBottom();

                }catch(e){
                    // نادیده گرفتن قطعه ناقص
                }
            }
        }


        if(!fullText){

            bubble.textContent =
                "پاسخی دریافت نشد. دوباره تلاش کن.";
        }

    }catch(error){

        typing.remove();

        addMessage(
            "ارتباط با سرور برقرار نشد. لطفاً دوباره تلاش کن.",
            "ai"
        );

    }finally{

        sendButton.classList.remove(
            "loading"
        );

        sendButton.disabled =
            false;

        input.focus();
    }
}


function clearChat(){

    messages.innerHTML = "";

    welcome.style.display =
        "block";

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

    data = request.get_json(
        silent=True
    ) or {}

    message = data.get(
        "message",
        ""
    ).strip()

    if not message:
        return jsonify({
            "error":
                "پیام خالی است."
        }), 400


    if not GROQ_API_KEY:
        return jsonify({
            "error":
                "GROQ_API_KEY در Render تنظیم نشده است."
        }), 500


    system_prompt = """
تو OFFLINE AI هستی؛ یک دستیار هوش مصنوعی مدرن.

هویت رسمی برند:

نام محصول:
OFFLINE AI

سازنده و بنیان‌گذار:
ریس آفلاین کندزی

اگر کاربر درباره سازنده، بنیان‌گذار، خالق یا صاحب OFFLINE AI پرسید، بگو:

«سازنده و بنیان‌گذار من ریس آفلاین کندزی است؛ خالق پروژه OFFLINE AI.»

اگر کاربر پرسید «تو کی هستی؟» یا درباره OFFLINE AI سؤال کرد، بگو:

«من OFFLINE AI هستم؛ یک دستیار هوش مصنوعی مدرن که با هدف ارائه تجربه‌ای هوشمند، زیبا و متفاوت ساخته شده‌ام. سازنده و بنیان‌گذار من ریس آفلاین کندزی است؛ کسی که ایده OFFLINE AI را به یک پروژه واقعی تبدیل کرده است.»

با کاربر به زبان خودش صحبت کن.
پاسخ‌ها طبیعی، واضح، محترمانه و مفید باشند.
درباره سازنده اطلاعاتی که مشخص نشده را اختراع نکن.
"""


    try:

        response = requests.post(

            "https://api.groq.com/openai/v1/chat/completions",

            headers={
                "Authorization":
                    f"Bearer {GROQ_API_KEY}",

                "Content-Type":
                    "application/json"
            },

            json={

                # مدل سریع برای گفت‌وگوی روزمره
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

                # پاسخ به صورت زنده
                "stream":
                    True
            },

            stream=True,

            timeout=60
        )


        if response.status_code != 200:

            try:
                error_data =
                    response.json()

                error_text =
                    error_data.get(
                        "error",
                        {}
                    ).get(
                        "message",
                        "خطا در سرویس هوش مصنوعی."
                    )

            except Exception:

                error_text =
                    "خطا در سرویس هوش مصنوعی."

            return jsonify({
                "error":
                    error_text
            }), 500


        def generate():

            try:

                for line in response.iter_lines(
                    decode_unicode=True
                ):

                    if not line:
                        continue


                    if not line.startswith(
                        "data:"
                    ):
                        continue


                    data =
                        line[5:].strip()


                    if data == "[DONE]":
                        break


                    try:

                        parsed =
                            json.loads(data)


                        choices =
                            parsed.get(
                                "choices",
                                []
                            )


                        if not choices:
                            continue


                        delta =
                            choices[0].get(
                                "delta",
                                {}
                            )


                        text =
                            delta.get(
                                "content",
                                ""
                            )


                        if text:

                            yield (
                                "data: "
                                + json.dumps(
                                    {
                                        "text":
                                            text
                                    },
                                    ensure_ascii=False
                                )
                                + "\n\n"
                            )

                    except Exception:
                        continue


                yield "data: [DONE]\n\n"


            except Exception as error:

                yield (
                    "data: "
                    + json.dumps(
                        {
                            "error":
                                "ارتباط با سرویس قطع شد."
                        },
                        ensure_ascii=False
                    )
                    + "\n\n"
                )


        return Response(

            generate(),

            mimetype="text/event-stream",

            headers={
                "Cache-Control":
                    "no-cache",

                "X-Accel-Buffering":
                    "no",

                "Connection":
                    "keep-alive"
            }
        )


    except requests.exceptions.Timeout:

        return jsonify({
            "error":
                "زمان پاسخ‌گویی تمام شد. دوباره تلاش کن."
        }), 504


    except Exception:

        return jsonify({
            "error":
                "خطایی در ارتباط با سرور رخ داد."
        }), 500


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
