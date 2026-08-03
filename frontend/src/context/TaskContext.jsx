import { createContext, useContext, useReducer, useCallback } from "react";
import { getHistory } from "../services/historyService";
import API from "../services/api";

const TaskContext = createContext(null);

const initialState = {
  result: null,
  history: [],
  loading: false,
  error: null,
};

function taskReducer(state, action) {
  switch (action.type) {
    case "SUBMIT_START":
      return { ...state, loading: true, error: null };

    case "SUBMIT_SUCCESS":
      return {
        ...state,
        loading: false,
        result: action.payload,
        // Reconcile the optimistic entry with the real response.
        history: state.history.map((item) =>
          item.id === action.optimisticId
            ? { ...action.payload, id: action.payload.id ?? item.id }
            : item,
        ),
      };

    case "SUBMIT_ERROR":
      return {
        ...state,
        loading: false,
        error: action.payload,
        // Mark the optimistic entry as failed rather than removing it,
        // so the user sees what was attempted and that it didn't work.
        history: state.history.map((item) =>
          item.id === action.optimisticId
            ? { ...item, status: "FAILED", message: action.payload }
            : item,
        ),
      };

    case "ADD_OPTIMISTIC_TASK":
      return {
        ...state,
        history: [action.payload, ...state.history],
      };

    case "SET_HISTORY":
      return { ...state, history: action.payload };

    case "CLEAR_ERROR":
      return { ...state, error: null };

    default:
      return state;
  }
}

export function TaskProvider({ children }) {
  const [state, dispatch] = useReducer(taskReducer, initialState);

  const loadHistory = useCallback(async () => {
    try {
      const data = await getHistory();
      dispatch({ type: "SET_HISTORY", payload: data });
    } catch (err) {
      dispatch({
        type: "SUBMIT_ERROR",
        payload: "Failed to load task history.",
      });
    }
  }, []);

  const submitTask = useCallback(async (taskText) => {
    // Optimistic entry: shows in the history list immediately, before
    // the request resolves, so the UI doesn't feel like it's waiting
    // on a round-trip before anything happens.
    const optimisticId = `optimistic-${Date.now()}`;

    dispatch({
      type: "ADD_OPTIMISTIC_TASK",
      payload: {
        id: optimisticId,
        task: taskText,
        status: "PENDING",
        tool: null,
        result: null,
        trace: [],
        created_at: new Date().toISOString(),
      },
    });

    dispatch({ type: "SUBMIT_START" });

    try {
      const response = await API.post("/tasks", { task: taskText });
      dispatch({
        type: "SUBMIT_SUCCESS",
        payload: response.data,
        optimisticId,
      });
    } catch (err) {
      const message =
        err.response?.data?.message ||
        "Something went wrong while processing your task. Please try again.";
      dispatch({ type: "SUBMIT_ERROR", payload: message, optimisticId });
    }
  }, []);

  const clearError = useCallback(() => {
    dispatch({ type: "CLEAR_ERROR" });
  }, []);

  const value = {
    result: state.result,
    history: state.history,
    loading: state.loading,
    error: state.error,
    submitTask,
    loadHistory,
    clearError,
  };

  return <TaskContext.Provider value={value}>{children}</TaskContext.Provider>;
}

export function useTask() {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error("useTask must be used within a TaskProvider");
  }
  return context;
}
