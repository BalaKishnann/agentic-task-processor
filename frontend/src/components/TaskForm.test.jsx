import { describe, it, expect, vi, beforeEach } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import TaskForm from "./TaskForm";
import { useTask } from "../context/TaskContext";

vi.mock("../context/TaskContext", () => ({
  useTask: vi.fn(),
}));

vi.mock("react-toastify", () => ({
  toast: { success: vi.fn(), error: vi.fn() },
}));

function renderTaskForm(overrides = {}) {
  useTask.mockReturnValue({
    submitTask: vi.fn().mockResolvedValue(undefined),
    loading: false,
    ...overrides,
  });

  return render(<TaskForm />);
}

describe("TaskForm", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("renders the input and submit button", () => {
    renderTaskForm();

    expect(
      screen.getByPlaceholderText(/example: calculate/i),
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /execute task/i }),
    ).toBeInTheDocument();
  });

  it("shows a validation error when submitting an empty task", async () => {
    const user = userEvent.setup();
    renderTaskForm();

    await user.click(screen.getByRole("button", { name: /execute task/i }));

    expect(await screen.findByText(/please enter a task/i)).toBeInTheDocument();
  });

  it("calls submitTask with trimmed input on valid submit", async () => {
    const submitTask = vi.fn().mockResolvedValue(undefined);
    const user = userEvent.setup();
    renderTaskForm({ submitTask });

    await user.type(
      screen.getByPlaceholderText(/example: calculate/i),
      "  calculate 5 + 3  ",
    );
    await user.click(screen.getByRole("button", { name: /execute task/i }));

    await waitFor(() => {
      expect(submitTask).toHaveBeenCalledWith("calculate 5 + 3");
    });
  });

  it("clears the input after successful submit", async () => {
    const user = userEvent.setup();
    renderTaskForm();

    const input = screen.getByPlaceholderText(/example: calculate/i);
    await user.type(input, "calculate 2 + 2");
    await user.click(screen.getByRole("button", { name: /execute task/i }));

    await waitFor(() => {
      expect(input).toHaveValue("");
    });
  });

  it("disables input and button while loading", () => {
    renderTaskForm({ loading: true });

    expect(screen.getByPlaceholderText(/example: calculate/i)).toBeDisabled();
    expect(screen.getByRole("button", { name: /processing/i })).toBeDisabled();
  });

  it("shows suggestions on focus", async () => {
    const user = userEvent.setup();
    renderTaskForm();

    await user.click(screen.getByPlaceholderText(/example: calculate/i));

    expect(await screen.findByText(/calculate 250 \* 8/i)).toBeInTheDocument();
  });

  it("fills and submits when a suggestion is clicked", async () => {
    const submitTask = vi.fn().mockResolvedValue(undefined);
    const user = userEvent.setup();
    renderTaskForm({ submitTask });

    await user.click(screen.getByPlaceholderText(/example: calculate/i));
    const suggestion = await screen.findByText(/calculate 250 \* 8/i);
    await user.click(suggestion);

    await waitFor(() => {
      expect(submitTask).toHaveBeenCalledWith("calculate 250 * 8");
    });
  });

  it("rejects a task over 500 characters via maxLength on the input", () => {
    renderTaskForm();

    const input = screen.getByPlaceholderText(/example: calculate/i);
    expect(input).toHaveAttribute("maxLength", "500");
  });
});
