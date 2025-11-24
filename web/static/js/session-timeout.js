// G52: Session Timeout Handling
// Tracks user idle time and warns before session expiry
// Provides graceful logout and session extension
// Configuration can be customized per deployment

const SessionTimeout = {
  // Configuration (override these in init)
  totalSessionMinutes: 30, // Total session duration
  warningMinutesBefore: 5, // Warn this many minutes before expiry
  idleMinutesBeforeWarning: 25, // Show warning after this many idle minutes
  warningIntervalSeconds: 1, // Update countdown every N seconds
  logoutUrl: '/logout', // URL to redirect to on logout

  // Internal state
  sessionStartTime: null,
  lastActivityTime: null,
  timeoutHandle: null,
  countdownHandle: null,
  modalOpen: false,
  sessionExpired: false,

  /**
   * Initialize session timeout tracking
   * @param {Object} config - Configuration options
   */
  init(config = {}) {
    // Merge config
    Object.assign(SessionTimeout, config);

    SessionTimeout.sessionStartTime = Date.now();
    SessionTimeout.lastActivityTime = Date.now();

    // Track user activity
    document.addEventListener('mousedown', () => SessionTimeout.recordActivity());
    document.addEventListener('keydown', () => SessionTimeout.recordActivity());
    document.addEventListener('touch', () => SessionTimeout.recordActivity());
    document.addEventListener('scroll', () => SessionTimeout.recordActivity());

    // Start idle timeout check
    SessionTimeout.startIdleCheck();
  },

  /**
   * Record user activity and reset idle timer
   */
  recordActivity() {
    SessionTimeout.lastActivityTime = Date.now();

    // If modal was shown, dismiss it (user is active)
    if (SessionTimeout.modalOpen) {
      SessionTimeout.dismiss();
    }
  },

  /**
   * Start checking for idle timeout
   */
  startIdleCheck() {
    // Check idle status every 10 seconds
    const checkInterval = setInterval(() => {
      const minutesIdle = (Date.now() - SessionTimeout.lastActivityTime) / 1000 / 60;
      const minutesUntilExpiry =
        SessionTimeout.totalSessionMinutes - minutesIdle;

      // Show warning if within warning window
      if (
        minutesUntilExpiry <= SessionTimeout.warningMinutesBefore &&
        minutesUntilExpiry > 0 &&
        !SessionTimeout.modalOpen
      ) {
        SessionTimeout.showWarning(minutesUntilExpiry);
      }

      // Auto-logout if time expired
      if (minutesUntilExpiry <= 0 && !SessionTimeout.sessionExpired) {
        SessionTimeout.sessionExpired = true;
        SessionTimeout.autoLogout();
      }
    }, 10000); // Check every 10 seconds

    SessionTimeout.timeoutHandle = checkInterval;
  },

  /**
   * Show session timeout warning modal
   * @param {number} minutesRemaining - Minutes until session expires
   */
  showWarning(minutesRemaining) {
    const modal = document.getElementById('session-timeout-modal');
    if (!modal) return;

    SessionTimeout.modalOpen = true;

    // Update countdown display
    SessionTimeout.updateCountdown();

    // Show modal
    modal.classList.add('active');
    modal.setAttribute('aria-hidden', 'false');

    // Focus close button for accessibility
    const closeBtn = modal.querySelector('.session-timeout-close');
    if (closeBtn) closeBtn.focus();

    // Announce to screen readers
    if (typeof Toast !== 'undefined' && Toast.warning) {
      Toast.warning(
        'Session Expiring',
        `Your session expires in ${Math.round(minutesRemaining)} minutes. Click to continue.`
      );
    }

    // Start countdown updates
    SessionTimeout.startCountdown();
  },

  /**
   * Update countdown display
   */
  updateCountdown() {
    const minutesIdle = (Date.now() - SessionTimeout.lastActivityTime) / 1000 / 60;
    const minutesRemaining = SessionTimeout.totalSessionMinutes - minutesIdle;

    if (minutesRemaining <= 0) {
      SessionTimeout.autoLogout();
      return;
    }

    const minutes = Math.floor(minutesRemaining);
    const seconds = Math.floor((minutesRemaining % 1) * 60);

    const countdownEl = document.getElementById('timeout-countdown');
    if (countdownEl) {
      countdownEl.textContent =
        `${minutes}:${seconds.toString().padStart(2, '0')}`;
    }
  },

  /**
   * Start updating countdown timer
   */
  startCountdown() {
    if (SessionTimeout.countdownHandle) clearInterval(SessionTimeout.countdownHandle);

    SessionTimeout.countdownHandle = setInterval(() => {
      SessionTimeout.updateCountdown();
    }, SessionTimeout.warningIntervalSeconds * 1000);
  },

  /**
   * Stop countdown timer
   */
  stopCountdown() {
    if (SessionTimeout.countdownHandle) {
      clearInterval(SessionTimeout.countdownHandle);
      SessionTimeout.countdownHandle = null;
    }
  },

  /**
   * Extend session (dismiss warning and continue)
   */
  extend() {
    SessionTimeout.lastActivityTime = Date.now();
    SessionTimeout.dismiss();

    // Optional: call API to extend server-side session
    if (SessionTimeout.extendUrl) {
      fetch(SessionTimeout.extendUrl, { method: 'POST' }).catch((e) =>
        console.error('Failed to extend session:', e)
      );
    }

    // Announce extension
    if (typeof Toast !== 'undefined' && Toast.success) {
      Toast.success('Session Extended', 'Your session has been extended.');
    }
  },

  /**
   * Dismiss warning modal
   */
  dismiss() {
    const modal = document.getElementById('session-timeout-modal');
    if (modal) {
      modal.classList.remove('active');
      modal.setAttribute('aria-hidden', 'true');
    }

    SessionTimeout.modalOpen = false;
    SessionTimeout.stopCountdown();
  },

  /**
   * Logout immediately
   */
  logout() {
    SessionTimeout.sessionExpired = true;
    SessionTimeout.dismiss();

    // Clear session data
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem('sessionId');
    }

    // Redirect to login/logout page
    window.location.href = SessionTimeout.logoutUrl;
  },

  /**
   * Auto-logout when time expires
   */
  autoLogout() {
    const modal = document.getElementById('session-timeout-modal');
    if (modal) {
      // Update message
      const title = modal.querySelector('.session-timeout-title');
      if (title) {
        title.textContent = 'Your Session Has Expired';
      }

      const message = modal.querySelector('.session-timeout-message');
      if (message) {
        message.innerHTML =
          'Your session has expired for security. Please log in again to continue.';
      }

      // Hide action buttons
      const actions = modal.querySelector('.session-timeout-actions');
      if (actions) {
        actions.style.display = 'none';
      }

      // Show modal
      modal.classList.add('active');
      modal.setAttribute('aria-hidden', 'false');
    }

    // Redirect after 5 seconds
    setTimeout(() => {
      SessionTimeout.logout();
    }, 5000);
  },
};

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => SessionTimeout.init());
} else {
  SessionTimeout.init();
}
