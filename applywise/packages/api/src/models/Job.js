const mongoose = require("mongoose");

// MongoDB job model (Phase 7).
// Core fields required by the task: userId, company, role, status, jobLink, notes
// plus createdAt/updatedAt via timestamps.
//
// Backward-compat fields are included so existing clients can continue sending/receiving
// the Firestore-shaped payload (email, link, dateApplied, etc.) without breaking.
const jobSchema = new mongoose.Schema(
  {
    userId: { type: String, required: true, index: true },

    company: { type: String, required: true },
    role: { type: String, required: true },
    status: { type: String, required: true },

    // Task field name
    jobLink: { type: String, default: "" },

    notes: { type: String, default: "" },

    // Backward compatibility with existing clients
    email: { type: String, default: "" },
    stipend: { type: String, default: "" },
    description: { type: String, default: "" },
    link: { type: String, default: "" }, // original client field
    source: { type: String, default: "" },
    dateApplied: { type: String, default: "" },
    timestamp: { type: String, default: "" }, // ISO string for compatibility
  },
  { timestamps: true }
);

module.exports = mongoose.models.Job || mongoose.model("Job", jobSchema);

