from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

# ================= GLOBAL STATE =================
subjects = []
friends = []
invites = []
profile = {}

DAYS = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

# ================= CORE LOGIC =================
def build_subject(name, confidence):
    confidence = int(confidence)
    if confidence <= 2:
        return {"name":name,"confidence":confidence,"hours":3,"tag":"High Focus"}
    elif confidence == 3:
        return {"name":name,"confidence":confidence,"hours":2,"tag":"Medium Focus"}
    return {"name":name,"confidence":confidence,"hours":1,"tag":"Low Focus"}

def generate_timetable():
    table = {d:[] for d in DAYS}
    i=0
    for s in subjects:
        table[DAYS[i%7]].append(f"{s['name']} ({s['hours']}h)")
        i+=1
    return table

def planner_tips():
    tips=[]
    for s in subjects:
        if s["confidence"]<=2:
            tips.append(f"🔥 {s['name']} ku daily deep focus session thevai.")
        elif s["confidence"]==3:
            tips.append(f"📘 {s['name']} ku revision + practice mix pannunga.")
        else:
            tips.append(f"✅ {s['name']} strong area – weekly revision podhum.")
    if not tips:
        tips.append("➕ Subjects add pannina apram tips generate aagum.")
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
.hero{background:linear-gradient(120deg,#042f2e,#0f766e);color:white;padding:80px;text-align:center}
.container{max-width:1150px;margin:auto;padding:32px}
.card{background:white;border-radius:20px;padding:28px;margin-bottom:26px;
box-shadow:0 16px 38px rgba(0,0,0,.08)}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:26px}
input,select,button{padding:13px;width:100%;margin-top:10px;border-radius:12px;border:1px solid #ccc}
button{background:#0f766e;color:white;border:none;font-weight:600}
.friend{background:#5eead4;color:#042f2e;padding:8px 16px;border-radius:20px;margin:6px;display:inline-block}
table{width:100%;border-collapse:collapse}
th,td{border:1px solid #ddd;padding:14px;text-align:center}
th{background:#99f6e4}
footer{text-align:center;padding:22px;background:#ecfeff;color:#555}
</style>
</head>

<body>

<nav>
<b>StudySmart AI</b>
<div>
<a href="/">Home</a>
<a href="/planner">Planner</a>
<a href="/peers">Peers</a>
</div>
</nav>

{% if page=="home" %}
<div class="hero">
<h1>StudySmart AI</h1>
<p>AI-inspired study planner that adapts to student confidence & behavior</p>
</div>

<div class="container">

<div class="card">
<h3>❗ Problem We Solve</h3>
<p>
Students often create study timetables that look good on paper but fail in reality.
They don’t account for confidence level, weak topics, prerequisites, or motivation.
StudySmart AI addresses this gap using adaptive planning.
</p>
</div>

<div class="card">
<h3>⚙️ How StudySmart AI Works</h3>
<ol>
<li>Student enters subjects and confidence levels</li>
<li>System generates an adaptive weekly timetable</li>
<li>Invite friends to create accountability</li>
<li>Planner continuously guides focus using smart tips</li>
</ol>
</div>

<div class="card">
<h3>✨ Key Features</h3>
<ul>
<li>Confidence-based time allocation</li>
<li>Auto-generated weekly timetable</li>
<li>Invite & accept peer flow (mail-ready architecture)</li>
<li>Actionable daily study suggestions</li>
</ul>
</div>

<div class="card">
<h3>🎓 Student Profile</h3>
<form method="post">
<input name="name" placeholder="Your Name">
<button>Save Profile</button>
</form>
{% if profile %}
<p>Welcome, <b>{{profile.name}}</b> 👋</p>
{% endif %}
</div>

</div>
{% endif %}

{% if page=="planner" %}
<div class="container">

<div class="card">
<h3>🧠 Planner Intelligence</h3>
<p>
This planner automatically prioritizes weak subjects and distributes workload
across the week to reduce stress and burnout.
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
<h3>🎯 Focus Legend</h3>
<ul>
<li><b>High Focus</b> – Weak subjects, need deep concentration</li>
<li><b>Medium Focus</b> – Moderate understanding, regular revision</li>
<li><b>Low Focus</b> – Strong subjects, light practice</li>
</ul>
</div>

<div class="card">
<h3>💡 Smart Study Tips</h3>
<ul>
{% for t in tips %}
<li>{{t}}</li>
{% endfor %}
</ul>
</div>

</div>
{% endif %}

{% if page=="peers" %}
<div class="container">

<div class="card">
<h3>📨 Invite Friend</h3>
<p>
Invite friends to join your study circle.  
They receive an invite link, accept it, and access the same planner.
</p>
<form method="post">
<input name="fname" placeholder="Friend Name" required>
<input name="email" placeholder="Friend Email" required>
<button>Generate Invite Link</button>
</form>
</div>

{% for i in invites %}
<div class="card">
<b>{{i.name}}</b> ({{i.email}})<br>
Invite Link:<br>
<a href="{{i.link}}" target="_blank">{{i.link}}</a>
</div>
{% endfor %}

<div class="card">
<h3>👥 Connected Friends</h3>
{% for f in friends %}
<span class="friend">{{f}}</span>
{% endfor %}
</div>

</div>
{% endif %}

{% if page=="join" %}
<div class="container">
<div class="card">
<h2>🎉 You are invited to StudySmart AI</h2>
<p>Email: <b>{{email}}</b></p>
<form method="post">
<button>Accept Invite</button>
</form>
</div>
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
@app.route("/",methods=["GET","POST"])
def home():
    global profile
    if request.method=="POST":
        profile={"name":request.form["name"]}
    return render_template_string(HTML,page="home",profile=profile)

@app.route("/planner",methods=["GET","POST"])
def planner():
    if request.method=="POST":
        subjects.append(build_subject(
            request.form["subject"],
            request.form["confidence"]
        ))
    return render_template_string(
        HTML,page="planner",
        days=DAYS,
        timetable=generate_timetable(),
        tips=planner_tips()
    )

@app.route("/peers",methods=["GET","POST"])
def peers():
    if request.method=="POST":
        fname=request.form["fname"]
        email=request.form["email"]
        link=url_for("join",email=email,_external=True)
        invites.append({"name":fname,"email":email,"link":link})
    return render_template_string(
        HTML,page="peers",
        invites=invites,
        friends=friends
    )

@app.route("/join",methods=["GET","POST"])
def join():
    email=request.args.get("email")
    if request.method=="POST":
        friends.append(email)
        return redirect(url_for("planner"))
    return render_template_string(HTML,page="join",email=email)

# ================= RUN =================
if __name__=="__main__":
    app.run(debug=True)
