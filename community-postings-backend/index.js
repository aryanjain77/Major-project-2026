const express = require("express");
const helmet = require("helmet");
const cors = require("cors");
const cookieParser = require("cookie-parser");
const mongoose = require("mongoose");
const authRouter = require("./routers/authRouter.js");
const postsRouter = require("./routers/postsRouter.js");
const dns = require('dns');

const app = express();
app.use(cors());
app.use(helmet());
app.use(cookieParser());
app.use(express.json());
app.use(express.urlencoded({extended: true}));

dns.setServers(["8.8.8.8"]);

mongoose.connect(process.env.MONGO_URI).then(()=> {
    console.log("connected to database");
}).catch((error)=>{
    console.log(error);
});

app.use("/api/posts", postsRouter)
app.use("/api/auth", authRouter);

app.get("/", (req, res)=>{
    res.json({message :"hello from the server"});
})

app.listen(process.env.PORT, ()=> {
    console.log(`listening on port ${process.env.PORT}`);
});
