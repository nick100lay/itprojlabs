


export const API_URL = process.env.REACT_APP_API_URL

export function getApiUrl(endpoint) {
    return API_URL + "/" + endpoint;
}


export const API_ENDPOINTS = {
    PLAYERS: "players",
    CURRENT_MATCHES: "current-matches",
    COMPLETED_MATCHES: "completed-matches"
}