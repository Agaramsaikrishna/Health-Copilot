from typing import Dict, List, Optional, Any
from models.schemas import *




def health_risk_assessment(profile: HealthProfile) -> Dict[str, Any]:
    """Mock function for comprehensive health risk assessment"""
    
    risks = []
    recommendations = []
    screening_due = []
    
    # BMI calculation and assessment
    bmi = profile.weight / ((profile.height / 100) ** 2)
    bmi_category = ""
    
    if bmi < 18.5:
        bmi_category = "Underweight"
        risks.append("Underweight - may indicate nutritional deficiency")
        recommendations.append("Consult healthcare provider about healthy weight gain")
    elif 18.5 <= bmi < 25:
        bmi_category = "Normal weight"
    elif 25 <= bmi < 30:
        bmi_category = "Overweight"
        risks.append("Overweight - increased risk for heart disease and diabetes")
        recommendations.append("Consider structured weight management program")
    else:
        bmi_category = "Obese"
        risks.append("Obesity - significantly increased health risks")
        recommendations.append("Strongly recommend medical consultation for weight management")
    
    # Age-based risk assessment and screening recommendations
    age_risks = {
        (18, 30): {
            "risks": ["Establishing unhealthy lifestyle patterns"],
            "screenings": ["Annual wellness check", "STD screening if sexually active"]
        },
        (30, 40): {
            "risks": ["Metabolic syndrome", "Early cardiovascular changes"],
            "screenings": ["Blood pressure check", "Cholesterol screening", "Diabetes screening"]
        },
        (40, 50): {
            "risks": ["Cardiovascular disease", "Pre-diabetes", "Hormone changes"],
            "screenings": ["Mammogram (women)", "Prostate check (men)", "Eye exam", "Skin cancer screening"]
        },
        (50, 65): {
            "risks": ["Increased cancer risk", "Bone density loss", "Cardiovascular disease"],
            "screenings": ["Colonoscopy", "Bone density scan", "Advanced cardiac screening"]
        },
        (65, 100): {
            "risks": ["Multiple chronic conditions", "Cognitive decline", "Falls risk"],
            "screenings": ["Comprehensive geriatric assessment", "Cognitive screening", "Fall risk assessment"]
        }
    }
    
    # Find appropriate age group
    for (min_age, max_age), age_data in age_risks.items():
        if min_age <= profile.age < max_age:
            risks.extend(age_data["risks"])
            screening_due.extend(age_data["screenings"])
            break
    
    # Gender-specific risks
    if profile.gender.lower() == "female":
        if profile.age >= 21:
            screening_due.append("Cervical cancer screening (Pap smear)")
        if profile.age >= 40:
            screening_due.append("Annual mammogram")
        if profile.age >= 50:
            screening_due.append("Bone density screening")
    elif profile.gender.lower() == "male":
        if profile.age >= 40:
            screening_due.append("Prostate health screening")
        if profile.age >= 45:
            screening_due.append("Cardiovascular risk assessment")
    
    # Medical history analysis
    high_risk_conditions = {
        "hypertension": "Cardiovascular disease risk",
        "diabetes": "Diabetic complications risk",
        "heart disease": "Cardiovascular events risk",
        "cancer": "Cancer recurrence monitoring needed",
        "stroke": "Recurrent stroke risk"
    }
    
    for condition in profile.medical_history:
        for risk_condition, risk_desc in high_risk_conditions.items():
            if risk_condition.lower() in condition.lower():
                risks.append(risk_desc)
                recommendations.append(f"Regular monitoring for {condition}")
    
    # Lifestyle factor analysis
    lifestyle = profile.lifestyle_factors
    
    if lifestyle.get("smoking", "").lower() in ["yes", "current", "daily"]:
        risks.append("Smoking-related health risks (cancer, heart disease, COPD)")
        recommendations.append("Smoking cessation program - highest priority intervention")
    
    exercise_freq = lifestyle.get("exercise_frequency", "").lower()
    if exercise_freq in ["rarely", "never", "sedentary"]:
        risks.append("Sedentary lifestyle - increased risk for multiple conditions")
        recommendations.append("Gradual increase in physical activity to 150 min/week")
    
    alcohol_use = lifestyle.get("alcohol", "").lower()
    if alcohol_use in ["heavy", "daily", "excessive"]:
        risks.append("Excessive alcohol use - liver disease and other health risks")
        recommendations.append("Consider alcohol reduction or cessation support")
    
    # Family history assessment
    familial_risks = {
        "heart disease": "Increased cardiovascular risk - early screening recommended",
        "diabetes": "Genetic predisposition to diabetes - regular glucose monitoring",
        "cancer": "Increased cancer risk - enhanced screening protocols",
        "alzheimer": "Cognitive health monitoring important"
    }
    
    for family_condition in profile.family_history:
        for condition, risk_desc in familial_risks.items():
            if condition.lower() in family_condition.lower():
                risks.append(risk_desc)
    
    # Generate risk score (simplified)
    risk_score = len(risks)
    risk_level = "Low" if risk_score <= 2 else ("Moderate" if risk_score <= 5 else "High")
    
    # Next appointment recommendations
    next_checkup = "1 year" if risk_level == "Low" else ("6 months" if risk_level == "Moderate" else "3 months")
    
    return {
        "success": True,
        "bmi": round(bmi, 1),
        "bmi_category": bmi_category,
        "risk_level": risk_level,
        "risk_factors": risks,
        "health_recommendations": recommendations,
        "screening_due": list(set(screening_due)),  # Remove duplicates
        "next_checkup_recommended": next_checkup,
        "lifestyle_improvements": [
            "Maintain regular exercise routine",
            "Follow balanced, nutritious diet",
            "Ensure adequate sleep (7-9 hours)",
            "Manage stress through healthy coping mechanisms",
            "Avoid tobacco and limit alcohol"
        ],
        "emergency_signs": [
            "Chest pain or pressure",
            "Severe shortness of breath",
            "Sudden severe headache",
            "Signs of stroke (FAST protocol)",
            "Severe abdominal pain"
        ],
        "disclaimer": "This assessment is for informational purposes only. Always consult healthcare professionals for medical advice."
    }
