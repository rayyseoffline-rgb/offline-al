<style>
*{
box-sizing:border-box;
-webkit-tap-highlight-color:transparent
}

html,body{
margin:0;
width:100%;
height:100%;
overflow:hidden
}

body{
font-family:Tahoma,Arial,sans-serif;
color:#173047;
background:
radial-gradient(circle at 10% 0%,#d9f4ff 0,transparent 32%),
radial-gradient(circle at 100% 100%,#dce8ff 0,transparent 35%),
linear-gradient(135deg,#f7fbff,#edf6fc)
}

.app{
height:100dvh;
max-width:860px;
margin:auto;
display:flex;
flex-direction:column;
position:relative;
overflow:hidden;
background:rgba(255,255,255,.38);
backdrop-filter:blur(25px);
-webkit-backdrop-filter:blur(25px);
box-shadow:0 0 60px rgba(72,135,180,.12)
}

/* HEADER */

.header{
height:74px;
flex-shrink:0;
display:flex;
align-items:center;
justify-content:space-between;
padding:9px 14px;
background:rgba(255,255,255,.72);
border-bottom:1px solid rgba(90,145,180,.16);
backdrop-filter:blur(22px);
-webkit-backdrop-filter:blur(22px);
z-index:3
}

.brand{
display:flex;
align-items:center;
gap:11px
}

.logo,.heroIcon{
display:grid;
place-items:center;
background:
linear-gradient(145deg,#ffffff,#e8f7ff);
border:1px solid #b8dcec;
box-shadow:
0 10px 30px rgba(39,133,177,.14),
inset 0 1px #ffffff
}

.logo{
width:48px;
height:48px;
border-radius:16px
}

.logo svg{
width:34px
}

.title{
font-size:17px;
font-weight:900;
color:#16384e
}

.sub{
font-size:9px;
color:#7893a5;
margin-top:4px
}

.dot{
display:inline-block;
width:6px;
height:6px;
border-radius:50%;
background:#25c982;
box-shadow:0 0 10px #25c982;
margin-left:5px
}

.clear{
width:42px;
height:42px;
border:1px solid #c8dce7;
border-radius:14px;
background:rgba(255,255,255,.65);
color:#557286;
font-size:18px;
box-shadow:0 5px 15px rgba(50,100,130,.08)
}

/* WELCOME */

.welcome{
text-align:center;
padding:25px 15px 12px
}

.heroIcon{
width:100px;
height:100px;
margin:auto;
border-radius:30px;
box-shadow:
0 20px 55px rgba(45,112,150,.18),
0 0 45px rgba(60,180,230,.12)
}

.heroIcon svg{
width:68px
}

.welcome h1{
font-size:24px;
margin:15px 0 7px;
background:linear-gradient(90deg,#173e58,#199bd2);
-webkit-background-clip:text;
background-clip:text;
color:transparent
}

.welcome p{
margin:0;
color:#7891a5;
font-size:11px
}

.chips{
display:flex;
justify-content:center;
gap:7px;
margin-top:12px;
flex-wrap:wrap
}

.chip{
font-size:9px;
color:#52748a;
border:1px solid #c8e0ec;
background:rgba(255,255,255,.6);
padding:6px 10px;
border-radius:20px;
box-shadow:0 5px 15px rgba(70,130,160,.06)
}

/* MESSAGES */

.messages{
flex:1;
overflow-y:auto;
padding:6px 12px 14px;
scroll-behavior:smooth
}

.messages::-webkit-scrollbar{
width:3px
}

.messages::-webkit-scrollbar-thumb{
background:#b6d3e2;
border-radius:9px
}

.message{
display:flex;
gap:8px;
margin:13px 0;
animation:show .2s ease
}

.message.user{
flex-direction:row-reverse
}

@keyframes show{
from{
opacity:0;
transform:translateY(5px)
}
to{
opacity:1;
transform:none
}
}

/* PROFILE */

.profileWrap{
width:38px;
min-width:38px
}

.profile{
width:38px;
height:38px;
border-radius:13px;
display:grid;
place-items:center;
font-size:8px;
font-weight:900;
background:
linear-gradient(145deg,#e8f8ff,#cceefe);
border:1px solid #a9d5e8;
color:#24769d;
box-shadow:0 7px 18px rgba(60,140,175,.12)
}

.user .profile{
background:
linear-gradient(145deg,#eef2f5,#dce5ea);
border-color:#c4d2da;
color:#607887
}

.profileName{
text-align:center;
margin-top:4px;
font-size:7px;
color:#7892a3;
white-space:nowrap
}

/* GLASS BUBBLES */

.content{
max-width:84%
}

.bubble{
padding:11px 14px;
border-radius:18px;
font-size:13px;
line-height:1.95;
white-space:pre-wrap;
word-break:break-word;
unicode-bidi:plaintext;
box-shadow:
0 10px 28px rgba(40,100,130,.08);
backdrop-filter:blur(18px);
-webkit-backdrop-filter:blur(18px)
}

.ai .bubble{
background:
linear-gradient(
145deg,
rgba(255,255,255,.78),
rgba(240,250,255,.55)
);
border:1px solid rgba(116,178,205,.25);
border-top-right-radius:5px;
color:#27475a
}

.user .bubble{
background:
linear-gradient(
145deg,
rgba(221,243,255,.9),
rgba(201,233,249,.68)
);
border:1px solid rgba(78,156,195,.22);
border-top-left-radius:5px;
color:#21455c
}

/* TYPING */

.typing{
display:flex;
gap:5px;
height:20px;
align-items:center
}

.typing i{
width:5px;
height:5px;
border-radius:50%;
background:#32a8dc;
animation:b 1s infinite
}

.typing i:nth-child(2){
animation-delay:.15s
}

.typing i:nth-child(3){
animation-delay:.3s
}

@keyframes b{
50%{
opacity:1;
transform:translateY(-4px)
}
0%,100%{
opacity:.25
}
}

/* SUGGESTIONS */

.suggestions{
display:flex;
gap:7px;
overflow-x:auto;
padding:5px 12px 9px
}

.suggestions::-webkit-scrollbar{
display:none
}

.suggestion{
flex-shrink:0;
padding:8px 12px;
border-radius:19px;
border:1px solid #c7dfe9;
background:rgba(255,255,255,.68);
color:#54758a;
font:10px Tahoma;
box-shadow:0 5px 15px rgba(60,120,150,.06)
}

/* INPUT */

.inputArea{
padding:8px 12px calc(10px + env(safe-area-inset-bottom));
background:rgba(255,255,255,.72);
border-top:1px solid rgba(100,150,175,.16);
backdrop-filter:blur(22px);
-webkit-backdrop-filter:blur(22px)
}

.inputBox{
display:flex;
align-items:flex-end;
gap:7px;
padding:5px;
border:1px solid #c4dce8;
border-radius:21px;
background:rgba(255,255,255,.72);
box-shadow:
0 8px 25px rgba(50,110,140,.08),
inset 0 1px #fff
}

.inputBox textarea{
flex:1;
min-width:0;
height:43px;
max-height:115px;
resize:none;
outline:0;
border:0;
background:transparent;
color:#17384c;
font:13px Tahoma;
padding:12px 8px
}

.inputBox textarea::placeholder{
color:#91a7b5
}

.send{
width:43px;
height:43px;
border:0;
border-radius:15px;
background:
linear-gradient(145deg,#35b8ed,#177db5);
color:white;
font-size:18px;
box-shadow:
0 7px 18px rgba(30,135,190,.2)
}

.send:active{
transform:scale(.94)
}

.send:disabled{
opacity:.45
}

.footer{
text-align:center;
margin-top:6px;
color:#8299a8;
font-size:7px
}

@media(max-width:480px){

.header{
height:65px
}

.logo{
width:43px;
height:43px
}

.heroIcon{
width:82px;
height:82px;
border-radius:25px
}

.heroIcon svg{
width:56px
}

.welcome h1{
font-size:21px
}

.bubble{
font-size:12.5px
}

}
</style>
