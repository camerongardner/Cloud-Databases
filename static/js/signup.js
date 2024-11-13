// static/js/signup.js

document.addEventListener('DOMContentLoaded', function() {
    // Firebase configuration
    const firebaseConfig = {
        apiKey: "AIzaSyDkUqqU4j6CwLNNnbrDlHOLssHK4rEN6VQ",
        authDomain: "applied-programming-module-5.firebaseapp.com",
        projectId: "applied-programming-module-5",
        storageBucket: "applied-programming-module-5.firebasestorage.app",
        messagingSenderId: "663027144395",
        appId: "1:663027144395:web:8b022523bc6d240ba3ed4e"
      };
    // Initialize Firebase
    if (!firebase.apps.length) {
        firebase.initializeApp(firebaseConfig);
    }
    console.log("Firebase initialized in signup.js");

    const signupForm = document.getElementById('signup-form');
    const messageDiv = document.getElementById('message');

    signupForm.addEventListener('submit', function(e) {
        e.preventDefault();
        console.log("Signup form submitted");

        const name = document.getElementById('name').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const degreeID = document.getElementById('degreeID').value.trim();

        // Basic Validation
        if (!name || !email || !password || !degreeID) {
            console.log("Validation failed: Missing fields");
            messageDiv.style.color = 'red';
            messageDiv.innerText = 'Please fill in all fields.';
            return;
        }

        console.log("Submitting signup form with:", { name, email, degreeID });

        firebase.auth().createUserWithEmailAndPassword(email, password)
            .then((userCredential) => {
                // Signed up
                console.log("User created successfully:", userCredential.user);
                const user = userCredential.user;
                return user.getIdToken();
            })
            .then((idToken) => {
                console.log("Obtained ID token:", idToken);
                // Send user data to Flask backend
                return fetch('/api/signup', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + idToken
                    },
                    body: JSON.stringify({
                        name: name,
                        email: email,
                        degreeID: degreeID
                    })
                });
            })
            .then(response => {
                console.log("Received response from backend:", response);
                return response.json();
            })
            .then(data => {
                console.log("Received response data:", data);
                if (data.status === 'success') {
                    messageDiv.style.color = 'green';
                    messageDiv.innerText = data.message;
                    // Redirect to login or dashboard
                    window.location.href = '/login';
                } else {
                    console.log("Signup failed:", data.message);
                    messageDiv.style.color = 'red';
                    messageDiv.innerText = data.message;
                }
            })
            .catch((error) => {
                console.error("Error during signup process:", error);
                messageDiv.style.color = 'red';
                messageDiv.innerText = error.message;
            });
    });
});
