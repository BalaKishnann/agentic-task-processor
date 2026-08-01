import requests
import os

from app.tools.base_tool import BaseTool


class WeatherTool(BaseTool):


    def can_handle(self, task: str) -> bool:

        keywords = [
            "weather",
            "temperature",
            "forecast",
            "climate"
        ]

        return any(
            word in task.lower()
            for word in keywords
        )

    def execute(self, task: str):

        task_lower = task.lower()

        if "toronto" in task_lower:
            city = "Toronto"
            weather = "22°C, Sunny"

        elif "vancouver" in task_lower:
            city = "Vancouver"
            weather = "18°C, Cloudy"

        elif "montreal" in task_lower:
            city = "Montreal"
            weather = "20°C, Partly Cloudy"

        else:
            city = "Unknown"
            weather = "25°C, Clear"

        return {
            "tool": "WeatherMockTool",
            "city": city,
            "weather": weather,
            "message": f"The current weather in {city} is {weather}."
        }


    def execute_Ori(self, task: str):

        try:

            city = self.extract_city(task)


            api_key = os.getenv(
                "WEATHER_API_KEY"
            )


            url = (
                "https://api.openweathermap.org/data/2.5/weather"
            )


            params = {

                "q": city,

                "appid": api_key,

                "units": "metric"

            }


            response = requests.get(
                url,
                params=params,
                timeout=5
            )


            response.raise_for_status()


            data = response.json()


            return {

                "tool": "Weather",

                "city":
                    data["name"],

                "temperature":
                    data["main"]["temp"],

                "condition":
                    data["weather"][0]["description"],

                "humidity":
                    data["main"]["humidity"]

            }


        except requests.exceptions.Timeout:


            return {

                "tool": "Weather",

                "error":
                "Weather API timeout"

            }


        except Exception as e:


            return {

                "tool": "Weather",

                "error":
                str(e)

            }



    def extract_city(self, task):

        """
        Simple extraction logic.
        Later we replace this with LLM extraction.
        """

        words = task.split()

        return words[-1]