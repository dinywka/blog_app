function passwordSwitchVisibility() {
  const passwordInput = document.getElementById("Password"); // Fix the ID here
  const toggleButton = document.getElementById("toggleButton");
  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    toggleButton.classList.replace("fa-eye", "fa-eye-slash");
  } else {
    passwordInput.type = "password";
    toggleButton.classList.replace("fa-eye-slash", "fa-eye");
  }
}
