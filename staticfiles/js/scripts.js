// registration/static/js/scripts.js
document.addEventListener('DOMContentLoaded', () => {
  // Main page: Register button
  const registerButton = document.getElementById('registerButton');
  if (registerButton) {
      registerButton.addEventListener('click', () => {
          const url = registerButton.getAttribute('data-url');
          if (url) {
              window.location.href = url;
          } else {
              console.error('Register button missing data-url attribute');
          }
      });
  }

  // Main page: Exit button
  const exitButton = document.getElementById('exitButton');
  if (exitButton) {
      exitButton.addEventListener('click', () => {
          window.close();
      });
  }

  // Confirmation page: Back to Home button
  const backToHomeButton = document.getElementById('backToHomeButton');
  if (backToHomeButton) {
      backToHomeButton.addEventListener('click', () => {
          const url = backToHomeButton.getAttribute('data-url');
          if (url) {
              window.location.href = url;
          } else {
              console.error('Back to Home button missing data-url attribute');
          }
      });
  }

  // Register page: Form validation
  const registerForm = document.getElementById('registerForm');
  if (registerForm) {
      registerForm.addEventListener('submit', function(e) {
          const hours = document.getElementById('hours_per_week').value;
          const salary = document.getElementById('hourly_salary').value;
          if (hours <= 0 || salary <= 0) {
              e.preventDefault();
              alert('Hours and salary must be positive numbers.');
          }
      });
  }
});