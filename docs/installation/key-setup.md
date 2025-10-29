# Piper Morgan: Secure API Key Setup (Keychain-First)

Your API keys are stored securely in your operating system's keychain, never in plaintext config files.

## Where Keys Are Stored

- **macOS**: Keychain Access (service: `piper-morgan`)
- **Windows**: Credential Manager
- **Linux**: Secret Service (varies by desktop environment)

## Supported Providers

| Provider | Required | Format |
|----------|----------|--------|
| OpenAI | Yes | `sk-...` |
| Anthropic | Optional | `sk-ant-...` |
| Gemini | Optional | API key from Google Cloud |
| Perplexity | Optional | `pplx-...` |

## Method 1: Setup Wizard (Recommended)

```bash
python main.py setup
```

Steps:
1. System checks (Docker, Python, port 8001, database)
2. Create user account (username, optional email)
3. Add API keys:
   - Enter key (input masked, won't appear on screen)
   - Key is validated with provider API
   - Key is stored securely in OS keychain

Supports resume: if setup interrupted, run again to continue from where you left off.

## Method 2: CLI Commands

```bash
# Add a new key (key input is masked)
python main.py keys add openai

# List all configured providers
python main.py keys list

# Validate all configured keys
python main.py keys validate

# Validate a single provider
python main.py keys validate anthropic
```

## Environment Variables (Headless / Server)

For headless servers without GUI keychain access, you can set environment variables:

```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
```

The app will read these if keychain keys aren't found. However, on laptops, keychain is strongly recommended for security.

## Troubleshooting

### Key validation fails
- Check that your API key is correct (copy/paste carefully)
- Verify your account has permissions for the model you're using
- Check provider rate limits or account status
- Some providers charge for API access; ensure billing is set up

### Keychain backend missing (Linux)
- Install your desktop environment's secret service backend:
  - **GNOME**: `gnome-keyring`
  - **KDE**: `kwallet`
  - **Generic**: `python-keyring` with `secretstorage`
- See [keyring docs](https://keyring.readthedocs.io) for details

### Install Certificates error on macOS (Errno 13)
- This is rare but can happen if Python's certificate bundle is read-only
- Fix: upgrade certifi in your venv:
  ```bash
  python -m pip install --upgrade certifi
  ```

## Key Security Notes

- **Never** commit API keys to Git
- **Never** paste keys in chat/email/documents
- **Never** store keys in `config/PIPER.user.md` (that file is for preferences only)
- Use OS keychain or environment variables; keychain is preferred on laptops
- Rotate keys regularly (see `python main.py keys validate` or setup wizard to update)

## Configuration File Separation

- `config/PIPER.user.md` → Your preferences, timezone, working hours, projects, etc.
- OS Keychain → Your API keys (secure, encrypted)
- Environment variables → For server/headless deployments

DO NOT mix them up!

---

**Last Updated**: October 28, 2025
**Status**: Ready for alpha testing
