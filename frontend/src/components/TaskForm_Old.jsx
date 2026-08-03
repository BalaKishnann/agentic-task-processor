import { useState } from "react";
import API from "../services/api";

const MAX_TASK_LENGTH = 500;

function TaskForm({ onResult, onTaskCompleted }) {
  const [task, setTask] = useState("");
  const [error, setError] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);

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

  async function executeTask() {
    const validationError = validateTask(task);

    if (validationError) {
      setError(validationError);
      return;
    }

    setError("");
    setIsSubmitting(true);

    try {
      const response = await API.post("/tasks", {
        task: task.trim(),
      });

      onResult(response.data);
      onTaskCompleted();
    } catch (err) {
      console.error(err);

      const message =
        err.response?.data?.message ||
        "Something went wrong while processing your task. Please try again.";

      setError(message);
    } finally {
      setIsSubmitting(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !isSubmitting) {
      executeTask();
    }
  }

  return (
    <div className="card shadow-sm">
      <div className="card-body">
        <h4>Enter Task</h4>

        <input
          type="text"
          className={`form-control ${error ? "is-invalid" : ""}`}
          placeholder="Example: Calculate 250 * 8"
          value={task}
          maxLength={MAX_TASK_LENGTH}
          onChange={(e) => {
            setTask(e.target.value);
            if (error) setError("");
          }}
          onKeyDown={handleKeyDown}
          disabled={isSubmitting}
        />

        {error && (
          <div className="text-danger mt-2" role="alert">
            {error}
          </div>
        )}

        <button
          className="btn btn-primary mt-3"
          onClick={executeTask}
          disabled={isSubmitting}
        >
          {isSubmitting ? "Processing..." : "Execute Task"}
        </button>
      </div>
    </div>
  );
}

export default TaskForm;
