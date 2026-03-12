const env = {
  nodeEnv: process.env.NODE_ENV || "development",
  port: process.env.PORT || 3000,
  mongoUri: process.env.MONGO_URI,
  tokenSecret: process.env.TOKEN_SECRET,
  codeSendingEmail: process.env.NODE_CODE_SENDING_EMAIL_ADDRESS,
  verificationCodeSecret: process.env.HMAC_VERIFICATION_CODE_SECRET,
  firebaseProjectId: process.env.FIREBASE_PROJECT_ID,
  firebaseClientEmail: process.env.FIREBASE_CLIENT_EMAIL,
  firebasePrivateKey: process.env.FIREBASE_PRIVATE_KEY,
  aiServiceUrl: process.env.AI_SERVICE_URL,
};

module.exports = { env };

