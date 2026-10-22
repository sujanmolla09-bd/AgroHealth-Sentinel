from fastapi import FastAPI, HTTPException
from agent_logic import AgroHealthAgents, WorkerTelemetry, SafetyRecommendation

app = FastAPI(
    title="AgroHealth-Sentinel API",
    description="Preventive occupational-health platform for agricultural workers."
)

# Initialize the automated multi-agent core
agents = AgroHealthAgents()

@app.get("/")
def read_root():
    return {
        "status": "ONLINE",
        "infrastructure": "Google Cloud & Render Fabric Sync",
        "region_focus": "Thakurgaon, Bangladesh"
    }

@app.post("/api/v1/process-telemetry", response_model=SafetyRecommendation)
async def process_worker_safety(telemetry: WorkerTelemetry):
    try:
        # 1. Trigger Heat Risk Agent
        risk = agents.heat_risk_agent(telemetry)
        
        # 2. Trigger Worker Safety Agent
        safety_plan = agents.worker_safety_agent(risk, telemetry)
        
        # 3. Trigger Health Escalation Agent
        escalate = agents.health_escalation_agent(risk, telemetry, safety_plan)
        
        details_msg = f"Worker alert in {telemetry.location}. Hydration: {safety_plan['hydration_liters']}L, Break: {safety_plan['break_mins']} mins."
        
        return SafetyRecommendation(
            risk_level=risk,
            action_required=safety_plan['action'],
            escalation_needed=escalate,
            details=details_msg
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
