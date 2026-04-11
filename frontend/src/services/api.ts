import axios from "axios"

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "/api",
})

export const wsUrl = import.meta.env.VITE_WS_URL || "ws://localhost:8000/ws"

export default api

// Teams
export const getTeams = () => api.get("/v1/teams/")
export const createTeam = (data: any) => api.post("/v1/teams/", data)
export const updateTeam = (id: number, data: any) => api.patch(`/v1/teams/${id}/`, data)

// Scores
export const getScores = () => api.get("/v1/scores/")
export const createScore = (data: any) => api.post("/v1/scores/", data)

// Quests
export const getQuests = () => api.get("/v1/quests/")