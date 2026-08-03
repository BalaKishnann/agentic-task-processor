class ExecutionTrace:

    def __init__(self):
        self.steps = []

    def add(self, message: str):
        self.steps.append(message)

    def get_steps(self):
        return self.steps

    def get_trace(self):
        return self.steps
