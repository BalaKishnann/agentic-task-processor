import API from "./api";

export async function getHistory() {

    const response = await API.get("/tasks/history");

    return response.data;

}