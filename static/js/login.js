// static/js/login.js

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
    console.log("Firebase initialized in login.js");

    const loginForm = document.getElementById('login-form');
    const messageDiv = document.getElementById('message');

    loginForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;

        firebase.auth().signInWithEmailAndPassword(email, password)
            .then((userCredential) => {
                // Logged in
                console.log("User logged in:", userCredential.user);
                userCredential.user.getIdTokenResult()
                    .then((idTokenResult) => {
                        // Check if the user has the admin custom claim
                        if (idTokenResult.claims.admin) {
                            // Redirect to admin dashboard
                            window.location.href = '/admin';
                        } else {
                            // Redirect to user dashboard or home page
                            alert('Access denied. Admins only.');
                            firebase.auth().signOut();
                            window.location.href = '/login';
                        }
                    })
                    .catch((error) => {
                        console.error('Error getting ID token result:', error);
                        messageDiv.style.color = 'red';
                        messageDiv.innerText = 'Error logging in. Please try again.';
                    });
            })
            .catch((error) => {
                console.error('Login error:', error);
                messageDiv.style.color = 'red';
                messageDiv.innerText = error.message;
            });
    });
});
