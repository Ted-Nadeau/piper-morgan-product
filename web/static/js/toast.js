/**
 * Toast Notification System
 * WCAG 2.2 AA Accessible
 *
 * Usage:
 *   Toast.success('Settings saved!', 'Your preferences have been updated')
 *   Toast.error('Upload failed', 'File size must be less than 10MB')
 *   Toast.warning('Session expiring', 'You will be logged out in 5 minutes')
 *   Toast.info('New feature', 'Dark mode is now available in settings')
 *
 * Accessibility:
 * - aria-live="polite" announces toasts to screen readers
 * - aria-atomic="true" announces entire toast content
 * - Keyboard navigation: Tab to close button, Escape dismisses
 * - Color contrast: WCAG AA compliant
 */

const Toast = {
  // SVG Icons (one-character emoji icons for simplicity)
  icons: {
    success: '✓',
    error: '✕',
    warning: '⚠',
    info: 'ⓘ'
  },

  // Default duration (milliseconds) - 7s for better readability
  defaultDuration: 7000,

  /**
   * Show toast notification
   * @param {string} type - 'success', 'error', 'warning', or 'info'
   * @param {string} title - Toast title
   * @param {string} message - Toast message
   * @param {number} duration - Optional override for auto-dismiss duration
   */
  show(type, title, message, duration = null) {
    const container = document.getElementById('toast-container');
    const template = document.getElementById('toast-template');

    if (!container || !template) {
      console.error('Toast: Container or template not found. Ensure toast.html is included in page.');
      return;
    }

    // Validate type
    if (!this.icons[type]) {
      console.warn(`Toast: Invalid type "${type}". Using "info".`);
      type = 'info';
    }

    // Clone template
    const toastElement = template.content.cloneNode(true).querySelector('.toast');
    const closeBtn = toastElement.querySelector('.toast-close');
    const titleEl = toastElement.querySelector('.toast-title');
    const messageEl = toastElement.querySelector('.toast-message');
    const iconEl = toastElement.querySelector('.toast-icon');

    // Set type class
    toastElement.classList.add(`toast-${type}`);

    // Set content
    iconEl.textContent = this.icons[type];
    titleEl.textContent = title;
    messageEl.textContent = message;

    // Add to container
    container.appendChild(toastElement);

    // Close button handler
    const dismiss = () => this.dismiss(toastElement);
    closeBtn.addEventListener('click', dismiss);

    // Keyboard support
    closeBtn.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        e.preventDefault();
        dismiss();
      }
    });

    // Auto-dismiss after duration
    const dismissDuration = duration || this.defaultDuration;
    const timeoutId = setTimeout(() => {
      if (toastElement.parentElement) {
        dismiss();
      }
    }, dismissDuration);

    // Store timeout ID for cleanup if manually dismissed
    toastElement.dataset.timeoutId = timeoutId;
  },

  /**
   * Dismiss toast with animation
   * @param {Element} toastElement - Toast DOM element
   */
  dismiss(toastElement) {
    if (!toastElement || !toastElement.parentElement) {
      return;
    }

    // Clear auto-dismiss timeout if still pending
    const timeoutId = toastElement.dataset.timeoutId;
    if (timeoutId) {
      clearTimeout(parseInt(timeoutId));
    }

    // Add exit animation
    toastElement.classList.add('toast-exit');

    // Remove after animation completes (matches CSS animation duration: 0.2s)
    setTimeout(() => {
      if (toastElement.parentElement) {
        toastElement.remove();
      }
    }, 200);
  },

  /**
   * Success toast
   * @param {string} title - Toast title
   * @param {string} message - Toast message
   * @param {number} duration - Optional auto-dismiss duration
   */
  success(title, message, duration = null) {
    this.show('success', title, message, duration);
  },

  /**
   * Error toast
   * @param {string} title - Toast title
   * @param {string} message - Toast message
   * @param {number} duration - Optional auto-dismiss duration
   */
  error(title, message, duration = null) {
    this.show('error', title, message, duration);
  },

  /**
   * Warning toast
   * @param {string} title - Toast title
   * @param {string} message - Toast message
   * @param {number} duration - Optional auto-dismiss duration
   */
  warning(title, message, duration = null) {
    this.show('warning', title, message, duration);
  },

  /**
   * Info toast
   * @param {string} title - Toast title
   * @param {string} message - Toast message
   * @param {number} duration - Optional auto-dismiss duration
   */
  info(title, message, duration = null) {
    this.show('info', title, message, duration);
  }
};

// Export for modules/bundlers
if (typeof module !== 'undefined' && module.exports) {
  module.exports = Toast;
}
