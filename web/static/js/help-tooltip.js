// G5: Contextual Help Tooltips
// Manages help icon interactions, visibility, keyboard navigation
// Accessibility: WCAG 2.2 AA with aria-expanded, aria-hidden, keyboard support

const HelpTooltip = {
  activeTooltip: null,

  /**
   * Initialize help tooltip functionality
   * Called once on page load
   */
  init() {
    // Attach global click handler for closing tooltips
    document.addEventListener('click', (e) => {
      // Close if click outside tooltip
      if (!e.target.closest('.help-tooltip')) {
        HelpTooltip.closeAll();
      }
    });

    // Attach keyboard handler for Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        HelpTooltip.closeAll();
      }
    });
  },

  /**
   * Toggle tooltip visibility
   * @param {Event} event - Click event from help icon
   */
  toggle(event) {
    const button = event.currentTarget;
    const tooltip = button.closest('.help-tooltip');

    // Close other active tooltips
    if (HelpTooltip.activeTooltip && HelpTooltip.activeTooltip !== tooltip) {
      HelpTooltip.activeTooltip.classList.remove('active');
      const prevButton = HelpTooltip.activeTooltip.querySelector('.help-icon');
      if (prevButton) {
        prevButton.setAttribute('aria-expanded', 'false');
        prevButton.setAttribute('aria-label', 'Show help');
      }
    }

    // Toggle current tooltip
    const isActive = tooltip.classList.toggle('active');
    button.setAttribute('aria-expanded', isActive.toString());
    button.setAttribute('aria-label', isActive ? 'Hide help' : 'Show help');

    if (isActive) {
      HelpTooltip.activeTooltip = tooltip;
      // Ensure tooltip is visible - adjust position if needed
      HelpTooltip.adjustTooltipPosition(tooltip);
      // Focus content for screen readers
      const content = tooltip.querySelector('.help-content');
      if (content) {
        content.setAttribute('aria-hidden', 'false');
      }
    } else {
      HelpTooltip.activeTooltip = null;
      const content = tooltip.querySelector('.help-content');
      if (content) {
        content.setAttribute('aria-hidden', 'true');
      }
    }

    // Prevent event from bubbling
    event.stopPropagation();
  },

  /**
   * Close all active tooltips
   */
  closeAll() {
    if (HelpTooltip.activeTooltip) {
      HelpTooltip.activeTooltip.classList.remove('active');
      const button = HelpTooltip.activeTooltip.querySelector('.help-icon');
      if (button) {
        button.setAttribute('aria-expanded', 'false');
        button.setAttribute('aria-label', 'Show help');
      }
      const content = HelpTooltip.activeTooltip.querySelector('.help-content');
      if (content) {
        content.setAttribute('aria-hidden', 'true');
      }
      HelpTooltip.activeTooltip = null;
    }
  },

  /**
   * Adjust tooltip position to keep within viewport
   * @param {Element} tooltip - Tooltip container
   */
  adjustTooltipPosition(tooltip) {
    const content = tooltip.querySelector('.help-content');
    if (!content) return;

    // Get positions
    const rect = tooltip.getBoundingClientRect();
    const contentRect = content.getBoundingClientRect();
    const viewportWidth = window.innerWidth;

    // Check if tooltip extends past right edge
    if (contentRect.right > viewportWidth - 16) {
      tooltip.classList.add('right-align');
    } else {
      tooltip.classList.remove('right-align');
    }
  },
};

// Global function for inline onclick handlers
function toggleHelpTooltip(event) {
  HelpTooltip.toggle(event);
}

// Initialize on page load
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => HelpTooltip.init());
} else {
  HelpTooltip.init();
}
