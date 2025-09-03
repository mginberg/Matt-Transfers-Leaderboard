import streamlit as st
import pandas as pd

# --- Load Google Sheet ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1ydOa1IBcWFTqxX4Ocm2jqtI4DkgVFkueTPy7n8VIFzY/export?format=csv"
data = pd.read_csv(SHEET_URL)
data = data.sort_values("Deals", ascending=False).reset_index(drop=True)

st.set_page_config(page_title="Spin the Wheel Leaderboard", page_icon="🏆", layout="wide")

# ---------------- TOP BANNER ----------------
st.markdown("""
<div style='text-align:center; padding:20px; background-color:#f8f9fa; border-radius:12px;'>
    <h1 style='color:#d32f2f;'>🚨 SEPTEMBER SPIN-THE-WHEEL CONTEST 🚨</h1>
    <h2 style='color:#333;'>🎉 MATT TRANSFERS EDITION 🎉</h2>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- TWO COLUMNS ----------------
left, right = st.columns([1,1])

# LEFT SIDE = Rules + Wheel
with left:
    st.markdown("""
    ### 🔑 How It Works
    - Every **"Intake Complete" = 1 raffle entry**  
    - Your total MATT TRANSFERS = your total entries  
    - The more you close, the better your odds  
    - Anyone with at least 1 entry is eligible  

    ### 🎡 Number of Spins
    - We will spin the wheel **4 times** 🎯  
    - Each spin = 1 of the prizes below  
    - Once you win, your entries are removed  

    ### 🏆 Prizes
    1. 🥇 **$600**  
    2. 🥈 **$400**  
    3. 🥉 **$300**  
    4. 💵 **$200**  

    ### 🎥 Live Spin & Payout
    - Live spin held **October 1st**  
    - Winners paid via **Zelle same day**  

    ### ⚠️ The Catch
    - You can **only win once**  
    - After winning, your entries are removed  
    """)

    st.markdown("## 🎡 Prize Wheel")
    wheel_html = """
    <div style="display:flex; justify-content:center; align-items:center;">
    <canvas id="wheelcanvas" width="350" height="350"></canvas>
    </div>
    <script>
    var options = ["$600", "$400", "$300", "$200"];
    var startAngle = 0;
    var arc = Math.PI / (options.length/2);
    var ctx;
    var spinAngle = 0.02;   // slower base spin
    var pulse = 0.005;      // wobble effect

    function drawRouletteWheel() {
      var canvas = document.getElementById("wheelcanvas");
      if (canvas.getContext) {
        var outsideRadius = 150;
        var textRadius = 115;
        var insideRadius = 40;
        ctx = canvas.getContext("2d");
        ctx.clearRect(0,0,350,350);

        ctx.strokeStyle = "black";
        ctx.lineWidth = 2;
        ctx.font = "bold 16px Helvetica, Arial";

        for(var i = 0; i < options.length; i++) {
          var angle = startAngle + i * arc;
          ctx.fillStyle = ["#e74c3c","#f1c40f","#2ecc71","#3498db"][i];
          ctx.beginPath();
          ctx.arc(175, 175, outsideRadius, angle, angle + arc, false);
          ctx.arc(175, 175, insideRadius, angle + arc, angle, true);
          ctx.stroke();
          ctx.fill();

          ctx.save();
          ctx.fillStyle = "white";
          ctx.translate(175 + Math.cos(angle + arc / 2) * textRadius,
                        175 + Math.sin(angle + arc / 2) * textRadius);
          ctx.rotate(angle + arc / 2 + Math.PI/2);
          ctx.fillText(options[i], -ctx.measureText(options[i]).width/2, 0);
          ctx.restore();
        }
      }
    }

    function rotateWheel(){
      // add pulse wobble
      spinAngle += (Math.random() - 0.5) * pulse;
      startAngle += spinAngle;
      drawRouletteWheel();
      requestAnimationFrame(rotateWheel);
    }

    drawRouletteWheel();
    rotateWheel();
    </script>
    """
    st.components.v1.html(wheel_html, height=370)

# RIGHT SIDE = Leaderboard
with right:
    st.markdown("<h2 style='text-align:center;'>🏆 Live Leaderboard</h2>", unsafe_allow_html=True)

    for i, row in data.iterrows():
        rank = i + 1
        name = row["Agent"]
        deals = int(row["Deals"])  # ensure integer
        slack_url = row["Slack URL"] if "Slack URL" in row and pd.notna(row["Slack URL"]) else ""

        # handle singular/plural
        deal_label = "Deal" if deals == 1 else "Deals"

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
            st.markdown(f"### {medal} {name} — **{deals} {deal_label}**")
            if deals > 0:
                st.progress(deals / data['Deals'].max())
            else:
                st.progress(0)

        # 👇 spacing between rows
        st.markdown("<div style='margin-bottom:25px;'></div>", unsafe_allow_html=True)
