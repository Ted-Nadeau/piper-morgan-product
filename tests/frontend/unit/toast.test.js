/**
 * Toast Notification System Tests
 *
 * Tests web/static/js/toast.js
 * Covers: show(), dismiss(), success/error/warning/info methods
 */

describe('Toast Notification System', () => {
  beforeEach(() => {
    // Set up DOM with toast container and template
    global.createToastContainer();

    // Load toast.js
    global.loadScript('toast.js');
  });

  describe('Toast.show()', () => {
    test('creates toast element with correct structure', () => {
      Toast.show('success', 'Test Title', 'Test message');

      const toast = document.querySelector('.toast');
      expect(toast).toBeTruthy();
      expect(toast.classList.contains('toast-success')).toBe(true);
    });

    test('sets title and message content', () => {
      Toast.show('info', 'My Title', 'My message content');

      const title = document.querySelector('.toast-title');
      const message = document.querySelector('.toast-message');

      expect(title.textContent).toBe('My Title');
      expect(message.textContent).toBe('My message content');
    });

    test('sets correct icon for each type', () => {
      const types = ['success', 'error', 'warning', 'info'];
      const expectedIcons = ['✓', '✕', '⚠', 'ⓘ'];

      types.forEach((type, index) => {
        document.getElementById('toast-container').innerHTML = '';
        Toast.show(type, 'Title', 'Message');

        const icon = document.querySelector('.toast-icon');
        expect(icon.textContent).toBe(expectedIcons[index]);
      });
    });

    test('falls back to info type for invalid type', () => {
      // Suppress console warning for this test
      const warnSpy = jest.spyOn(console, 'warn').mockImplementation();

      Toast.show('invalid-type', 'Title', 'Message');

      const toast = document.querySelector('.toast');
      expect(toast.classList.contains('toast-info')).toBe(true);
      expect(warnSpy).toHaveBeenCalledWith(expect.stringContaining('Invalid type'));

      warnSpy.mockRestore();
    });

    test('logs error when container is missing', () => {
      document.getElementById('toast-container').remove();
      const errorSpy = jest.spyOn(console, 'error').mockImplementation();

      Toast.show('success', 'Title', 'Message');

      expect(errorSpy).toHaveBeenCalledWith(expect.stringContaining('Container or template not found'));
      errorSpy.mockRestore();
    });
  });

  describe('Toast.dismiss()', () => {
    test('adds exit animation class', () => {
      Toast.show('success', 'Title', 'Message');
      const toast = document.querySelector('.toast');

      Toast.dismiss(toast);

      expect(toast.classList.contains('toast-exit')).toBe(true);
    });

    test('removes toast after animation delay', () => {
      jest.useFakeTimers();

      Toast.show('success', 'Title', 'Message');
      const toast = document.querySelector('.toast');

      Toast.dismiss(toast);

      // Toast should still exist during animation
      expect(document.querySelector('.toast')).toBeTruthy();

      // After animation delay (200ms), toast should be removed
      jest.advanceTimersByTime(250);
      expect(document.querySelector('.toast')).toBeFalsy();

      jest.useRealTimers();
    });

    test('handles null element gracefully', () => {
      expect(() => Toast.dismiss(null)).not.toThrow();
    });

    test('handles already-removed element gracefully', () => {
      Toast.show('success', 'Title', 'Message');
      const toast = document.querySelector('.toast');
      toast.remove();

      expect(() => Toast.dismiss(toast)).not.toThrow();
    });
  });

  describe('Auto-dismiss functionality', () => {
    test('auto-dismisses after default duration', () => {
      jest.useFakeTimers();

      Toast.show('success', 'Title', 'Message');
      expect(document.querySelector('.toast')).toBeTruthy();

      // Advance past default duration (7000ms) + animation (200ms)
      jest.advanceTimersByTime(7300);
      expect(document.querySelector('.toast')).toBeFalsy();

      jest.useRealTimers();
    });

    test('respects custom duration', () => {
      jest.useFakeTimers();

      Toast.show('success', 'Title', 'Message', 2000);

      // At 1500ms, toast should still exist
      jest.advanceTimersByTime(1500);
      expect(document.querySelector('.toast')).toBeTruthy();

      // At 2300ms (duration + animation), toast should be gone
      jest.advanceTimersByTime(800);
      expect(document.querySelector('.toast')).toBeFalsy();

      jest.useRealTimers();
    });

    test('clears timeout when manually dismissed', () => {
      jest.useFakeTimers();

      Toast.show('success', 'Title', 'Message', 5000);
      const toast = document.querySelector('.toast');

      // Manually dismiss before auto-dismiss
      Toast.dismiss(toast);

      // Advance time - should not cause errors
      jest.advanceTimersByTime(6000);

      jest.useRealTimers();
    });
  });

  describe('Convenience methods', () => {
    test('Toast.success() creates success toast', () => {
      Toast.success('Success!', 'Operation completed');

      const toast = document.querySelector('.toast');
      expect(toast.classList.contains('toast-success')).toBe(true);
    });

    test('Toast.error() creates error toast', () => {
      Toast.error('Error!', 'Something went wrong');

      const toast = document.querySelector('.toast');
      expect(toast.classList.contains('toast-error')).toBe(true);
    });

    test('Toast.warning() creates warning toast', () => {
      Toast.warning('Warning!', 'Please be careful');

      const toast = document.querySelector('.toast');
      expect(toast.classList.contains('toast-warning')).toBe(true);
    });

    test('Toast.info() creates info toast', () => {
      Toast.info('Info', 'Here is some information');

      const toast = document.querySelector('.toast');
      expect(toast.classList.contains('toast-info')).toBe(true);
    });
  });

  describe('Keyboard accessibility', () => {
    test('close button receives keyboard events', () => {
      Toast.show('success', 'Title', 'Message');

      const closeBtn = document.querySelector('.toast-close');
      expect(closeBtn).toBeTruthy();
      expect(closeBtn.getAttribute('aria-label')).toBe('Close notification');
    });

    test('Escape key dismisses toast via close button', () => {
      jest.useFakeTimers();

      Toast.show('success', 'Title', 'Message');
      const closeBtn = document.querySelector('.toast-close');

      // Simulate Escape key on close button
      const escapeEvent = new KeyboardEvent('keydown', {
        key: 'Escape',
        bubbles: true
      });
      closeBtn.dispatchEvent(escapeEvent);

      // Wait for animation
      jest.advanceTimersByTime(250);
      expect(document.querySelector('.toast')).toBeFalsy();

      jest.useRealTimers();
    });
  });

  describe('Multiple toasts', () => {
    test('can display multiple toasts simultaneously', () => {
      Toast.success('First', 'Message 1');
      Toast.error('Second', 'Message 2');
      Toast.info('Third', 'Message 3');

      const toasts = document.querySelectorAll('.toast');
      expect(toasts.length).toBe(3);
    });
  });
});
