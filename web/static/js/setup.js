// Setup Wizard JavaScript (Issue #390, #528)
(function() {
    'use strict';

    // State
    let currentStep = 1;
    let openaiValid = false;
    let userId = null;
    let slackConnected = false;  // Issue #528: Track Slack OAuth status
    const apiKeys = { openai: null, anthropic: null, gemini: null, notion: null };
    const keychainKeys = { openai: false, anthropic: false, gemini: false, notion: false }; // Track which keys came from keychain

    // DOM elements
    const steps = document.querySelectorAll('.setup-step');
    const progressSteps = document.querySelectorAll('.setup-progress .step');
    const errorDiv = document.getElementById('error-message');

    // Utility functions
    function showError(message, title = 'Error') {
        if (typeof Toast !== 'undefined') {
            Toast.error(title, message);
        } else {
            // Fallback for when Toast not loaded
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            setTimeout(() => { errorDiv.style.display = 'none'; }, 5000);
        }
    }

    function showStep(stepNum) {
        steps.forEach(s => s.classList.remove('active'));
        progressSteps.forEach((p, i) => {
            p.classList.remove('active', 'completed');
            if (i + 1 < stepNum) p.classList.add('completed');
            if (i + 1 === stepNum) p.classList.add('active');
        });
        document.getElementById(`step-${stepNum}`).classList.add('active');
        currentStep = stepNum;

        // Check keychain availability when entering step 2
        if (stepNum === 2) {
            checkKeychainAvailability();
        }
    }

    // Check if keys exist in keychain and show buttons
    async function checkKeychainAvailability() {
        const providers = ['openai', 'anthropic', 'gemini', 'notion'];
        for (const provider of providers) {
            try {
                const response = await fetch(`/setup/check-keychain/${provider}`);
                const data = await response.json();
                const btn = document.querySelector(`.keychain-btn[data-provider="${provider}"]`);
                if (btn && data.exists) {
                    btn.classList.remove('hidden');
                }
            } catch (err) {
                // Silently fail - button stays hidden
                console.log(`Keychain check failed for ${provider}:`, err);
            }
        }
    }

    // Step 1: System Check
    document.getElementById('check-system-btn').addEventListener('click', async function() {
        this.disabled = true;
        this.textContent = 'Checking...';
        document.getElementById('step-1-description').textContent = 'Checking that all required services are running...';

        try {
            const statusDiv = document.getElementById('system-status');

            // Show progress animation while checking
            statusDiv.innerHTML = `
                <div class="service-status checking">⏳ Checking Docker...</div>
                <div class="service-status checking">⏳ Checking PostgreSQL...</div>
                <div class="service-status checking">⏳ Checking Redis...</div>
                <div class="service-status checking">⏳ Checking ChromaDB...</div>
                <div class="service-status checking">⏳ Checking Temporal...</div>
            `;

            const response = await fetch('/setup/check-system', { method: 'POST' });
            const data = await response.json();

            // Animate results appearing sequentially
            const services = [
                { name: 'Docker', ready: data.docker_available },
                { name: 'PostgreSQL', ready: data.postgres_ready },
                { name: 'Redis', ready: data.redis_ready },
                { name: 'ChromaDB', ready: data.chromadb_ready },
                { name: 'Temporal (optional)', ready: data.temporal_ready },
            ];

            statusDiv.innerHTML = '';

            // Reveal each service result with 200ms delay for visual feedback
            for (let i = 0; i < services.length; i++) {
                const service = services[i];
                await new Promise(resolve => setTimeout(resolve, 200));

                const serviceEl = document.createElement('div');
                serviceEl.className = `service-status ${service.ready ? 'ready' : 'not-ready'}`;
                serviceEl.style.opacity = '0';
                serviceEl.style.transform = 'translateY(10px)';
                serviceEl.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                serviceEl.textContent = `${service.ready ? '✓' : '✗'} ${service.name}`;

                statusDiv.appendChild(serviceEl);

                // Trigger animation
                requestAnimationFrame(() => {
                    serviceEl.style.opacity = '1';
                    serviceEl.style.transform = 'translateY(0)';
                });
            }

            if (data.all_required_ready) {
                // Small delay before showing next button for satisfaction
                await new Promise(resolve => setTimeout(resolve, 400));
                document.getElementById('next-1').style.display = 'block';
                this.style.display = 'none';
            } else {
                showError('Required services are offline. Run: docker-compose up -d', 'Services Not Running');
                this.disabled = false;
                this.textContent = 'Retry Check';
            }
        } catch (err) {
            if (!navigator.onLine) {
                showError('Check your internet connection and try again.', 'No Connection');
            } else {
                showError('Unable to reach server. Please try again.', 'Connection Failed');
            }
            this.disabled = false;
            this.textContent = 'Retry Check';
        }
    });

    document.getElementById('next-1').addEventListener('click', () => showStep(2));

    // Step 2: API Key Validation
    document.querySelectorAll('.validate-key-btn').forEach(btn => {
        btn.addEventListener('click', async function() {
            const provider = this.dataset.provider;
            const input = document.getElementById(`${provider}-key`);
            const statusDiv = document.getElementById(`${provider}-status`);
            const apiKey = input.value.trim();

            if (!apiKey) {
                statusDiv.textContent = 'Please enter an API key';
                statusDiv.className = 'validation-status invalid';
                return;
            }

            this.disabled = true;
            statusDiv.textContent = 'Validating...';
            statusDiv.className = 'validation-status';

            try {
                const response = await fetch('/setup/validate-key', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ provider, api_key: apiKey })
                });
                const data = await response.json();

                if (data.valid) {
                    // Use workspace_name for Notion, otherwise use generic message
                    const message = data.workspace_name
                        ? `✓ Valid (Connected to '${data.workspace_name}')`
                        : `✓ ${data.message}`;
                    statusDiv.textContent = message;
                    statusDiv.className = 'validation-status valid';
                    apiKeys[provider] = apiKey;
                    keychainKeys[provider] = false; // Manually entered
                    if (provider === 'openai') {
                        openaiValid = true;
                        document.getElementById('next-2').disabled = false;
                    }
                } else {
                    statusDiv.textContent = '✗ ' + data.message;
                    statusDiv.className = 'validation-status invalid';
                    if (provider === 'openai') openaiValid = false;
                }
            } catch (err) {
                statusDiv.textContent = '✗ Validation failed';
                statusDiv.className = 'validation-status invalid';
                if (!navigator.onLine) {
                    showError('Check your internet connection and try again.', 'No Connection');
                } else {
                    showError('Unable to validate API key. Please try again.', 'Validation Failed');
                }
            }
            this.disabled = false;
        });
    });

    // Keychain button handlers
    document.querySelectorAll('.keychain-btn').forEach(btn => {
        btn.addEventListener('click', async function() {
            const provider = this.dataset.provider;
            const input = document.getElementById(`${provider}-key`);
            const statusDiv = document.getElementById(`${provider}-status`);

            this.disabled = true;
            statusDiv.textContent = 'Retrieving from keychain...';
            statusDiv.className = 'validation-status';

            try {
                const response = await fetch('/setup/use-keychain', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ provider })
                });
                const data = await response.json();

                if (data.success && data.valid) {
                    // Show masked value in input
                    input.value = '••••••••••••••••';
                    input.disabled = true;
                    statusDiv.textContent = '✓ ' + data.message;
                    statusDiv.className = 'validation-status valid';
                    apiKeys[provider] = '__FROM_KEYCHAIN__'; // Signal to use keychain
                    keychainKeys[provider] = true;
                    // Hide keychain button, disable validate button
                    this.classList.add('hidden');
                    document.querySelector(`.validate-key-btn[data-provider="${provider}"]`).disabled = true;
                    if (provider === 'openai') {
                        openaiValid = true;
                        document.getElementById('next-2').disabled = false;
                    }
                } else if (data.success && !data.valid) {
                    statusDiv.textContent = '✗ ' + data.message;
                    statusDiv.className = 'validation-status invalid';
                } else {
                    statusDiv.textContent = '✗ ' + data.message;
                    statusDiv.className = 'validation-status invalid';
                }
            } catch (err) {
                statusDiv.textContent = '✗ Keychain access failed';
                statusDiv.className = 'validation-status invalid';
                showError('Unable to access system keychain. Enter key manually instead.', 'Keychain Error');
            }
            this.disabled = false;
        });
    });

    document.getElementById('next-2').addEventListener('click', () => showStep(3));

    // Step 3: Account Creation - Initialize form validation
    if (typeof FormValidation !== 'undefined' && typeof Validators !== 'undefined') {
        FormValidation.init('account-form', {
            username: [Validators.required(), Validators.minLength(3)],
            email: [Validators.required(), Validators.email()],
            password: [Validators.required(), Validators.minLength(8)],
            'password-confirm': [
                Validators.required(),
                Validators.custom(
                    (value) => value === document.getElementById('password').value,
                    'Passwords do not match'
                )
            ]
        });
    }

    document.getElementById('account-form').addEventListener('submit', async function(e) {
        e.preventDefault();

        // Use FormValidation if available
        if (typeof FormValidation !== 'undefined') {
            if (!FormValidation.validateForm('account-form')) {
                showError('Please fix the form errors before continuing.', 'Validation Error');
                return;
            }
        }

        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const passwordConfirm = document.getElementById('password-confirm').value;

        // Fallback password check if FormValidation not loaded
        if (typeof FormValidation === 'undefined' && password !== passwordConfirm) {
            showError('Passwords do not match.', 'Validation Error');
            return;
        }

        const submitBtn = this.querySelector('button[type="submit"]');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Creating...';

        try {
            const response = await fetch('/setup/create-user', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password, password_confirm: passwordConfirm })
            });
            const data = await response.json();

            if (data.success) {
                userId = data.user_id;
                // Complete setup
                await completeSetup();
            } else {
                showError(data.message || 'Failed to create account.', 'Account Creation Failed');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Create Account';
            }
        } catch (err) {
            if (!navigator.onLine) {
                showError('Check your internet connection and try again.', 'No Connection');
            } else {
                showError('Unable to create account. Please try again.', 'Account Creation Failed');
            }
            submitBtn.disabled = false;
            submitBtn.textContent = 'Create Account';
        }
    });

    async function completeSetup() {
        try {
            // Don't send keys that came from keychain (they're already stored)
            const response = await fetch('/setup/complete', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    openai_key: keychainKeys.openai ? null : apiKeys.openai,
                    anthropic_key: keychainKeys.anthropic ? null : apiKeys.anthropic,
                    gemini_key: keychainKeys.gemini ? null : apiKeys.gemini,
                    notion_key: keychainKeys.notion ? null : apiKeys.notion
                })
            });
            const data = await response.json();

            if (data.success) {
                showStep(4);
            } else {
                showError(data.message || 'Unable to complete setup.', 'Setup Failed');
            }
        } catch (err) {
            if (!navigator.onLine) {
                showError('Check your internet connection and try again.', 'No Connection');
            } else {
                showError('Unable to complete setup. Please try again.', 'Setup Failed');
            }
        }
    }

    // Check initial setup status
    async function checkSetupStatus() {
        try {
            const response = await fetch('/setup/status');
            const data = await response.json();
            if (data.setup_complete) {
                window.location.href = '/login';
            }
        } catch (err) {
            // Ignore - just continue with setup
        }
    }

    // =========================================================================
    // Slack OAuth Functions (Issue #528: ALPHA-SETUP-SLACK)
    // =========================================================================

    // Check for OAuth callback params in URL (after redirect from Slack)
    function checkSlackCallbackParams() {
        const params = new URLSearchParams(window.location.search);

        if (params.get('slack_success') === 'true') {
            const workspace = params.get('slack_workspace') || 'Workspace';
            showSlackConnected(decodeURIComponent(workspace));
            // Clean URL by removing OAuth params
            window.history.replaceState({}, document.title, '/setup#step-2');
        } else if (params.get('slack_error')) {
            const error = params.get('slack_error');
            showSlackError(getSlackErrorMessage(error));
            window.history.replaceState({}, document.title, '/setup#step-2');
        }
    }

    // Check if Slack is already configured
    async function checkSlackStatus() {
        try {
            const response = await fetch('/setup/slack/status');
            const data = await response.json();

            if (data.configured) {
                showSlackConnected(data.workspace_name || 'Connected');
            }
        } catch (err) {
            console.log('Slack status check failed:', err);
        }
    }

    // Start OAuth flow - redirects to Slack
    async function connectSlack() {
        const btn = document.getElementById('connect-slack-btn');
        if (btn) {
            btn.disabled = true;
            btn.textContent = 'Connecting...';
        }

        try {
            const response = await fetch('/setup/slack/oauth/start');
            const data = await response.json();

            if (data.auth_url) {
                // Redirect to Slack OAuth
                window.location.href = data.auth_url;
            } else {
                showSlackError('Failed to start OAuth flow');
                if (btn) {
                    btn.disabled = false;
                    btn.textContent = 'Connect to Slack';
                }
            }
        } catch (err) {
            showSlackError('Connection failed. Please try again.');
            if (btn) {
                btn.disabled = false;
                btn.textContent = 'Connect to Slack';
            }
        }
    }

    function showSlackConnected(workspace) {
        const notConnected = document.getElementById('slack-not-connected');
        const connected = document.getElementById('slack-connected');
        const workspaceName = document.getElementById('slack-workspace-name');
        const errorDiv = document.getElementById('slack-error');

        if (notConnected) notConnected.style.display = 'none';
        if (connected) connected.style.display = 'flex';
        if (workspaceName) workspaceName.textContent = `Connected to ${workspace}`;
        if (errorDiv) errorDiv.style.display = 'none';
        slackConnected = true;
    }

    function showSlackError(message) {
        const errorDiv = document.getElementById('slack-error');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
    }

    function getSlackErrorMessage(error) {
        const messages = {
            'access_denied': 'Authorization was denied. Please try again.',
            'missing_params': 'OAuth callback missing parameters.',
            'callback_failed': 'Failed to complete authorization.',
            'invalid_state': 'Session expired. Please try again.',
        };
        return messages[error] || 'An error occurred. Please try again.';
    }

    // Event listeners for Slack OAuth
    const connectSlackBtn = document.getElementById('connect-slack-btn');
    if (connectSlackBtn) {
        connectSlackBtn.addEventListener('click', connectSlack);
    }

    // Initialize Slack OAuth on page load
    checkSlackCallbackParams();
    checkSlackStatus();

    // =========================================================================
    // Google Calendar OAuth Functions (Issue #529: ALPHA-SETUP-CALENDAR)
    // =========================================================================

    // Check for OAuth callback params in URL (after redirect from Google)
    function checkCalendarCallbackParams() {
        const params = new URLSearchParams(window.location.search);

        if (params.get('calendar_success') === 'true') {
            const email = params.get('calendar_email') || 'Calendar';
            showCalendarConnected(decodeURIComponent(email));
            // Clean URL by removing OAuth params
            window.history.replaceState({}, document.title, '/setup#step-2');
        } else if (params.get('calendar_error')) {
            const error = params.get('calendar_error');
            showCalendarError(getCalendarErrorMessage(error));
            window.history.replaceState({}, document.title, '/setup#step-2');
        }
    }

    // Check if Calendar is already configured
    async function checkCalendarStatus() {
        try {
            const response = await fetch('/setup/calendar/status');
            const data = await response.json();

            if (data.configured) {
                showCalendarConnected(data.email || 'Connected');
            }
        } catch (err) {
            console.log('Calendar status check failed:', err);
        }
    }

    // Start OAuth flow - redirects to Google
    async function connectCalendar() {
        const btn = document.getElementById('connect-calendar-btn');
        if (btn) {
            btn.disabled = true;
            btn.textContent = 'Connecting...';
        }

        try {
            const response = await fetch('/setup/calendar/oauth/start');
            const data = await response.json();

            if (data.auth_url) {
                // Redirect to Google OAuth
                window.location.href = data.auth_url;
            } else {
                showCalendarError('Failed to start OAuth flow');
                if (btn) {
                    btn.disabled = false;
                    btn.textContent = 'Connect Calendar';
                }
            }
        } catch (err) {
            showCalendarError('Connection failed. Please try again.');
            if (btn) {
                btn.disabled = false;
                btn.textContent = 'Connect Calendar';
            }
        }
    }

    function showCalendarConnected(email) {
        const notConnected = document.getElementById('calendar-not-connected');
        const connected = document.getElementById('calendar-connected');
        const emailSpan = document.getElementById('calendar-email');
        const errorDiv = document.getElementById('calendar-error');

        if (notConnected) notConnected.style.display = 'none';
        if (connected) connected.style.display = 'flex';
        if (emailSpan) emailSpan.textContent = `Connected: ${email}`;
        if (errorDiv) errorDiv.style.display = 'none';
    }

    function showCalendarError(message) {
        const errorDiv = document.getElementById('calendar-error');
        if (errorDiv) {
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
        }
    }

    function getCalendarErrorMessage(error) {
        const messages = {
            'access_denied': 'Authorization was denied. Please try again.',
            'missing_params': 'OAuth callback missing parameters.',
            'callback_failed': 'Failed to complete authorization.',
        };
        return messages[error] || 'An error occurred. Please try again.';
    }

    // Event listeners for Calendar OAuth
    const connectCalendarBtn = document.getElementById('connect-calendar-btn');
    if (connectCalendarBtn) {
        connectCalendarBtn.addEventListener('click', connectCalendar);
    }

    // Initialize Calendar OAuth on page load
    checkCalendarCallbackParams();
    checkCalendarStatus();

    checkSetupStatus();
})();
