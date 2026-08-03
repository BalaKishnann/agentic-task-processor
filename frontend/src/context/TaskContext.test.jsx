import { describe, it, expect, vi, beforeEach } from "vitest";
import { renderHook, act, waitFor } from "@testing-library/react";

import { TaskProvider, useTask } from "./TaskContext";
import { getHistory } from "../services/historyService";
import API from "../services/api";

vi.mock("../services/historyService", () => ({
  getHistory: vi.fn(),
}));

vi.mock("../services/api", () => ({
  default: {
    post: vi.fn(),
  },
}));

function wrapper({ children }) {
  return <TaskProvider>{children}</TaskProvider>;
}

describe("TaskContext", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe("useTask outside provider", () => {
    it("throws when used without a TaskProvider", () => {
      // Suppress the expected React error log for this one test.
      const consoleError = vi
        .spyOn(console, "error")
        .mockImplementation(() => {});

      expect(() => renderHook(() => useTask())).toThrow(
        "useTask must be used within a TaskProvider",
      );

      consoleError.mockRestore();
    });
  });

  describe("initial state", () => {
    it("starts with empty result, history, and no loading/error", () => {
      const { result } = renderHook(() => useTask(), { wrapper });

      expect(result.current.result).toBeNull();
      expect(result.current.history).toEqual([]);
      expect(result.current.loading).toBe(false);
      expect(result.current.error).toBeNull();
    });
  });

  describe("loadHistory", () => {
    it("populates history on success", async () => {
      getHistory.mockResolvedValue([
        { id: 1, task: "calculate 2 + 2", status: "SUCCESS" },
      ]);

      const { result } = renderHook(() => useTask(), { wrapper });

      await act(async () => {
        await result.current.loadHistory();
      });

      expect(result.current.history).toHaveLength(1);
      expect(result.current.history[0].task).toBe("calculate 2 + 2");
    });

    it("sets an error if the history fetch fails", async () => {
      getHistory.mockRejectedValue(new Error("network error"));

      const { result } = renderHook(() => useTask(), { wrapper });

      await act(async () => {
        await result.current.loadHistory();
      });

      expect(result.current.error).toBe("Failed to load task history.");
    });
  });

  describe("submitTask", () => {
    it("adds an optimistic PENDING entry immediately", async () => {
      let resolvePost;
      API.post.mockReturnValue(
        new Promise((resolve) => {
          resolvePost = resolve;
        }),
      );

      const { result } = renderHook(() => useTask(), { wrapper });

      act(() => {
        result.current.submitTask("calculate 5 + 5");
      });

      // Before the API call resolves, the optimistic entry should
      // already be in history with PENDING status.
      expect(result.current.history).toHaveLength(1);
      expect(result.current.history[0].status).toBe("PENDING");
      expect(result.current.history[0].task).toBe("calculate 5 + 5");
      expect(result.current.loading).toBe(true);

      // Resolve to avoid an unhandled promise dangling into other tests.
      await act(async () => {
        resolvePost({ data: { status: "SUCCESS", result: { value: 10 } } });
      });
    });

    it("reconciles the optimistic entry with the real response on success", async () => {
      API.post.mockResolvedValue({
        data: {
          tool: "CalculatorTool",
          status: "SUCCESS",
          result: { expression: "5 + 5", value: 10 },
          message: null,
          trace: ["Expression extracted: 5 + 5"],
        },
      });

      const { result } = renderHook(() => useTask(), { wrapper });

      await act(async () => {
        await result.current.submitTask("calculate 5 + 5");
      });

      expect(result.current.loading).toBe(false);
      expect(result.current.result.status).toBe("SUCCESS");
      expect(result.current.history).toHaveLength(1);
      expect(result.current.history[0].status).toBe("SUCCESS");
    });

    it("marks the optimistic entry as FAILED on API error", async () => {
      API.post.mockRejectedValue({
        response: { data: { message: "Invalid expression" } },
      });

      const { result } = renderHook(() => useTask(), { wrapper });

      await act(async () => {
        await result.current.submitTask("calculate garbage");
      });

      expect(result.current.loading).toBe(false);
      expect(result.current.error).toBe("Invalid expression");
      expect(result.current.history).toHaveLength(1);
      expect(result.current.history[0].status).toBe("FAILED");
    });

    it("falls back to a generic error message when the API error has no message", async () => {
      API.post.mockRejectedValue(new Error("network down"));

      const { result } = renderHook(() => useTask(), { wrapper });

      await act(async () => {
        await result.current.submitTask("calculate 1 + 1");
      });

      expect(result.current.error).toBe(
        "Something went wrong while processing your task. Please try again.",
      );
    });
  });

  describe("clearError", () => {
    it("resets error to null", async () => {
      getHistory.mockRejectedValue(new Error("fail"));

      const { result } = renderHook(() => useTask(), { wrapper });

      await act(async () => {
        await result.current.loadHistory();
      });

      expect(result.current.error).not.toBeNull();

      act(() => {
        result.current.clearError();
      });

      expect(result.current.error).toBeNull();
    });
  });
});
