from app.tools.weather_tool import WeatherTool


tool = WeatherTool()


task = "What is the weather in Toronto"


if tool.can_handle(task):

    result = tool.execute(task)

    print(result)

else:

    print("Weather tool cannot handle task")