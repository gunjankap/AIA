# schemes.py

SCHEMES = {
    "Startup India": {
        "source": "startupindia.gov.in",
        "personas": ["student", "early", "msme"],

        "required_attributes": [
            "registered",
            "entity_type",
            "startup_age_years",
            "turnover"
        ],

        "rules": [
            {
                "attribute": "registered",
                "condition": True,
                "message": "Startup must be registered"
            },
            {
                "attribute": "entity_type",
                "condition": ["Private Limited", "LLP", "Partnership"],
                "message": "Entity type not eligible"
            },
            {
                "attribute": "startup_age_years",
                "condition": lambda x: x <= 10,
                "message": "Startup older than 10 years"
            },
            {
                "attribute": "turnover",
                "condition": lambda x: x <= 100,
                "message": "Turnover exceeds ₹100 Cr"
            }
        ],

        "documents": [
            "Certificate of Incorporation",
            "PAN",
            "DPIIT Recognition Application"
        ],

        "apply_via": "Startup India Portal"
    }
}
