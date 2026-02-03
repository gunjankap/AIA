from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests

from Agmarknet import fetch_prices, STATE_MARKET_DATA
BASE_URL = "https://api.data.gov.in/resource/"
RESOURCE_ID = "9ef84268-d588-465a-a308-a864a43d0070"
API_KEY = "579b464db66ec23bdd0000015f64dcbd29ff41b540c4229cd8206fe6"

STATE_MARKET_DATA = {
    "Andhra Pradesh": {
        "Anantapur": ["Anantapur", "Anaparthy"],
        "East Godavari": ["Amalapuram(Mpl. Gate),RBZ", "Alamuru", "Ambajipeta"],
        "Kurnool": ["Adoni", "Adoni,RBZ", "A.A.Nagar,Kurnool,RBZ", "Alur"],
        "Prakasam": ["Addanki"],
        "Vijayanagaram": ["Amadalavalasa", "Amudalavalasa ,RBZ"],
        "Visakhapatnam": ["Akkaihpalem,RBZ,Visakhapatnam", "Anakapally"],
        "West Godavari": ["Achanta", "Akiveedu"]
    },
    "Assam": {
        "Barpeta": ["Barpeta Road"],
        "BONGAIGAON": ["Bongaigaon"],
        "Cachar": ["Cachar"],
        "Darrang": ["Besimari"],
        "Dhubri": ["Bilasipara"],
        "Goalpara": ["Balajan Tiniali"],
        "Kamrup": [
            "Alupatty Char", "Ambagan", "Anand Bazar", "Baginadi", "Balugaon",
            "Banglagarh", "Bardhumsa", "Bindukuri", "Bhaga", "Bohorihat", "Brahmaputra Private Market"
        ],
        "Kokrajhar": ["Boralimari"],
        "Lakhimpur": ["Burhagaon"]
    },
    "Haryana": {
        "Ambala": ["Ambala"],
        "Bhiwani": ["Bhiwani", "Loharu"],
        "Fatehabad": ["Fatehabad", "Ratia", "Tohana"],
        "Gurgaon": ["Gurgaon", "Sohna"],
        "Hissar": ["Hissar", "Barwala", "Adampur"],
        "Jhajjar": ["Jhajjar", "Bahadurgarh"],
        "Jind": ["Jind", "Narwana", "Uchana"],
        "Kaithal": ["Kaithal", "Cheeka", "Pundri"],
        "Karnal": ["Karnal", "Nilokheri", "Assandh", "Indri", "Gharaunda"],
        "Kurukshetra": ["Kurukshetra", "Ladwa", "Shahabad"],
        "Mahendragarh-Narnaul": ["Mahendragarh", "Narnaul", "Ateli"],
        "Palwal": ["Palwal", "Hodal"],
        "Panchkula": ["Panchkula"],
        "Panipat": ["Panipat", "Samalkha", "Israna"],
        "Rewari": ["Rewari", "Kosli", "Dharuhera"],
        "Rohtak": ["Rohtak", "Meham", "Kalanaur"],
        "Sirsa": ["Sirsa", "Ellenabad", "Rania", "Kalanwali"]
    },
    "Himachal Pradesh": {
        "Bilaspur": ["Bilaspur"],
        "Chamba": ["Chamba", "Banikhet", "Tissa"],
        "Hamirpur": ["Hamirpur"],
        "Kangra": ["Dharamshala", "Kangra", "Palampur", "Nagrota Bagwan", "Nurpur"],
        "Kinnaur": ["Kalpa"],
        "Kullu": ["Kullu"],
        "Mandi": ["Mandi", "Sundernagar", "Jogindernagar"],
        "Shimla": ["Shimla", "Rohru", "Rampur", "Theog"],
        "Sirmore": ["Nahan", "Paonta Sahib"],
        "Solan": ["Solan", "Nalagarh"],
        "Una": ["Una", "Gagret", "Amb"]
    },
    "Maharashtra": {
        "Ahmednagar": ["Ahmednagar", "Kopargaon", "Newasa", "Rahata", "Rahuri", "Sangamner", "Shevgaon", "Shrirampur"],
        "Akola": ["Akola", "Balapur", "Murtajapur", "Patur", "Telhara"],
        "Amravati": ["Amravati", "Achalpur", "Anjangaon Surji", "Chandur Bazar", "Warud"],
        "Beed": ["Ambajogai", "Beed", "Georai", "Kaij", "Parli", "Shirur Kasar"],
        "Bhandara": ["Bhandara", "Sakoli", "Tumsar"],
        "Buldhana": ["Buldhana", "Chikhli", "Deulgaon Raja", "Jalgaon Jamod", "Khamgaon", "Lonar", "Malkapur", "Motala", "Shegaon"],
        "Chandrapur": ["Ballarpur", "Chandrapur", "Mul", "Rajura", "Warora"],
        "Chhatrapati Sambhajinagar": ["Aurangabad", "Kannad", "Paithan", "Phulambri", "Sillod", "Vaijapur"],
        "Dharashiv (Osmanabad)": ["Kalamb", "Omerga", "Paranda", "Tuljapur", "Umarga", "Osmanabad"],
        "Dhule": ["Dhule", "Sakri", "Shirpur"],
        "Gondiya": ["Arjuni Morgaon", "Gondia", "Tirora"],
        "Hingoli": ["Hingoli", "Sengaon"],
        "Jalgaon": ["Bhusawal", "Chopda", "Erandol", "Jalgaon", "Yawal"],
        "Jalna": ["Ambad", "Badnapur", "Jalna", "Mantha", "Partur"],
        "Kolhapur": ["Ajara", "Gadhinglaj", "Ichalkaranji", "Karveer", "Kolhapur", "Panhala", "Shahuwadi"],
        "Latur": ["Ausa", "Latur", "Nilanga", "Renapur", "Udgir"],
        "Nanded": ["Deglur", "Hadgaon", "Kandhar", "Kinwat", "Mukhed", "Nanded"],
        "Nandurbar": ["Nandurbar", "Shahada", "Taloda"],
        "Nagpur": ["Bhiwapur", "Kalameshwar", "Katol", "Nagpur", "Narkhed", "Ramtek", "Saoner", "Umred"],
        "Nashik": ["Dindori", "Igatpuri", "Malegaon", "Manmad", "Nashik", "Satana", "Sinnar", "Yeola"],
        "Parbhani": ["Gangakhed", "Jintur", "Manwat", "Parbhani", "Pathri", "Sonpeth"],
        "Pune": ["Baramati", "Daund", "Indapur", "Junnar", "Pune", "Shirur"],
        "Raigad": ["Alibag", "Karjat", "Mahad", "Panvel", "Pen", "Roha"],
        "Ratnagiri": ["Chiplun", "Devrukh", "Khed", "Mandangad", "Ratnagiri"],
        "Sangli": ["Ashta", "Islampur", "Jat", "Kadegaon", "Kavathe Mahankal", "Miraj", "Sangli", "Tasgaon", "Walwa"],
        "Satara": ["Karad", "Phaltan", "Satara", "Wai"],
        "Solapur": ["Akkalkot", "Barshi", "Karmala", "Mohol", "Pandharpur", "Sangola", "Solapur"],
        "Thane": ["Bhiwandi", "Kalyan", "Murbad", "Shahapur", "Thane", "Vasai"],
        "Wardha": ["Arvi", "Deoli", "Hinganghat", "Wardha"],
        "Washim": ["Karanja", "Malegaon", "Mangrulpir", "Risod", "Washim"],
        "Yavatmal": ["Darwha", "Digras", "Ghatanji", "Kelapur", "Pusad", "Umarkhed", "Wani", "Yavatmal"]
    }
}
app = FastAPI()

# Allow CORS for local frontend dev

class PriceRequest(BaseModel):
    state: str
    district: str
    market: str

@app.post("/api/tomato-prices")
def tomato_prices(req: PriceRequest):
    params = {
        "api-key": API_KEY,
        "format": "json",
        "filters[state]": req.state.strip(),
        "filters[district]": req.district.strip(),
        "filters[market]": req.market.strip(),
        "filters[commodity]": "Tomato",
        "limit": 10,
        "sort": "arrival_date:desc"
    }
    try:
        response = requests.get(BASE_URL + RESOURCE_ID, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        records = data.get("records", [])
        # Only return relevant fields
        return {"records": [
            {
                "date": r.get("arrival_date", "N/A"),
                "variety": r.get("variety", "N/A"),
                "min_price": r.get("min_price", "N/A"),
                "max_price": r.get("max_price", "N/A"),
                "modal_price": r.get("modal_price", "N/A"),
            }
            for r in records
        ]}
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/markets")
def get_markets():
    # Return all states, districts, and markets for dropdowns
    # Change this import:
    from Agmarknet import STATE_MARKET_DATA
    return STATE_MARKET_DATA