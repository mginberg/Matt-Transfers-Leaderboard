import streamlit as st
import pandas as pd

# --- Leaderboard setup (same as before) ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ydOa1IBcWFTqxX4Ocm2jqtI4DkgVFkueTPy7n8VIFzY/export?format=csv"
data = pd.read_csv(SHEET_URL)
data = data.sort_values("Deals", ascending=False).reset_index(drop=True)

st.set_page_config(page_title="Spin the Wheel Leaderboard", page_icon="🏆", layout="centered")
st.markdown("<h1 style='text-align:center;'>🏆 Monthly Deal Leaderboard</h1>", unsafe_allow_html=True)

for i, row in data.iterrows():
    rank = i + 1
    name = row["Agent"]
    deals = row["Deals"]
    slack_url = row["Slack URL"] if "Slack URL" in row and pd.notna(row["Slack URL"]) else ""
    if rank == 1:
        medal = "🥇"
    elif rank == 2:
        medal = "🥈"
    elif rank == 3:
        medal = "🥉"
    else:
        medal = f"{rank}."
    cols = st.columns([1,5])
    with cols[0]:
        if slack_url:
            st.image(slack_url, width=60)
    with cols[1]:
        st.markdown(f"### {medal} {name} — **{deals} deals**")
        st.progress(deals / data['Deals'].max())

# --- Contest header ---
st.markdown("""
# 🚨 SEPTEMBER SPIN-THE-WHEEL CONTEST 🚨
🎉 **MATT TRANSFERS EDITION** 🎉  

We're raffling off **$1,500 CASH** at the end of the month!

🥇 $600  
🥈 $400  
🥉 $300  
💵 $200  

Every "Intake Complete" = 1 raffle entry.  
The more you write, the better your odds.  
""")

# --- Prize Wheel (auto-spinning) ---
st.markdown("## 🎡 Prize Wheel")
wheel_html = """
<div style="display:flex; justify-content:center; align-items:center;">
<canvas id="wheelcanvas" width="400" height="400"></canvas>
</div>
<script>
var options = ["$600", "$400", "$300", "$200"];
var startAngle = 0;
var arc = Math.PI / (options.length/2);
var ctx;
var spinAngle = 0.1;

function drawRouletteWheel() {
  var canvas = document.getElementById("wheelcanvas");
  if (canvas.getContext) {
    var outsideRadius = 180;
    var textRadius = 140;
    var insideRadius = 50;
    ctx = canvas.getContext("2d");
    ctx.clearRect(0,0,400,400);

    ctx.strokeStyle = "black";
    ctx.lineWidth = 2;
    ctx.font = "bold 18px Helvetica, Arial";

    for(var i = 0; i < options.length; i++) {
      var angle = startAngle + i * arc;
      ctx.fillStyle = ["#e74c3c","#f1c40f","#2ecc71","#3498db"][i];
      ctx.beginPath();
      ctx.arc(200, 200, outsideRadius, angle, angle + arc, false);
      ctx.arc(200, 200, insideRadius, angle + arc, angle, true);
      ctx.stroke();
      ctx.fill();

      ctx.save();
      ctx.fillStyle = "white";
      ctx.translate(200 + Math.cos(angle + arc / 2) * textRadius,
                    200 + Math.sin(angle + arc / 2) * textRadius);
      ctx.rotate(angle + arc / 2 + Math.PI/2);
      ctx.fillText(options[i], -ctx.measureText(options[i]).width/2, 0);
      ctx.restore();
    }
  }
}

function rotateWheel(){
  startAngle += spinAngle;
  drawRouletteWheel();
  requestAnimationFrame(rotateWheel);
}

drawRouletteWheel();
rotateWheel();
</script>
"""
st.components.v1.html(wheel_html, height=420)
