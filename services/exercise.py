from models.schemas import ExerciseRequest , FitnessLevel
from typing import Dict, List, Optional, Any

def get_exercise_plan(request: ExerciseRequest) -> Dict[str, Any]:
    """Mock function to generate comprehensive exercise recommendations"""
    
    # Base exercise plans by fitness level
    base_plans = {
        FitnessLevel.BEGINNER: {
            "cardio": {
                "type": "Low-impact activities",
                "duration": "15-20 minutes",
                "intensity": "Light to moderate",
                "examples": ["Walking", "Swimming", "Stationary bike"]
            },
            "strength": {
                "type": "Bodyweight and light resistance",
                "sets": "2 sets",
                "reps": "8-12 repetitions",
                "examples": ["Push-ups (modified if needed)", "Squats", "Lunges"]
            },
            "flexibility": {
                "type": "Basic stretching and mobility",
                "duration": "10-15 minutes",
                "examples": ["Full body stretching", "Yoga basics"]
            },
            "frequency": "3-4 times per week",
            "rest_days": "At least 1 day between strength sessions"
        },
        FitnessLevel.INTERMEDIATE: {
            "cardio": {
                "type": "Moderate intensity activities",
                "duration": "30-40 minutes",
                "intensity": "Moderate to vigorous",
                "examples": ["Jogging", "Cycling", "Dance fitness"]
            },
            "strength": {
                "type": "Progressive resistance training",
                "sets": "3 sets",
                "reps": "8-15 repetitions",
                "examples": ["Push-ups", "Pull-ups", "Weight training"]
            },
            "flexibility": {
                "type": "Dynamic and static stretching",
                "duration": "15-20 minutes",
                "examples": ["Yoga flow", "Pilates", "Foam rolling"]
            },
            "frequency": "4-5 times per week",
            "rest_days": "1-2 active recovery days"
        },
        FitnessLevel.ADVANCED: {
            "cardio": {
                "type": "High-intensity and varied activities",
                "duration": "45-60 minutes",
                "intensity": "Moderate to high intensity",
                "examples": ["HIIT training", "Running", "Sport activities"]
            },
            "strength": {
                "type": "Advanced resistance training",
                "sets": "3-4 sets",
                "reps": "6-15 repetitions",
                "examples": ["Compound movements", "Olympic lifts", "Functional training"]
            },
            "flexibility": {
                "type": "Comprehensive mobility work",
                "duration": "20-30 minutes",
                "examples": ["Advanced yoga", "Deep tissue work", "Movement patterns"]
            },
            "frequency": "5-6 times per week",
            "rest_days": "1-2 active recovery or complete rest days"
        }
    }
    
    plan = base_plans[request.fitness_level].copy()
    adaptations = []
    
    # Adjust for available time
    if request.available_time < 30:
        adaptations.append("Plan adjusted for shorter sessions - focus on high-intensity intervals")
        plan["time_note"] = "Consider splitting workouts or doing high-intensity circuits"
    elif request.available_time > 60:
        adaptations.append("Extended time allows for comprehensive warm-up and cool-down")
        plan["time_note"] = "Include thorough warm-up and recovery periods"
    
    # Adjust for equipment
    if not request.equipment_available or "none" in [eq.lower() for eq in request.equipment_available]:
        adaptations.append("Plan adapted for bodyweight exercises only")
        plan["equipment_note"] = "All exercises can be performed using body weight"
    else:
        available_equipment = ", ".join(request.equipment_available)
        plan["equipment_note"] = f"Plan utilizes: {available_equipment}"
    
    # Consider physical limitations
    if request.physical_limitations:
        adaptations.append("Plan modified to accommodate physical limitations")
        limitation_notes = []
        for limitation in request.physical_limitations:
            if "knee" in limitation.lower():
                limitation_notes.append("Low-impact alternatives for knee-friendly exercises")
            elif "back" in limitation.lower():
                limitation_notes.append("Core strengthening and proper form emphasis")
            elif "shoulder" in limitation.lower():
                limitation_notes.append("Modified upper body exercises")
        
        plan["limitation_accommodations"] = limitation_notes
    
    # Weekly schedule suggestion
    weekly_schedule = []
    frequency_num = int(plan["frequency"].split("-")[0])
    
    for i in range(frequency_num):
        day_plan = {
            f"Day {i+1}": {
                "focus": ["cardio", "strength", "flexibility"][i % 3],
                "duration": f"{request.available_time} minutes"
            }
        }
        weekly_schedule.append(day_plan)
    
    return {
        "success": True,
        "fitness_level": request.fitness_level.value,
        "exercise_plan": plan,
        "weekly_schedule": weekly_schedule,
        "adaptations": adaptations,
        "safety_reminders": [
            "Start slowly and gradually increase intensity",
            "Listen to your body and rest when needed",
            "Maintain proper form to prevent injury",
            "Stay hydrated during workouts"
        ],
        "disclaimer": "Consult a fitness professional before starting any new exercise program, especially if you have health conditions."
    }