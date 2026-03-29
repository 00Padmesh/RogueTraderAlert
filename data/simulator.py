import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

def simulate_traders(n_traders=10, n_days=60, seed=42):
    np.random.seed(seed)
    traders = [fake.first_name() for _ in range(n_traders)]
    
    records = []
    for trader in traders:
        base_position = np.random.uniform(10000, 50000)
        base_pnl = np.random.uniform(-2000, 3000)
        
        for day in range(n_days):
            # Normal behaviour
            position = base_position * np.random.uniform(0.8, 1.2)
            pnl = base_pnl * np.random.uniform(0.5, 1.5)
            hidden_loss = 0
            
            # Inject rogue behaviour in last 10 days for 2 traders
            if trader in traders[:2] and day >= 50:
                position = base_position * np.random.uniform(7, 10)  # unusually large
                pnl = abs(base_pnl) * np.random.uniform(-5, -2)      # consistent losses
                hidden_loss = abs(pnl) * np.random.uniform(0.3, 0.7) # hiding losses
            
            records.append({
                "trader": trader,
                "day": day + 1,
                "position_size": round(position, 2),
                "daily_pnl": round(pnl, 2),
                "hidden_loss": round(hidden_loss, 2),
                "cumulative_pnl": 0  # will calculate after
            })
    
    df = pd.DataFrame(records)
    
    # Calculate cumulative PnL per trader
    df["cumulative_pnl"] = df.groupby("trader")["daily_pnl"].cumsum().round(2)
    
    return df, traders

if __name__ == "__main__":
    df, traders = simulate_traders()
    print(df.head(20))
    print(f"\nTraders: {traders}")