from groq import Groq

client = Groq(api_key="API KEY HERE")

def explain_alert(alert):
    reasons_text = "\n".join([f"- {r}" for r in alert["reasons"]])
    
    prompt = f"""You are a senior risk analyst at an investment bank.

A trader named {alert["trader"]} has been flagged by our surveillance system with a risk score of {alert["risk_score"]}/100.

The following anomalies were detected:
{reasons_text}

Write a concise 3-4 sentence risk report explaining:
1. What behaviour was detected
2. Why it is concerning
3. What action should be taken

Be professional, direct, and specific. Do not use bullet points."""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    from detection.rules import detect_anomalies
    from data.simulator import simulate_traders
    
    df, _ = simulate_traders()
    alerts = detect_anomalies(df)
    
    print(explain_alert(alerts[0]))