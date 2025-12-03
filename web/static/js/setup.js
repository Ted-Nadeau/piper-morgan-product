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
    function showError(message) {
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
        setTimeout(() => { errorDiv.style.display = 'none'; }, 5000);
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
            const response = await fetch('/setup/check-system', { method: 'POST' });
            const data = await response.json();

            const statusDiv = document.getElementById('system-status');
            statusDiv.innerHTML = `
                <div class="service-status ${data.postgres_ready ? 'ready' : 'not-ready'}">
                    ${data.postgres_ready ? '✓' : '✗'} PostgreSQL
                </div>
                <div class="service-status ${data.redis_ready ? 'ready' : 'not-ready'}">
                    ${data.redis_ready ? '✓' : '✗'} Redis
                </div>
                <div class="service-status ${data.chromadb_ready ? 'ready' : 'not-ready'}">
                    ${data.chromadb_ready ? '✓' : '✗'} ChromaDB
                </div>
                <div class="service-status ${data.temporal_ready ? 'ready' : 'not-ready'}">
                    ${data.temporal_ready ? '✓' : '✗'} Temporal (optional)
                </div>
            `;

            if (data.all_required_ready) {
                document.getElementById('next-1').style.display = 'block';
                this.style.display = 'none';
            } else {
                showError('Some required services are not running. Please start Docker services.');
                this.disabled = false;
                this.textContent = 'Retry Check';
            }
        } catch (err) {
            showError('Failed to check system: ' + err.message);
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
            }
            this.disabled = false;
        });
    });

    document.getElementById('next-2').addEventListener('click', () => showStep(3));

    // Step 3: Account Creation
    document.getElementById('account-form').addEventListener('submit', async function(e) {
        e.preventDefault();

        const username = document.getElementById('username').value.trim();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const passwordConfirm = document.getElementById('password-confirm').value;

        if (password !== passwordConfirm) {
            showError('Passwords do not match');
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
                showError(data.message || 'Failed to create account');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Create Account';
            }
        } catch (err) {
            showError('Failed to create account: ' + err.message);
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
                showError(data.message || 'Setup completion failed');
            }
        } catch (err) {
            showError('Setup completion failed: ' + err.message);
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
