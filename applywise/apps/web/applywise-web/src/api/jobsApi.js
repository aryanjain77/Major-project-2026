const API_BASE_URL = "http://localhost:3000/api/jobs";

function getToken() {
  return localStorage.getItem("applywise_token") || "";
}

async function request(path = "", options = {}) {
  const token = getToken();

  const headers = {
    "Content-Type": "application/json",
    ...(options.headers || {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers,
    // Keep cookie-based auth compatible for existing flows
    credentials: "include",
  });

  const text = await res.text();
  const data = text ? JSON.parse(text) : null;

  if (!res.ok) {
    const message = data?.message || `Request failed (${res.status})`;
    const err = new Error(message);
    err.status = res.status;
    err.data = data;
    throw err;
  }

  return data;
}

export async function getJobs() {
  return request("", { method: "GET" });
}

export async function createJob(job) {
  return request("", { method: "POST", body: JSON.stringify(job) });
}

export async function updateJob(id, updates) {
  return request(`/${encodeURIComponent(id)}`, {
    method: "PUT",
    body: JSON.stringify(updates),
  });
}

export async function deleteJob(id) {
  return request(`/${encodeURIComponent(id)}`, { method: "DELETE" });
}

