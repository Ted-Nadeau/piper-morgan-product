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
   * @param {string} config.mode - Dialog mode: 'confirm' (default) or 'form' (Issue #462)
   * @param {string} config.title - Dialog title (e.g., "Delete Standup?")
   * @param {string} config.message - Warning message (text only)
   * @param {string} config.content - HTML content for form dialogs (Issue #462)
   * @param {string} config.confirmText - Button text (e.g., "Delete", "Reset", "Clear")
   * @param {string} config.cancelText - Cancel button text (default: "Cancel")
   * @param {Function} config.onConfirm - Callback when user confirms
   * @param {Function} config.onCancel - Callback when user cancels (optional)
   */
  show(config = {}) {
    const dialog = document.getElementById('confirmation-dialog');
    if (!dialog) return;

    // Determine mode: 'confirm' (default) for destructive actions, 'form' for create/edit
    // Issue #462: Mode controls icon visibility and button styling
    const mode = config.mode || 'confirm';

    // Update dialog text and buttons
    const title = dialog.querySelector('.confirmation-dialog-title');
    const message = dialog.querySelector('.confirmation-dialog-message');
    const confirmBtn = dialog.querySelector('#dialog-confirm-btn');
    const cancelBtn = dialog.querySelector('.confirmation-dialog-actions [onclick="Dialog.cancel()"]');
    const iconEl = dialog.querySelector('.confirmation-dialog-icon');

    // Icon visibility based on mode (Issue #462)
    // - 'confirm' mode: Show warning icon for destructive actions
    // - 'form' mode: Hide icon for create/edit actions
    if (iconEl) {
      iconEl.style.display = mode === 'form' ? 'none' : 'block';
    }

    // Button styling based on mode (Issue #462)
    // - 'confirm' mode: btn-danger (red) for destructive actions
    // - 'form' mode: btn-primary (blue) for positive actions
    if (confirmBtn) {
      if (mode === 'form') {
        confirmBtn.classList.remove('btn-danger');
        confirmBtn.classList.add('btn-primary');
      } else {
        confirmBtn.classList.remove('btn-primary');
        confirmBtn.classList.add('btn-danger');
      }
    }

    // Title and border styling based on mode (Issue #478)
    // - 'confirm' mode: danger red title and border
    // - 'form' mode: primary blue title and neutral border
    const dialogContent = dialog.querySelector('.confirmation-dialog-content');
    if (title) {
      title.style.color = mode === 'form' ? '#2c3e50' : '';  // Dark text for forms, default (red) for confirm
    }
    if (dialogContent) {
      dialogContent.style.borderColor = mode === 'form' ? '#ecf0f1' : '';  // Neutral border for forms, default (red) for confirm
    }

    if (title) title.textContent = config.title || 'Confirm Action';
    // Support both 'content' (HTML for forms) and 'message' (text for confirmations)
    // Issue #462: Form dialogs pass HTML in 'content', confirmation dialogs use 'message'
    if (message) {
      if (config.content) {
        // HTML content for form dialogs (e.g., create todo/list/project)
        message.innerHTML = config.content;
      } else {
        // Text message for confirmation dialogs
        message.textContent = config.message || 'Are you sure you want to proceed? This action cannot be undone.';
      }
    }
    // Button text: use provided text, or default based on mode
    if (confirmBtn) confirmBtn.textContent = config.confirmText || (mode === 'form' ? 'Create' : 'Confirm');
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

    // Focus: for form dialogs, focus first input; for confirmations, focus confirm button
    setTimeout(() => {
      if (config.content) {
        // Form dialog: focus first input field
        const firstInput = dialog.querySelector('input, select, textarea');
        if (firstInput) firstInput.focus();
      } else if (confirmBtn) {
        confirmBtn.focus();
      }
    }, 100);

    // Set up keyboard handler for Escape key
    document.addEventListener('keydown', Dialog._handleKeydown);

    // Announce to screen readers
    if (typeof Toast !== 'undefined' && Toast.warning) {
      Toast.info(config.title || 'Confirm Action', 'Press Tab to navigate buttons, Enter to confirm, Escape to cancel');
    }
  },

  /**
   * Show confirmation dialog (alias for show with confirm-mode defaults)
   * Used by templates: Dialog.confirm({ title, message, onConfirm })
   * @param {Object} config - Same as show() config
   */
  confirm(config = {}) {
    // If called with config object, it's a setup call
    // If called without args (from button onclick), it's the confirm action
    if (config && (config.title || config.message || config.onConfirm)) {
      Dialog.show({
        mode: 'confirm',
        confirmText: config.confirmText || 'Remove',
        ...config,
      });
      return;
    }

    // Called from confirm button - execute the confirmation
    Dialog._doConfirm();
  },

  /**
   * Execute confirmation action and close dialog
   * For form dialogs, callback can return false to keep dialog open (validation failed)
   * @private
   */
  async _doConfirm() {
    if (!Dialog.isOpen) return;

    if (Dialog.confirmCallback && typeof Dialog.confirmCallback === 'function') {
      // Call the callback and check return value
      // If callback returns false, don't close the dialog (validation failed)
      const result = await Dialog.confirmCallback();
      if (result === false) {
        return; // Keep dialog open
      }
    }

    Dialog.close();
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
