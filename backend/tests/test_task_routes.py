class TestProcessTask:

    def test_calculator_task_succeeds(self, client):
        response = client.post("/tasks", json={"task": "calculate 5 + 3"})

        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "SUCCESS"
        assert body["tool"] == "CalculatorTool"
        assert body["result"]["value"] == 8

    def test_unrecognized_task_returns_400(self, client):
        response = client.post("/tasks", json={"task": "xyzzy plugh nonsense"})

        assert response.status_code == 400
        body = response.json()
        assert body["status"] == "FAILED"

    def test_division_by_zero_returns_400(self, client):
        response = client.post("/tasks", json={"task": "calculate 10 / 0"})

        assert response.status_code == 400
        assert response.json()["status"] == "FAILED"

    def test_missing_task_field_returns_422(self, client):
        # No "task" key at all — should fail Pydantic validation
        # on TaskRequest before it ever reaches the agent.
        response = client.post("/tasks", json={})

        assert response.status_code == 422

    def test_response_matches_task_schema(self, client):
        response = client.post("/tasks", json={"task": "calculate 2 + 2"})
        body = response.json()

        assert set(body.keys()) == {"tool", "status", "result", "message", "trace"}


class TestTaskHistory:

    def test_empty_history_returns_empty_list(self, client):
        response = client.get("/tasks/history")

        assert response.status_code == 200
        assert response.json() == []

    def test_history_reflects_submitted_task(self, client):
        client.post("/tasks", json={"task": "calculate 100 * 2"})

        response = client.get("/tasks/history")

        assert response.status_code == 200
        history = response.json()
        assert len(history) == 1
        assert history[0]["task"] == "calculate 100 * 2"
        assert history[0]["status"] == "SUCCESS"
        assert history[0]["result"]["value"] == 200

    def test_history_ordered_most_recent_first(self, client):
        client.post("/tasks", json={"task": "calculate 1 + 1"})
        client.post("/tasks", json={"task": "calculate 2 + 2"})

        response = client.get("/tasks/history")
        history = response.json()

        assert len(history) == 2
        assert history[0]["task"] == "calculate 2 + 2"
        assert history[1]["task"] == "calculate 1 + 1"
