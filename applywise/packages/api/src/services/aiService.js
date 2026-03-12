const { env } = require("../config/env");

const DEFAULT_AI_URL = "http://localhost:5000";

function getAiBaseUrl() {
  return process.env.AI_SERVICE_URL || env.aiServiceUrl || DEFAULT_AI_URL;
}

async function classifyEmailText(text) {
  const baseUrl = getAiBaseUrl();
  const url = `${baseUrl.replace(/\/+$/, "")}/classify`;

  // Node 18+ has global fetch. If you're on an older Node, add a fetch polyfill.
  if (typeof fetch !== "function") {
    throw new Error("fetch is not available in this Node runtime");
  }

  const res = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  const data = await res.json().catch(() => null);

  if (!res.ok) {
    const msg = data?.message || `AI service error (${res.status})`;
    const err = new Error(msg);
    err.status = res.status;
    err.data = data;
    throw err;
  }

  return data; // expected: { type: "rejected|interview|oa|hr|selected" }
}

module.exports = { classifyEmailText };

