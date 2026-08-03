import requests
import os

from app.tools.base_tool import BaseTool


class WeatherTool(BaseTool):

    MOCK_WEATHER_DATA = {
        "toronto": {"city": "Toronto", "weather": "22°C, Sunny"},
        "vancouver": {"city": "Vancouver", "weather": "18°C, Cloudy"},
        "montreal": {"city": "Montreal", "weather": "20°C, Partly Cloudy"},
    }

    def can_handle(self, task: str) -> bool:

        keywords = ["weather", "temperature", "forecast", "climate"]

        return any(word in task.lower() for word in keywords)

    def execute(self, task: str, trace):
        """
        Mock implementation: returns canned data for a small set of
        known cities, falls back to a generic value otherwise. Not a
        real weather lookup — see execute_live() for the real
        OpenWeatherMap integration, currently unused by default.
        """

        task_lower = task.lower()

        match = next(
            (data for key, data in self.MOCK_WEATHER_DATA.items() if key in task_lower),
            None,
        )

        if match is None:
            match = {"city": "Unknown", "weather": "25°C, Clear"}

        trace.add(f"Weather resolved for city: {match['city']}")

        return self.success(
            {
                "city": match["city"],
                "weather": match["weather"],
            },
            trace,
            message=f"The current weather in {match['city']} is {match['weather']}.",
        )

    def execute_live(self, task: str, trace):
        """
        Real OpenWeatherMap integration. Not wired into execute() by
        default — requires WEATHER_API_KEY to be set. Swap this in for
        execute() once you're ready to go live; tests for this path
        should mock the requests.get call rather than hitting the real API.
        """

        try:
            city = self.extract_city(task)
            api_key = os.getenv("WEATHER_API_KEY")

            if not api_key:
                return self.failure("WEATHER_API_KEY is not configured.", trace)

            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {"q": city, "appid": api_key, "units": "metric"}

            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()

            trace.add(f"Live weather fetched for {city}")

            return self.success(
                {
                    "city": data["name"],
                    "temperature": data["main"]["temp"],
                    "condition": data["weather"][0]["description"],
                    "humidity": data["main"]["humidity"],
                },
                trace,
            )

        except requests.exceptions.Timeout:
            return self.failure("Weather API timeout.", trace)
        except Exception as e:
            return self.failure(str(e), trace)

    def extract_city(self, task):
        """
        Simple extraction logic.
        Later we replace this with LLM extraction.
        """
        words = task.split()
        return words[-1]
