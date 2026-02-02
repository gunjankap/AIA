SCHEMES = {
    "Startup India": {
        "source": "startupindia.gov.in",
        "purpose": "Recognition, tax benefits, ecosystem access",
        "personas": ["student", "early", "msme"],

        "required_attributes": {
            "registered": {
                "question": "Is your startup registered?",
                "type": "boolean",
                "why": "Startup India requires a registered entity"
            },
            "entity_type": {
                "question": "Entity type",
                "type": "select",
                "options": ["Private Limited", "LLP", "Partnership", "Proprietorship"],
                "why": "Only certain entity types are eligible"
            },
            "startup_age": {
                "question": "Startup age (years)",
                "type": "number",
                "why": "Startup must be ≤ 10 years old"
            },
            "turnover": {
                "question": "Annual turnover (₹ Cr)",
                "type": "number",
                "why": "Turnover must be ≤ ₹100 Cr"
            },
            "sector": {
                "question": "Startup sector / idea",
                "type": "text",
                "why": "Innovation-driven requirement"
            }
        },

        "rules": [
            lambda u: u["registered"] or "Startup must be registered",
            lambda u: u["entity_type"] in ["Private Limited", "LLP", "Partnership"]
                      or "Entity type not eligible",
            lambda u: u["startup_age"] <= 10 or "Startup older than 10 years",
            lambda u: u["turnover"] <= 100 or "Turnover exceeds ₹100 Cr"
        ]
    },

    "IIM Incubation": {
        "source": "IIM Incubation Centres",
        "purpose": "Incubation, mentorship, seed funding",
        "personas": ["student", "early"],

        "required_attributes": {
            "is_student": {
                "question": "Are you a current student or recent alumnus?",
                "type": "boolean",
                "why": "Primary eligibility requirement"
            },
            "startup_stage": {
                "question": "Startup stage",
                "type": "select",
                "options": ["Idea", "Prototype", "Pilot"],
                "why": "Incubation focuses on early stage"
            },
            "team_size": {
                "question": "Team size",
                "type": "number",
                "why": "Team commitment assessment"
            }
        },

        "rules": [
            lambda u: u["is_student"] or "Founder must be a student/alumnus"
        ]
    }
}
