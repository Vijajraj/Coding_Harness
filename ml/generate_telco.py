import pandas as pd
import numpy as np

np.random.seed(42)

n = 1000
tenure = np.random.randint(0, 73, size=n)
monthly = np.round(np.random.normal(70, 30, size=n).clip(18, 150), 2)
contract = np.random.choice(['Month-to-month', 'One year', 'Two year'], size=n, p=[0.6, 0.25, 0.15])
internet = np.random.choice(['DSL', 'Fiber optic', 'No'], size=n, p=[0.4, 0.4, 0.2])

# synthetic churn probability
logit = -1.5 + 0.02 * (monthly - 70) - 0.03 * tenure + np.where(contract == 'Month-to-month', 0.6, -0.3) + np.where(internet == 'Fiber optic', 0.4, 0.0)
prob = 1 / (1 + np.exp(-logit))
churn = np.where(np.random.rand(n) < prob, 'Yes', 'No')

# build df
df = pd.DataFrame({
    'tenure': tenure,
    'MonthlyCharges': monthly,
    'Contract': contract,
    'InternetService': internet,
    'Churn': churn
})

out = r'c:/Users/vraj1/OneDrive/Documents/vs code/telco_churn.csv'
df.to_csv(out, index=False)
print('CSV_CREATED', out, df.shape)
print(df.head().to_string(index=False))