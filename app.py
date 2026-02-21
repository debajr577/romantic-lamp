from flask import Flask, render_template_string, request

app = Flask(__name__)

DEFAULT_MESSAGE = "We should talk more <3 "

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>For You <3 </title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
body {
    margin: 0;
    height: 100vh;
    background: #0b0b0b;
    display: flex;
    justify-content: center;
    align-items: center;
    font-family: 'Georgia', serif;
    overflow: hidden;
}

/* MAIN SCENE */
.scene {
    position: relative;
    width: 1100px;
    height: 650px;
    background: linear-gradient(to bottom, #111, #0a0a0a);
    border-radius: 20px;
    overflow: hidden;
}

/* VERTICAL STRIPE WALL DECOR */
.stripes {
    position: absolute;
    left: 0;
    top: 0;
    width: 120px;
    height: 100%;
    background: repeating-linear-gradient(
        to right,
        #ffffff10,
        #ffffff10 3px,
        transparent 3px,
        transparent 15px
    );
}

/* SOFT LIGHT GLOW */
.light-glow {
    position: absolute;
    width: 750px;
    height: 750px;
    background: radial-gradient(circle, rgba(255,210,120,0.9) 0%, rgba(255,180,60,0.4) 40%, transparent 70%);
    top: -200px;
    left: -100px;
    opacity: 0;
    transition: opacity 1.2s ease;
    pointer-events: none;
}

/* LAMP */
.lamp {
    position: absolute;
    bottom: 110px;
    left: 200px;
    cursor: pointer;
    transition: transform 0.4s ease;
}

.lamp:hover {
    transform: scale(1.05);
}

/* BOARD */
.board {
    position: absolute;
    top: 160px;
    right: 200px;
    width: 400px;
    padding: 40px;
    background: #2a1d14;
    color: #f5f5f5;
    font-size: 26px;
    text-align: center;
    border-radius: 15px;
    box-shadow: 0 0 0 rgba(255,200,120,0);
    opacity: 0;
    transition: all 1.2s ease;
}

/* CHAINS */
.board:before, .board:after {
    content: "";
    position: absolute;
    width: 4px;
    height: 80px;
    background: #444;
    top: -80px;
}

.board:before { left: 50px; }
.board:after { right: 50px; }

/* TABLE */
.table {
    position: absolute;
    bottom: 0;
    width: 100%;
    height: 120px;
    background: #050505;
}

/* FLOWER VASE */
.vase {
    position: absolute;
    bottom: 120px;
    right: 80px;
    animation: sway 3s ease-in-out infinite alternate;
}

/* STEM */
.stem {
    stroke: #2e8b57;
    stroke-width: 4;
}

/* PETALS */
.petal {
    fill: crimson;
}

/* CENTER */
.center {
    fill: gold;
}

/* ANIMATION */
@keyframes sway {
    from { transform: rotate(-3deg); }
    to { transform: rotate(3deg); }
}

/* ACTIVE STATE */
.on .light-glow {
    opacity: 1;
}

.on .board {
    opacity: 1;
    box-shadow: 0 0 40px rgba(255,200,120,0.8);
}

/* FORM */
.form-box {
    position: absolute;
    bottom: 10px;
    width: 100%;
    text-align: center;
}

input {
    padding: 10px;
    width: 350px;
    border-radius: 6px;
    border: none;
    background: #1c1c1c;
    color: white;
}

button {
    padding: 10px 20px;
    border: none;
    background: crimson;
    color: white;
    border-radius: 6px;
    cursor: pointer;
}
</style>
</head>

<body>

<div class="scene" id="scene">

    <div class="stripes"></div>
    <div class="light-glow"></div>

    <!-- LAMP -->
    <div class="lamp" onclick="turnOnLamp()">
        <svg width="180" height="300" viewBox="0 0 200 350">
            <path d="M40 40 L160 40 L140 140 L60 140 Z" fill="#dcdcdc"/>
            <rect x="95" y="140" width="10" height="150" fill="#c0c0c0"/>
            <ellipse cx="100" cy="310" rx="50" ry="15" fill="#888"/>
        </svg>
    </div>

    <!-- BOARD -->
    <div class="board">
        {{ message }}
    </div>

    <!-- FLOWER VASE (UPDATED PAIR WITH PETALS) -->
    <div class="vase">
        <svg width="160" height="220" viewBox="0 0 200 260">

            <!-- Vase -->
            <ellipse cx="100" cy="230" rx="40" ry="12" fill="#222"/>
            <path d="M75 120 Q100 95 125 120 L115 220 Q100 235 85 220 Z" fill="#333"/>

            <!-- Stem 1 -->
            <line x1="80" y1="120" x2="80" y2="50" class="stem"/>

            <!-- Stem 2 -->
            <line x1="120" y1="120" x2="120" y2="60" class="stem"/>

            <!-- Flower 1 -->
            <g>
                <circle cx="80" cy="45" r="6" class="center"/>
                <ellipse cx="80" cy="30" rx="6" ry="12" class="petal"/>
                <ellipse cx="80" cy="60" rx="6" ry="12" class="petal"/>
                <ellipse cx="65" cy="45" rx="12" ry="6" class="petal"/>
                <ellipse cx="95" cy="45" rx="12" ry="6" class="petal"/>
            </g>

            <!-- Flower 2 -->
            <g>
                <circle cx="120" cy="55" r="6" class="center"/>
                <ellipse cx="120" cy="40" rx="6" ry="12" class="petal"/>
                <ellipse cx="120" cy="70" rx="6" ry="12" class="petal"/>
                <ellipse cx="105" cy="55" rx="12" ry="6" class="petal"/>
                <ellipse cx="135" cy="55" rx="12" ry="6" class="petal"/>
            </g>

        </svg>
    </div>

    <div class="table"></div>

    <div class="form-box">
        <form method="POST">
            <input type="text" name="new_message" placeholder="Edit your message here">
            <button type="submit">Update</button>
        </form>
    </div>

</div>

<script>
function turnOnLamp() {
    document.getElementById("scene").classList.add("on");
}
</script>

</body>
</html>
"""

from flask import session, redirect, url_for

app.secret_key = "super_secret_key_123"
PASSWORD = "puchku"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == PASSWORD:
            session["auth"] = True
            return redirect(url_for("home"))
        else:
            return """
            <h3 style='text-align:center;margin-top:100px;color:red;'>Wrong password</h3>
            <a href='/' style='display:block;text-align:center;'>Try again</a>
            """

    return """
    <h2 style='text-align:center;margin-top:100px;'>Enter Password</h2>
    <form method='POST' style='text-align:center;'>
        <input type='password' name='password' placeholder='Password' required>
        <button type='submit'>Enter</button>
    </form>
    """

@app.route("/home", methods=["GET", "POST"])
def home():
    if not session.get("auth"):
        return redirect(url_for("login"))

    message = DEFAULT_MESSAGE
    if request.method == "POST":
        new_message = request.form.get("new_message")
        if new_message:
            message = new_message
    return render_template_string(HTML, message=message)
