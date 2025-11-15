// G61: Keyboard Shortcuts System
// Manages keyboard shortcuts for power users
// Shortcuts:
//  - Cmd/Ctrl + ?: Show shortcuts help
//  - Cmd/Ctrl + S: Save current form
//  - Cmd/Ctrl + Return: Submit form
//  - Escape: Close panels

const KeyboardShortcuts = {
  panelOpen: false,
  saveCallback: null,
  submitCallback: null,

  /**
   * Initialize keyboard shortcuts
   * @param {Function} onSave - Callback for save shortcut
   * @param {Function} onSubmit - Callback for submit shortcut
   */
  init(onSave = null, onSubmit = null) {
    KeyboardShortcuts.saveCallback = onSave;
    KeyboardShortcuts.submitCallback = onSubmit;

    // Main keyboard handler
    document.addEventListener('keydown', (e) => {
      const isMac = navigator.platform.toUpperCase().indexOf('MAC') >= 0;
      const isCtrlOrCmd = isMac ? e.metaKey : e.ctrlKey;

      // Cmd/Ctrl + ? : Show shortcuts
      if (isCtrlOrCmd && e.shiftKey && e.key === '?') {
        e.preventDefault();
        KeyboardShortcuts.toggle();
      }

      // Cmd/Ctrl + S : Save
      if (isCtrlOrCmd && e.key === 's') {
        e.preventDefault();
        KeyboardShortcuts.executeSave();
      }

      // Cmd/Ctrl + Return : Submit form
      if (isCtrlOrCmd && e.key === 'Enter') {
        e.preventDefault();
        KeyboardShortcuts.executeSubmit();
      }

      // Escape : Close panels
      if (e.key === 'Escape') {
        if (KeyboardShortcuts.panelOpen) {
          e.preventDefault();
          KeyboardShortcuts.close();
        }
      }
    });
  },

  /**
   * Toggle shortcuts panel visibility
   */
  toggle() {
    if (KeyboardShortcuts.panelOpen) {
      KeyboardShortcuts.close();
    } else {
      KeyboardShortcuts.open();
    }
  },

  /**
   * Open shortcuts panel
   */
  open() {
    const panel = document.getElementById('shortcuts-panel');
    if (panel) {
      panel.classList.add('active');
      panel.setAttribute('aria-hidden', 'false');
      KeyboardShortcuts.panelOpen = true;
      // Focus close button for accessibility
      const closeBtn = panel.querySelector('.shortcuts-close');
      if (closeBtn) closeBtn.focus();
    }
  },

  /**
   * Close shortcuts panel
   */
  close() {
    const panel = document.getElementById('shortcuts-panel');
    if (panel) {
      panel.classList.remove('active');
      panel.setAttribute('aria-hidden', 'true');
      KeyboardShortcuts.panelOpen = false;
    }
  },

  /**
   * Execute save callback
   */
  executeSave() {
    if (KeyboardShortcuts.saveCallback) {
      KeyboardShortcuts.saveCallback();
    }
  },

  /**
   * Execute submit callback
   */
  executeSubmit() {
    if (KeyboardShortcuts.submitCallback) {
      KeyboardShortcuts.submitCallback();
    }
  },

  /**
   * Announce shortcut to user (via toast)
   * @param {string} message - Message to show
   */
  announce(message) {
    // If Toast system is available, use it
    if (typeof Toast !== 'undefined' && Toast.info) {
      Toast.info('Keyboard Shortcut', message);
    }
  },
};

// Initialize keyboard shortcuts on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => KeyboardShortcuts.init());
} else {
  KeyboardShortcuts.init();
}
