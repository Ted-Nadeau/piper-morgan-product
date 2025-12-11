// Setup Wizard JavaScript (Issue #390)
(function() {
    'use strict';

    // State
    let currentStep = 1;
    let openaiValid = false;
    let userId = null;
    const apiKeys = { openai: null, anthropic: null, gemini: null };
    const keychainKeys = { openai: false, anthropic: false, gemini: false }; // Track which keys came from keychain

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
        const providers = ['openai', 'anthropic', 'gemini'];
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
                    statusDiv.textContent = '✓ Valid';
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
                    gemini_key: keychainKeys.gemini ? null : apiKeys.gemini
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

    checkSetupStatus();
})();
