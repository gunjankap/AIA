# logic.py

def evaluate_scheme(scheme, user):
    failed_reasons = []

    for rule in scheme["rules"]:
        result = rule(user)
        if result is not True:
            failed_reasons.append(result)

    if failed_reasons:
        return "Not Eligible", failed_reasons

    return "Eligible", []
