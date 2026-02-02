def evaluate_scheme(scheme, user):
    reasons = []

    for rule in scheme["rules"]:
        key, condition, message = rule
        value = user.get(key)

        if callable(condition):
            if value is None or not condition(value):
                reasons.append(message)
        else:
            if value != condition and not (isinstance(condition, list) and value in condition):
                reasons.append(message)

    if not reasons:
        return "Eligible", None
    elif len(reasons) < 2:
        return "Conditionally Eligible", reasons
    else:
        return "Not Eligible", reasons
