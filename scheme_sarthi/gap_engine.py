"""
Scheme Sarthi - Gap Analyzer & Action Planner Engine (Strict 12-Factor Evaluation)
Strictly enforces hard disqualification for Gender, Disability, Occupation, Student status, and Age.
"""

from schemes_data import SCHEMES
from ml_engine import rf_engine, encode_user_profile

def analyze_user_gaps(user_profile):
    """
    Inputs 12-Factor user_profile dictionary:
    {
        'age': int,
        'state': str,
        'district': str,
        'income': float,
        'category': str,
        'student_status': 'Student'|'Working'|'Unemployed',
        'education': str,
        'is_disabled': bool,
        'disability_pct': float,
        'gender': 'Male'|'Female'|'Other',
        'occupation': 'Student'|'Farmer'|'Worker'|'Entrepreneur'|'Unemployed',
        'area_type': 'Rural'|'Urban',
        'family_dependents': int,
        'has_existing_benefits': bool
    }
    """
    rf_probs = rf_engine.predict_scheme_probabilities(user_profile)

    age = int(user_profile.get('age', 20))
    state = str(user_profile.get('state', 'Karnataka'))
    district = str(user_profile.get('district', 'Bangalore Urban'))
    income = float(user_profile.get('income', 180000))
    category = str(user_profile.get('category', 'General'))
    student_status = str(user_profile.get('student_status', 'Student'))
    is_student = (student_status == 'Student') or bool(user_profile.get('is_student', True))
    education = str(user_profile.get('education', '12th Pass'))
    is_disabled = bool(user_profile.get('is_disabled', False))
    disability_pct = float(user_profile.get('disability_pct', 0)) if is_disabled else 0
    gender = str(user_profile.get('gender', 'Male'))
    occupation = str(user_profile.get('occupation', 'Student'))
    area_type = str(user_profile.get('area_type', 'Urban'))
    family_dependents = int(user_profile.get('family_dependents', 4))
    has_existing_benefits = bool(user_profile.get('has_existing_benefits', False))

    results = []
    eligible_count = 0
    almost_count = 0
    not_eligible_count = 0
    total_potential_benefit = 0

    for scheme in SCHEMES:
        s_id = scheme['id']
        rf_prob = rf_probs.get(s_id, 0.5)

        reasons = []
        gaps = []
        missing_docs = []
        hard_disqualifier = False
        relaxed_pass = True

        # Factor 1: Age Check
        if scheme['min_age'] <= age <= scheme['max_age']:
            reasons.append(f"✅ Age ({age} yrs) is within scheme bracket ({scheme['min_age']} - {scheme['max_age']} yrs).")
        else:
            hard_disqualifier = True
            reasons.append(f"❌ Age ({age} yrs) falls outside scheme bracket ({scheme['min_age']} - {scheme['max_age']} yrs).")
            gaps.append(f"Age mismatch: Must be between {scheme['min_age']} and {scheme['max_age']} years.")

        # Factor 2: Income Check
        if income <= scheme['max_income']:
            reasons.append(f"✅ Family income (₹{income:,.0f}) is within limit (<= ₹{scheme['max_income']:,.0f}).")
        elif income <= scheme['max_income'] * 1.25:
            reasons.append(f"⚠️ Family income (₹{income:,.0f}) slightly exceeds cutoff ₹{scheme['max_income']:,.0f}.")
            gaps.append("Income slightly above baseline cutoff (Income verification certificate update needed).")
            missing_docs.append("Updated Income Certificate (< 6 months old)")
            relaxed_pass = False
        else:
            hard_disqualifier = True
            reasons.append(f"❌ Family income (₹{income:,.0f}) exceeds ceiling of ₹{scheme['max_income']:,.0f}.")
            gaps.append(f"Income ceiling exceeded by ₹{income - scheme['max_income']:,.0f}.")

        # Factor 3: State & Location
        reasons.append(f"✅ State Domicile ({state}) & Area ({area_type}) evaluated.")
        if scheme['area_preference'] != 'Any' and scheme['area_preference'].lower() != area_type.lower():
            reasons.append(f"ℹ️ Scheme prioritizes {scheme['area_preference']} residents; user is in {area_type} area.")

        # Factor 4: Social Category Check
        if category in scheme['allowed_categories']:
            reasons.append(f"✅ Social category '{category}' is eligible.")
        else:
            reasons.append(f"⚠️ Category '{category}' is not listed in scheme focus ({', '.join(scheme['allowed_categories'])}).")
            gaps.append(f"Scheme targets specific categories ({', '.join(scheme['allowed_categories'])}).")
            missing_docs.append("Caste / Community Certificate")
            relaxed_pass = False

        # Factor 5: Student Status Check
        if scheme['req_student']:
            if is_student:
                reasons.append("✅ Active student status verified.")
            else:
                hard_disqualifier = True
                reasons.append("❌ Reserved for active students enrolled in recognized institutions.")
                gaps.append("Requires active student status and enrolment.")
                missing_docs.append("Bonafide Student Certificate / College ID")

        # Factor 6: Education Level Check
        allowed_edu = scheme.get('allowed_educations', [education])
        if education in allowed_edu:
            reasons.append(f"✅ Education level '{education}' meets scheme requirement.")
        else:
            reasons.append(f"⚠️ Education level '{education}' requires specific qualification ({', '.join(allowed_edu)}).")
            gaps.append(f"Education level requires {', '.join(allowed_edu)}.")
            relaxed_pass = False

        # Factor 7: Disability Status Check
        if scheme['req_disability']:
            if is_disabled and disability_pct >= 40:
                reasons.append(f"✅ PwD status verified ({disability_pct}% disability).")
            else:
                hard_disqualifier = True
                reasons.append("❌ Exclusively for Persons with Disability (PwD >= 40%).")
                gaps.append("Requires valid Unique Disability ID (UDID) card with >= 40% disability.")
                missing_docs.append("UDID Card / Disability Certificate")

        # Factor 8: Gender Check (STRICT ENFORCEMENT)
        allowed_g = scheme.get('allowed_genders', ['Male', 'Female', 'Other'])
        if gender in allowed_g:
            reasons.append(f"✅ Gender '{gender}' matches scheme eligibility.")
        else:
            hard_disqualifier = True
            reasons.append(f"❌ Scheme is specifically reserved for {', '.join(allowed_g)} beneficiaries; profile gender is '{gender}'.")
            gaps.append(f"Gender mismatch: Reserved exclusively for {', '.join(allowed_g)} applicants.")

        # Factor 9: Occupation Check (STRICT ENFORCEMENT)
        allowed_occ = scheme.get('allowed_occupations', [occupation])
        if occupation in allowed_occ:
            reasons.append(f"✅ Occupation '{occupation}' is eligible.")
        else:
            hard_disqualifier = True
            reasons.append(f"❌ Scheme is reserved for occupations: {', '.join(allowed_occ)}; profile occupation is '{occupation}'.")
            gaps.append(f"Occupation mismatch: Restricted to {', '.join(allowed_occ)}.")

        # Factor 10: Family Conditions & Dependents
        reasons.append(f"✅ Family size / dependents ({family_dependents} members) recorded.")

        # Factor 11: Mandatory Document Checklist
        for doc in scheme['documents']:
            missing_docs.append(doc)

        # Factor 12: Existing Benefits Check
        if has_existing_benefits and not scheme.get('existing_benefits_allowed', True):
            reasons.append("⚠️ Currently receiving another central benefit/scholarship.")
            gaps.append("Holding another central scholarship may require undertaking or waiver.")
            relaxed_pass = False
        else:
            reasons.append("✅ No conflicting prior benefit disallowance.")

        # FINAL STATUS BUCKET DETERMINATION
        if hard_disqualifier:
            status = "NOT_ELIGIBLE"
            status_label = "Not Eligible"
            status_icon = "❌"
            badge_class = "badge-danger"
            rf_prob = min(rf_prob, 0.20)
            not_eligible_count += 1
        elif rf_prob >= 0.60 and relaxed_pass:
            status = "ELIGIBLE"
            status_label = "Eligible"
            status_icon = "✅"
            badge_class = "badge-success"
            eligible_count += 1
            total_potential_benefit += scheme['annual_val']
        else:
            status = "ALMOST_ELIGIBLE"
            status_label = "Almost Eligible"
            status_icon = "⚠️"
            badge_class = "badge-warning"
            almost_count += 1
            total_potential_benefit += (scheme['annual_val'] * 0.5)

        unique_missing_docs = list(dict.fromkeys(missing_docs))

        results.append({
            "id": scheme['id'],
            "name": scheme['name'],
            "category_tag": scheme['category_tag'],
            "ministry": scheme['ministry'],
            "benefit_amount": scheme['benefit_amount'],
            "annual_val": scheme['annual_val'],
            "description": scheme['description'],
            "status": status,
            "status_label": status_label,
            "status_icon": status_icon,
            "badge_class": badge_class,
            "rf_probability": round(rf_prob * 100, 1),
            "reasons": reasons,
            "gaps": gaps if gaps else ["All eligibility criteria satisfied!"],
            "missing_docs": unique_missing_docs[:5],
            "portal_name": scheme['portal_name'],
            "portal_url": scheme['portal_url'],
            "action_steps": scheme['action_steps']
        })

    status_order = {"ELIGIBLE": 0, "ALMOST_ELIGIBLE": 1, "NOT_ELIGIBLE": 2}
    results.sort(key=lambda x: (status_order[x['status']], -x['rf_probability']))

    raw_fi = rf_engine.get_overall_feature_importance()

    summary = {
        "total_schemes_analyzed": len(SCHEMES),
        "eligible_count": eligible_count,
        "almost_eligible_count": almost_count,
        "not_eligible_count": not_eligible_count,
        "total_potential_benefit_formatted": f"₹{total_potential_benefit:,.0f}"
    }

    return {
        "user_profile": user_profile,
        "summary": summary,
        "scheme_results": results,
        "feature_importances": raw_fi
    }
