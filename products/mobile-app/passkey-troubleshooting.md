# Passkey Troubleshooting Guide

This guide helps you resolve common issues when creating or using passkeys with the Rozo wallet app.

---

## Common Issues Overview

| Issue | Platform | Quick Fix |
|-------|----------|-----------|
| "Use PIN, pattern or password" loop | Android | [See Solution](#use-pin-pattern-or-password-loop-android) |
| "Authentication Failed" error | Android/iOS | [See Solution](#authentication-failed-when-logging-in) |
| Passkey not syncing to new device | All | [See Solution](#passkey-not-showing-on-new-device) |
| Can't create passkey | Android | [See Solution](#cant-create-passkey-on-android) |
| QR code sign-in not working | All | [See Solution](#qr-code-cross-device-authentication-not-working) |

---

## "Use PIN, pattern or password" Loop (Android)

### What it looks like

![Use PIN pattern or password screen](https://raw.githubusercontent.com/RozoAI/rozo-docs/main/assets/screenshots/pin-pattern-loop.png)

Users get stuck on this screen during passkey creation. Even after entering the correct PIN, pattern, or password, the same prompt keeps appearing.

### Why this happens

This is a known issue with **Google Play Services** sync on some Android devices. The passkey system requires your device's credential manager to be properly synced with Google, and sometimes this sync gets stuck or fails silently.

### Solutions

**Solution 1: Restart Google Play Services**

1. Go to **Settings** → **Apps** → **Google Play Services**
2. Tap **Force Stop**
3. Go back and try creating the passkey again

**Solution 2: Clear Credential Manager cache**

1. Go to **Settings** → **Apps** → **Show system apps**
2. Find **Credential Manager** or **Google Play Services**
3. Tap **Storage** → **Clear Cache** (not Clear Data)
4. Restart your phone
5. Try creating the passkey again

**Solution 3: Update Google Play Services**

1. Open **Google Play Store**
2. Search for "Google Play Services"
3. If an update is available, tap **Update**
4. After updating, restart your phone

**Solution 4: Check Google Account sync**

1. Go to **Settings** → **Accounts** → **Google**
2. Select your Google account
3. Make sure **Sync** is enabled
4. Tap **Sync now** to force a sync
5. Wait a few minutes, then try again

**Solution 5: Add screen lock (if not set)**

Passkeys require a secure screen lock. If you only have "Swipe" or "None":

1. Go to **Settings** → **Security** → **Screen lock**
2. Set up **PIN**, **Pattern**, or **Password**
3. Also set up a fingerprint if your device supports it
4. Try creating the passkey again

{% hint style="warning" %}
**Still not working?** Some older Android devices or custom ROMs may have compatibility issues with passkeys. Try using the web app on Chrome (desktop) to create your account, then add a passkey on your Android device later.
{% endhint %}

---

## "Authentication Failed" When Logging In

### What it looks like

![Authentication Failed error](https://raw.githubusercontent.com/RozoAI/rozo-docs/main/assets/screenshots/auth-failed.jpeg)

You tap "Login with Passkey" but get an "Authentication Failed" error, even though you have a passkey saved.

### Why this happens

This typically occurs when:
- You're trying to use a passkey from a different device/ecosystem
- The passkey was created on a different platform (e.g., PC) and isn't synced to your phone
- Google Password Manager hasn't synced yet
- The passkey was deleted or corrupted

### Solutions

**Solution 1: Verify you're using the correct passkey**

1. On Android: Go to **Settings** → **Passwords & accounts** → **Google Password Manager**
2. Search for "rozo" or the app domain
3. Check if a passkey exists for this account

**Solution 2: Wait for sync (if passkey was just created)**

If you just created the passkey on another device:
- Wait 5-10 minutes for Google Password Manager to sync
- Make sure your phone has internet connection
- Try signing in again

**Solution 3: Create passkey on PC, can't use on phone?**

Passkeys created in **Chrome on PC** sync to **Google Password Manager** and should work on Android. However:

- They do **NOT** sync to iPhone/iOS (different ecosystem)
- On iPhone, you need to create a **separate passkey** stored in iCloud Keychain

**To access your account on a device without the passkey:**

1. Open the web app on the new device
2. Tap "Login with Passkey"
3. Select "Use a different device" or "Sign in with another device"
4. Scan the QR code with your phone that HAS the passkey
5. Once signed in, go to **Security** settings and add a new passkey for this device

**Solution 4: Use connected wallet as backup**

If you've connected a wallet to your account:

1. Open the web app
2. Select "Sign in with Wallet"
3. Connect your wallet and approve
4. Once signed in, go to **Security** and add a new passkey

{% hint style="info" %}
**Pro tip:** After creating your account, immediately add passkeys on all your devices AND connect a backup wallet. This prevents lockout situations.
{% endhint %}

---

## Passkey Not Showing on New Device

### Symptoms

- You created a passkey on one device
- When you try to sign in on another device, it says "No passkey found" or prompts you to create a new account

### Understanding passkey sync

Passkeys **only sync within the same ecosystem**:

| Created On | Syncs To |
|------------|----------|
| iPhone/iPad/Mac | Other Apple devices (via iCloud Keychain) |
| Android/Chrome | Other Android devices & Chrome browsers (via Google Password Manager) |
| Windows | Other Windows devices (via Microsoft Account) |

**Cross-ecosystem example:**
- ❌ Passkey on iPhone → Will NOT appear on Android
- ❌ Passkey on Android → Will NOT appear on iPhone
- ✅ Passkey on Android → Will appear on Chrome (PC) if signed into same Google account

### Solutions

**If new device is same ecosystem:**

1. Make sure you're signed into the **same account** (Apple ID / Google account)
2. Check that sync is enabled:
   - iOS: **Settings** → **[Your name]** → **iCloud** → **Passwords & Keychain** → On
   - Android: **Settings** → **Passwords & accounts** → **Google** → Sync enabled
3. Wait 5-10 minutes for sync
4. Restart the device and try again

**If new device is different ecosystem:**

You need to add a **new passkey** on the new device:

1. Sign in using QR code authentication:
   - Open app on new device → Tap "Login with Passkey" → Select "Use another device"
   - Scan QR code with your original device
   - Authenticate on original device
2. Once signed in, go to **Security** settings
3. Tap "Add Passkey"
4. Authenticate on the new device
5. Done! You now have passkeys on both ecosystems

---

## Can't Create Passkey on Android

### Symptoms

- Passkey creation fails silently
- App shows loading forever
- Error message appears during setup

### Checklist

**1. Check Android version**
- Passkeys require **Android 9 or newer**
- Go to **Settings** → **About phone** → Check Android version

**2. Check Google Play Services version**
- Open **Google Play Store** → Search "Google Play Services" → Update if available
- Passkeys require a recent version of Google Play Services

**3. Verify screen lock is set up**
- Go to **Settings** → **Security** → **Screen lock**
- Must be **PIN**, **Pattern**, **Password**, or **Biometric** (not "Swipe" or "None")

**4. Check Google account**
- Go to **Settings** → **Accounts** → Ensure a Google account is signed in
- Passkeys are stored in Google Password Manager, which requires a Google account

**5. Check if passkeys are enabled**
- Go to **Settings** → **Passwords & accounts** → **Google Password Manager**
- Tap the gear icon (settings)
- Ensure "Offer to save passkeys" is enabled

**6. Try a different browser (if using web app)**
- Use **Chrome** for best passkey support
- Make sure Chrome is updated to the latest version

{% hint style="warning" %}
**Device compatibility:** Some budget phones, older devices, or phones with custom ROMs may not fully support passkeys. If nothing works, try creating your account on the web (Chrome on PC) and add the mobile device later.
{% endhint %}

---

## QR Code Cross-Device Authentication Not Working

### Symptoms

- QR code appears but nothing happens when scanned
- "Unable to connect" error
- Bluetooth pairing fails

### Requirements

Both devices need:
- ✅ Bluetooth enabled
- ✅ Physically close together (within a few feet)
- ✅ Updated operating system
- ✅ Camera permission (for scanning device)

### Solutions

**1. Enable Bluetooth on both devices**
- This is required for security verification
- The devices must be physically close together

**2. Check camera permissions**
- The scanning device needs camera access
- Go to app settings and enable camera permission

**3. Move devices closer**
- Bluetooth range check is a security feature
- Keep both devices within arm's reach

**4. Restart both devices**
- Turn off both phones
- Wait 30 seconds
- Turn them back on and try again

**5. Update your software**
- Make sure both devices have the latest OS updates
- Update the app to the latest version

**6. Try a different network**
- Corporate networks sometimes block this feature
- Try on home WiFi or mobile data

---

## Creating Account on Web, Using on Mobile

### Recommended setup flow

For the smoothest experience, we recommend:

1. **Create account on Chrome (desktop)**
   - Go to the web app
   - Click "Create Wallet"
   - Create your passkey (saved to Google Password Manager)

2. **Connect a backup wallet**
   - Go to **Security** settings
   - Click "Connect Wallet"
   - Connect your preferred wallet

3. **Add passkey on your phone**
   - **Android:** Open the app → Login with Passkey → Should work automatically (synced via Google)
   - **iPhone:** Open web app → Login with Passkey → Use QR code with PC → Then add new passkey in Security

4. **Verify everything works**
   - Sign out
   - Sign back in with passkey on each device
   - Sign in once with connected wallet to verify backup

---

## Still Need Help?

If you've tried all the solutions above and still have issues:

1. **Check our FAQ** — Many common questions are answered there
2. **Join our Discord** — Community members and team can help troubleshoot
3. **Contact Support** — Email us with:
   - Your device model and OS version
   - Screenshots of the error
   - Steps you've already tried

{% hint style="info" %}
**When reporting issues, please include:**
- Device: (e.g., "Samsung Galaxy S23, Android 14")
- What you were trying to do
- The exact error message or screenshot
- What you've already tried
{% endhint %}

---

## Quick Reference: Error Messages

| Error Message | Likely Cause | Solution |
|---------------|--------------|----------|
| "Use PIN, pattern or password" | Google Play Services sync issue | [See solution](#use-pin-pattern-or-password-loop-android) |
| "Authentication Failed" | Passkey not on this device | [See solution](#authentication-failed-when-logging-in) |
| "No passkey found" | Different ecosystem | Add new passkey on this device |
| "Unable to verify" | Bluetooth/proximity issue | Enable Bluetooth, move devices closer |
| "Passkey creation failed" | Device compatibility | Check Android version, screen lock |
