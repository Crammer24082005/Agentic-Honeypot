from persona_agent import generate_reply
from extractor import extract_info

def run_honeypot(initial_message, scammer_api):
    history = [{"role": "user", "content": initial_message}]
    extracted = {
        "upi_ids": [],
        "bank_accounts": [],
        "ifsc_codes": [],
        "phishing_links": []
    }

    rounds = 0
    MAX_ROUNDS = 12  # longer conversation

    while rounds < MAX_ROUNDS:
        reply = generate_reply(history)
        history.append({"role": "assistant", "content": reply})

        scammer_reply = scammer_api(reply)
        history.append({"role": "user", "content": scammer_reply})

        info = extract_info(scammer_reply)
        for k in extracted:
            extracted[k].extend(info[k])

        # Only stop if we already extracted good info AND had enough chat
        if (extracted["upi_ids"] or extracted["bank_accounts"]) and rounds > 6:
            break

        rounds += 1

    for k in extracted:
        extracted[k] = list(set(extracted[k]))

    return {
        "conversation_log": history,
        "extracted_data": extracted
    }
