const admin = require("firebase-admin");
const { env } = require("../config/env");

let app;

if (!admin.apps.length) {
  if (env.firebaseProjectId && env.firebaseClientEmail && env.firebasePrivateKey) {
    app = admin.initializeApp({
      credential: admin.credential.cert({
        projectId: env.firebaseProjectId,
        clientEmail: env.firebaseClientEmail,
        // PRIVATE_KEY is usually stored with escaped newlines in env
        privateKey: env.firebasePrivateKey.replace(/\\n/g, "\n"),
      }),
    });
  } else {
    console.warn(
      "Firebase Admin is not fully configured. FIREBASE_PROJECT_ID, FIREBASE_CLIENT_EMAIL, and FIREBASE_PRIVATE_KEY must be set to use /api/jobs."
    );
  }
}

const db = admin.apps.length ? admin.firestore() : null;

module.exports = { db };

