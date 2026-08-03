import ast
import operator
import re

from app.tools.base_tool import BaseTool


class CalculatorTool(BaseTool):

    # Only these AST node types / operators are permitted.
    # Anything else (names, calls, attributes, subscripts, etc.) is rejected.
    _ALLOWED_OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def can_handle(self, task: str) -> bool:

        task = task.lower()

        keywords = ["calculate", "add", "subtract", "multiply", "divide"]

        return any(word in task for word in keywords)

    def execute_old(self, task: str, trace):

        expression = self.parse_expression(task)
        trace.add(f"Expression extracted: {expression}")

        if expression is None:
            return {
                "tool": "Calculator",
                "status": "FAILED",
                "message": "Unable to identify a valid mathematical expression.",
            }

        try:
            result = self.safe_eval(expression)
            trace.add("Calculation completed successfully.")
            return {
                "tool": "Calculator",
                "status": "SUCCESS",
                "result": {"expression": expression, "value": result},
                "trace": trace.get_steps(),
            }

        except ZeroDivisionError:
            return {
                "tool": "Calculator",
                "status": "FAILED",
                "message": "Division by zero is not allowed.",
            }
        except Exception as ex:
            return {
                "tool": "Calculator",
                "status": "FAILED",
                "message": f"Invalid expression: {ex}",
            }

    def execute(self, task: str, trace):

        expression = self.parse_expression(task)
        trace.add(f"Expression extracted: {expression}")

        if expression is None:
            return self.failure(
                "Unable to identify a valid mathematical expression.",
                trace,
            )

        try:
            result = self.safe_eval(expression)
            trace.add("Calculation completed successfully.")
            return self.success(
                {"expression": expression, "value": result},
                trace,
            )

        except ZeroDivisionError:
            return self.failure("Division by zero is not allowed.", trace)
        except Exception as ex:
            return self.failure(f"Invalid expression: {ex}", trace)

    def parse_expression(self, task: str):

        task = task.lower()

        task = task.replace("calculate", "")

        match = re.search(r"(\d+\s*[\+\-\*/]\s*\d+)", task)

        if match:
            return match.group(1)

        return None

    def safe_eval(self, expression: str):
        """
        Safely evaluate a simple arithmetic expression string
        (e.g. "3 + 4", "10 / 2") without using eval().

        Parses the expression into an AST and recursively walks it,
        allowing only numeric literals and the arithmetic operators
        listed in _ALLOWED_OPERATORS. Anything else (names, function
        calls, attribute access, imports, etc.) raises a ValueError,
        so arbitrary code execution is not possible.
        """
        node = ast.parse(expression, mode="eval").body
        return self._eval_node(node)

    def _eval_node(self, node):

        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant: {node.value!r}")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in self._ALLOWED_OPERATORS:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return self._ALLOWED_OPERATORS[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in self._ALLOWED_OPERATORS:
                raise ValueError(f"Unsupported operator: {op_type.__name__}")
            operand = self._eval_node(node.operand)
            return self._ALLOWED_OPERATORS[op_type](operand)

        raise ValueError(f"Unsupported expression element: {type(node).__name__}")
