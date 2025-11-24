// G43: Form Validation System
// Provides real-time validation feedback and error prevention
// Validates required fields, value ranges, and custom constraints
// WCAG 2.2 AA: aria-invalid, aria-describedby for error messages

const FormValidation = {
  validators: {},
  errors: {},

  /**
   * Initialize form validation for a form
   * @param {string} formId - ID of form element
   * @param {Object} rules - Validation rules: { fieldName: [validators] }
   * @param {Function} onSubmit - Callback when validation succeeds
   */
  init(formId, rules = {}, onSubmit = null) {
    const form = document.getElementById(formId);
    if (!form) return;

    FormValidation.validators[formId] = rules;
    FormValidation.errors[formId] = {};

    // Add real-time validation for each field
    Object.keys(rules).forEach((fieldName) => {
      const field = form.querySelector(`[name="${fieldName}"]`);
      if (!field) return;

      // Validate on blur and input
      field.addEventListener('blur', () => FormValidation.validateField(formId, fieldName));
      field.addEventListener('input', () => FormValidation.validateField(formId, fieldName));
      field.addEventListener('change', () => FormValidation.validateField(formId, fieldName));
    });

    // Prevent default submit if validation fails
    if (form.onsubmit === null) {
      form.addEventListener('submit', (e) => {
        if (!FormValidation.validateForm(formId)) {
          e.preventDefault();
          return false;
        }
        if (onSubmit) {
          e.preventDefault();
          onSubmit();
        }
      });
    }
  },

  /**
   * Validate a single field
   * @param {string} formId - ID of form
   * @param {string} fieldName - Name of field to validate
   * @returns {boolean} - True if valid
   */
  validateField(formId, fieldName) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const field = form.querySelector(`[name="${fieldName}"]`);
    if (!field) return true;

    const rules = FormValidation.validators[formId]?.[fieldName] || [];
    let error = null;

    // Run each validator
    for (const validator of rules) {
      error = validator(field);
      if (error) break;
    }

    // Update field state
    FormValidation.setFieldError(field, error);
    FormValidation.errors[formId][fieldName] = error;

    return !error;
  },

  /**
   * Validate entire form
   * @param {string} formId - ID of form
   * @returns {boolean} - True if all fields valid
   */
  validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    let isValid = true;
    Object.keys(FormValidation.validators[formId] || {}).forEach((fieldName) => {
      if (!FormValidation.validateField(formId, fieldName)) {
        isValid = false;
      }
    });

    return isValid;
  },

  /**
   * Display/clear error message for a field
   * @param {Element} field - Input field
   * @param {string|null} error - Error message or null if valid
   */
  setFieldError(field, error) {
    const fieldContainer = field.closest('.preference-section') || field.parentElement;
    let errorEl = fieldContainer?.querySelector('.error-message');

    if (error) {
      // Set invalid state
      field.setAttribute('aria-invalid', 'true');

      // Create error message if doesn't exist
      if (!errorEl) {
        errorEl = document.createElement('div');
        errorEl.className = 'error-message';
        errorEl.setAttribute('role', 'alert');
        field.parentElement.appendChild(errorEl);
      }

      errorEl.textContent = error;
      errorEl.style.display = 'block';
      field.setAttribute('aria-describedby', `error-${field.name}`);
    } else {
      // Clear invalid state
      field.setAttribute('aria-invalid', 'false');
      if (errorEl) {
        errorEl.style.display = 'none';
        errorEl.textContent = '';
      }
      field.removeAttribute('aria-describedby');
    }
  },

  /**
   * Get all validation errors for a form
   * @param {string} formId - ID of form
   * @returns {Object} - Errors by field name
   */
  getErrors(formId) {
    return FormValidation.errors[formId] || {};
  },

  /**
   * Clear all errors for a form
   * @param {string} formId - ID of form
   */
  clearErrors(formId) {
    const form = document.getElementById(formId);
    if (!form) return;

    const errorEls = form.querySelectorAll('.error-message');
    errorEls.forEach((el) => {
      el.style.display = 'none';
      el.textContent = '';
    });

    const fields = form.querySelectorAll('[aria-invalid]');
    fields.forEach((field) => {
      field.setAttribute('aria-invalid', 'false');
      field.removeAttribute('aria-describedby');
    });

    FormValidation.errors[formId] = {};
  },
};

// Built-in validators
const Validators = {
  /**
   * Require field to have a value
   */
  required: () => (field) => {
    const value = field.value?.trim();
    if (!value && field.type !== 'radio' && field.type !== 'checkbox') {
      return `${field.name.replace(/_/g, ' ')} is required`;
    }
    return null;
  },

  /**
   * Require at least one radio button selected
   */
  requiredRadio: (groupName) => (field) => {
    if (field.type !== 'radio') return null;
    const group = document.querySelector(`input[name="${groupName}"]:checked`);
    return group ? null : `Please select a ${groupName.replace(/_/g, ' ')}`;
  },

  /**
   * Validate email format
   */
  email: () => (field) => {
    const value = field.value?.trim();
    if (!value) return null;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(value) ? null : 'Please enter a valid email';
  },

  /**
   * Validate minimum value
   */
  min: (minValue) => (field) => {
    const value = parseFloat(field.value);
    return value >= minValue ? null : `Minimum value is ${minValue}`;
  },

  /**
   * Validate maximum value
   */
  max: (maxValue) => (field) => {
    const value = parseFloat(field.value);
    return value <= maxValue ? null : `Maximum value is ${maxValue}`;
  },

  /**
   * Validate string length
   */
  minLength: (length) => (field) => {
    const value = field.value?.trim();
    return value && value.length >= length ? null : `Minimum ${length} characters required`;
  },

  /**
   * Custom validator function
   */
  custom: (validatorFn, message) => (field) => {
    return validatorFn(field.value) ? null : message;
  },
};
