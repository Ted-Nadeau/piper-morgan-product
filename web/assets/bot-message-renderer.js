/**
 * DDD Bot Message Renderer - Domain service for consistent message rendering
 */

/**
 * Render bot message with consistent formatting
 * @param {string} content - The message content
 * @param {string} type - 'success', 'error', 'thinking'
 * @param {boolean} isThinking - Whether this is a thinking/loading state
 * @returns {string} - Rendered HTML
 */
function renderBotMessage(content, type = 'success', isThinking = false) {
    if (!content) return '';
    if (isThinking) return content; // Don't process thinking messages

    // Domain logic: Apply markdown only to success messages
    let processedContent = content;
    if (type === 'success' && typeof marked !== 'undefined') {
        try {
            processedContent = marked.parse(content);
        } catch (error) {
            console.warn('Markdown parsing failed:', error);
            processedContent = content; // Fallback to raw content
        }
    }

    // Domain logic: Apply consistent CSS classes
    const cssClasses = ['result', type];
    if (isThinking) cssClasses.push('thinking');

    return `<div class="${cssClasses.join(' ')}">${processedContent}</div>`;
}

/**
 * Handle direct API responses
 * @param {Object} result - API response object
 * @param {HTMLElement} element - DOM element to update
 */
function handleDirectResponse(result, element) {
    console.log('Direct response:', result.message);
    element.innerHTML = renderBotMessage(result.message, 'success', false);

    // Phase 3: Render pattern suggestions if present
    if (result.suggestions && result.suggestions.length > 0) {
        element.innerHTML += renderSuggestions(result.suggestions);
    }
}

/**
 * Render pattern suggestions UI (Phase 3)
 * @param {Array} suggestions - Array of suggestion objects
 * @returns {string} - Rendered HTML
 */
function renderSuggestions(suggestions) {
    const count = suggestions.length;
    const plural = count === 1 ? '' : 's';

    return `
        <div class="suggestions-container">
            <div class="suggestions-badge" onclick="toggleSuggestionsPanel()">
                💡 ${count} pattern suggestion${plural}
                <span class="badge-chevron">▼</span>
            </div>
            <div class="suggestions-panel" id="suggestions-panel" style="display: none;">
                <div class="suggestions-header">
                    <strong>Suggested Actions</strong>
                    <span class="suggestions-subtitle">Based on your past patterns</span>
                </div>
                ${suggestions.map((s, idx) => renderSuggestionCard(s, idx)).join('')}
            </div>
        </div>
    `;
}

/**
 * Render individual suggestion card (Phase 3)
 * @param {Object} suggestion - Suggestion object
 * @param {number} index - Card index
 * @returns {string} - Rendered HTML
 */
function renderSuggestionCard(suggestion, index) {
    const confidence = Math.round(suggestion.confidence * 100);
    const patternType = suggestion.pattern_type.replace('_', ' ').toLowerCase();
    const usageText = `Used ${suggestion.usage_count} time${suggestion.usage_count === 1 ? '' : 's'}`;

    // Extract reasoning from pattern_data
    const reasoning = suggestion.pattern_data?.reasoning ||
                     suggestion.pattern_data?.description ||
                     `${patternType} pattern detected`;

    return `
        <div class="suggestion-card" data-pattern-id="${suggestion.pattern_id}">
            <div class="suggestion-content">
                <div class="suggestion-reasoning">${reasoning}</div>
                <div class="suggestion-meta">
                    <span class="suggestion-type">${patternType}</span>
                    <span class="suggestion-usage">${usageText}</span>
                </div>
                <div class="confidence-bar-container">
                    <div class="confidence-bar" style="width: ${confidence}%"></div>
                    <span class="confidence-label">${confidence}% confidence</span>
                </div>
            </div>
            <div class="suggestion-actions">
                <button class="suggestion-btn accept" onclick="handleSuggestionFeedback('${suggestion.pattern_id}', 'accept')">
                    ✓ Accept
                </button>
                <button class="suggestion-btn reject" onclick="handleSuggestionFeedback('${suggestion.pattern_id}', 'reject')">
                    ✗ Reject
                </button>
                <button class="suggestion-btn dismiss" onclick="handleSuggestionFeedback('${suggestion.pattern_id}', 'dismiss')">
                    Dismiss
                </button>
            </div>
        </div>
    `;
}

/**
 * Toggle suggestions panel visibility (Phase 3)
 */
function toggleSuggestionsPanel() {
    const panel = document.getElementById('suggestions-panel');
    const badge = document.querySelector('.suggestions-badge');
    const chevron = document.querySelector('.badge-chevron');

    if (panel.style.display === 'none') {
        panel.style.display = 'block';
        chevron.textContent = '▲';
        badge.classList.add('expanded');
    } else {
        panel.style.display = 'none';
        chevron.textContent = '▼';
        badge.classList.remove('expanded');
    }
}

/**
 * Handle suggestion feedback (Phase 3)
 * @param {string} patternId - Pattern UUID
 * @param {string} action - 'accept', 'reject', or 'dismiss'
 */
async function handleSuggestionFeedback(patternId, action) {
    console.log(`Suggestion feedback: ${action} for pattern ${patternId}`);

    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/learning/patterns/${patternId}/feedback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action: action })
        });

        if (!response.ok) {
            throw new Error('Feedback submission failed');
        }

        const result = await response.json();

        // Remove the suggestion card with animation
        const card = document.querySelector(`[data-pattern-id="${patternId}"]`);
        if (card) {
            card.style.opacity = '0.5';
            card.style.transition = 'opacity 0.3s';
            setTimeout(() => {
                card.remove();

                // Update badge count
                const remaining = document.querySelectorAll('.suggestion-card').length;
                if (remaining === 0) {
                    document.querySelector('.suggestions-container').remove();
                } else {
                    const badge = document.querySelector('.suggestions-badge');
                    const plural = remaining === 1 ? '' : 's';
                    badge.innerHTML = `💡 ${remaining} pattern suggestion${plural} <span class="badge-chevron">▲</span>`;
                }
            }, 300);
        }

        // Show feedback toast
        showFeedbackToast(action);

    } catch (error) {
        console.error('Feedback error:', error);
        alert('Failed to submit feedback. Please try again.');
    }
}

/**
 * Show feedback toast message (Phase 3)
 * @param {string} action - Feedback action
 */
function showFeedbackToast(action) {
    const messages = {
        accept: '✓ Pattern accepted - confidence increased',
        reject: '✗ Pattern rejected - confidence decreased',
        dismiss: 'Pattern dismissed'
    };

    const toast = document.createElement('div');
    toast.className = 'feedback-toast';
    toast.textContent = messages[action];
    document.body.appendChild(toast);

    setTimeout(() => toast.classList.add('show'), 10);
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 2000);
}

/**
 * Handle workflow completion responses
 * @param {Object} data - Workflow data object
 * @param {HTMLElement} element - DOM element to update
 */
function handleWorkflowResponse(data, element) {
    console.log('Workflow response:', data.message);

    if (data.type === 'analyze_file' || data.type === 'generate_report') {
        const message = data.message || 'File analysis completed successfully!';
        element.innerHTML = renderBotMessage(message, 'success', false);
    } else {
        // GitHub issue logic (keep existing special case)
        const finalResult = data.tasks && data.tasks[data.tasks.length - 1]?.result?.issue;
        if (finalResult && finalResult.url) {
            element.innerHTML = `
                <div class="result success">
                    <strong>✅ GitHub Issue Created!</strong><br>
                    <strong>#${finalResult.number}:</strong> ${finalResult.title}<br>
                    <strong>URL:</strong> <a href="${finalResult.url}" target="_blank">View on GitHub</a>
                </div>`;
        } else {
            const message = data.message || 'Workflow completed successfully!';
            element.innerHTML = renderBotMessage(message, 'success', false);
        }
    }
}

/**
 * Handle error responses
 * @param {Error} error - Error object
 * @param {HTMLElement} element - DOM element to update
 */
function handleErrorResponse(error, element) {
    console.error('Error response:', error.message);
    element.innerHTML = renderBotMessage(error.message, 'error', false);
}
