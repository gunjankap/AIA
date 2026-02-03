import requests

# API endpoint and key
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

def check_available_commodities(state, district, market):
    """Check what commodities are available for a given market"""
    params = {
        "api-key": API_KEY,
        "format": "json",
        "filters[state]": state,
        "filters[district]": district,
        "filters[market]": market,
        "limit": 1
    }

    try:
        response = requests.get(BASE_URL + RESOURCE_ID, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        
        if 'records' in data and len(data['records']) > 0:
            commodities = {rec['commodity'] for rec in data['records']}
            return sorted(commodities)
        return []
    except requests.exceptions.RequestException:
        return None

def fetch_prices(state, district, market, commodity="Tomato"):
    """Fetch prices for a specific commodity"""
    params = {
        "api-key": API_KEY,
        "format": "json",
        "filters[state]": state.strip(),
        "filters[district]": district.strip(),
        "filters[market]": market.strip(),
        "filters[commodity]": commodity.strip(),
        "limit": 10,
        "sort": "arrival_date:desc"
    }

    try:
        print(f"\nFetching data for {market}, {district}, {state}...")
        response = requests.get(BASE_URL + RESOURCE_ID, params=params, timeout=30)
        response.raise_for_status()
        data = response.json()
        records = data.get("records", [])

        if not records:
            available = check_available_commodities(state, district, market)
            if available is None:
                print("\n🚨 Error connecting to API. Please try again later.")
            elif available:
                print(f"\nℹ️ No data for Tomato, but this market has: {', '.join(available)}")
            else:
                print("\nℹ️ No data available for any commodity in this market.")
            return False

        print(f"\n✅ Latest {commodity} Prices in {market}, {district}, {state}:")
        print("-" * 70)
        print("{:<15} {:<20} {:<10} {:<10} {:<10}".format(
            "Date", "Variety", "Min Price", "Max Price", "Modal Price"))
        print("-" * 70)

        for record in records:
            print("{:<15} {:<20} {:<10} {:<10} {:<10}".format(
                record.get('arrival_date', 'N/A'),
                record.get('variety', 'N/A'),
                record.get('min_price', 'N/A'),
                record.get('max_price', 'N/A'),
                record.get('modal_price', 'N/A')))
        return True

    except requests.exceptions.RequestException as e:
        print(f"\n🚨 Error fetching data: {str(e)}")
        return False

def get_user_choice(options, prompt, allow_new_input=False):
    """Get user choice with improved validation and searching"""
    while True:
        print("\nAvailable options:")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        
        if allow_new_input:
            print(f"{len(options)+1}. Enter different value")
        
        choice = input(f"\n{prompt} (enter number or name): ").strip()
        
        if choice.isdigit():
            choice_num = int(choice)
            if allow_new_input and choice_num == len(options)+1:
                return None
            if 1 <= choice_num <= len(options):
                return options[choice_num - 1]
            print(f"❌ Please enter a number between 1 and {len(options)}")
        else:
            matched = [opt for opt in options if choice.lower() in opt.lower()]
            if len(matched) == 1:
                return matched[0]
            elif len(matched) > 1:
                print(f"❌ Multiple matches: {', '.join(matched)}")
            elif allow_new_input:
                return choice
            else:
                print("❌ No match found. Please try again.")

def main():
    print("📊 Agricultural Market Price Fetcher - Agmarknet API")
    
    while True:
        # Select state
        states = list(STATE_MARKET_DATA.keys())
        selected_state = get_user_choice(states, "Select a state")
        if not selected_state:
            continue
        
        # Select district
        districts = list(STATE_MARKET_DATA[selected_state].keys())
        selected_district = get_user_choice(districts, f"Select district in {selected_state}")
        if not selected_district:
            continue
        
        # Select market
        markets = STATE_MARKET_DATA[selected_state][selected_district]
        selected_market = get_user_choice(markets, f"Select market in {selected_district}", allow_new_input=True)
        if not selected_market:
            continue
        
        # Try fetching tomato prices
        success = fetch_prices(selected_state, selected_district, selected_market)
        
        if not success:
            # If no tomato data, show other available commodities
            available = check_available_commodities(selected_state, selected_district, selected_market)
            if available:
                print("\nWould you like to try another commodity?")
                commodity = get_user_choice(available, "Select commodity", allow_new_input=True)
                if commodity:
                    fetch_prices(selected_state, selected_district, selected_market, commodity)
        
        # Ask to continue
        if input("\nCheck another market? (y/n): ").lower() != 'y':
            break

if __name__ == "__main__":
    main()