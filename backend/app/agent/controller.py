class AgentController:

    def process(self, task: str):

        return {
            "status": "SUCCESS",
            "receivedTask": task,
            "message": "Agent received the task."
        }
