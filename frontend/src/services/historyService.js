import API from "./api";

export async function getHistory() {
  const response = await API.get("/tasks/history");
  return response.data;
}

export async function clearHistory() {
  const response = await API.delete("/tasks/history");
  return response.data;
}

export async function deleteHistoryEntry(id) {
  const response = await API.delete(`/tasks/history/${id}`);
  return response.data;
}
