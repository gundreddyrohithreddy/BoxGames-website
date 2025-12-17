function validateRegisterForm() {
  const fullName = document.getElementById("full_name").value.trim();
  const email = document.getElementById("email").value.trim();
  const phone = document.getElementById("phone").value.trim();
  const password = document.getElementById("password").value;
  const confirmPassword = document.getElementById("confirm_password").value;

  if (fullName.length < 3) { alert("Name too short"); return false; }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { alert("Invalid email"); return false; }
  if (!/^[6-9]\d{9}$/.test(phone)) { alert("Invalid Indian phone"); return false; }
  if (password.length < 8) { alert("Password must be ≥8 chars"); return false; }
  if (password !== confirmPassword) { alert("Passwords mismatch"); return false; }
  return true;
}

function validateLoginForm() {
  const cred = document.getElementById("email_or_phone").value.trim();
  const pwd = document.getElementById("login_password");
  if (!cred || !pwd) { alert("Fill all"); return false; }
  return true;
}

function validateOTP() {
  const phone = document.getElementById("otp_phone").value.trim();
  const code = document.getElementById("otp_code").value.trim();
  if (!/^[6-9]\d{9}$/.test(phone) || !/^\d{4}$/.test(code)) {
    alert("Invalid phone or OTP"); return false;
  }
  return true;
}
