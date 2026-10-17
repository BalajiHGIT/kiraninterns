
from flask import Flask, render_template_string, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "cab_booking_demo_key"

RATES = {"Auto": 12, "Sedan": 18, "SUV": 25}

ROUTES = {
    "1": ("Pune Station", "Shivajinagar", 5),
    "2": ("Swargate", "Kothrud", 8),
    "3": ("Hinjawadi", "Wakad", 10)
}

# Car images require an internet connection
   
CARS = {
    "Auto": "https://commons.wikimedia.org/wiki/Special:FilePath/An_auto_rickshaw_on_the_road_of_Delhi,_India.jpg?width=600",
    "Sedan": "https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&w=600&q=80",
    "SUV": "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=600&q=80"
}


STYLE = """
* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #10172a, #173b65, #087e8b);
    color: #182338;
    min-height: 100vh;
    padding: 25px 14px;
}

.card {
    max-width: 760px;
    margin: 25px auto;
    background: #ffffff;
    border-radius: 24px;
    padding: 28px;
    box-shadow: 0 18px 55px #0005;
}

.hero {
    text-align: center;
    padding: 12px 0 20px;
}

.logo { font-size: 48px; }

h1 {
    color: #173b65;
    margin-bottom: 10px;
}

.subtitle {
    color: #64748b;
    line-height: 1.6;
}

h2 { color: #173b65; }

.cars {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 12px;
    margin: 20px 0;
}

.car {
    border: 2px solid #e2e8f0;
    border-radius: 15px;
    overflow: hidden;
    background: white;
}

.car img {
    width: 100%;
    height: 115px;
    object-fit: cover;
    display: block;
}

.car-info {
    padding: 10px;
    text-align: center;
}

.car-info h3 {
    margin: 4px 0;
    font-size: 16px;
}

.price {
    color: #087e8b;
    font-weight: bold;
    font-size: 14px;
}

label {
    display: block;
    margin: 16px 0 7px;
    font-weight: bold;
}

select {
    width: 100%;
    padding: 13px;
    border: 1px solid #cbd5e1;
    border-radius: 10px;
    background: white;
    font-size: 15px;
}

button, .btn {
    display: block;
    width: 100%;
    border: 0;
    border-radius: 12px;
    padding: 14px;
    margin-top: 15px;
    text-align: center;
    text-decoration: none;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    background: linear-gradient(90deg, #087e8b, #1769aa);
    color: white;
}

.secondary {
    background: #edf2f7;
    color: #173b65;
}

.danger { background: #d94848; color: white; }

.details {
    background: #f1f7fb;
    border-radius: 15px;
    padding: 18px;
    line-height: 2;
}

.fare {
    text-align: center;
    background: #e1f8ed;
    padding: 18px;
    border-radius: 15px;
    margin-top: 15px;
}

.fare strong {
    font-size: 32px;
    color: #087e55;
}

.otp {
    text-align: center;
    font-size: 38px;
    letter-spacing: 8px;
    font-weight: bold;
    color: #087e55;
    background: #e1f8ed;
    border-radius: 15px;
    padding: 18px;
}

.center { text-align: center; }

footer {
    text-align: center;
    color: #64748b;
    font-size: 13px;
    margin-top: 22px;
}

@media (max-width: 520px) {
    .card { padding: 18px; }
    .cars { grid-template-columns: 1fr; }
    .car img { height: 175px; }
}
"""

def page(content):
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>RideGo | Cab Booking</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>""" + STYLE + """</style>
    </head>
    <body>
        <main class="card">
            """ + content + """
            <footer>🚕 RideGo · Your Journey, Our Priority</footer>
        </main>
    </body>
    </html>
    """)

@app.route("/")
def home():
    session.pop("booking", None)
    content = """
    <div class="hero">
        <div class="logo">🚕</div>
        <h1>Welcome to RideGo!</h1>
        <p class="subtitle">
            Your Journey, Our Priority ✨<br>
            Safe rides. Happy journeys. Every time!
        </p>
    </div>

    <div class="cars">
        <div class="car">
            <img src='""" + CARS["Auto"] + """' alt="Auto">
            <div class="car-info">
                <h3>🛺 Auto</h3>
                <div class="price">₹12 / km</div>
            </div>
        </div>
        <div class="car">
            <img src='""" + CARS["Sedan"] + """' alt="Sedan">
            <div class="car-info">
                <h3>🚘 Sedan</h3>
                <div class="price">₹18 / km</div>
            </div>
        </div>
        <div class="car">
            <img src='""" + CARS["SUV"] + """' alt="SUV">
            <div class="car-info">
                <h3>🚙 SUV</h3>
                <div class="price">₹25 / km</div>
            </div>
        </div>
    </div>

    <a class="btn" href="/book">🚕 Book Your Ride</a>
    <a class="btn secondary" href="/exit">Exit</a>
    """
    return page(content)

@app.route("/book", methods=["GET", "POST"])
def book():
    if request.method == "POST":
        cab = request.form.get("cab")
        route = request.form.get("route")

        if cab not in RATES or route not in ROUTES:
            return page("""
            <h2>Invalid selection!</h2>
            <a class="btn" href="/book">Try Again</a>
            """)

        source, destination, distance = ROUTES[route]
        session["booking"] = {
            "cab": cab,
            "source": source,
            "destination": destination,
            "distance": distance,
            "rate": RATES[cab],
            "fare": distance * RATES[cab]
        }
        return redirect(url_for("details"))

    content = """
    <h1>🚘 Choose Your Ride</h1>
    <p class="subtitle">Select a cab and your preferred route.</p>

    <div class="cars">
    """
    for cab, rate in RATES.items():
        content += f"""
        <div class="car">
            <img src="{CARS[cab]}" alt="{cab}">
            <div class="car-info">
                <h3>{cab}</h3>
                <div class="price">₹{rate}/km</div>
            </div>
        </div>
        """

    content += """
    </div>
    <form method="POST">
        <label>Choose Cab Type</label>
        <select name="cab" required>
            <option value="Auto">🛺 Auto - ₹12/km</option>
            <option value="Sedan">🚘 Sedan - ₹18/km</option>
            <option value="SUV">🚙 SUV - ₹25/km</option>
        </select>

        <label>Choose Route</label>
        <select name="route" required>
            <option value="1">Pune Station → Shivajinagar (5 km)</option>
            <option value="2">Swargate → Kothrud (8 km)</option>
            <option value="3">Hinjawadi → Wakad (10 km)</option>
        </select>

        <button type="submit">Calculate My Fare →</button>
    </form>
    <a class="btn secondary" href="/">← Main Menu</a>
    """
    return page(content)

@app.route("/details")
def details():
    booking = session.get("booking")
    if not booking:
        return redirect(url_for("home"))

    content = f"""
    <div class="hero">
        <div class="logo">🧾</div>
        <h1>Your Ride Summary</h1>
        <p class="subtitle">Please check your booking details.</p>
    </div>

    <div class="details">
        <b>🚘 Cab:</b> {booking['cab']}<br>
        <b>📍 Pickup:</b> {booking['source']}<br>
        <b>🏁 Destination:</b> {booking['destination']}<br>
        <b>🛣️ Distance:</b> {booking['distance']} km<br>
        <b>💵 Rate:</b> ₹{booking['rate']}/km
    </div>

    <div class="fare">
        <div>Total Estimated Fare</div>
        <strong>₹{booking['fare']}</strong>
    </div>

    <p class="center">Ready to start your journey?</p>
    <form action="/confirm" method="POST">
        <button type="submit">✅ Confirm & Share OTP</button>
    </form>
    <form action="/cancel" method="POST">
        <button class="danger" type="submit">✖ Cancel Ride</button>
    </form>
    """
    return page(content)

@app.route("/confirm", methods=["POST"])
def confirm():
    booking = session.get("booking")
    if not booking:
        return redirect(url_for("home"))

    if "otp" not in booking:
        booking["otp"] = random.randint(1000, 9999)
        session["booking"] = booking

    content = f"""
    <div class="hero">
        <div class="logo">🎉</div>
        <h1>Booking Confirmed!</h1>
        <p class="subtitle">Thank you for choosing RideGo.</p>
    </div>

    <p class="center">Your demo booking OTP is:</p>
    <div class="otp">{booking['otp']}</div>

    <div class="fare">
        <h2>🎊 Happy Journey!</h2>
        <p>Have a safe and wonderful ride!</p>
    </div>

    <p class="center">
        🔒 OTP shared. Cancellation is not allowed now.
    </p>
    <a class="btn" href="/">Return to Main Menu</a>
    """
    return page(content)

@app.route("/cancel", methods=["POST"])
def cancel():
    booking = session.get("booking")
    if not booking:
        return redirect(url_for("home"))

    if "otp" in booking:
        return page("""
        <h1>🔒 Ride Locked</h1>
        <p class="center">OTP has already been shared.
        Cancellation is not allowed.</p>
        <a class="btn" href="/">Main Menu</a>
        """)

    session.pop("booking", None)
    return page("""
    <div class="hero">
        <div class="logo">😌</div>
        <h1>Ride Cancelled</h1>
        <p class="subtitle">Your ride was cancelled before OTP sharing.</p>
        <p class="center">No OTP has been shared.</p>
    </div>
    <a class="btn" href="/">Back to Main Menu</a>
    """)

@app.route("/exit")
def exit_app():
    session.clear()
    return page("""
    <div class="hero">
        <div class="logo">👋</div>
        <h1>Thank You!</h1>
        <p class="subtitle">Thanks for riding with RideGo.</p>
        <h2 class="center">Have a Happy Journey! 💚</h2>
    </div>
    <a class="btn" href="/">Book Another Ride</a>
    """)

if __name__ == "__main__":
    app.run(debug=True)
