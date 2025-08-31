from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_new_conversation():
    r = client.post("/api/v1/chat/webhook", json={"conversation_id": None, "message": "Debate that electric cars are worse than gas cars about transportation."})
    assert r.status_code == 200
    data = r.json()
    assert "conversation_id" in data
    assert isinstance(data["message"], list)
    assert data["message"][-1]["role"] == "bot"

def test_follow_up():
    r1 = client.post("/api/v1/chat/webhook", json={"conversation_id": None, "message": "Debate that the Earth is flat about the shape of the Earth."})
    cid = r1.json()["conversation_id"]
    r2 = client.post("/api/v1/chat/webhook", json={"conversation_id": cid, "message": "But satellite photos show curvature."})
    assert r2.status_code == 200
    data = r2.json()
    assert data["message"][-1]["role"] == "bot"
    assert len(data["message"]) <= 10
