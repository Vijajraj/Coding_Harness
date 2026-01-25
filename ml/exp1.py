import os
import sys
import pickle
import pandas as pd
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.utils import concordance_index
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer


def load_and_clean(path: str):
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found: {path}")
    df = pd.read_csv(path)
    if 'Churn' not in df.columns or 'tenure' not in df.columns:
        raise ValueError("Input CSV must contain 'Churn' and 'tenure' columns")
    df = df.dropna(subset=['Churn', 'tenure'])
    df['Churn'] = df['Churn'].map({'Yes': 1, 'No': 0})
    return df


def build_preprocessor():
    # Use backward-compatible OneHotEncoder args
    return ColumnTransformer([
        ('num', StandardScaler(), ['MonthlyCharges']),
        ('cat', OneHotEncoder(drop='first', sparse=False, handle_unknown='ignore'), ['Contract', 'InternetService'])
    ])


def get_feature_names(preprocessor, num_cols=['MonthlyCharges'], cat_cols=['Contract', 'InternetService']):
    try:
        return list(preprocessor.get_feature_names_out())
    except Exception:
        # Fallback for older sklearn: build names manually
        cat = preprocessor.named_transformers_['cat']
        cat_names = []
        for col, cats in zip(cat_cols, cat.categories_):
            start = 1 if getattr(cat, 'drop', None) == 'first' else 0
            for val in cats[start:]:
                cat_names.append(f"{col}_{val}")
        return num_cols + cat_names


def prepare_dataframe(X, feature_names, meta_df):
    df = pd.DataFrame(X, columns=feature_names, index=meta_df.index)
    df[['tenure', 'Churn']] = meta_df[['tenure', 'Churn']]
    # sanitize names
    df.columns = [c.replace(' ', '_').replace('-', '_') for c in df.columns]
    df = df.dropna()
    return df


def main(csv_path='telco_churn.csv'):
    df = load_and_clean(csv_path)

    features = ['MonthlyCharges', 'Contract', 'InternetService']
    train, test = train_test_split(df[features + ['tenure', 'Churn']], test_size=0.2, random_state=42)

    preprocessor = build_preprocessor()
    X_train = preprocessor.fit_transform(train.drop(columns=['tenure', 'Churn']))
    feature_names = get_feature_names(preprocessor)
    train_data = prepare_dataframe(X_train, feature_names, train)

    # Fit Kaplan-Meier (training)
    kmf = KaplanMeierFitter()
    kmf.fit(train_data['tenure'], train_data['Churn'], label='KM (train)')
    ax = kmf.plot_survival_function()

    # Fit Cox Proportional Hazards
    cph = CoxPHFitter()
    cph.fit(train_data, duration_col='tenure', event_col='Churn')

    print(f"\nTraining concordance index: {cph.concordance_index_:.3f}")

    # Interpret feature effects
    hr = cph.summary[['exp(coef)', 'p']].sort_values('exp(coef)', ascending=False)
    print('\nHazard ratios (exp(coef)) and p-values:')
    print(hr.to_string())

    # Prepare test set and evaluate
    X_test = preprocessor.transform(test.drop(columns=['tenure', 'Churn']))
    test_feature_names = feature_names
    test_data = prepare_dataframe(X_test, test_feature_names, test)

    # Ensure column alignment
    common_cols = [c for c in train_data.columns if c in test_data.columns]
    if 'tenure' not in common_cols or 'Churn' not in common_cols:
        raise RuntimeError('Required columns missing after preprocessing')

    # Predict partial hazard and compute c-index on test
    partial_haz = cph.predict_partial_hazard(test_data[common_cols].drop(columns=['tenure', 'Churn']))
    test_c = concordance_index(test_data['tenure'], -partial_haz, event_observed=test_data['Churn'])
    print(f"Test concordance index: {test_c:.3f}")

    # Plot survival (training KM)
    ax.set_title('Kaplan-Meier Survival Curve (Train)')
    # Save plot to file for non-interactive runs
    ax.figure.savefig('km_train.png')
    print("\nSaved KM plot to km_train.png")
    plt.tight_layout()
    plt.show()

    # Save model and preprocessor for later use
    with open('cph_model.pkl', 'wb') as f:
        pickle.dump({'cph': cph, 'preprocessor': preprocessor, 'feature_names': feature_names}, f)
    print('\nModel and preprocessor saved to cph_model.pkl')


if __name__ == '__main__':
    csv_path = sys.argv[1] if len(sys.argv) > 1 else 'telco_churn.csv'
    main(csv_path)
