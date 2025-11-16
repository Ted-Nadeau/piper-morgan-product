// G58: Focus Management System
// Provides utilities for focus trap, focus restoration, and focus movement
// Used by modals, dialogs, and other interactive components
// WCAG 2.2 AA: Proper focus management for keyboard navigation

const FocusManager = {
  // Stack of focus contexts (for nested modals)
  focusStack: [],

  /**
   * Get all focusable elements within a container
   * @param {HTMLElement} container - Container element to search
   * @returns {HTMLElement[]} Array of focusable elements
   */
  getFocusableElements(container) {
    if (!container) return [];

    const focusableSelectors = [
      'a[href]',
      'button:not([disabled])',
      'input:not([disabled])',
      'select:not([disabled])',
      'textarea:not([disabled])',
      '[tabindex]:not([tabindex="-1"])',
      'audio[controls]',
      'video[controls]',
      '[contenteditable]:not([contenteditable="false"])',
    ].join(',');

    return Array.from(container.querySelectorAll(focusableSelectors)).filter(
      (element) => {
        // Check if element is visible
        const style = window.getComputedStyle(element);
        return style.display !== 'none' && style.visibility !== 'hidden';
      }
    );
  },

  /**
   * Save current focus and apply focus trap to element
   * @param {HTMLElement} element - Element to trap focus within
   * @param {boolean} autoFocusFirst - Focus first element (default: true)
   */
  trap(element, autoFocusFirst = true) {
    if (!element) return;

    // Save current focused element
    const previouslyFocused = document.activeElement;

    // Add to focus stack
    FocusManager.focusStack.push({
      element: element,
      previouslyFocused: previouslyFocused,
      keydownListener: (event) => FocusManager._handleTrapKeydown(event, element),
    });

    // Add keyboard event listener for Tab key
    const context = FocusManager.focusStack[FocusManager.focusStack.length - 1];
    document.addEventListener('keydown', context.keydownListener);

    // Focus first element if requested
    if (autoFocusFirst) {
      const focusableElements = FocusManager.getFocusableElements(element);
      if (focusableElements.length > 0) {
        focusableElements[0].focus();
      }
    }
  },

  /**
   * Release focus trap and restore focus to previous element
   * @param {HTMLElement} element - Element to release trap from (optional, uses last in stack)
   */
  release(element = null) {
    if (FocusManager.focusStack.length === 0) return;

    let contextIndex = FocusManager.focusStack.length - 1;

    // Find matching context if element provided
    if (element) {
      contextIndex = FocusManager.focusStack.findIndex(ctx => ctx.element === element);
      if (contextIndex === -1) return;
    }

    const context = FocusManager.focusStack[contextIndex];

    // Remove keyboard listener
    document.removeEventListener('keydown', context.keydownListener);

    // Restore focus
    if (context.previouslyFocused && context.previouslyFocused !== document.body) {
      setTimeout(() => {
        context.previouslyFocused.focus();
      }, 0);
    }

    // Remove from stack
    FocusManager.focusStack.splice(contextIndex, 1);
  },

  /**
   * Move focus to specific element
   * @param {HTMLElement|string} target - Element or selector to focus
   */
  moveTo(target) {
    let element = target;

    // Handle string selectors
    if (typeof target === 'string') {
      element = document.querySelector(target);
    }

    if (element && typeof element.focus === 'function') {
      element.focus();
      return true;
    }
    return false;
  },

  /**
   * Check if element is focusable
   * @param {HTMLElement} element - Element to check
   * @returns {boolean} True if element can receive focus
   */
  isFocusable(element) {
    if (!element) return false;

    const focusableElements = FocusManager.getFocusableElements(element.parentElement || document.body);
    return focusableElements.includes(element);
  },

  /**
   * Get currently focused element
   * @returns {HTMLElement|null} Currently focused element
   */
  getCurrentFocus() {
    return document.activeElement;
  },

  /**
   * Move focus to next focusable element
   * @param {HTMLElement} container - Container to search within
   */
  moveToNext(container) {
    const focusableElements = FocusManager.getFocusableElements(container);
    if (focusableElements.length === 0) return;

    const currentFocus = document.activeElement;
    const currentIndex = focusableElements.indexOf(currentFocus);

    if (currentIndex === -1 || currentIndex === focusableElements.length - 1) {
      focusableElements[0].focus();
    } else {
      focusableElements[currentIndex + 1].focus();
    }
  },

  /**
   * Move focus to previous focusable element
   * @param {HTMLElement} container - Container to search within
   */
  moveToPrevious(container) {
    const focusableElements = FocusManager.getFocusableElements(container);
    if (focusableElements.length === 0) return;

    const currentFocus = document.activeElement;
    const currentIndex = focusableElements.indexOf(currentFocus);

    if (currentIndex <= 0) {
      focusableElements[focusableElements.length - 1].focus();
    } else {
      focusableElements[currentIndex - 1].focus();
    }
  },

  /**
   * Handle Tab key within focus trap
   * @private
   */
  _handleTrapKeydown(event, element) {
    if (event.key !== 'Tab') return;

    const focusableElements = FocusManager.getFocusableElements(element);
    if (focusableElements.length === 0) return;

    const activeElement = document.activeElement;
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];

    if (event.shiftKey) {
      // Shift+Tab: move backward
      if (activeElement === firstElement) {
        event.preventDefault();
        lastElement.focus();
      }
    } else {
      // Tab: move forward
      if (activeElement === lastElement) {
        event.preventDefault();
        firstElement.focus();
      }
    }
  },

  /**
   * Announce text to screen readers
   * @param {string} text - Text to announce
   * @param {string} priority - Priority level: 'polite' or 'assertive' (default: 'polite')
   */
  announce(text, priority = 'polite') {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', priority);
    announcement.setAttribute('aria-atomic', 'true');
    announcement.className = 'sr-only'; // Visually hidden
    announcement.textContent = text;

    document.body.appendChild(announcement);

    // Remove after announcement
    setTimeout(() => {
      announcement.remove();
    }, 1000);
  },
};

// Ensure style for screen-reader-only content exists
if (!document.querySelector('style[data-focus-manager]')) {
  const style = document.createElement('style');
  style.setAttribute('data-focus-manager', 'true');
  style.textContent = `
    .sr-only {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border-width: 0;
    }
  `;
  document.head.appendChild(style);
}
