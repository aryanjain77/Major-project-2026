// Very simple in-memory rate limiter to protect the API.
// The limit is intentionally high to avoid affecting normal usage.
const windowMs = 15 * 60 * 1000; // 15 minutes
const maxRequests = 1000;

const ipStore = new Map();

const rateLimiter = (req, res, next) => {
  const now = Date.now();
  const ip = req.ip || req.connection.remoteAddress || "unknown";

  const entry = ipStore.get(ip) || { count: 0, start: now };

  if (now - entry.start > windowMs) {
    entry.count = 0;
    entry.start = now;
  }

  entry.count += 1;
  ipStore.set(ip, entry);

  if (entry.count > maxRequests) {
    return res.status(429).json({
      success: false,
      message: "Too many requests, please try again later.",
    });
  }

  next();
};

module.exports = { rateLimiter };

