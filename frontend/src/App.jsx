import { useState, useEffect } from "react";

import Header from "./components/Header";
import TaskForm from "./components/TaskForm";
import ResultCard from "./components/ResultCard";
import TracePanel from "./components/TracePanel";

import { getHistory } from "./services/historyService";
import HistoryTable from "./components/HistoryTable";

function App() {

    const [result, setResult] = useState(null);
    const [history, setHistory] = useState([]);

        async function loadHistory() {
        const data = await getHistory();
        setHistory(data);
    }

    useEffect(() => {
        loadHistory();
    }, []);

    return (

        <div className="container mt-5">

            <Header />

            <TaskForm
                onResult={setResult}
                onTaskCompleted={loadHistory}
            />

            <ResultCard result={result} />

            <TracePanel trace={result?.trace} />

            <HistoryTable history={history} />

        </div>

    );

}

export default App;