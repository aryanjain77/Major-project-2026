// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyDvQwMpMwAUF5u94203yXxneEGKfEN8vxI",
  authDomain: "applywise-web.firebaseapp.com",
  projectId: "applywise-web",
  storageBucket: "applywise-web.firebasestorage.app",
  messagingSenderId: "70281274655",
  appId: "1:70281274655:web:b823988fe1e573176f7c2a"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
// src/firebase.js (add these lines at the end)
import { getFirestore } from "firebase/firestore";

export const db = getFirestore(app);