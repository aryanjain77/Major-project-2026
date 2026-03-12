const express = require("express");
const helmet = require("helmet");
const cors = require("cors");
const cookieParser = require("cookie-parser");
const dns = require("dns");
const authRouter = require("./routes/authRouter");
const postsRouter = require("./routes/postsRouter");
const jobsRouter = require("./routes/jobsRouter");
const aiRouter = require("./routes/aiRouter");
const { connectDB } = require("./config/db");
const { env } = require("./config/env");
const { rateLimiter } = require("./middlewares/rateLimiter");
const { errorHandler } = require("./middlewares/errorHandler");

const app = express();

app.use(cors());
app.use(helmet());
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(rateLimiter);

dns.setServers(["8.8.8.8"]);
connectDB();

app.use("/api/posts", postsRouter);
app.use("/api/auth", authRouter);
app.use("/api/jobs", jobsRouter);
app.use("/api/ai", aiRouter);

app.get("/api/health", (req, res) => {
    res.json({ status: "ok" });
});

app.get("/", (req, res) => {
    res.json({ message: "hello from the server" });
});

app.use(errorHandler);

app.listen(env.port, () => {
    console.log(`listening on port ${env.port}`);
});
