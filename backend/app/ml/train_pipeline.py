import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, classification_report
from app.ml.dataset_generator import generate_synthetic_student_dataset, SKILL_COLUMNS

def train_and_evaluate_model(save_path: str = None) -> dict:
    """Trains and serializes the AI/ML career role classification model."""
    print("Generating student skill dataset for ML training...")
    df = generate_synthetic_student_dataset(n_samples=6000, random_state=42)

    feature_cols = SKILL_COLUMNS + ["cgpa", "project_count", "certification_count"]
    X = df[feature_cols]
    y_raw = df["target_career"]

    le = LabelEncoder()
    y = le.fit_transform(y_raw)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(f"Training set: {len(X_train)} samples, Test set: {len(X_test)} samples.")
    print("Training Random Forest Classifier...")

    model = RandomForestClassifier(
        n_estimators=120,
        max_depth=16,
        min_samples_split=4,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)

    # Evaluation
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted")
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(y_test, y_pred, average="macro")

    metrics = {
        "accuracy": round(float(acc), 4),
        "weighted_f1": round(float(f1), 4),
        "weighted_precision": round(float(precision), 4),
        "weighted_recall": round(float(recall), 4),
        "macro_f1": round(float(macro_f1), 4),
        "test_samples": len(y_test),
        "train_samples": len(y_train)
    }

    print(f"Model Evaluation Results:")
    print(f" - Accuracy: {metrics['accuracy'] * 100:.2f}%")
    print(f" - Weighted F1: {metrics['weighted_f1'] * 100:.2f}%")
    print(f" - Macro F1: {metrics['macro_f1'] * 100:.2f}%")

    artifact = {
        "model": model,
        "label_encoder": le,
        "feature_names": feature_cols,
        "metrics": metrics,
        "classes": list(le.classes_)
    }

    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        joblib.dump(artifact, save_path)
        print(f"Serialized model artifact successfully saved to: {save_path}")

    return artifact

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    model_dir = os.path.join(current_dir, "models")
    target_path = os.path.join(model_dir, "career_classifier.joblib")
    train_and_evaluate_model(target_path)
