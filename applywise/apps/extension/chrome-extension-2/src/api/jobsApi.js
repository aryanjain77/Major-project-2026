// src/api/jobsApi.js
// Content scripts cannot use ES module import/export in most MV3 setups.
// This file is loaded before content.js via manifest.json and exposes a small
// API helper on the window.

(function () {
  var API_BASE_URL = "http://localhost:3000/api/jobs";

  function getToken() {
    return new Promise(function (resolve) {
      try {
        chrome.storage.local.get("applywise_token", function (result) {
          resolve(result && result.applywise_token ? result.applywise_token : null);
        });
      } catch (e) {
        resolve(null);
      }
    });
  }

  async function request(path, options) {
    var token = await getToken();
    if (!token) {
      console.error("[ApplyWise] Missing applywise_token in chrome.storage.local; skipping request:", path);
      throw new Error("Not authenticated: missing applywise_token");
    }

    var headers = Object.assign(
      { "Content-Type": "application/json", "Authorization": "Bearer " + token },
      (options && options.headers) || {}
    );

    var res = await fetch(API_BASE_URL + (path || ""), Object.assign({}, options || {}, { headers: headers }));
    var text = await res.text();
    var data = text ? JSON.parse(text) : null;

    if (!res.ok) {
      var message = (data && data.message) ? data.message : ("Request failed (" + res.status + ")");
      var err = new Error(message);
      err.status = res.status;
      err.data = data;
      throw err;
    }

    return data;
  }

  async function getJobs() {
    return request("", { method: "GET" });
  }

  async function createJob(payload) {
    return request("", { method: "POST", body: JSON.stringify(payload || {}) });
  }

  // Your backend currently supports PUT. The plan asked for PATCH, so we attempt
  // PATCH first and fall back to PUT if needed without changing UI behavior.
  async function updateJob(id, updates) {
    var safeId = encodeURIComponent(id);
    try {
      return await request("/" + safeId, { method: "PATCH", body: JSON.stringify(updates || {}) });
    } catch (e) {
      if (e && (e.status === 404 || e.status === 405)) {
        return request("/" + safeId, { method: "PUT", body: JSON.stringify(updates || {}) });
      }
      throw e;
    }
  }

  async function deleteJob(id) {
    return request("/" + encodeURIComponent(id), { method: "DELETE" });
  }

  window.ApplyWiseJobsApi = {
    getJobs: getJobs,
    createJob: createJob,
    updateJob: updateJob,
    deleteJob: deleteJob,
  };
})();

