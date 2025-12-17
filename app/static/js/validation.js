// Simple client-side validation for registration form
function validateRegistration() {
    var password = document.getElementById("password").value;
    var confirm = document.getElementById("confirm_password").value;
    if (password != confirm) {
        alert("Passwords do not match!");
        return false;
    }
    return true;
}
