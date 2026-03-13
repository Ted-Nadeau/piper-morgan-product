# Email Service Integration Research - MVP Planning

**Date**: November 1, 2025
**Purpose**: Research email service options for password reset implementation (Post-Alpha, Pre-MVP)
**Domains Available**: pipermorgan.ai, pmorgan.tech

---

## Executive Summary

**Recommendation**: **SendGrid** (Twilio) - Best balance of reliability, cost, and developer experience for MVP stage.

**Estimated MVP Cost**: $15-20/month
**Setup Time**: 2-3 hours
**Implementation Time**: 3-4 hours (password reset flow)

---

## Service Comparison

### 1. SendGrid (by Twilio) ⭐ **Recommended**

**Pricing**:
- Free tier: 100 emails/day (3,000/month) - Good for alpha/early MVP
- Essentials: $19.95/month - 50,000 emails/month - Good for MVP
- No credit card required for free tier

**Pros**:
- ✅ Industry standard, very reliable
- ✅ Excellent Python SDK (`sendgrid-python`)
- ✅ Great documentation and templates
- ✅ SMTP and API options
- ✅ Email tracking and analytics
- ✅ Template management built-in
- ✅ Easy domain verification

**Cons**:
- ⚠️ Owned by Twilio (acquisition risk)
- ⚠️ Free tier may be limiting if alpha grows

**Best For**: MVP and production scaling

**Setup Steps**:
1. Create SendGrid account (free)
2. Verify domain (pipermorgan.ai recommended)
3. Create API key
4. Add DNS records (SPF, DKIM, DMARC)
5. Install SDK: `pip install sendgrid`

**Code Example**:
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_password_reset(email: str, reset_token: str):
    message = Mail(
        from_email='noreply@pipermorgan.ai',
        to_emails=email,
        subject='Reset Your Piper Morgan Password',
        html_content=f"""
        <h2>Password Reset Request</h2>
        <p>Click the link below to reset your password:</p>
        <a href="https://pipermorgan.ai/reset-password?token={reset_token}">
            Reset Password
        </a>
        <p>This link expires in 1 hour.</p>
        """
    )
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    return response.status_code == 202
```

---

### 2. Mailgun

**Pricing**:
- Free tier: 5,000 emails/month (first 3 months)
- Flex: $35/month - 50,000 emails
- Pay as you go after free tier

**Pros**:
- ✅ Great for developers
- ✅ Excellent API
- ✅ Good deliverability
- ✅ Detailed logs and analytics

**Cons**:
- ⚠️ No permanent free tier
- ⚠️ More expensive than SendGrid long-term

**Best For**: High-volume transactional email

---

### 3. Amazon SES

**Pricing**:
- $0.10 per 1,000 emails
- ~$5/month for 50,000 emails (cheapest!)
- Free tier: 62,000 emails/month if sent from EC2

**Pros**:
- ✅ Extremely cheap at scale
- ✅ AWS integration if using AWS
- ✅ Very reliable

**Cons**:
- ⚠️ More complex setup
- ⚠️ Requires AWS account management
- ⚠️ Must request production access (sandbox by default)
- ⚠️ Less developer-friendly than SendGrid

**Best For**: High volume, AWS-native applications

---

### 4. Postmark

**Pricing**:
- Free tier: 100 emails/month
- $15/month - 10,000 emails
- $50/month - 50,000 emails

**Pros**:
- ✅ Best deliverability rates
- ✅ Focus on transactional email
- ✅ Excellent support
- ✅ Beautiful analytics

**Cons**:
- ⚠️ More expensive per email
- ⚠️ Smaller free tier

**Best For**: Mission-critical transactional email

---

### 5. Resend (Modern Alternative)

**Pricing**:
- Free tier: 3,000 emails/month
- Pro: $20/month - 50,000 emails

**Pros**:
- ✅ Modern, developer-first
- ✅ React email templates
- ✅ Very simple API
- ✅ Great documentation

**Cons**:
- ⚠️ Newer service (less proven)
- ⚠️ Smaller community

**Best For**: Modern stacks with React email templates

---

## Implementation Plan for MVP

### Phase 1: Domain Setup (30 minutes)

**Choose Domain**: pipermorgan.ai (primary brand)

**DNS Records to Add**:
```
# SPF Record (TXT)
v=spf1 include:sendgrid.net ~all

# DKIM Record (TXT)
[Provided by SendGrid after domain verification]

# DMARC Record (TXT)
v=DMARC1; p=none; rua=mailto:postmaster@pipermorgan.ai
```

### Phase 2: SendGrid Setup (1 hour)

1. Create SendGrid account
2. Verify email address
3. Add domain authentication
4. Wait for DNS propagation (24-48h)
5. Create API key with "Mail Send" permissions
6. Test with simple email

### Phase 3: Integration (3-4 hours)

**Create Email Service** (`services/email/email_service.py`):
```python
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from typing import Optional
import os

class EmailService:
    def __init__(self):
        self.client = SendGridAPIClient(
            os.getenv('SENDGRID_API_KEY')
        )
        self.from_email = 'noreply@pipermorgan.ai'

    async def send_password_reset(
        self,
        email: str,
        reset_token: str,
        user_name: Optional[str] = None
    ) -> bool:
        """Send password reset email"""
        reset_url = f"https://pipermorgan.ai/reset-password?token={reset_token}"

        message = Mail(
            from_email=self.from_email,
            to_emails=email,
            subject='Reset Your Piper Morgan Password',
            html_content=self._render_reset_template(
                user_name, reset_url
            )
        )

        try:
            response = self.client.send(message)
            return response.status_code == 202
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    def _render_reset_template(
        self,
        user_name: Optional[str],
        reset_url: str
    ) -> str:
        """Render password reset email template"""
        greeting = f"Hi {user_name}," if user_name else "Hi there,"

        return f"""
        <!DOCTYPE html>
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
            <h2>Password Reset Request</h2>
            <p>{greeting}</p>
            <p>We received a request to reset your Piper Morgan password.</p>
            <p>
                <a href="{reset_url}"
                   style="background-color: #007bff; color: white; padding: 12px 24px;
                          text-decoration: none; border-radius: 4px; display: inline-block;">
                    Reset Your Password
                </a>
            </p>
            <p style="color: #666;">
                This link will expire in 1 hour. If you didn't request this,
                you can safely ignore this email.
            </p>
            <hr style="border: none; border-top: 1px solid #eee; margin: 20px 0;">
            <p style="color: #999; font-size: 12px;">
                Piper Morgan - Your AI-Powered PM Assistant<br>
                <a href="https://pipermorgan.ai">pipermorgan.ai</a>
            </p>
        </body>
        </html>
        """
```

**Password Reset Flow**:
```python
# 1. User requests reset
POST /auth/request-reset
{
    "email": "user@example.com"
}

# 2. Generate reset token
token = secrets.token_urlsafe(32)
expiry = datetime.now() + timedelta(hours=1)
await db.store_reset_token(email, token, expiry)

# 3. Send email
await email_service.send_password_reset(email, token, user_name)

# 4. User clicks link, submits new password
POST /auth/reset-password
{
    "token": "abc123...",
    "new_password": "secure_password"
}

# 5. Validate token, update password
if await db.validate_reset_token(token):
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    await db.update_password(email, hashed)
    await db.delete_reset_token(token)
```

### Phase 4: Testing (1 hour)

**Test Checklist**:
- [ ] Domain verification complete
- [ ] Can send test email
- [ ] Password reset email delivers
- [ ] Reset link works
- [ ] Token expiration works
- [ ] Invalid token rejected
- [ ] Used token can't be reused

---

## Cost Projections

### Alpha Phase (10-20 users)
- **Emails/month**: ~50-100 (password resets only)
- **Cost**: $0 (free tier)

### MVP Phase (50-100 users)
- **Emails/month**: ~500-1,000 (resets + notifications)
- **Cost**: $0-15 (likely still free tier)

### Early Production (500 users)
- **Emails/month**: ~5,000-10,000
- **Cost**: $19.95/month (SendGrid Essentials)

### Scaling (5,000 users)
- **Emails/month**: ~50,000-100,000
- **Cost**: $19.95-89.95/month depending on volume

---

## Alternative: SMTP (Not Recommended)

**Option**: Use Gmail SMTP or custom SMTP server

**Pros**:
- ✅ No additional service
- ✅ Simple setup

**Cons**:
- ❌ Gmail limits: 500 emails/day
- ❌ Poor deliverability (likely spam folder)
- ❌ No analytics or tracking
- ❌ Can't scale
- ❌ Risk of account suspension

**Verdict**: Only use for local development testing

---

## Security Considerations

### Email Security Checklist

1. **SPF Record**: Prevents email spoofing
2. **DKIM Signing**: Verifies email authenticity
3. **DMARC Policy**: Instructs receivers on failed checks
4. **HTTPS Links**: All reset links use HTTPS
5. **Token Expiration**: Reset tokens expire in 1 hour
6. **One-Time Use**: Tokens invalidated after use
7. **Rate Limiting**: Limit reset requests per IP/email

### Best Practices

```python
# Generate secure tokens
import secrets
token = secrets.token_urlsafe(32)  # 256-bit entropy

# Hash tokens in database
import hashlib
token_hash = hashlib.sha256(token.encode()).hexdigest()
await db.store_reset_token(email, token_hash, expiry)

# Verify with constant-time comparison
import hmac
def verify_token(provided: str, stored: str) -> bool:
    return hmac.compare_digest(
        hashlib.sha256(provided.encode()).hexdigest(),
        stored
    )
```

---

## Timeline for MVP Implementation

**When**: Post-Alpha, Pre-MVP (Sprint A9 or A10)

**Estimated Timeline**:
- Domain setup: 30 min (+ 24-48h DNS propagation)
- SendGrid account: 15 min
- Integration code: 3-4 hours
- Testing: 1 hour
- Documentation: 30 min

**Total**: ~5-6 hours active work + DNS wait time

**Dependencies**:
- ✅ Alpha auth working (Issue #281 Option B)
- ✅ User accounts operational
- ✅ Web UI functional

---

## Recommendation Summary

**For MVP (Recommended)**:
- **Service**: SendGrid
- **Domain**: pipermorgan.ai
- **Tier**: Free initially, upgrade to Essentials ($20/mo) when needed
- **Timeline**: Implement after Alpha testing validates user flows
- **Cost**: $0-20/month depending on volume

**Next Steps**:
1. ✅ Complete Alpha testing without email (Option B auth)
2. ✅ Validate password reset UX needs with alpha testers
3. ⏭️ Create SendGrid account (when ready for MVP)
4. ⏭️ Verify pipermorgan.ai domain
5. ⏭️ Implement password reset flow
6. ⏭️ Test thoroughly with alpha users
7. ⏭️ Roll out to MVP users

---

**Status**: Research complete, ready for implementation when needed
**Next Review**: After Alpha testing completes
**Owner**: Christian (xian)

---

*This research provides a clear path forward for email integration while keeping alpha development focused on core multi-user functionality.*
