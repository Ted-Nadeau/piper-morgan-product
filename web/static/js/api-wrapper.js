/**
 * API Wrapper with Error Interception
 * WCAG 2.2 AA Accessible
 *
 * Usage:
 *   const response = await ApiWrapper.get('/api/todos')
 *   const data = await ApiWrapper.post('/api/todos', { title: 'New todo' })
 *
 * Automatically shows:
 * - Toast.error for 5xx errors
 * - Toast.warning for 4xx errors
 * - Toast.error for network failures
 *
 * Accessibility:
 * - Errors announced via toast system (aria-live)
 * - User-friendly messages, not technical details
 * - Consistent error handling across application
 */

const ApiWrapper = {
  // Default request timeout (30 seconds)
  defaultTimeout: 30000,

  /**
   * Wrapped fetch with error handling
   * @param {string} url - Request URL
   * @param {Object} options - Fetch options
   * @returns {Promise<Response>}
   */
  async fetch(url, options = {}) {
    const controller = new AbortController();
    const timeout = options.timeout || this.defaultTimeout;

    const timeoutId = setTimeout(() => {
      controller.abort();
    }, timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          'Content-Type': 'application/json',
          ...options.headers
        }
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        await this.handleHttpError(response);
      }

      return response;
    } catch (error) {
      clearTimeout(timeoutId);
      this.handleNetworkError(error);
      throw error;
    }
  },

  /**
   * Handle HTTP error responses (4xx, 5xx)
   * @param {Response} response - Fetch response
   */
  async handleHttpError(response) {
    let message = 'An error occurred';

    try {
      const data = await response.clone().json();
      message = data.detail || data.message || data.error || message;
    } catch {
      // Response wasn't JSON, use status text
      message = response.statusText || message;
    }

    if (response.status >= 500) {
      if (typeof Toast !== 'undefined') {
        Toast.error('Server Error', 'Something went wrong. Please try again later.');
      }
    } else if (response.status === 401) {
      if (typeof Toast !== 'undefined') {
        Toast.warning('Session Expired', 'Please log in again.');
      }
    } else if (response.status === 403) {
      if (typeof Toast !== 'undefined') {
        Toast.warning('Access Denied', 'You don\'t have permission for this action.');
      }
    } else if (response.status === 404) {
      if (typeof Toast !== 'undefined') {
        Toast.warning('Not Found', 'The requested resource was not found.');
      }
    } else if (response.status >= 400) {
      if (typeof Toast !== 'undefined') {
        Toast.warning('Request Failed', message);
      }
    }
  },

  /**
   * Handle network/connection errors
   * @param {Error} error - Error object
   */
  handleNetworkError(error) {
    if (typeof Toast === 'undefined') {
      console.error('ApiWrapper: Toast not available', error);
      return;
    }

    if (error.name === 'AbortError') {
      Toast.error('Request Timeout', 'The request took too long. Please try again.');
    } else if (!navigator.onLine) {
      Toast.error('No Connection', 'You appear to be offline. Check your internet connection.');
    } else {
      Toast.error('Connection Failed', 'Unable to reach the server. Please try again.');
    }
  },

  /**
   * GET request
   * @param {string} url - Request URL
   * @param {Object} options - Optional fetch options
   * @returns {Promise<Response>}
   */
  async get(url, options = {}) {
    return this.fetch(url, { ...options, method: 'GET' });
  },

  /**
   * POST request
   * @param {string} url - Request URL
   * @param {Object} body - Request body (will be JSON stringified)
   * @param {Object} options - Optional fetch options
   * @returns {Promise<Response>}
   */
  async post(url, body, options = {}) {
    return this.fetch(url, {
      ...options,
      method: 'POST',
      body: JSON.stringify(body)
    });
  },

  /**
   * PUT request
   * @param {string} url - Request URL
   * @param {Object} body - Request body (will be JSON stringified)
   * @param {Object} options - Optional fetch options
   * @returns {Promise<Response>}
   */
  async put(url, body, options = {}) {
    return this.fetch(url, {
      ...options,
      method: 'PUT',
      body: JSON.stringify(body)
    });
  },

  /**
   * DELETE request
   * @param {string} url - Request URL
   * @param {Object} options - Optional fetch options
   * @returns {Promise<Response>}
   */
  async delete(url, options = {}) {
    return this.fetch(url, { ...options, method: 'DELETE' });
  },

  /**
   * PATCH request
   * @param {string} url - Request URL
   * @param {Object} body - Request body (will be JSON stringified)
   * @param {Object} options - Optional fetch options
   * @returns {Promise<Response>}
   */
  async patch(url, body, options = {}) {
    return this.fetch(url, {
      ...options,
      method: 'PATCH',
      body: JSON.stringify(body)
    });
  }
};

// Export for modules/bundlers
if (typeof module !== 'undefined' && module.exports) {
  module.exports = ApiWrapper;
}
