// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyBsQvTssrO0HBMPwEiTOBKrBmNtMdIy2kc",
  authDomain: "seng2021-app-d4e5c.firebaseapp.com",
  databaseURL:
    "https://seng2021-app-d4e5c-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "seng2021-app-d4e5c",
  storageBucket: "seng2021-app-d4e5c.appspot.com",
  messagingSenderId: "606034367646",
  appId: "1:606034367646:web:16f808688016e876e0178f",
};

// Initialize Firebase
const firebaseApp = initializeApp(firebaseConfig);

export default firebaseApp;
