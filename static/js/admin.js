// static/js/admin.js

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
    console.log("Firebase initialized in admin.js");

    const logoutButton = document.getElementById('logout');
    const studentsTableBody = document.querySelector('#students-table tbody');

    logoutButton.addEventListener('click', function() {
        firebase.auth().signOut().then(() => {
            window.location.href = '/login';
        }).catch((error) => {
            console.error('Sign Out Error', error);
        });
    });

    // On page load, check if user is logged in and has admin privileges
    firebase.auth().onAuthStateChanged(function(user) {
        if (user) {
            user.getIdTokenResult().then((idTokenResult) => {
                // Check if the user has the admin custom claim
                if (idTokenResult.claims.admin) {
                    // User is an admin, fetch students
                    fetchStudents(idTokenResult.token);
                } else {
                    // User is not an admin, redirect to login or show error
                    alert('Access denied. Admins only.');
                    window.location.href = '/login';
                }
            }).catch((error) => {
                console.error('Error checking admin claim:', error);
                window.location.href = '/login';
            });
        } else {
            // No user is signed in, redirect to login
            window.location.href = '/login';
        }
    });

    // Function to fetch student records from Flask backend
    function fetchStudents(idToken) {
        fetch('/get_students', {
            method: 'GET',
            headers: {
                'Authorization': 'Bearer ' + idToken
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok. Status: ' + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                populateTable(data.students);
            } else {
                alert(data.message);
            }
        })
        .catch(function(error) {
            console.error('Error fetching students:', error);
            alert('Error fetching students. Please try again later.');
        });
    }

    // Function to populate the students table
    function populateTable(students) {
        studentsTableBody.innerHTML = ''; // Clear existing rows
        students.forEach(student => {
            const row = document.createElement('tr');

            const nameTd = document.createElement('td');
            nameTd.innerText = student.name;
            row.appendChild(nameTd);

            const emailTd = document.createElement('td');
            emailTd.innerText = student.email;
            row.appendChild(emailTd);

            const degreeIDTd = document.createElement('td');
            degreeIDTd.innerText = student.degreeID;
            row.appendChild(degreeIDTd);

            const enrollmentDateTd = document.createElement('td');
            const date = student.enrollmentDate ? new Date(student.enrollmentDate * 1000) : new Date();
            enrollmentDateTd.innerText = date.toLocaleDateString();
            row.appendChild(enrollmentDateTd);

            const statusTd = document.createElement('td');
            statusTd.innerText = student.status;
            row.appendChild(statusTd);

            const actionsTd = document.createElement('td');
            if (student.status !== 'approved') {
                const approveBtn = document.createElement('button');
                approveBtn.innerText = 'Approve';
                approveBtn.onclick = () => updateStatus(student.studentID, 'approved');
                actionsTd.appendChild(approveBtn);
            }
            if (student.status !== 'declined') {
                const declineBtn = document.createElement('button');
                declineBtn.innerText = 'Decline';
                declineBtn.onclick = () => updateStatus(student.studentID, 'declined');
                actionsTd.appendChild(declineBtn);
            }
            row.appendChild(actionsTd);

            studentsTableBody.appendChild(row);
        });
    }

    // Function to update student status
    function updateStatus(studentID, newStatus) {
        firebase.auth().currentUser.getIdToken(/* forceRefresh */ true)
            .then(function(idToken) {
                return fetch(`/update_status/${studentID}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + idToken
                    },
                    body: JSON.stringify({ status: newStatus })
                });
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    fetchStudents(); // Refresh the table
                } else {
                    alert(data.message);
                }
            })
            .catch(function(error) {
                console.error('Error updating status:', error);
            });
    }
});
