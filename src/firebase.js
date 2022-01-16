import { initializeApp } from "firebase/app"
import { getFirestore } from "firebase/firestore"

// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
    apiKey: "AIzaSyDF7H7WLsIPbmm5flUwmayrS50YXmO6xFA",
    authDomain: "todo-crud-app-232c6.firebaseapp.com",
    projectId: "todo-crud-app-232c6",
    storageBucket: "todo-crud-app-232c6.appspot.com",
    messagingSenderId: "746215391665",
    appId: "1:746215391665:web:197cd4cb4d05fc76fdbd90",
    measurementId: "G-LM5FS6SFBF"
};


const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

export { db };