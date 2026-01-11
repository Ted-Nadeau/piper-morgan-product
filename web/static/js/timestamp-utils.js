/**
 * Timestamp utilities for chat UI (Issue #564)
 * Provides formatting and comparison functions for date/session dividers
 */
const TimestampUtils = {
  /**
   * Format date for divider display
   * Returns: "Today", "Yesterday", or "January 9, 2026"
   * @param {string|number|Date} date - The date to format
   * @returns {string} Formatted date string
   */
  formatDateDivider(date) {
    const now = new Date();
    const messageDate = new Date(date);

    // Reset to start of day for comparison
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const messageDay = new Date(messageDate.getFullYear(), messageDate.getMonth(), messageDate.getDate());

    const diffDays = Math.floor((today - messageDay) / (1000 * 60 * 60 * 24));

    if (diffDays === 0) return "Today";
    if (diffDays === 1) return "Yesterday";

    return messageDate.toLocaleDateString(undefined, {
      month: 'long',
      day: 'numeric',
      year: 'numeric'
    });
  },

  /**
   * Check if two dates are on different calendar days
   * @param {string|number|Date} date1 - First date
   * @param {string|number|Date} date2 - Second date
   * @returns {boolean} True if dates are on different days
   */
  isDifferentDay(date1, date2) {
    if (!date1 || !date2) return false;
    const d1 = new Date(date1);
    const d2 = new Date(date2);
    return d1.toDateString() !== d2.toDateString();
  },

  /**
   * Check if gap between dates is > 8 hours (session gap)
   * @param {string|number|Date} date1 - First date
   * @param {string|number|Date} date2 - Second date
   * @returns {boolean} True if gap exceeds 8 hours
   */
  isSessionGap(date1, date2) {
    if (!date1 || !date2) return false;
    const gap = Math.abs(new Date(date2) - new Date(date1));
    return gap > (8 * 60 * 60 * 1000); // 8 hours in ms
  },

  /**
   * Format time for hover tooltip
   * Today: "2:30 PM"
   * Older: "Jan 9, 2:30 PM"
   * @param {string|number|Date} date - The date to format
   * @returns {string} Formatted time string
   */
  formatHoverTime(date) {
    const now = new Date();
    const messageDate = new Date(date);
    const isToday = now.toDateString() === messageDate.toDateString();

    if (isToday) {
      return messageDate.toLocaleTimeString(undefined, {
        hour: 'numeric',
        minute: '2-digit'
      });
    }

    return messageDate.toLocaleDateString(undefined, {
      month: 'short',
      day: 'numeric'
    }) + ', ' + messageDate.toLocaleTimeString(undefined, {
      hour: 'numeric',
      minute: '2-digit'
    });
  },

  /**
   * Check if date is more than 7 days ago (stale)
   * @param {string|number|Date} date - The date to check
   * @returns {boolean} True if date is more than 7 days ago
   */
  isStale(date) {
    const now = new Date();
    const messageDate = new Date(date);
    const diffDays = Math.floor((now - messageDate) / (1000 * 60 * 60 * 24));
    return diffDays > 7;
  }
};

// Export for module usage or attach to window
if (typeof module !== 'undefined' && module.exports) {
  module.exports = TimestampUtils;
} else {
  window.TimestampUtils = TimestampUtils;
}
