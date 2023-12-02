// Initialize Firebase with the provided configuration
const firebaseConfig = {
  apiKey: "AIzaSyDK773LkQ9J5z4Se2PDmu1q3zWoguYjqz8",
  authDomain: "cards-unhumanity.firebaseapp.com",
  projectId: "cards-unhumanity",
  storageBucket: "cards-unhumanity.appspot.com",
  messagingSenderId: "207262810415",
  appId: "1:207262810415:web:52e81c2ae6ae61859ba1da",
  measurementId: "G-QCGM5Q45D9"
};

firebase.initializeApp(firebaseConfig);

// Function to handle sign-in
function signInWithEmailAndPassword() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;

  firebase.auth().signInWithEmailAndPassword(email, password)
    .then((userCredential) => {
      // Signed in successfully
      const user = userCredential.user;
      // Handle further actions or redirects after successful sign-in
      console.log('Signed in:', user);
    })
    .catch((error) => {
      // Handle errors during sign-in
      const errorCode = error.code;
      const errorMessage = error.message;
      console.error('Sign-in error:', errorCode, errorMessage);
    });

}

function registerUser() {
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  const confirmPassword = document.getElementById('confirm_password').value;

  // Check if password and confirm password match
  if (password !== confirmPassword) {
    alert("Passwords don't match");
    return;
  }

  // Create user with email and password
  // Create user with email and password
  firebase.auth().createUserWithEmailAndPassword(email, password)
    .then((userCredential) => {
      // User registered successfully
      const user = userCredential.user;
      console.log('User registered:', user);
      // Handle further actions or redirects after successful registration
    })
    .catch((error) => {
      // Handle errors during registration
      const errorCode = error.code;
      const errorMessage = error.message;
      console.error('Registration error:', errorCode, errorMessage);
    })
}


