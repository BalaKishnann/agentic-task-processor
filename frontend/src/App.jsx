import { useState } from "react";

import Header from "./components/Header";
import TaskForm from "./components/TaskForm";
import ResultCard from "./components/ResultCard";

function App() {

    const [result, setResult] = useState(null);

    return (

        <div className="container mt-5">

            <Header />

            <TaskForm onResult={setResult} />

            <ResultCard result={result} />

        </div>

    );

}

export default App;