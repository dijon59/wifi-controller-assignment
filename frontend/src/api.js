

const API_BASE_URL = "http://localhost:8000"

async function request (path) {
    const response = await fetch(`${API_BASE_URL}${path}`, {
        headers: {
            "Content-Type": "application/json"
        }
    })
}
