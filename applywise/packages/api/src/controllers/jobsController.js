const Job = require("../models/Job");

// GET /api/jobs
// Returns jobs for the authenticated userId, sorted by timestamp/createdAt desc.
exports.getJobs = async (req, res) => {
  const { userId } = req.user || {};

  if (!userId) {
    return res.status(403).json({ success: false, message: "Unauthorized" });
  }

  try {
    const docs = await Job.find({ userId }).sort({ createdAt: -1 }).lean();

    const jobs = docs.map((d) => {
      const id = d._id.toString();
      // Prefer legacy `link` field in responses, but also support task's `jobLink`
      const link = d.link || d.jobLink || "";
      return {
        id,
        ...d,
        _id: undefined,
        link,
      };
    });

    res.json({ success: true, data: jobs });
  } catch (error) {
    console.error("Error fetching jobs:", error);
    res.status(500).json({ success: false, message: "Failed to fetch jobs" });
  }
};

// POST /api/jobs
// Creates a new job for the authenticated user.
exports.createJob = async (req, res) => {
  const { userId, email } = req.user || {};
  const {
    company,
    role,
    status,
    stipend = "",
    description = "",
    link = "",
    notes = "",
    dateApplied,
    source = "api",
  } = req.body || {};

  if (!userId) return res.status(403).json({ success: false, message: "Unauthorized" });

  if (!company || !role || !status) {
    return res.status(400).json({
      success: false,
      message: "company, role, and status are required",
    });
  }

  const job = {
    userId,
    email: email || "",
    company: company.trim(),
    role: role.trim(),
    status,
    stipend: stipend.trim ? stipend.trim() : stipend,
    description: description.trim ? description.trim() : description,
    link: link.trim ? link.trim() : link,
    jobLink: (link && link.trim) ? link.trim() : link,
    notes: notes.trim ? notes.trim() : notes,
    source,
    dateApplied:
      dateApplied || new Date().toISOString().split("T")[0],
    timestamp: new Date().toISOString(),
  };

  try {
    const created = await Job.create(job);
    res.status(201).json({
      success: true,
      data: { id: created._id.toString(), ...job },
    });
  } catch (error) {
    console.error("Error creating job:", error);
    res.status(500).json({ success: false, message: "Failed to create job" });
  }
};

// PUT/PATCH /api/jobs/:id
// Updates an existing job owned by the authenticated user.
exports.updateJob = async (req, res) => {
  const { id } = req.params;
  const { userId } = req.user || {};
  const updates = req.body || {};

  if (!id) {
    return res.status(400).json({ success: false, message: "Job id is required" });
  }

  if (!userId) return res.status(403).json({ success: false, message: "Unauthorized" });

  try {
    const allowedFields = [
      "company",
      "role",
      "status",
      "stipend",
      "description",
      "link",
      "notes",
      "dateApplied",
    ];

    const sanitizedUpdates = {};
    for (const key of allowedFields) {
      if (updates[key] !== undefined) {
        sanitizedUpdates[key] = updates[key];
      }
    }

    // keep jobLink in sync if link changes
    if (sanitizedUpdates.link !== undefined) {
      sanitizedUpdates.jobLink = sanitizedUpdates.link;
    }

    if (Object.keys(sanitizedUpdates).length === 0) {
      return res
        .status(400)
        .json({ success: false, message: "No valid fields to update" });
    }

    const updated = await Job.findOneAndUpdate(
      { _id: id, userId },
      { $set: sanitizedUpdates },
      { new: true }
    ).lean();

    if (!updated) {
      return res.status(404).json({ success: false, message: "Job not found" });
    }

    res.json({ success: true, message: "Job updated" });
  } catch (error) {
    console.error("Error updating job:", error);
    res.status(500).json({ success: false, message: "Failed to update job" });
  }
};

// DELETE /api/jobs/:id
// Deletes a job owned by the authenticated user.
exports.deleteJob = async (req, res) => {
  const { id } = req.params;
  const { userId } = req.user || {};

  if (!id) {
    return res.status(400).json({ success: false, message: "Job id is required" });
  }

  if (!userId) return res.status(403).json({ success: false, message: "Unauthorized" });

  try {
    const deleted = await Job.findOneAndDelete({ _id: id, userId }).lean();
    if (!deleted) {
      return res.status(404).json({ success: false, message: "Job not found" });
    }
    res.json({ success: true, message: "Job deleted" });
  } catch (error) {
    console.error("Error deleting job:", error);
    res.status(500).json({ success: false, message: "Failed to delete job" });
  }
};

// GET /api/jobs/:id
exports.getJobById = async (req, res) => {
  const { id } = req.params;
  const { userId } = req.user || {};

  if (!id) return res.status(400).json({ success: false, message: "Job id is required" });
  if (!userId) return res.status(403).json({ success: false, message: "Unauthorized" });

  try {
    const doc = await Job.findOne({ _id: id, userId }).lean();
    if (!doc) return res.status(404).json({ success: false, message: "Job not found" });

    const link = doc.link || doc.jobLink || "";
    return res.json({
      success: true,
      data: { id: doc._id.toString(), ...doc, _id: undefined, link },
    });
  } catch (error) {
    console.error("Error fetching job:", error);
    return res.status(500).json({ success: false, message: "Failed to fetch job" });
  }
};

