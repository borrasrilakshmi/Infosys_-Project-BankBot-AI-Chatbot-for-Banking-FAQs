def predict_intent(text):
    text = text.lower()
    if "transfer" in text:
        return "transfer"
    if "balance" in text:
        return "balance"
    if "create" in text:
        return "create_account"
    return "unknown"
