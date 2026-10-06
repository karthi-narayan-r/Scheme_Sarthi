"""
Scheme Sarthi - Random Forest Machine Learning Engine (12-Factor Vector)
Encodes 12 citizen factors into scikit-learn RandomForestClassifier ensemble model.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score
from schemes_data import SCHEMES

FEATURE_NAMES = [
    "Age",
    "Family Income",
    "Student Status",
    "Disability Status",
    "Disability Percentage",
    "Rural / Urban Area",
    "Gender: Female",
    "Gender: Male",
    "Occupation: Student",
    "Occupation: Farmer",
    "Occupation: Worker / Artisan",
    "Occupation: Unemployed",
    "Education: Below 10th",
    "Education: 10th / 12th Pass",
    "Education: Diploma / Degree",
    "Education: Post-Grad",
    "Family Dependents Count",
    "Already Receiving Other Benefits",
    "Category: General",
    "Category: EWS",
    "Category: OBC",
    "Category: SC",
    "Category: ST"
]

CATEGORY_MAP = {
    "General": [1, 0, 0, 0, 0],
    "EWS":     [0, 1, 0, 0, 0],
    "OBC":     [0, 0, 1, 0, 0],
    "SC":      [0, 0, 0, 1, 0],
    "ST":      [0, 0, 0, 0, 1]
}


def encode_user_profile(profile):
    """
    Encodes 12-factor citizen profile into numerical vector.
    """
    age = float(profile.get("age", 20))
    income = float(profile.get("income", 180000))
    is_student = 1.0 if profile.get("is_student", True) else 0.0
    
    is_disabled = 1.0 if profile.get("is_disabled", False) else 0.0
    disability_pct = float(profile.get("disability_pct", 0)) if is_disabled else 0.0
    
    is_rural = 1.0 if profile.get("area_type") == "Rural" else 0.0
    
    gender = profile.get("gender", "Male")
    gen_female = 1.0 if gender == "Female" else 0.0
    gen_male = 1.0 if gender == "Male" else 0.0
    
    occ = profile.get("occupation", "Student")
    occ_student = 1.0 if occ == "Student" else 0.0
    occ_farmer = 1.0 if occ == "Farmer" else 0.0
    occ_worker = 1.0 if occ in ["Worker", "Artisan", "Entrepreneur"] else 0.0
    occ_unemployed = 1.0 if occ == "Unemployed" else 0.0
    
    edu = profile.get("education", "12th Pass")
    edu_below10 = 1.0 if edu == "Below 10th" else 0.0
    edu_10_12 = 1.0 if edu in ["10th Pass", "12th Pass"] else 0.0
    edu_deg = 1.0 if edu in ["Diploma", "Degree"] else 0.0
    edu_pg = 1.0 if edu == "Post-Grad" else 0.0
    
    family_dependents = float(profile.get("family_dependents", 4))
    has_existing_benefits = 1.0 if profile.get("has_existing_benefits", False) else 0.0
    
    cat = profile.get("category", "General")
    cat_vec = CATEGORY_MAP.get(cat, CATEGORY_MAP["General"])

    vector = [
        age, income, is_student, is_disabled, disability_pct, is_rural,
        gen_female, gen_male,
        occ_student, occ_farmer, occ_worker, occ_unemployed,
        edu_below10, edu_10_12, edu_deg, edu_pg,
        family_dependents, has_existing_benefits
    ] + cat_vec

    return np.array(vector).reshape(1, -1)


def generate_synthetic_dataset(n_samples=2500, seed=42):
    """
    Generates synthetic citizen dataset modeling all 12 factor distributions.
    """
    np.random.seed(seed)
    
    ages = np.random.randint(10, 75, size=n_samples)
    incomes = np.random.choice(
        [50000, 120000, 200000, 280000, 400000, 600000, 900000, 1500000],
        size=n_samples, p=[0.25, 0.25, 0.15, 0.15, 0.10, 0.05, 0.03, 0.02]
    )
    students = np.random.choice([1, 0], size=n_samples, p=[0.45, 0.55])
    disabled = np.random.choice([1, 0], size=n_samples, p=[0.10, 0.90])
    disability_pcts = [np.random.randint(40, 90) if d == 1 else 0 for d in disabled]
    rural = np.random.choice([1, 0], size=n_samples, p=[0.60, 0.40])
    genders = np.random.choice(["Male", "Female", "Other"], size=n_samples, p=[0.50, 0.48, 0.02])
    occupations = np.random.choice(["Student", "Farmer", "Worker", "Unemployed"], size=n_samples, p=[0.40, 0.25, 0.20, 0.15])
    educations = np.random.choice(["Below 10th", "10th Pass", "12th Pass", "Diploma", "Degree", "Post-Grad"], size=n_samples)
    dependents = np.random.randint(1, 8, size=n_samples)
    existing_b = np.random.choice([1, 0], size=n_samples, p=[0.20, 0.80])
    categories = np.random.choice(["General", "EWS", "OBC", "SC", "ST"], size=n_samples, p=[0.30, 0.15, 0.30, 0.15, 0.10])

    X_rows = []
    Y_matrix = {scheme["id"]: [] for scheme in SCHEMES}

    for i in range(n_samples):
        prof = {
            "age": ages[i],
            "income": incomes[i],
            "is_student": students[i] == 1,
            "is_disabled": disabled[i] == 1,
            "disability_pct": disability_pcts[i],
            "area_type": "Rural" if rural[i] == 1 else "Urban",
            "gender": genders[i],
            "occupation": occupations[i],
            "education": educations[i],
            "family_dependents": dependents[i],
            "has_existing_benefits": existing_b[i] == 1,
            "category": categories[i]
        }
        
        row_x = encode_user_profile(prof)[0]
        X_rows.append(row_x)

        for scheme in SCHEMES:
            s_id = scheme["id"]
            age_ok = scheme["min_age"] <= ages[i] <= scheme["max_age"]
            inc_ok = incomes[i] <= scheme["max_income"]
            cat_ok = categories[i] in scheme["allowed_categories"]
            st_ok = (students[i] == 1) if scheme["req_student"] else True
            dis_ok = (disabled[i] == 1) if scheme["req_disability"] else True
            gen_ok = genders[i] in scheme["allowed_genders"]

            base_match = age_ok and inc_ok and cat_ok and st_ok and dis_ok and gen_ok
            prob = 0.95 if base_match else 0.05
            Y_matrix[s_id].append(1 if np.random.rand() < prob else 0)

    X = np.array(X_rows)
    return X, Y_matrix


class SchemeRFEngine:
    def __init__(self):
        self.models = {}
        self.metrics = {}
        self.feature_names = FEATURE_NAMES
        self.is_trained = False

    def train(self):
        """
        Trains Random Forest Classifiers for all schemes using scikit-learn.
        """
        print("Training 12-Factor Random Forest models for Scheme Sarthi...")
        X, Y_matrix = generate_synthetic_dataset(n_samples=2500, seed=42)

        for scheme in SCHEMES:
            s_id = scheme["id"]
            y = np.array(Y_matrix[s_id])

            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )

            rf = RandomForestClassifier(
                n_estimators=100,
                max_depth=12,
                min_samples_split=4,
                random_state=42,
                n_jobs=-1
            )
            rf.fit(X_train, y_train)

            y_pred = rf.predict(X_test)
            acc = accuracy_score(y_test, y_pred)
            prec = precision_score(y_test, y_pred, zero_division=0)
            rec = recall_score(y_test, y_pred, zero_division=0)

            self.models[s_id] = rf
            self.metrics[s_id] = {
                "accuracy": round(acc * 100, 2),
                "precision": round(prec * 100, 2),
                "recall": round(rec * 100, 2),
                "n_trees": 100
            }

        self.is_trained = True
        print(f"Successfully trained 12-Factor Random Forest models for {len(SCHEMES)} schemes.")

    def predict_scheme_probabilities(self, profile):
        """
        Returns Random Forest match probability for each scheme.
        """
        if not self.is_trained:
            self.train()

        X_user = encode_user_profile(profile)
        predictions = {}

        for scheme in SCHEMES:
            s_id = scheme["id"]
            rf = self.models[s_id]
            prob_matrix = rf.predict_proba(X_user)
            if prob_matrix.shape[1] > 1:
                prob = float(prob_matrix[0][1])
            else:
                prob = float(prob_matrix[0][0])
            predictions[s_id] = round(prob, 4)

        return predictions

    def get_overall_feature_importance(self):
        """
        Calculates aggregate feature importances across all 12-Factor Random Forest models.
        """
        if not self.is_trained:
            self.train()

        avg_importances = np.zeros(len(self.feature_names))
        for s_id, rf in self.models.items():
            avg_importances += rf.feature_importances_

        avg_importances /= len(self.models)

        results = [
            {"feature": fn, "importance": round(float(imp) * 100, 2)}
            for fn, imp in zip(self.feature_names, avg_importances)
        ]

        results.sort(key=lambda x: x["importance"], reverse=True)
        return results


# Global singleton instance
rf_engine = SchemeRFEngine()
rf_engine.train()
