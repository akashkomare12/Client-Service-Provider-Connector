document.addEventListener("DOMContentLoaded", () => {
    console.log("JavaScript loaded!");
  
    // Client Login
    const loginForm = document.getElementById("loginForm");
    if (loginForm) {
      loginForm.addEventListener("submit", async function (event) {
        event.preventDefault();
  
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;
        const csrfToken = getCSRFToken();
  
        try {
          const response = await fetch("/help/login/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ username, password }),
          });
  
          const data = await response.json();
  
          if (response.ok) {
            window.location.href = "/help/client_dashboard"; // Absolute URL for redirection
          } else {
            document.getElementById("error").textContent = data.error;
          }
        } catch (error) {
          document.getElementById("error").textContent =
            "An error occurred. Please try again.";
        }
      });
    }
  
    // Service Provider Login
    const serviceloginForm = document.getElementById("serviceloginForm");
    if (serviceloginForm) {
      serviceloginForm.addEventListener("submit", async function (event) {
        event.preventDefault();
  
        const username = document.getElementById("service_username").value;
        const password = document.getElementById("service_password").value;
        const csrfToken = getCSRFToken();
        try {
          const response = await fetch("/help/login_service_provider/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify({ username, password }),
          });
  
          const data = await response.json();
  
          if (response.ok) {
            window.location.href = "/help/service_dashboard"; // Absolute URL for redirection
          } else {
            document.getElementById("error").textContent = data.error;
          }
        } catch (error) {
          document.getElementById("error").textContent =
            "An error occurred. Please try again.";
        }
      });
    }
  
    // Client Registration
    const registerForm = document.getElementById("registerForm");
    if (registerForm) {
      registerForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent the form's default GET request
  
        // Collect form data
        const formData = {
          name: document.getElementById("name").value,
          username: document.getElementById("username").value,
          email: document.getElementById("email").value,
          city: document.getElementById("city").value,
          pincode: document.getElementById("pincode").value,
          mobile: document.getElementById("mobile").value,
          password: document.getElementById("password").value,
        };
  
        const csrfToken = getCSRFToken();
  
        try {
          const response = await fetch("/help/register/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken, // Include CSRF token
            },
            body: JSON.stringify(formData),
          });
  
          const data = await response.json();
  
          if (response.ok) {
            window.location.href = "/help/login-page/"; // Redirect on success
          } else {
            document.getElementById("error").textContent = data.error;
          }
        } catch (error) {
          document.getElementById("error").textContent =
            "An error occurred. Please try again.";
        }
      });
    }
  
    // Service Provider Registration
    const serviceregisterForm = document.getElementById("serviceregisterForm");
    if (serviceregisterForm) {
      serviceregisterForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent the form's default GET request
  
        // Collect form data
        const formData = {
          name: document.getElementById("service_name").value,
          username: document.getElementById("service_username").value,
          email: document.getElementById("service_email").value,
          city: document.getElementById("service_city").value,
          pincode: document.getElementById("service_pincode").value,
          mobile: document.getElementById("service_mobile").value,
          password: document.getElementById("service_password").value,
          skills: document.getElementById("skills").value,
        };
  
        const csrfToken = getCSRFToken();
  
        try {
          const response = await fetch("/help/register_service_provider/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken, // Include CSRF token
            },
            body: JSON.stringify(formData),
          });
  
          const data = await response.json();
  
          if (response.ok) {
            window.location.href = "/help/service-register-page/"; // Redirect on success
          } else {
            document.getElementById("error").textContent = data.error;
          }
        } catch (error) {
          document.getElementById("error").textContent =
            "An error occurred. Please try again.";
        }
      });
    }
  
    // Profile Update
    const updateProfileForm = document.getElementById("update-profile-form");
    if (updateProfileForm) {
      updateProfileForm.addEventListener("submit", async function (event) {
        event.preventDefault(); // Prevent default form submission behavior
  
        const formData = {
          name: document.getElementById("name").value,
          email: document.getElementById("email").value,
          mobile: document.getElementById("mobile").value,
          city: document.getElementById("city").value,
          pincode: document.getElementById("pincode").value,
        };
  
        const csrfToken = getCSRFToken();
        try {
          const response = await fetch("/help/update-profile/", {
            method: "PUT",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken,
            },
            body: JSON.stringify(formData),
          });
  
          if (response.ok) {
            window.location.href = "/help/client_dashboard"; // Redirect to client dashboard
          } else {
            const errorData = await response.json();
            document.getElementById("error").textContent =
              errorData.error || "Failed to update profile.";
          }
        } catch (error) {
          document.getElementById("error").textContent =
            "An error occurred. Please try again.";
        }
      });
    }
  
    // Book Service
    window.bookService = function (sp_id, service, client_id) {
      const date = new Date().toISOString().slice(0, 10); // Today's date
      let amount;
      if (service.toLowerCase() === "cook") {
        amount = 1000;
      } else if (service.toLowerCase() === "cleaner") {
        amount = 300;
      } else if (service.toLowerCase() === "electrician") {
        amount = 500;
      } else if (service.toLowerCase() === "plumber") {
        amount = 600;
      }
  
      fetch("/help/book_service/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
        body: JSON.stringify({
          sp_id: sp_id,
          u_id: client_id,
          service: service,
          date: date,
          amount: amount,
        }),
      })
        .then((response) => {
          if (response.ok) {
            alert("Service booked successfully!");
            window.location.reload(); // Reload the dashboard
          } else {
            response.json().then((data) => {
              alert(`Error: ${data.error}`);
            });
          }
        })
        .catch((error) => {
          console.error("Error during booking:", error);
          alert("An error occurred. Please try again.");
        });
    };
  
    // Logout Functionality
    window.logoutProvider = function () {
      fetch("/help/logout/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCSRFToken(),
        },
      })
        .then((response) => {
          if (response.ok) {
            location.href = "/help/";
          } else {
            alert("Logout failed");
          }
        })
        .catch((error) => console.error("Error:", error));
    };
    
    
      
    // CSRF Token Helper
    function getCSRFToken() {
      const name = "csrftoken";
      const cookies = document.cookie.split("; ");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].split("=");
        if (cookie[0] === name) {
          return cookie[1];
        }
      }
      return null;
    }
  });
  
  