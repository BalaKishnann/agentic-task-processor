import { useState } from "react";
import API from "../services/api";

function TaskForm({ onResult }) {

    const [task, setTask] = useState("");

    async function executeTask() {

        try {
            console.log("Sending request...");

            const response = await API.post("/tasks", {
                task: task
            });

            onResult(response.data);
            console.log("Response received:");
            console.log(response.data);

        } catch (error) {

            console.error(error);

        }

    }

    return (

        <div className="card shadow-sm">

            <div className="card-body">

                <h4>Enter Task</h4>

                <input
                    type="text"
                    className="form-control"
                    placeholder="Example: Calculate 250 * 8"
                    value={task}
                    onChange={(e) => setTask(e.target.value)}
                />

                <button
                    className="btn btn-primary mt-3"
                    onClick={executeTask}
                >
                    Execute Task
                </button>

            </div>

        </div>

    );

}

export default TaskForm;