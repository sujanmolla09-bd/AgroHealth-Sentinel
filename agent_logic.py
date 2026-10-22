import os
import numpy as np
from pydantic import BaseModel
import google.generativeai as genai

# Worker Telemetry Schema
class WorkerTelemetry(BaseModel):
    worker_id: str
    temperature: float  # Celsius
    humidity: float     # Percentage
    solar_radiation: float  # W/m^2
    exposure_time_hours: float
    location: str = "Thakurgaon, Bangladesh"

class SafetyRecommendation(BaseModel):
    risk_level: str
    action_required: str
    escalation_needed: bool
    details: str

class AgroHealthAgents:
    def __init__(self):
        # Gemini API Integration setup
        api_key = os.getenv("GEMINI_API_KEY", "MOCK_KEY_FOR_DEMO")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def heat_risk_agent(self, data: WorkerTelemetry) -> str:
        """Estimates environmental heat risk based on climate inputs."""
        # Humidex approximation for agricultural safety thresholds
        heat_index = data.temperature + (0.5555 * (((6.11 * np.exp(5417.7530 * ((1/273.16) - (1/(273.15 + data.temperature))))) * (data.humidity / 100)) - 10))
        
        if heat_index >= 40 or data.exposure_time_hours >= 4:
            return "CRITICAL"
        elif heat_index >= 32:
            return "ELEVATED"
        return "NORMAL"

    def worker_safety_agent(self, risk_level: str, data: WorkerTelemetry) -> dict:
        """Recommends preventive safety actions."""
        recommendations = {
            "NORMAL": {"action": "Continue normal rotation.", "break_mins": 0, "hydration_liters": 0.5},
            "ELEVATED": {"action": "Move to safe shade zone.", "break_mins": 15, "hydration_liters": 1.0},
            "CRITICAL": {"action": "Immediate halt field operations.", "break_mins": 30, "hydration_liters": 1.5}
        }
        return recommendations.get(risk_level, recommendations["NORMAL"])

    def health_escalation_agent(self, risk_level: str, data: WorkerTelemetry, safety: dict) -> bool:
        """Triggers supervisor human review protocol when threshold is passed."""
        if risk_level == "CRITICAL":
            # Escalation logic triggered
            return True
        return False
