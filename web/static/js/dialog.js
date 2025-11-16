// G24: Confirmation Dialog Utility
// Manages confirmation dialogs for destructive actions (delete, reset, clear)
// Provides focus trap, keyboard navigation (Escape to cancel), and callbacks
// WCAG 2.2 AA: Focus management, keyboard accessible, ARIA attributes

const Dialog = {
  // State
  isOpen: false,
  confirmCallback: null,
  cancelCallback: null,
  focusedElementBeforeOpen: null,

  /**
   * Show confirmation dialog
   * @param {Object} config - Configuration object
   * @param {string} config.title - Dialog title (e.g., "Delete Standup?")
   * @param {string} config.message - Warning message
   * @param {string} config.confirmText - Button text (e.g., "Delete", "Reset", "Clear")
   * @param {string} config.cancelText - Cancel button text (default: "Cancel")
   * @param {Function} config.onConfirm - Callback when user confirms
   * @param {Function} config.onCancel - Callback when user cancels (optional)
   */
  show(config = {}) {
    const dialog = document.getElementById('confirmation-dialog');
    if (!dialog) return;

    // Update dialog text and buttons
    const title = dialog.querySelector('.confirmation-dialog-title');
    const message = dialog.querySelector('.confirmation-dialog-message');
    const confirmBtn = dialog.querySelector('#dialog-confirm-btn');
    const cancelBtn = dialog.querySelector('[onclick="Dialog.cancel()"]').closest('button');

    if (title) title.textContent = config.title || 'Confirm Action';
    if (message) message.textContent = config.message || 'Are you sure you want to proceed? This action cannot be undone.';
    if (confirmBtn) confirmBtn.textContent = config.confirmText || 'Confirm';
    if (cancelBtn) cancelBtn.textContent = config.cancelText || 'Cancel';

    // Store callbacks
    Dialog.confirmCallback = config.onConfirm || null;
    Dialog.cancelCallback = config.onCancel || null;

    // Save focused element to restore later
    Dialog.focusedElementBeforeOpen = document.activeElement;

    // Show dialog
    dialog.classList.add('active');
    dialog.setAttribute('aria-hidden', 'false');
    Dialog.isOpen = true;

    // Focus confirm button
    setTimeout(() => {
      if (confirmBtn) confirmBtn.focus();
    }, 100);

    // Set up keyboard handler for Escape key
    document.addEventListener('keydown', Dialog._handleKeydown);

    // Announce to screen readers
    if (typeof Toast !== 'undefined' && Toast.warning) {
      Toast.info(config.title || 'Confirm Action', 'Press Tab to navigate buttons, Enter to confirm, Escape to cancel');
    }
  },

  /**
   * Confirm action and close dialog
   */
  confirm() {
    if (!Dialog.isOpen) return;

    Dialog.close();

    if (Dialog.confirmCallback && typeof Dialog.confirmCallback === 'function') {
      Dialog.confirmCallback();
    }
  },

  /**
   * Cancel action and close dialog
   */
  cancel() {
    if (!Dialog.isOpen) return;

    Dialog.close();

    if (Dialog.cancelCallback && typeof Dialog.cancelCallback === 'function') {
      Dialog.cancelCallback();
    }
  },

  /**
   * Close dialog and restore focus
   */
  close() {
    const dialog = document.getElementById('confirmation-dialog');
    if (!dialog) return;

    dialog.classList.remove('active');
    dialog.setAttribute('aria-hidden', 'true');
    Dialog.isOpen = false;

    // Remove keyboard handler
    document.removeEventListener('keydown', Dialog._handleKeydown);

    // Restore focus
    if (Dialog.focusedElementBeforeOpen) {
      Dialog.focusedElementBeforeOpen.focus();
    }

    // Clear callbacks
    Dialog.confirmCallback = null;
    Dialog.cancelCallback = null;
  },

  /**
   * Handle keyboard events (Escape to close)
   * @private
   */
  _handleKeydown(event) {
    if (!Dialog.isOpen) return;

    if (event.key === 'Escape') {
      event.preventDefault();
      Dialog.cancel();
    }

    // Focus trap: keep Tab within dialog
    if (event.key === 'Tab') {
      Dialog._handleTabKey(event);
    }
  },

  /**
   * Implement focus trap for Tab key
   * @private
   */
  _handleTabKey(event) {
    const dialog = document.getElementById('confirmation-dialog');
    if (!dialog || !dialog.classList.contains('active')) return;

    const focusableElements = dialog.querySelectorAll(
      'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );

    if (focusableElements.length === 0) return;

    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    const activeElement = document.activeElement;

    if (event.shiftKey) {
      // Shift+Tab: move focus backward
      if (activeElement === firstElement) {
        event.preventDefault();
        lastElement.focus();
      }
    } else {
      // Tab: move focus forward
      if (activeElement === lastElement) {
        event.preventDefault();
        firstElement.focus();
      }
    }
  },
};

// Alternative syntax for inline usage
function confirmDelete(config = {}) {
  Dialog.show({
    title: config.title || 'Delete this item?',
    message: config.message || 'This action cannot be undone.',
    confirmText: 'Delete',
    ...config,
  });
}

function confirmReset(config = {}) {
  Dialog.show({
    title: config.title || 'Reset to defaults?',
    message: config.message || 'This will reset all settings. This action cannot be undone.',
    confirmText: 'Reset',
    ...config,
  });
}

function confirmClear(config = {}) {
  Dialog.show({
    title: config.title || 'Clear all data?',
    message: config.message || 'This will permanently remove all data. This action cannot be undone.',
    confirmText: 'Clear',
    ...config,
  });
}
