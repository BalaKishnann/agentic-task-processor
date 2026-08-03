import { useState } from "react";
import { useTask } from "../context/TaskContext";

const MAX_TASK_LENGTH = 500;

function TaskForm() {
  const { submitTask, loading } = useTask();

  const [task, setTask] = useState("");
  const [validationError, setValidationError] = useState("");

  function validateTask(value) {
    const trimmed = value.trim();

    if (trimmed.length === 0) {
      return "Please enter a task before submitting.";
    }
    if (trimmed.length > MAX_TASK_LENGTH) {
      return `Task must be under ${MAX_TASK_LENGTH} characters.`;
    }
    return null;
  }

  async function handleSubmit() {
    const error = validateTask(task);

    if (error) {
      setValidationError(error);
      return;
    }

    setValidationError("");
    await submitTask(task.trim());
    setTask("");
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !loading) {
      handleSubmit();
    }
  }

  return (
    <div className="card shadow-sm">
      <div className="card-body">
        <h4>Enter Task</h4>

        <input
          type="text"
          className={`form-control ${validationError ? "is-invalid" : ""}`}
          placeholder="Example: Calculate 250 * 8"
          value={task}
          maxLength={MAX_TASK_LENGTH}
          onChange={(e) => {
            setTask(e.target.value);
            if (validationError) setValidationError("");
          }}
          onKeyDown={handleKeyDown}
          disabled={loading}
        />

        {validationError && (
          <div className="text-danger mt-2" role="alert">
            {validationError}
          </div>
        )}

        <button
          className="btn btn-primary mt-3"
          onClick={handleSubmit}
          disabled={loading}
        >
          {loading ? "Processing..." : "Execute Task"}
        </button>
      </div>
    </div>
  );
}

export default TaskForm;
