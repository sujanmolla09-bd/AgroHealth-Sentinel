import pytest
from fastapi.testclient import TestClient
from main import app

# ফাস্টএপিআই টেস্ট ক্লায়েন্ট ইনিশিয়ালাইজেশন
client = TestClient(app)

# ১. রুট নোড এবং ঠাকুরগাঁও রিজিউন সিঙ্ক টেস্ট
def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ONLINE"
    assert "Thakurgaon, Bangladesh" in data["region_focus"]

# ২. এআই টেলিমেট্রি এন্ডপয়েন্ট ইন্টিগ্রিটি ও অ্যাকশন লুপ টেস্ট
def test_process_telemetry_valid():
    # একটি হাই-রিস্ক আবহাওয়ার সিমুলেটেড ডাটা প্যাকেট
    test_payload = {
        "worker_id": "W-7058",
        "temperature": 41.5,
        "humidity": 72.0,
        "solar_radiation": 850.0,
        "exposure_time_hours": 4.5,
        "location": "Thakurgaon Sadar"
    }
    
    response = client.post("/api/v1/process-telemetry", json=test_payload)
    
    # এপিআই রেসপন্স এবং স্ট্রাকচার্ড JSON কমপ্লায়েন্স ভেরিফিকেশন
    assert response.status_code == 200
    res_data = response.json()
    assert "risk_level" in res_data
    assert "action_required" in res_data
    assert "escalation_needed" in res_data
    assert isinstance(res_data["escalation_needed"], bool)
