import { useEffect } from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import Header from "./components/Header";
import TaskForm from "./components/TaskForm";
import ResultCard from "./components/ResultCard";
import TracePanel from "./components/TracePanel";
import HistoryTable from "./components/HistoryTable";
import ErrorBoundary from "./components/ErrorBoundary";

import { TaskProvider, useTask } from "./context/TaskContext";

function AppContent() {
  const {
    result,
    history,
    loading,
    error,
    loadHistory,
    clearHistory,
    deleteHistoryEntry,
    clearError,
  } = useTask();

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  return (
    <div className="container mt-5">
      <Header />

      <ErrorBoundary message="The task form ran into a problem.">
        <TaskForm />
      </ErrorBoundary>

      {error && (
        <div
          className="alert alert-danger mt-3 d-flex justify-content-between align-items-center"
          role="alert"
        >
          <span>{error}</span>
          <button
            className="btn-close"
            onClick={clearError}
            aria-label="Dismiss"
          ></button>
        </div>
      )}

      <ErrorBoundary message="Couldn't display task history.">
        <div className="d-flex justify-content-between align-items-center mt-4 mb-2">
          <h5 className="mb-0">Task History</h5>
          {history.length > 0 && (
            <button
              className="btn btn-sm btn-outline-danger"
              onClick={() => {
                if (
                  window.confirm(
                    "Clear all task history? This cannot be undone.",
                  )
                ) {
                  clearHistory();
                }
              }}
            >
              Clear History
            </button>
          )}
        </div>
        <HistoryTable history={history} onDeleteEntry={deleteHistoryEntry} />
      </ErrorBoundary>

      <ErrorBoundary message="Couldn't display the result.">
        <ResultCard result={result} />
      </ErrorBoundary>

      <ErrorBoundary message="Couldn't display the execution trace.">
        <TracePanel trace={result?.trace} />
      </ErrorBoundary>

      <ErrorBoundary message="Couldn't display task history.">
        <HistoryTable history={history} />
      </ErrorBoundary>

      <ToastContainer position="top-right" autoClose={3000} />
    </div>
  );
}

function App() {
  return (
    <ErrorBoundary message="The app ran into an unexpected error.">
      <TaskProvider>
        <AppContent />
      </TaskProvider>
    </ErrorBoundary>
  );
}

export default App;
