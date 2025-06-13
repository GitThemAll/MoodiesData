from multiprocessing import process
import os
import threading
from datetime import date
from flask import Flask, Blueprint, jsonify
from flask_cors import CORS
import pandas as pd

from application.services.clv_service import ClvService

app = Flask(__name__)
CORS(app)
clv_bp = Blueprint('clv', __name__)
service = ClvService()

# Keep track of which model-targets are currently being trained
PROCESSED_DATA_PATH = os.path.join("resources", "data", "processed", "clv")
NEXT_THREE_MONTHS_PREDICTIONS_FILE = os.path.join(PROCESSED_DATA_PATH, "next_3_months_spend.csv")
NEXT_MONTH_PREDICTIONS_FILE = os.path.join(PROCESSED_DATA_PATH, "next_1_months_spend.csv")
training_tasks = set()
training_lock = threading.Lock()

def train_two_stage_model(cutoff_date, model_target_variable, target_amount_of_months):
    train_df = service.run_data_pipeline(
        from_api=False,
        mode="train",
        cutoff_date=cutoff_date,
        model_target_variable=model_target_variable,
        target_amount_of_months=target_amount_of_months,
    )
    service.create_models(train_df, model_target_variable=model_target_variable)

    inference_df = service.run_data_pipeline(
        from_api=False,
        mode="inference",
        cutoff_date=cutoff_date,
        model_target_variable=model_target_variable,
        target_amount_of_months=target_amount_of_months,
    )
    next_month_predictions = service.predict(inference_df)
    pd.DataFrame(
        next_month_predictions.round(2),
        columns=["Email", model_target_variable]
    ).to_csv(os.path.join(PROCESSED_DATA_PATH, f"{model_target_variable}.csv"), index=False)

def kick_off_training_for(model_target_variable: str):
    """
    Spawn a thread to train just the specified model.
    """
    with training_lock:
        if model_target_variable in training_tasks:
            return  # already running
        training_tasks.add(model_target_variable)

    def _train_and_cleanup():
        try:
            if model_target_variable == "next_3_months_spend":
                train_two_stage_model(cutoff_date=date(2025, 1, 1),
                                      model_target_variable=model_target_variable,
                                      target_amount_of_months=3)
            else:  # next_1_months_spend
                train_two_stage_model(cutoff_date=date(2025, 3, 1),
                                      model_target_variable=model_target_variable,
                                      target_amount_of_months=1)
        finally:
            with training_lock:
                training_tasks.discard(model_target_variable)

    thread = threading.Thread(target=_train_and_cleanup, daemon=True)
    thread.start()

@clv_bp.route('/predictions/next-three-months', methods=['GET'])
def get_three_month_predictions():

    if not os.path.isfile(NEXT_THREE_MONTHS_PREDICTIONS_FILE):
        kick_off_training_for("next_3_months_spend")
        return (
            jsonify({
                "status": "pending",
                "message": "Predictions are being generated. Please check back in a few minutes."
            }),
            202
        )

    df = pd.read_csv(NEXT_THREE_MONTHS_PREDICTIONS_FILE)
    return jsonify(df.to_dict(orient='records'))

@clv_bp.route('/predictions/next-month', methods=['GET'])
def get_next_month_prediction():
    if not os.path.isfile(NEXT_MONTH_PREDICTIONS_FILE):
        kick_off_training_for("next_1_months_spend")
        return (
            jsonify({
                "status": "pending",
                "message": "Predictions are being generated. Please check back in a few minutes."
            }),
            202
        )

    df = pd.read_csv(NEXT_MONTH_PREDICTIONS_FILE)
    return jsonify(df.to_dict(orient='records'))

@clv_bp.route('/predictions/', methods=['GET'])
def get_clv_prediction_next_1_and_3_months():
    # If either file is missing, tell the client to retry later.
    missing = [
        name for name in (NEXT_MONTH_PREDICTIONS_FILE, NEXT_THREE_MONTHS_PREDICTIONS_FILE)
        if not os.path.isfile(name)
    ]
    if missing:
        # kick off whatever's missing
        for var, fn in [("next_1_months_spend", NEXT_MONTH_PREDICTIONS_FILE),
                        ("next_3_months_spend", NEXT_THREE_MONTHS_PREDICTIONS_FILE)]:
            if fn in missing:
                kick_off_training_for(var)
        return (
            jsonify({
                "status": "pending",
                "message": "Some predictions are still being generated. Please try again in a few minutes."
            }),
            202
        )

    # both files exist: merge and return
    df1 = pd.read_csv(NEXT_MONTH_PREDICTIONS_FILE)
    df3 = pd.read_csv(NEXT_THREE_MONTHS_PREDICTIONS_FILE)
    combined = df1.merge(df3, on='Email')
    return jsonify(combined.to_dict(orient='records'))

@clv_bp.route('/lifetime', methods=['GET'])
def get_lifetime_clv():
    df_lifetime_clv = service.get_lifetime_clv()
    return jsonify(df_lifetime_clv.to_dict(orient='records'))

@clv_bp.route('/lifetime_clv_distribution', methods=['GET'])
def get_lifetime_clv_distribution():
    df_lifetime_clv = service.get_lifetime_clv()
    # Create bins for CLV ranges
    bins = [0, 50, 100, 200, 300, 400, 500, float('inf')]
    labels = ['0-50', '50-100', '100-200', '200-300', '300-400', '400-500', '500+']
    
    # Add a new column with the binned values
    df_lifetime_clv['CLV_Range'] = pd.cut(df_lifetime_clv['Lifetime CLV'], bins=bins, labels=labels)
    
    # Count customers in each bin
    distribution = df_lifetime_clv['CLV_Range'].value_counts().sort_index()
    
    # Convert to dictionary format for JSON response
    result = {
        'distribution': {
            range_name: int(count) for range_name, count in distribution.items()
        }
    }
    
    return jsonify(result)