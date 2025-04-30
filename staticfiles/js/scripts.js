<<<<<<< HEAD
// Helper function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to detect and send the user's timezone to the server
function setUserTimezone() {
    // Debug the initial value of timezoneSet
    console.log("Debug: Initial window.timezoneSet =", window.timezoneSet);

    // Check if timezone has already been set in localStorage
    if (localStorage.getItem('timezoneSet') === 'true') {
        console.log('Timezone already set in localStorage');
        return;
    }

    // If window.timezoneSet is true, skip setting the timezone
    if (window.timezoneSet === true) {
        console.log('Timezone already set in session');
        localStorage.setItem('timezoneSet', 'true');
        return;
    }

    const timezone = Intl.DateTimeFormat().resolvedOptions().timeZone;
    if (!timezone) {
        console.error('Could not detect user timezone');
        return;
    }

    // Send the timezone to the server via AJAX
    fetch('/set_timezone/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({ timezone: timezone }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Timezone set successfully:', timezone);
            localStorage.setItem('timezoneSet', 'true');
            // Only reload if necessary (first time setting the timezone)
            if (!window.timezoneSet) {
                window.location.reload();
            }
        } else {
            console.error('Failed to set timezone:', data.message);
        }
    })
    .catch(error => console.error('Error setting timezone:', error));
}

// Function to populate positions based on department selection
function populatePositions(departmentSelect, positionSelect, selectedPosition) {
    if (!departmentSelect || !positionSelect) {
        console.error('Department or Position select element not found');
        return;
    }

    const positions = {
        'Front-Desk': ['Cashier', 'Carry-Out', 'Assistant Manager', 'Department Manager', 'General Manager'],
        'Receiving': ['Morning Stock', 'Lumber Yard Associate', 'Receiving Associate', 'Assistant Manager', 'Department Manager'],
        'Electrical': ['Sales Associate', 'Assistant Manager', 'Department Manager'],
        'Plumbing': ['Sales Associate', 'Assistant Manager', 'Department Manager'],
        'Wall Coverings': ['Sales Associate', 'Assistant Manager', 'Department Manager'],
        'Flooring': ['Sales Associate', 'Assistant Manager', 'Department Manager'],
        'Hardware': ['Sales Associate', 'Assistant Manager', 'Department Manager'],
        'Building Materials': ['Sales Associate', 'Assistant Manager', 'Department Manager']
    };

    const selectedDepartment = departmentSelect.value;
    positionSelect.innerHTML = '<option value="" disabled selected>Select Position</option>';
    
    if (positions[selectedDepartment]) {
        positions[selectedDepartment].forEach(position => {
            const option = document.createElement('option');
            option.value = position;
            option.textContent = position;
            if (position === selectedPosition) {
                option.selected = true;
            }
            positionSelect.appendChild(option);
        });
    }
}

// Utility function to navigate to a URL from a button's data-url attribute
function navigateToUrl(button, buttonName) {
    if (!button) {
        console.error(`${buttonName} button not found`);
        return;
    }
    button.addEventListener('click', function () {
        const url = button.getAttribute('data-url');
        if (url) {
            window.location.href = url;
        } else {
            console.error(`${buttonName} button is missing data-url attribute`);
        }
    });
}

// Utility function to validate form inputs
function validateForm(form) {
    if (!form) {
        console.warn('Form not found for validation');
        return;
    }
    form.addEventListener('submit', function (e) {
        const hoursInput = document.getElementById('hours_per_week');
        const salaryInput = document.getElementById('hourly_salary');

        if (hoursInput && salaryInput) {
            const hours = parseFloat(hoursInput.value);
            const salary = parseFloat(salaryInput.value);
            if (isNaN(hours) || isNaN(salary) || hours <= 0 || salary <= 0) {
                e.preventDefault();
                alert('Please ensure hours and salary are positive numbers.');
            }
        }
    });
}

// Main event listener for DOM content loaded
document.addEventListener('DOMContentLoaded', function () {
    console.log('scripts.js loaded');

    // Set user timezone
    setUserTimezone();

    // Handle navigation for all buttons with data-url attribute
    const buttons = document.querySelectorAll('[data-url]');
    buttons.forEach(button => {
        const buttonName = button.id || button.textContent.trim() || 'Unnamed';
        navigateToUrl(button, buttonName);
    });

    // Main page: Exit button (if present)
    const exitButton = document.getElementById('exitButton');
    if (exitButton) {
        exitButton.addEventListener('click', function () {
            console.log('Exit button clicked');
            window.close();
            setTimeout(function () {
                alert('Unable to close the tab automatically. Please close it manually.');
            }, 100);
        });
    }

    // Register page: Form validation
    validateForm(document.getElementById('registerForm'));

    // Register page: Populate positions dropdown
    const departmentSelect = document.getElementById('department');
    const positionSelect = document.getElementById('position');
    if (departmentSelect && positionSelect) {
        departmentSelect.addEventListener('change', () => {
            populatePositions(departmentSelect, positionSelect, null);
        });
    }
=======
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
>>>>>>> 5bac7396538c333b6b061a6a48f0cb071cbf1da0
});