const mongoose = require("mongoose");
const { env } = require("./env");

const connectDB = () => {
  if (!env.mongoUri) {
    console.error("MONGO_URI is not defined");
    return;
  }

  mongoose
    .connect(env.mongoUri)
    .then(() => {
      console.log("connected to database");
    })
    .catch((error) => {
      console.log(error);
    });
};

module.exports = { connectDB };

