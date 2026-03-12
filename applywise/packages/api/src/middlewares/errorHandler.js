// Generic error-handling middleware to avoid unhandled exceptions leaking details
// Business logic and status codes from controllers remain unchanged.
// This only catches errors passed to `next(err)` or thrown in async handlers.
const errorHandler = (err, req, res, next) => {
  console.error(err);

  if (res.headersSent) {
    return next(err);
  }

  const status = err.status || 500;
  const message = err.message || "Internal Server Error";

  res.status(status).json({
    success: false,
    message,
  });
};

module.exports = { errorHandler };

