
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier

MODEL_LOG = "logistic_model.pkl"
MODEL_XGB = "xgb_model.pkl"

def train_models():
    # Synthetic training data (replace with historical labeled dataset)
    X = np.random.rand(500, 1)
    y = (X[:,0] > 0.5).astype(int)

    log_model = LogisticRegression()
    log_model.fit(X, y)
    joblib.dump(log_model, MODEL_LOG)

    xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
    xgb_model.fit(X, y)
    joblib.dump(xgb_model, MODEL_XGB)

def predict_probability(score):
    try:
        log_model = joblib.load(MODEL_LOG)
        xgb_model = joblib.load(MODEL_XGB)
        X = np.array([[score/10]])
        prob_log = log_model.predict_proba(X)[0][1]
        prob_xgb = xgb_model.predict_proba(X)[0][1]
        return round((prob_log + prob_xgb)/2, 3)
    except:
        return 0.5
