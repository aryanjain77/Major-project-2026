const mongoose = require("mongoose");

// Job schema mirrors the Firestore job document used by the dashboard and extension.
// In this phase, persistence is still handled by Firestore; this schema is used
// for validation/typing and prepares for a future Mongo migration.
const jobSchema = new mongoose.Schema(
  {
    userId: { type: String, required: true },
    email: { type: String, required: true, index: true },
    company: { type: String, required: true },
    role: { type: String, required: true },
    status: { type: String, required: true },
    stipend: { type: String, default: "" },
    description: { type: String, default: "" },
    link: { type: String, default: "" },
    notes: { type: String, default: "" },
    source: { type: String, default: "api" },
    dateApplied: { type: String }, // stored as ISO date string (YYYY-MM-DD)
    timestamp: { type: Date }, // stored as JS Date; Firestore will convert to Timestamp
  },
  {
    timestamps: false,
  }
);

const Job = mongoose.models.Job || mongoose.model("Job", jobSchema);

module.exports = Job;

