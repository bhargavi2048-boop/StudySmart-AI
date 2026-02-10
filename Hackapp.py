from flask import Flask, request, render_template_string, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "studysmart_secret"

# ================= GLOBAL STATE =================
subjects = []
friends = []
invites = []

DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

# ================= CORE LOGIC =================
def build_subject(name, confidence):
    confidence = int(confidence)
    if confidence <= 2:
        return {"name":name,"confidence":confidence,"hours":3,"tag":"🔥 High Focus"}
    elif confidence == 3:
        return {"name":name,"confidence":confidence,"hours":2,"tag":"📘 Medium Focus"}
    return {"name":name,"confidence":confidence,"hours":1,"tag":"✅ Low Focus"}

def generate_timetable():
    table = {d:[] for d in DAYS}
    i = 0
    for s in subjects:
        table[DAYS[i % 7]].append(f"{s['name']} ({s['hours']}h)")
        i += 1
    return table

def planner_tips():
    tips = []
    for s in subjects:
        if s["confidence"] <= 2:
            tips.append(f"🔥 {s['name']} ku daily deep focus + practice sessions thevai.")
        elif s["confidence"] == 3:
            tips.append(f"📘 {s['name']} ku revision + problem solving mix pannunga.")
        else:
            tips.append(f"✅ {s['name']} already strong – weekly revision podhum.")
    if not tips:
        tips.append("➕ Once subjects are added, the system automatically generates smart study tips.")
    return tips

# ================= UI =================
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>StudySmart AI</title>
<style>
body{margin:0;font-family:'Segoe UI';background:#f0fdfa}
nav{background:#042f2e;color:white;padding:18px 30px;display:flex;justify-content:space-between}
nav a{color:white;margin-left:20px;text-decoration:none;font-weight:600}
.hero{background:linear-gradient(120deg,#042f2e,#0f766e);color:white;padding:90px;text-align:center}
.container{max-width:1150px;margin:auto;padding:32px}
.card{background:white;border-radius:20px;padding:28px;margin-bottom:26px;
box-shadow:0 16px 38px rgba(0,0,0,.08)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:26px}
input,select,button{padding:13px;width:100%;margin-top:10px;border-radius:12px;border:1px solid #ccc}
button{background:#0f766e;color:white;border:none;font-weight:600;cursor:pointer}
table{width:100%;border-collapse:collapse}
th,td{border:1px solid #ddd;padding:14px;text-align:center}
th{background:#99f6e4}
footer{text-align:center;padding:22px;background:#ecfeff;color:#555}
.badge{display:inline-block;background:#ccfbf1;color:#065f46;padding:6px 14px;
border-radius:20px;margin:6px;font-weight:600}
</style>
</head>

<body>

<nav>
<b>StudySmart AI</b>
<div>
<a href="/">Home</a>
{% if session.get("user") %}
<span>👤 {{session.user}}</span>
<a href="/planner">Planner</a>
<a href="/peers">Peers</a>
<a href="/logout">Logout</a>
{% else %}
<a href="/login">Login</a>
{% endif %}
</div>
</nav>

{% if page=="home" %}
<div class="hero">
<h1>🎓 StudySmart AI</h1>
<p>AI-powered smart study planner for students</p>
<a href="/login"><button style="width:200px">Get Started</button></a>
</div>

<div class="container">
<div class="card">
<h3>🚀 What is StudySmart AI?</h3>
<p>
StudySmart AI is an intelligent study planner that helps students focus on weak subjects,
manage time efficiently and reduce exam stress.
</p>
</div>

<div class="grid">
<div class="card">
<h3>✨ Key Features</h3>
<ul>
<li>AI-based subject prioritization</li>
<li>Weekly timetable generation</li>
<li>Smart study tips</li>
<li>Peer collaboration</li>
</ul>
</div>

<div class="card">
<h3>🎯 Who Can Use?</h3>
<ul>
<li>School students</li>
<li>College students</li>
<li>Engineering & CS students</li>
<li>Self-learners</li>
</ul>
</div>
</div>
</div>
{% endif %}

{% if page=="login" %}
<div class="container">
<div class="card">
<h2>🔐 Student Login</h2>
<p>
After successful login, you will be able to access:
</p>
<ul>
<li>Personalized AI planner</li>
<li>Subject-wise timetable</li>
<li>Smart study tips</li>
</ul>
<form method="post">
<input name="name" placeholder="Enter your name" required>
<button>Login & Start Planning</button>
</form>
</div>
</div>
{% endif %}

{% if page=="planner" %}
<div class="container">

<div class="card">
<h3>🧠 Planner Intelligence</h3>
<p>
This AI planner automatically gives <b>more time to weak subjects</b>,
balances workload and improves consistency.
</p>
</div>

<div class="grid">
<div class="card">
<h3>➕ Add Subject</h3>
<form method="post">
<input name="subject" placeholder="Subject Name" required>
<select name="confidence">
<option value="1">Very Weak</option>
<option value="2">Weak</option>
<option value="3">Average</option>
<option value="4">Good</option>
<option value="5">Strong</option>
</select>
<button>Add Subject</button>
</form>
</div>

<div class="card">
<h3>📅 Weekly Timetable</h3>
<table>
<tr>{% for d in days %}<th>{{d}}</th>{% endfor %}</tr>
<tr>
{% for d in days %}
<td>{% for s in timetable[d] %}{{s}}<br>{% endfor %}</td>
{% endfor %}
</tr>
</table>
</div>
</div>

<div class="card">
<h3>📊 Subject Focus Overview</h3>
{% for s in subjects %}
<span class="badge">{{s.name}} – {{s.tag}}</span>
{% endfor %}
</div>

<div class="card">
<h3>💡 Smart Study Tips</h3>
<ul>
{% for t in tips %}
<li>{{t}}</li>
{% endfor %}
</ul>
</div>

<div class="card">
<h3>🔥 Motivation</h3>
<p>
Consistency beats motivation. Daily small effort = big results 💪
</p>
</div>

</div>
{% endif %}

{% if page=="peers" %}
<div class="container">
<div class="card">
<h3>📨 Invite Friend</h3>
<form method="post">
<input name="fname" placeholder="Friend Name" required>
<input name="email" placeholder="Friend Email" required>
<button>Generate Invite</button>
</form>
</div>

{% for i in invites %}
<div class="card">
<b>{{i.name}}</b> ({{i.email}})<br>
<a href="{{i.link}}" target="_blank">{{i.link}}</a>
</div>
{% endfor %}
</div>
{% endif %}

<footer>
StudySmart AI © 2026 <br>
<b>Designed & Developed by Bhargavi</b>
</footer>

</body>
</html>
"""

# ================= ROUTES =================
@app.route("/")
def home():
    return render_template_string(HTML, page="home")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=="POST":
        session["user"] = request.form["name"]
        return redirect(url_for("planner"))
    return render_template_string(HTML, page="login")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/planner", methods=["GET","POST"])
def planner():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method=="POST":
        subjects.append(build_subject(
            request.form["subject"],
            request.form["confidence"]
        ))
    return render_template_string(
        HTML, page="planner",
        days=DAYS,
        timetable=generate_timetable(),
        tips=planner_tips(),
        subjects=subjects
    )

@app.route("/peers", methods=["GET","POST"])
def peers():
    if "user" not in session:
        return redirect(url_for("login"))
    if request.method=="POST":
        fname=request.form["fname"]
        email=request.form["email"]
        link=url_for("planner",_external=True)
        invites.append({"name":fname,"email":email,"link":link})
    return render_template_string(HTML,page="peers",invites=invites)

# ================= RUN =================
if __name__=="__main__":
    app.run(debug=True)
