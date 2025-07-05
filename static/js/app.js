// Sustainable Travel Route Finder - Main JavaScript

document.addEventListener("DOMContentLoaded", function () {
  // Initialize tooltips
  var tooltipTriggerList = [].slice.call(
    document.querySelectorAll('[data-bs-toggle="tooltip"]')
  );
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
  });

  // Form validation enhancement
  const routeForm = document.getElementById("routeForm");
  if (routeForm) {
    routeForm.addEventListener("submit", function (e) {
      const origin = document.getElementById("origin").value.trim();
      const destination = document.getElementById("destination").value.trim();

      if (!origin || !destination) {
        e.preventDefault();
        showAlert(
          "Please enter both starting point and destination.",
          "warning"
        );
        return false;
      }

      if (origin === destination) {
        e.preventDefault();
        showAlert(
          "Starting point and destination cannot be the same.",
          "warning"
        );
        return false;
      }

      // Show loading state
      showLoading();
    });
  }

  // Auto-complete functionality for location inputs
  const locationInputs = document.querySelectorAll(
    'input[name="origin"], input[name="destination"]'
  );
  locationInputs.forEach((input) => {
    input.addEventListener(
      "input",
      debounce(function () {
        const query = this.value.trim();
        if (query.length > 2) {
          // Here you could implement actual geocoding API calls
          // For now, we'll just show a placeholder
          console.log("Searching for:", query);
        }
      }, 300)
    );
  });

  // Smooth scrolling for anchor links
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({
          behavior: "smooth",
          block: "start",
        });
      }
    });
  });

  // Initialize map if present
  initializeMap();
});

// Utility functions
function showAlert(message, type = "info") {
  const alertContainer = document.createElement("div");
  alertContainer.className = `alert alert-${type} alert-dismissible fade show`;
  alertContainer.innerHTML = `
        <i class="fas fa-${
          type === "error" ? "exclamation-triangle" : "info-circle"
        } me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

  const container = document.querySelector(".main-container");
  if (container) {
    container.insertBefore(alertContainer, container.firstChild);

    // Auto-dismiss after 5 seconds
    setTimeout(() => {
      if (alertContainer.parentNode) {
        alertContainer.remove();
      }
    }, 5000);
  }
}

function showLoading() {
  const submitBtn = document.querySelector('button[type="submit"]');
  if (submitBtn) {
    const originalText = submitBtn.innerHTML;
    submitBtn.innerHTML =
      '<span class="loading-spinner me-2"></span>Finding routes...';
    submitBtn.disabled = true;

    // Re-enable after 10 seconds as fallback
    setTimeout(() => {
      submitBtn.innerHTML = originalText;
      submitBtn.disabled = false;
    }, 10000);
  }
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func.apply(this, args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

function initializeMap() {
  const mapContainer = document.getElementById("map");
  if (mapContainer && typeof L !== "undefined") {
    // Map initialization is handled in the result template
    console.log("Map container found, ready for initialization");
  }
}

// Route sharing functionality
function shareRoute() {
  const text = `Eco-friendly route found! Check out this sustainable travel option.`;

  if (navigator.share) {
    navigator
      .share({
        title: "Eco-Friendly Route",
        text: text,
        url: window.location.href,
      })
      .catch((err) => {
        console.log("Error sharing:", err);
        copyToClipboard(text);
      });
  } else {
    copyToClipboard(text);
  }
}

function copyToClipboard(text) {
  if (navigator.clipboard) {
    navigator.clipboard
      .writeText(text)
      .then(() => {
        showAlert("Route information copied to clipboard!", "success");
      })
      .catch((err) => {
        console.log("Failed to copy:", err);
        fallbackCopyToClipboard(text);
      });
  } else {
    fallbackCopyToClipboard(text);
  }
}

function fallbackCopyToClipboard(text) {
  const textArea = document.createElement("textarea");
  textArea.value = text;
  textArea.style.position = "fixed";
  textArea.style.left = "-999999px";
  textArea.style.top = "-999999px";
  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    document.execCommand("copy");
    showAlert("Route information copied to clipboard!", "success");
  } catch (err) {
    console.log("Fallback copy failed:", err);
    showAlert("Could not copy to clipboard. Please copy manually.", "warning");
  }

  document.body.removeChild(textArea);
}

// Print functionality
function printResults() {
  window.print();
}

// Environmental impact calculations
function calculateEnvironmentalImpact(emissionSavings) {
  const treesEquivalent = Math.round(emissionSavings / 0.022);
  const drivingKmEquivalent = (emissionSavings / 0.12).toFixed(1);

  return {
    trees: treesEquivalent,
    drivingKm: drivingKmEquivalent,
  };
}

// Accessibility enhancements
function enhanceAccessibility() {
  // Add ARIA labels to interactive elements
  const buttons = document.querySelectorAll("button:not([aria-label])");
  buttons.forEach((button) => {
    if (button.textContent.trim()) {
      button.setAttribute("aria-label", button.textContent.trim());
    }
  });

  // Add skip links for keyboard navigation
  const skipLink = document.createElement("a");
  skipLink.href = "#main-content";
  skipLink.className = "sr-only sr-only-focusable";
  skipLink.textContent = "Skip to main content";
  document.body.insertBefore(skipLink, document.body.firstChild);
}

// Performance monitoring
function trackPerformance() {
  if ("performance" in window) {
    window.addEventListener("load", () => {
      const loadTime =
        performance.timing.loadEventEnd - performance.timing.navigationStart;
      console.log(`Page load time: ${loadTime}ms`);
    });
  }
}

// Initialize additional features
document.addEventListener("DOMContentLoaded", function () {
  enhanceAccessibility();
  trackPerformance();
});
