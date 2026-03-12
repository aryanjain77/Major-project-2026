const { classifyEmailText } = require("../services/aiService");

exports.classify = async (req, res) => {
  const { emailText } = req.body || {};

  if (!emailText || typeof emailText !== "string") {
    return res.status(400).json({
      success: false,
      message: "emailText is required",
    });
  }

  try {
    const result = await classifyEmailText(emailText);
    return res.json({ success: true, ...result });
  } catch (err) {
    console.error("AI classify error:", err);
    return res.status(502).json({
      success: false,
      message: "AI service unavailable",
    });
  }
};

