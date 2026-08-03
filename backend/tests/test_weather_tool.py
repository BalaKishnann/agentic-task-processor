import pytest
import requests

from app.tools.weather_tool import WeatherTool
from app.agent.execution_trace import ExecutionTrace


@pytest.fixture
def weather_tool():
    return WeatherTool()


@pytest.fixture
def trace():
    return ExecutionTrace()


class TestCanHandle:

    @pytest.mark.parametrize(
        "task",
        [
            "What's the weather in Toronto",
            "temperature in Vancouver",
            "give me the forecast for tomorrow",
            "what's the climate like there",
        ],
    )
    def test_recognizes_weather_keywords(self, weather_tool, task):
        assert weather_tool.can_handle(task) is True

    @pytest.mark.parametrize(
        "task",
        [
            "Calculate 5 + 3",
            "what time is it",
            "summarize this document",
        ],
    )
    def test_rejects_non_weather_tasks(self, weather_tool, task):
        assert weather_tool.can_handle(task) is False


class TestExecute:

    def test_known_city_toronto(self, weather_tool, trace):
        result = weather_tool.execute("What's the weather in Toronto", trace)

        assert result["status"] == "SUCCESS"
        assert result["tool"] == "WeatherTool"
        assert result["result"]["city"] == "Toronto"
        assert "22°C" in result["result"]["weather"]

    def test_known_city_vancouver(self, weather_tool, trace):
        result = weather_tool.execute("temperature in vancouver please", trace)

        assert result["result"]["city"] == "Vancouver"

    def test_unknown_city_falls_back(self, weather_tool, trace):
        result = weather_tool.execute("what's the weather in Atlantis", trace)

        assert result["status"] == "SUCCESS"
        assert result["result"]["city"] == "Unknown"

    def test_response_includes_trace(self, weather_tool, trace):
        result = weather_tool.execute("weather in Toronto", trace)

        assert isinstance(result["trace"], list)
        assert len(result["trace"]) > 0


class TestExecuteLive:
    """
    Tests for the real API path. requests.get is mocked so these never
    make actual network calls.
    """

    def test_missing_api_key_fails_cleanly(self, weather_tool, trace, monkeypatch):
        monkeypatch.delenv("WEATHER_API_KEY", raising=False)

        result = weather_tool.execute_live("weather in Toronto", trace)

        assert result["status"] == "FAILED"
        assert "WEATHER_API_KEY" in result["message"]

    def test_successful_live_call(self, weather_tool, trace, monkeypatch):
        monkeypatch.setenv("WEATHER_API_KEY", "fake-key")

        class MockResponse:
            def raise_for_status(self):
                pass

            def json(self):
                return {
                    "name": "Toronto",
                    "main": {"temp": 21.5, "humidity": 60},
                    "weather": [{"description": "clear sky"}],
                }

        def mock_get(*args, **kwargs):
            return MockResponse()

        monkeypatch.setattr("requests.get", mock_get)

        result = weather_tool.execute_live("weather in Toronto", trace)

        assert result["status"] == "SUCCESS"
        assert result["result"]["city"] == "Toronto"
        assert result["result"]["temperature"] == 21.5

    def test_timeout_handled(self, weather_tool, trace, monkeypatch):
        monkeypatch.setenv("WEATHER_API_KEY", "fake-key")

        def mock_get(*args, **kwargs):
            raise requests.exceptions.Timeout()

        monkeypatch.setattr("requests.get", mock_get)

        result = weather_tool.execute_live("weather in Toronto", trace)

        assert result["status"] == "FAILED"
        assert "timeout" in result["message"].lower()
