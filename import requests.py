import requests

# --- Config ---
API_KEY = "6baa0aacc2d49d0b2a39aefa2472d414"

# --- Disease Rules (Updated Full Set) ---
DISEASES = [
    {
        "name": "Tomato Yellow Curl Virus",
        "temp_range": (30, 34),
        "humidity_range": (40, 55),
        "advice": [
            "Use insect-proof netting.",
            "Monitor whitefly population regularly.",
            "Apply imidacloprid or similar treatment if necessary."
        ]
    },
    {
        "name": "Two-Spotted Spider Mites",
        "temp_range": (32, 36),
        "humidity_range": (30, 40),
        "advice": [
            "Increase humidity to deter mites.",
            "Spray neem oil or insecticidal soap weekly.",
            "Introduce natural predators like predatory mites."
        ]
    },
    {
        "name": "Early Blight",
        "temp_range": (24, 30),
        "humidity_range": (70, 90),
        "advice": [
            "Remove lower leaves.",
            "Apply fungicides like mancozeb.",
            "Water at the base to avoid wet foliage."
        ]
    },
    {
        "name": "Late Blight",
        "temp_range": (15, 22),
        "humidity_range": (90, 100),
        "advice": [
            "Use fungicide like mancozeb.",
            "Remove infected plant parts immediately.",
            "Avoid overhead irrigation."
        ]
    },
    {
        "name": "Bacterial Spot",
        "temp_range": (25, 30),
        "humidity_range": (75, 90),
        "advice": [
            "Apply copper-based sprays.",
            "Avoid overhead watering.",
            "Use certified disease-free seeds."
        ]
    },
    {
        "name": "Leaf Mold",
        "temp_range": (18, 25),
        "humidity_range": (85, 100),
        "advice": [
            "Improve airflow and ventilation.",
            "Spray copper-based fungicides.",
            "Avoid wetting leaves."
        ]
    },
    {
        "name": "Septoria Leaf Spot",
        "temp_range": (21, 27),
        "humidity_range": (85, 100),
        "advice": [
            "Remove infected leaves promptly.",
            "Apply chlorothalonil or copper fungicides.",
            "Ensure leaves remain dry as much as possible."
        ]
    }
]

# --- Stress Conditions ---
STRESS_CONDITIONS = [
    {
        "name": "Heat Stress",
        "condition": lambda t, h: t > 34,
        "advice": [
            "Provide shade during peak sunlight hours.",
            "Water early in the morning or late in the evening.",
            "Mulch to reduce soil temperature and retain moisture."
        ]
    },
    {
        "name": "Drought Stress",
        "condition": lambda t, h: h < 35,
        "advice": [
            "Increase watering frequency.",
            "Use drip irrigation for water efficiency.",
            "Apply organic mulch to retain soil moisture."
        ]
    },
    {
        "name": "Cold Stress",
        "condition": lambda t, h: t < 10,
        "advice": [
            "Use covers to retain heat at night.",
            "Avoid fertilizing during cold spells.",
            "Water during the day to warm up the soil."
        ]
    },
    {
        "name": "Pest Vulnerability",
        "condition": lambda t, h: t > 32 and h < 40,
        "advice": [
            "Monitor for pests like mites and whiteflies.",
            "Apply neem oil or insecticidal soap.",
            "Raise humidity slightly to reduce pest activity."
        ]
    }
]

# --- Weather Functions ---
def get_weather_by_city(city):
    geocode_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    res = requests.get(geocode_url)
    res.raise_for_status()
    data = res.json()
    lat = data["coord"]["lat"]
    lon = data["coord"]["lon"]
    country = data["sys"]["country"]
    state = data.get("state", "N/A")
    return get_weather(lat, lon), data["name"], country, state

def get_weather(lat, lon):
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    )
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()
    return {
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"]
    }

# --- Analysis Functions ---
def check_disease_risks(weather, temp_tolerance=5, hum_tolerance=5):
    risks = []
    temp = weather["temp"]
    humidity = weather["humidity"]

    for disease in DISEASES:
        t_low, t_high = disease["temp_range"]
        h_low, h_high = disease["humidity_range"]

        temp_match = (t_low - temp_tolerance <= temp <= t_high + temp_tolerance)
        hum_match = (h_low - hum_tolerance <= humidity <= h_high + hum_tolerance)

        temp_score = 100 - (abs(((t_low + t_high) / 2) - temp) / ((t_high - t_low) / 2) * 100)
        hum_score = 100 - (abs(((h_low + h_high) / 2) - humidity) / ((h_high - h_low) / 2) * 100)
        temp_score = max(0, min(temp_score, 100))
        hum_score = max(0, min(hum_score, 100))
        avg_score = int((temp_score + hum_score) / 2)

        if temp_match and hum_match:
            if avg_score >= 70:
                risk_level = "HIGH"
            elif avg_score >= 40:
                risk_level = "MODERATE"
            else:
                risk_level = "LOW"
        elif temp_match or hum_match:
            risk_level = "POTENTIAL"
        else:
            continue  # No match at all

        risks.append({
            "disease": disease["name"],
            "risk": risk_level,
            "probability": avg_score,
            "expected_range": f"Temp: {t_low}-{t_high} °C, Humidity: {h_low}-{h_high}%",
            "advice": disease["advice"]
        })

    return risks


def check_stress_conditions(weather):
    stresses = []
    temp = weather["temp"]
    humidity = weather["humidity"]

    for condition in STRESS_CONDITIONS:
        if condition["condition"](temp, humidity):
            stresses.append({
                "name": condition["name"],
                "advice": condition["advice"]
            })

    return stresses

def get_general_plant_health(temp, humidity):
    ideal_temp = (24, 30)
    ideal_humidity = (60, 80)

    temp_score = 100 - min(abs(temp - (ideal_temp[0] + ideal_temp[1])/2), 100)
    hum_score = 100 - min(abs(humidity - (ideal_humidity[0] + ideal_humidity[1])/2), 100)
    health_score = int((temp_score + hum_score) / 2)

    if health_score >= 80:
        return "Excellent", "🌱 Conditions are ideal for tomato growth"
    elif health_score >= 60:
        return "Good", "🌿 Conditions are generally good for tomatoes"
    elif health_score >= 40:
        return "Fair", "⚠️ Conditions are suboptimal - monitor plants closely"
    else:
        return "Poor", "❌ Conditions are stressful for tomatoes - take preventive measures"

# --- Main Interaction ---
def check_location():
    city = input("Enter your city name: ")
    try:
        weather_data, location, country, state = get_weather_by_city(city)
        disease_risks = check_disease_risks(weather_data)
        stress_conditions = check_stress_conditions(weather_data)
        health_status, health_message = get_general_plant_health(weather_data["temp"], weather_data["humidity"])

        print(f"\n📍 Location: {location}, {state}, {country}")
        print(f"🌡️ Temp: {weather_data['temp']} °C")
        print(f"💧 Humidity: {weather_data['humidity']}%")
        print(f"\n📊 Plant Health: {health_status}")
        print(f"   {health_message}")

        if stress_conditions:
            print("\n⚠️ Environmental Stress Alerts:")
            for stress in stress_conditions:
                print(f"\n🔥 {stress['name']} Detected:")
                for tip in stress['advice']:
                    print(f"  - {tip}")

        print("\n🚨 Disease Warnings:")
        if disease_risks:
            for r in disease_risks:
                print(f"\n🌿 {r['disease']}: {r['risk']} RISK ({r['probability']}% chance)")
                print(f"   Expected Range → {r['expected_range']}")
                for tip in r['advice']:
                    print(f"  - {tip}")
        else:
            print("✅ No high-risk diseases based on current conditions.")

        while True:
            another = input("\n🔁 Check another location? (yes/no, press Enter to quit): ").strip().lower()
            if another in ["yes", "y"]:
                check_location()
                break
            elif another in ["no", "n", ""]:
                print("✅ Thank you for using the Tomato Disease Forecast System!")
                break
            else:
                print("❗Please enter 'yes', 'no', or press Enter to exit.")

    except requests.exceptions.HTTPError:
        print("❌ Could not find the weather data. Please check the city name and try again.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")


# --- Run Program ---
if __name__ == "__main__":
    print("🍅 Tomato Plant Disease & Stress Detection System")
    print("------------------------------------------------")
    check_location()
