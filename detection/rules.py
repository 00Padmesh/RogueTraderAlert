import pandas as pd

def detect_anomalies(df):
    all_profiles = []
    
    for trader in df["trader"].unique():
        trader_df = df[df["trader"] == trader].copy()
        
        # Calculate baselines from first 50 days
        baseline = trader_df[trader_df["day"] <= 50]
        recent = trader_df[trader_df["day"] > 50]
        
        if recent.empty:
            continue
        
        avg_position = baseline["position_size"].mean()
        avg_pnl = baseline["daily_pnl"].mean()
        
        reasons = []
        risk_score = 0
        
        # Rule 1: Position size spike
        recent_avg_position = recent["position_size"].mean()
        position_ratio = recent_avg_position / avg_position
        if position_ratio > 3:
            reasons.append(f"Position size is {position_ratio:.1f}x their 50-day average")
            risk_score += 40
        
        # Rule 2: Consecutive loss days
        consecutive_losses = (recent["daily_pnl"] < 0).sum()
        if consecutive_losses >= 5:
            reasons.append(f"{consecutive_losses} loss days out of last 10")
            risk_score += 30
        
        # Rule 3: Hidden losses detected
        total_hidden = recent["hidden_loss"].sum()
        if total_hidden > 0:
            reasons.append(f"${total_hidden:,.0f} in potential hidden losses detected")
            risk_score += 30
        
        # Rule 4: PnL deterioration
        recent_avg_pnl = recent["daily_pnl"].mean()
        if avg_pnl > 0 and recent_avg_pnl < 0:
            reasons.append("Strategy has completely reversed from profitable to loss-making")
            risk_score += 20
        
        # We save EVERY trader now, not just the flagged ones
        all_profiles.append({
            "trader": trader,
            "risk_score": min(risk_score, 100),
            "reasons": reasons if reasons else ["Normal trading activity. No anomalies detected."],
            "avg_position_baseline": round(avg_position, 2),
            "avg_position_recent": round(recent_avg_position, 2),
            "total_hidden_loss": round(total_hidden, 2)
        })
    
    return sorted(all_profiles, key=lambda x: x["risk_score"], reverse=True)