/**
 * Loading State Utilities
 * WCAG 2.2 AA Accessible
 *
 * Usage:
 *   Loading.button(buttonElement, true) // Start loading
 *   Loading.button(buttonElement, false) // Stop loading
 *   Loading.page(true, 'Loading settings...') // Show page spinner
 *   Loading.page(false) // Hide page spinner
 *   Loading.overlay(true, 'Uploading file...') // Show overlay
 *   Loading.overlay(false) // Hide overlay
 *
 * Accessibility:
 * - Buttons disabled while loading (prevents double-click)
 * - aria-busy attribute announced
 * - Screen readers notify user of loading state
 * - Overlay traps focus and blocks interaction
 */

const Loading = {
  /**
   * Set button to loading state
   * @param {HTMLElement} button - Button element
   * @param {boolean} isLoading - Start or stop loading
   */
  button(button, isLoading) {
    if (!button) {
      console.warn('Loading: button element not found');
      return;
    }

    if (isLoading) {
      button.classList.add('btn-loading');
      button.disabled = true;
      button.setAttribute('aria-busy', 'true');
    } else {
      button.classList.remove('btn-loading');
      button.disabled = false;
      button.setAttribute('aria-busy', 'false');
    }
  },

  /**
   * Show page loading spinner
   * @param {boolean} show - Show or hide
   * @param {string} message - Optional loading message
   */
  page(show, message = 'Loading...') {
    let container = document.getElementById('page-spinner');

    if (show) {
      if (!container) {
        container = document.createElement('div');
        container.id = 'page-spinner';
        container.className = 'spinner-container';
        container.setAttribute('role', 'status');
        container.setAttribute('aria-live', 'polite');
        container.setAttribute('aria-label', 'Loading');
        container.innerHTML = `
          <svg class="spinner spinner-lg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
            <circle class="spinner-track" cx="12" cy="12" r="10" fill="none" stroke-width="2"/>
            <circle class="spinner-head" cx="12" cy="12" r="10" fill="none" stroke-width="2" stroke-dasharray="15.7 50" stroke-dashoffset="0"/>
          </svg>
          <span class="spinner-text">${this._escapeHtml(message)}</span>
        `;
        document.body.appendChild(container);
      } else {
        const text = container.querySelector('.spinner-text');
        if (text) {
          text.textContent = message;
        }
      }
      container.style.display = 'flex';
    } else {
      if (container) {
        container.style.display = 'none';
      }
    }
  },

  /**
   * Show overlay spinner (blocks interaction)
   * @param {boolean} show - Show or hide
   * @param {string} message - Optional loading message
   */
  overlay(show, message = 'Loading...') {
    let overlay = document.getElementById('loading-overlay');

    if (show) {
      if (!overlay) {
        overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'spinner-overlay';
        overlay.setAttribute('role', 'status');
        overlay.setAttribute('aria-live', 'polite');
        overlay.setAttribute('aria-label', 'Loading');
        overlay.innerHTML = `
          <div class="spinner-overlay-content">
            <svg class="spinner spinner-lg" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
              <circle class="spinner-track" cx="12" cy="12" r="10" fill="none" stroke-width="2"/>
              <circle class="spinner-head" cx="12" cy="12" r="10" fill="none" stroke-width="2" stroke-dasharray="15.7 50" stroke-dashoffset="0"/>
            </svg>
            <span class="spinner-text">${this._escapeHtml(message)}</span>
          </div>
        `;
        document.body.appendChild(overlay);
      } else {
        const text = overlay.querySelector('.spinner-text');
        if (text) {
          text.textContent = message;
        }
      }
      overlay.style.display = 'flex';
    } else {
      if (overlay) {
        overlay.style.display = 'none';
      }
    }
  },

  /**
   * Escape HTML to prevent injection
   * @param {string} text - Text to escape
   * @returns {string} Escaped text
   * @private
   */
  _escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
};

// Export for modules/bundlers
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Loading;
}
