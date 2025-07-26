from typing import List, Dict, Optional
from enum import Enum
from pydantic import BaseModel, Field

class ReminderType(str, Enum):
    CHECKUP = "checkup"
    MEDICATION = "medication"
    EXERCISE = "exercise"
    SCREENING = "screening"
    VACCINATION = "vaccination"

class Frequency(str, Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"

class FitnessLevel(str, Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class ReminderRequest(BaseModel):
    type: ReminderType
    title: str
    frequency: Frequency
    start_date: str
    notes: Optional[str] = None

class DietRequest(BaseModel):
    dietary_restrictions: List[str] = []
    health_goals: List[str] = []
    current_conditions: List[str] = []
    preferred_cuisine: Optional[str] = None
    age: Optional[int] = None
    activity_level: Optional[str] = None

class ExerciseRequest(BaseModel):
    fitness_level: FitnessLevel
    available_time: int
    equipment_available: List[str] = []
    physical_limitations: List[str] = []
    preferred_activities: List[str] = []

# class HealthProfile(BaseModel):
#     user_id: str
#     age: int
#     gender: str
#     height: float
#     weight: float
#     medical_history: List[str] = []
#     current_medications: List[str] = []
#     lifestyle_factors: Dict[str, str] = {}
#     allergies: List[str] = []
#     family_history: List[str] = []


    
    
class HealthProfile(BaseModel):
    user_id: str
    age: int
    gender: str
    height: float = Field(..., description="Height in cm")
    weight: float = Field(..., description="Weight in kg")
    medical_history: List[str] = Field(default_factory=list)
    current_medications: List[str] = Field(default_factory=list)
    lifestyle_factors: Dict[str, str] = Field(default_factory=dict)
    allergies: List[str] = Field(default_factory=list)
    family_history: List[str] = Field(default_factory=list)
    
    
    
class HealthConsultationRequest(BaseModel):
    query: str
    user_profile: HealthProfile
    preferred_llm: str = "groq"
    include_evaluation: bool = False
    