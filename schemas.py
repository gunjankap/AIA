SCHEMES = {
    "Startup India": {
        "personas": ["student", "early", "msme"],
        "rules": [
            ("registered", True, "Startup must be registered"),
            ("entity_type", ["Private Limited", "LLP", "Partnership"], "Invalid entity type"),
            ("startup_age_years", lambda x: x <= 10, "Startup older than 10 years"),
            ("turnover", lambda x: x <= 100, "Turnover exceeds ₹100 Cr")
        ],
        "documents": [
            "Certificate of Incorporation",
            "PAN",
            "DPIIT Application"
        ]
    },

    "IIM Incubation": {
        "personas": ["student", "early"],
        "rules": [
            ("is_student", True, "Founder must be a student or alumnus"),
            ("startup_stage", ["Idea", "Prototype", "Pilot"], "Not suitable stage")
        ],
        "documents": [
            "Pitch Deck",
            "Problem Statement",
            "Student ID / Alumni Proof"
        ]
    },

    "PMEGP": {
        "personas": ["early", "msme"],
        "rules": [
            ("age", lambda x: x >= 18, "Applicant must be 18+"),
            ("turnover", lambda x: x <= 50, "Not a micro enterprise"),
            ("prior_subsidy", False, "Already availed subsidy")
        ],
        "documents": [
            "Aadhaar",
            "Project Report",
            "Bank Details"
        ]
    },

    "SIDBI Support": {
        "personas": ["early", "msme"],
        "rules": [
            ("registered", True, "Business must be registered"),
            ("turnover", lambda x: x > 0, "Revenue required"),
        ],
        "documents": [
            "Financial Statements",
            "GST Returns",
            "Bank Statements"
        ]
    }
}
