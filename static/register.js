function check() {
  if (document.getElementById("password").value != document.getElementById("confirm_password").value) {
    alert("Password Mismatch");
  }
}
