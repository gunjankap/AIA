# schemes.py

SCHEMES = {
    "Startup India": {
        "source": "startupindia.gov.in",
        "personas": ["student", "early", "msme"],
        "purpose": "Recognition, tax benefits, startup ecosystem access",

        # 👇 STEP-2: required attributes
        "required_attributes": {
            "registered": {
                "question": "Is your startup registered?",
                "type": "boolean",
                "why": "Startup India requires a registered entity"
            },
            "entity_type": {
                "question": "What is your entity type?",
                "type": "select",
                "options": ["Private Limited", "LLP", "Partnership", "Proprietorship"],
                "why": "Only certain entity types are eligible"
            },
            "startup_age_years": {
                "question": "How many years old is your startup?",
                "type": "number",
                "why": "Startup must be ≤ 10 years old"
            },
            "turnover": {
                "question": "What is your annual turnover (₹ in Cr)?",
                "type": "number",
                "why": "Turnover must be ≤ ₹100 Cr"
            },
            "sector": {
                "question": "Which sector best describes your startup?",
                "type": "text",
                "why": "Innovation-driven requirement"
            }
        },

        # 👇 Eligibility rules
        "rules": [
            lambda u: u["registered"] is True or "Startup must be registered",
            lambda u: u["entity_type"] in ["Private Limited", "LLP", "Partnership"]
                      or "Entity type not eligible",
            lambda u: u["startup_age_years"] <= 10 or "Startup older than 10 years",
            lambda u: u["turnover"] <= 100 or "Turnover exceeds ₹100 Cr"
        ]
    },

    "IIM Incubation": {
        "source": "IIM incubation centre guidelines",
        "personas": ["student", "early"],
        "purpose": "Incubation, mentorship, seed funding",

        "required_attributes": {
            "is_student": {
                "question": "Are you currently a student or recent alumnus?",
                "type": "boolean",
                "why": "IIM incubation prioritizes students/alumni"
            },
            "startup_stage": {
                "question": "What stage is your startup at?",
                "type": "select",
                "options": ["Idea", "Prototype", "Pilot"],
                "why": "Incubation is meant for early-stage ideas"
            },
            "sector": {
                "question": "Startup sector / problem area?",
                "type": "text",
                "why": "Innovation potential assessment"
            },
            "team_size": {
                "question": "How many people are in your team?",
                "type": "number",
                "why": "Team commitment check"
            }
        },

        "rules": [
            lambda u: u["is_student"] is True or "Founder must be a student/alumnus",
            lambda u: u["startup_stage"] in ["Idea", "Prototype", "Pilot"]
                      or "Startup stage not suitable"
        ]
    },

    "PMEGP": {
        "source": "msme.gov.in",
        "personas": ["early", "msme"],
        "purpose": "Self-employment & MSME credit-linked subsidy",

        "required_attributes": {
            "age": {
                "question": "What is your age?",
                "type": "number",
                "why": "Applicant must be 18+"
            },
            "turnover": {
                "question": "Annual turnover (₹ in Lakhs)?",
                "type": "number",
                "why": "MSME classification"
            },
            "project_cost": {
                "question": "Planned project investment (₹ in Lakhs)?",
                "type": "number",
                "why": "Subsidy calculation"
            },
            "prior_pmegp": {
                "question": "Have you availed PMEGP earlier?",
                "type": "boolean",
                "why": "Previous beneficiaries are not eligible"
            },
            "location": {
                "question": "Is your business in Urban or Rural area?",
                "type": "select",
                "options": ["Urban", "Rural"],
                "why": "Subsidy slab depends on location"
            }
        },

        "rules": [
            lambda u: u["age"] >= 18 or "Applicant must be at least 18",
            lambda u: u["turnover"] <= 50 or "Not a micro/small enterprise",
            lambda u: u["prior_pmegp"] is False or "Already availed PMEGP"
        ]
    },

    "SIDBI Support": {
        "source": "sidbi.in",
        "personas": ["early", "msme"],
        "purpose": "Credit, growth capital, MSME financing",

        "required_attributes": {
            "registered": {
                "question": "Is your business registered?",
                "type": "boolean",
                "why": "SIDBI supports registered businesses"
            },
            "years_operation": {
                "question": "How many years have you been operating?",
                "type": "number",
                "why": "Operating history assessment"
            },
            "turnover": {
                "question": "Annual turnover (₹ in Lakhs)?",
                "type": "number",
                "why": "Creditworthiness check"
            },
            "loan_default": {
                "question": "Any prior loan default?",
                "type": "boolean",
                "why": "Risk screening"
            }
        },

        "rules": [
            lambda u: u["registered"] is True or "Business must be registered",
            lambda u: u["loan_default"] is False or "Prior loan default detected"
        ]
    }
}
