document.addEventListener("DOMContentLoaded", function () {
  const password1Input = document.querySelector(
    "input[id='password']"
  );

  const password1Tooltip =
    password1Input.parentElement.querySelector(".register-tooltip");

  const password2Input = document.querySelector(
    "input[id='confirm_password']"
  );
  const password2Tooltip =
    password2Input.parentElement.querySelector(".register-tooltip");

  const passwordMatchMessage = document.createElement("span");
  passwordMatchMessage.textContent = "Passwords do not match.";
  passwordMatchMessage.style.color = "#ff3333";
  passwordMatchMessage.style.fontSize = "0.9rem";
  passwordMatchMessage.className = "password-match-message";
  passwordMatchMessage.style.display = "none";
  passwordMatchMessage.style.marginLeft =
    "1rem"; /* Add margin to the right of the input field */

  password2Input.parentElement.appendChild(passwordMatchMessage);

  const confirmPassContainer = password2Input.parentElement;

  password2Input.addEventListener("input", function () {
    if (password2Input.value !== password1Input.value) {
      password2Input.classList.add("passwords-not-match");
      passwordMatchMessage.style.display = "block";
    } else {
      password2Input.classList.remove("passwords-not-match");
      passwordMatchMessage.style.display = "none";
    }
  });

  const registerForm = document.querySelector(".register-form");

  registerForm.addEventListener("submit", function (event) {
    const password1 = password1Input.value;
    const password2 = password2Input.value;

    if (
      password1.length < 8 ||
      !/[A-Za-z]/.test(password1) ||
      !/\d/.test(password1)
    ) {
      event.preventDefault();
      alert(
        "Your password must contain at least 8 characters, including letters and numbers."
      );
    }

    if (password1 !== password2) {
      event.preventDefault();
      password2Input.classList.add("passwords-not-match");
      passwordMatchMessage.style.display = "block";
      password2Input.focus();
    }
  });
});