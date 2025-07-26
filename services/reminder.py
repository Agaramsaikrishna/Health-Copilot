import random
from datetime import datetime, timedelta
from typing import Dict, Any
from models.schemas import ReminderRequest, Frequency
from agno.tools import tool



@tool(name="schedule_reminder", description="Set a health-related reminder (e.g., walk, checkup, medication)")
def schedule_reminder(request: ReminderRequest) -> Dict[str, Any]:
    reminder_id = f"rem_{random.randint(1000, 9999)}"
    try:
        start = datetime.strptime(request.start_date, "%Y-%m-%d")
        freq = {
            Frequency.DAILY: timedelta(days=1),
            Frequency.WEEKLY: timedelta(weeks=1),
            Frequency.MONTHLY: timedelta(days=30),
            Frequency.YEARLY: timedelta(days=365)
        }
        next_date = start + freq[request.frequency]
        return {
            "success": True,
            "reminder_id": reminder_id,
            "title": request.title,
            "next_reminder": next_date.strftime("%Y-%m-%d"),
            "frequency": request.frequency.value,
            "notes": request.notes or "N/A"
        }
    except ValueError as e:
        return {
            "success": False,
            "error": str(e)
        }
