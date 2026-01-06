# Passkey FAQ

Everything you need to know about passkeys—a modern, secure way to sign in without passwords.

---

## Getting Started Checklist

{% hint style="danger" %}
**Important:** Complete these steps immediately after creating your account to prevent lockout.
{% endhint %}

After creating your account with a passkey, you should:

- [ ] **Connect a Stellar wallet** — Go to Security settings on the web app and connect your Stellar wallet (Freighter, Lobstr, xBull). This is your backup if you lose passkey access.
- [ ] **Add passkeys on other devices** — If you use both iPhone and Android, add a passkey on each device.
- [ ] **Verify your backup works** — Sign out and try signing in with your Stellar wallet to confirm it's set up correctly.

| Sign-in Method | Where to Set Up | Purpose |
|----------------|-----------------|---------|
| Passkey | Created during signup | Primary sign-in (biometrics) |
| Additional passkeys | Security settings | Access from other devices |
| Stellar wallet | Security settings (web only) | Backup recovery method |

---

## Passkey Basics

### What is a passkey?

A passkey is a digital credential that replaces traditional passwords. Instead of typing a password, you authenticate using your device's built-in security—like Face ID, Touch ID, fingerprint, or screen lock PIN.

Passkeys are based on the **WebAuthn** standard and use public-key cryptography, making them significantly more secure than passwords.

---

### How are passkeys different from passwords?

| Aspect | Passwords | Passkeys |
|--------|-----------|----------|
| **Security** | Can be guessed, stolen, or leaked | Cannot be phished or stolen remotely |
| **User Experience** | Must remember or store securely | Just use biometrics or device PIN |
| **Phishing Risk** | High—fake sites can steal passwords | None—bound to specific domain |
| **Reuse Risk** | Often reused across sites | Unique per site automatically |
| **Server Storage** | Stored (can be breached) | Only public key stored (useless if breached) |

---

### Why are passkeys more secure than passwords?

Passkeys use **public-key cryptography**. When you create a passkey, your device generates two keys:

- **Private key** — kept securely on your device, never leaves
- **Public key** — shared with the website

During sign-in, your device proves it has the private key without ever sending it. This means:

- Nothing secret is transmitted over the network
- Nothing valuable is stored on the server to steal
- Phishing sites can't intercept your credentials
- Each passkey is unique to each website

---

### What do I need to use passkeys?

Most modern devices already support passkeys. You need:

- A device with secure authentication (Face ID, Touch ID, fingerprint, or PIN)
- An updated operating system

**Supported platforms:**

| Platform | Minimum Version |
|----------|-----------------|
| iOS / iPadOS | 16+ |
| macOS | Ventura+ |
| Android | 9+ |
| Windows | 10+ |
| Chrome | 109+ |
| Safari | 16+ |
| Firefox | 122+ |
| Edge | 109+ |

---

## Creating and Using Passkeys

### How do I create a passkey?

1. Sign up for a new account or go to security settings on an existing account
2. Look for "Create passkey" or "Add passkey" option
3. Follow the prompts on your device
4. Authenticate with your biometrics or PIN
5. Done! The passkey is automatically created and stored

---

### How do I sign in with a passkey?

1. Go to the sign-in page
2. Select the passkey option (often shown as "Sign in with passkey" or a key icon)
3. Your device prompts for Face ID, Touch ID, fingerprint, or PIN
4. Authenticate
5. You're signed in—no password needed

---

### Can I have multiple passkeys for the same account?

**Yes!** You can register multiple passkeys for the same account. This is highly recommended for backup access.

For example:
- One passkey on your iPhone (stored in iCloud Keychain)
- Another passkey on your Android phone (stored in Google Password Manager)
- A third in a password manager like 1Password

Each passkey has a unique `credentialId`, and the website stores all of them linked to your account.

---

### What happens if I'm prompted for a passkey but I'm on a different device?

You can use **cross-device authentication**:

1. The device you're on displays a QR code
2. Scan it with your phone (which has your passkey)
3. Bluetooth verifies both devices are physically close
4. Your phone authenticates you

{% hint style="info" %}
This doesn't transfer the passkey—it just lets you sign in that one time.
{% endhint %}

---

## Passkey Syncing Across Devices

### Do passkeys sync across my devices?

Yes, but **only within the same ecosystem**:

| Ecosystem | Sync Method | Devices |
|-----------|-------------|---------|
| **Apple** | iCloud Keychain | iPhone, iPad, Mac |
| **Google** | Google Password Manager | Android, Chrome (all platforms) |
| **Microsoft** | Windows Hello | Windows devices |
| **Password Managers** | Their own sync | Cross-platform |

---

### Can I use a passkey stored in Google Password Manager on my iPhone?

**Not directly.**

iOS requires all browsers to use Safari's engine, which only accesses iCloud Keychain for passkeys. Even Chrome on iOS cannot access Google Password Manager passkeys.

**Workaround:** Use cross-device authentication:
1. Your iPhone shows a QR code
2. Scan it with your Android phone
3. Your Android authenticates you

For regular use on both platforms, **register separate passkeys on each device**.

---

### Where exactly are my passkeys stored?

| Platform | Storage Location |
|----------|------------------|
| iPhone / iPad / Mac | iCloud Keychain (end-to-end encrypted) |
| Android | Google Password Manager |
| Chrome (desktop) | Google Password Manager (when signed in) |
| Windows | Windows Hello / Microsoft Account |
| 1Password, Dashlane, Bitwarden | Their encrypted cloud (cross-platform) |

---

### Cross-platform compatibility matrix

Here's what works when your passkey is stored in Google Password Manager:

| Device / Browser | Direct Access? | Alternative |
|------------------|----------------|-------------|
| Android (any browser) | ✅ Yes | — |
| Chrome on Windows | ✅ Yes | — |
| Chrome on macOS | ✅ Yes | — |
| Chrome on Linux | ✅ Yes | — |
| Safari on macOS | ❌ No | Uses iCloud Keychain |
| iOS (any browser) | ❌ No | QR code + Android phone |

{% hint style="warning" %}
For seamless cross-ecosystem access, use a password manager that supports passkeys on all platforms (1Password, Dashlane, Bitwarden).
{% endhint %}

---

## Recovery and Backup

### What if I lose my phone?

If your passkeys are synced to a cloud service (iCloud, Google), you can recover them by signing into a new device with the same account.

**If you lose access to your passkey entirely**, you can still recover your account using a connected Stellar wallet:

1. Open the web app on any device
2. Select "Sign in with Stellar Wallet"
3. Connect your Stellar wallet (Freighter, Lobstr, xBull, etc.)
4. Once signed in, go to **Security** and add a new passkey

{% hint style="warning" %}
**No connected wallet?** If you haven't connected a Stellar wallet and lose all passkey access, account recovery may not be possible. Always set up a backup sign-in method.
{% endhint %}

---

### What if I lose access to my cloud account (Apple ID or Google)?

This is a critical scenario. If you lose access to your iCloud or Google account, you may lose access to your synced passkeys.

**How to protect yourself:**

| Backup Method | How It Helps |
|---------------|--------------|
| Connect a Stellar wallet | Sign in from any device, independent of passkeys |
| Passkeys on multiple ecosystems | iPhone + Android = two independent backups |
| Recovery keys for cloud accounts | Regain access to iCloud/Google if locked out |

---

### How do I connect a Stellar wallet for backup?

1. Sign in to your account (using passkey)
2. Open the **web app** (wallet connection is only available on web)
3. Go to **Security** settings
4. Click "Connect Stellar Wallet"
5. Choose your wallet (Freighter, Lobstr, xBull, etc.)
6. Approve the connection in your wallet

**Supported Stellar wallets:**
- Freighter (browser extension)
- Lobstr (mobile & web)
- xBull (browser extension & mobile)
- Other WalletConnect-compatible Stellar wallets

{% hint style="info" %}
Your Stellar wallet becomes an alternative sign-in method. You can use it to access your account even if all your passkeys are lost.
{% endhint %}

---

### Can I export or backup my passkeys manually?

**Generally, no.** Passkeys are designed so the private key never leaves the secure enclave of your device. This is a security feature—it prevents theft.

Your backup options are:
- **Cloud sync**: iCloud Keychain (Apple) or Google Password Manager (Android)
- **Connected Stellar wallet**: Independent backup sign-in method
- **Multiple passkeys**: Register on multiple devices/ecosystems

---

### What recovery options does this app provide?

| Recovery Method | Availability | Notes |
|-----------------|--------------|-------|
| Multiple passkeys | ✅ Supported | Add passkeys on different devices |
| Stellar wallet connection | ✅ Supported | Set up in Security settings (web only) |
| QR code cross-device auth | ✅ Supported | Use another device's passkey to sign in |
| Email recovery | ❌ Not available | — |
| Phone/SMS recovery | ❌ Not available | — |

{% hint style="danger" %}
**Critical:** Since we don't support email or phone recovery, connecting a Stellar wallet is the **only way** to recover your account if you lose all passkey access. Set this up immediately after creating your account.
{% endhint %}

---

## Security Questions

### Can someone steal my passkey?

**Extremely difficult.** The private key is stored in a secure hardware enclave (like Apple's Secure Enclave or Android's Titan chip) and never leaves your device.

Even if someone steals your phone, they can't extract the passkey without your biometrics or PIN.

Unlike passwords, passkeys **cannot** be:
- Phished
- Guessed
- Intercepted over the network
- Stolen from a server breach

---

### What if someone forces me to unlock my phone?

This is a concern with any biometric authentication. Most devices offer quick ways to disable biometrics:

| Device | Emergency Disable |
|--------|-------------------|
| iPhone | Press side button 5 times |
| Android | Use lockdown mode (usually power menu) |
| Windows | Windows + L to lock |

The device will then require only your PIN/password, which you can refuse to provide.

---

### Are passkeys safe if my iCloud or Google account is hacked?

**Additional protection exists:**

- **iCloud Keychain**: End-to-end encrypted—even Apple can't read your passkeys. An attacker needs your account credentials AND access to a trusted device.
- **Google Password Manager**: Uses encryption, though implementation differs from Apple.

**Always enable two-factor authentication on your cloud accounts.**

---

### Can a website see my biometric data?

**No.** Your biometric data (fingerprint, face scan) never leaves your device.

Here's what happens:
1. You initiate sign-in
2. Your device verifies your biometrics **locally**
3. Device uses the private key to sign a cryptographic challenge
4. Only the signature is sent to the website

The website receives **zero** biometric information.

---

## Practical Scenarios

### I created my account on Android. How do I add a passkey on my iPhone?

Since passkeys don't sync between Google Password Manager and iCloud Keychain, you need to register a **new passkey** on your iPhone. Here's how:

**Method 1: Using QR code authentication (if you have your Android)**

1. Open the app/website on your iPhone
2. Tap "Sign in with passkey"
3. Select "Use a different device" or "Sign in with another device"
4. A QR code appears on your iPhone screen
5. Scan it with your Android phone
6. Authenticate on your Android (fingerprint/PIN)
7. You're now signed in on your iPhone
8. Go to **Security** settings and tap "Add passkey"
9. Authenticate with Face ID / Touch ID on iPhone
10. Done! New passkey saved to iCloud Keychain

**Method 2: Using your connected Stellar wallet (if you don't have your Android)**

If you've already connected a Stellar wallet (like Freighter, Lobstr, or xBull) to your account:

1. Open the web app on your iPhone browser
2. Tap "Sign in" → Select "Sign in with Stellar Wallet"
3. Connect your Stellar wallet and approve the sign-in
4. Once signed in, go to **Security** settings
5. Tap "Add passkey"
6. Authenticate with Face ID / Touch ID on iPhone
7. Done! New passkey saved to iCloud Keychain

**Now you have multiple sign-in methods:**
- Original passkey on Android (Google Password Manager)
- New passkey on iPhone (iCloud Keychain)
- Connected Stellar wallet (works anywhere)

{% hint style="warning" %}
**Important:** We strongly recommend connecting a Stellar wallet as a backup sign-in method. This allows you to recover your account even if you lose access to all your passkey devices.
{% endhint %}

---

### I created my account on iPhone. How do I add a passkey on my Android?

The process is the same in reverse:

**Method 1: Using QR code authentication (if you have your iPhone)**

1. Open the app/website on your Android
2. Tap "Sign in with passkey"
3. Select "Use a different device"
4. Scan the QR code with your iPhone
5. Authenticate on your iPhone (Face ID / Touch ID)
6. You're signed in on Android
7. Go to **Security** settings and tap "Add passkey"
8. Authenticate with fingerprint / PIN on Android
9. Done! New passkey saved to Google Password Manager

**Method 2: Using your connected Stellar wallet**

1. Open the web app on your Android browser
2. Tap "Sign in" → Select "Sign in with Stellar Wallet"
3. Connect your Stellar wallet and approve the sign-in
4. Go to **Security** settings → tap "Add passkey"
5. Authenticate with fingerprint / PIN
6. Done!

---

### I use both iPhone and Android. What should I do?

**Set up all sign-in methods for maximum security:**

1. ✅ Create passkey on iPhone → saved to iCloud Keychain
2. ✅ Add passkey on Android → saved to Google Password Manager  
3. ✅ Connect a Stellar wallet → works on any device as backup

This way, you're protected even if you lose one device or switch ecosystems.

---

### Quick reference: Adding passkeys across platforms

| Scenario | Method 1 (Have original device) | Method 2 (No original device) |
|----------|--------------------------------|-------------------------------|
| Created on Android, need on iPhone | Sign in via QR code → Add passkey | Sign in with Stellar wallet → Add passkey |
| Created on iPhone, need on Android | Sign in via QR code → Add passkey | Sign in with Stellar wallet → Add passkey |
| Lost all passkey devices | — | Sign in with Stellar wallet → Add new passkeys |
| New device, same ecosystem | Passkey syncs automatically | No action needed |

{% hint style="success" %}
**Pro tip:** Connect a Stellar wallet to your account immediately after signup. This is your safety net if you ever lose access to your passkey devices.
{% endhint %}

---

### Can I use passkeys on a public or borrowed computer?

**Yes, using cross-device authentication:**

1. Select "Sign in with passkey" on the public computer
2. Choose "Use a different device" or similar option
3. Public computer displays a QR code
4. Scan with your phone
5. Authenticate on your phone

{% hint style="success" %}
The passkey never touches the public computer—it stays securely on your phone. This is much safer than typing a password on an untrusted machine.
{% endhint %}

---

### Do passkeys work offline?

**Partially:**

- ✅ Authentication itself works offline (your device signs the challenge locally)
- ❌ You still need network connectivity to communicate with the website/app
- ❌ Initial passkey creation requires both device and service to be online

---

### What if a website doesn't support passkeys yet?

You'll need to use traditional passwords for that site.

**Passkey adoption is growing rapidly.** Major sites that already support passkeys:
- Google
- Apple
- Microsoft
- Amazon
- PayPal
- GitHub
- Nintendo
- PlayStation
- Many banks and financial services

In the meantime, use a password manager and enable two-factor authentication.

---

## Troubleshooting

### Why isn't my passkey showing up on my new device?

**Check these items:**

1. ✅ Signed into the same cloud account (Apple ID / Google account)?
2. ✅ iCloud Keychain or Google Password Manager sync enabled?
3. ✅ Device has internet connection?
4. ✅ Wait a few minutes—sync can take time
5. ✅ If using a password manager, is it installed and unlocked?

---

### The website says my passkey is invalid. What happened?

**Possible causes:**

| Issue | Solution |
|-------|----------|
| Passkey was revoked on server | Register a new passkey |
| Using passkey from wrong account | Check you're signed into correct account |
| Website updated authentication | Re-register passkey |
| Domain mismatch | Ensure you're on the correct website URL |

---

### Cross-device authentication (QR code) isn't working

**Troubleshooting steps:**

1. ✅ Bluetooth enabled on both devices?
2. ✅ Devices physically close together? (within a few feet)
3. ✅ Both devices have updated software?
4. ✅ Not on a restricted corporate network?
5. ✅ Try moving away from Bluetooth interference

{% hint style="info" %}
Bluetooth proximity check is a security feature—it prevents remote attacks.
{% endhint %}

---

## Glossary

| Term | Definition |
|------|------------|
| **WebAuthn** | The web standard that enables passkeys. Defines how browsers and servers communicate for passwordless authentication. |
| **FIDO2** | The broader authentication framework that includes WebAuthn. FIDO = Fast Identity Online. |
| **Relying Party (RP)** | The website or app that accepts passkeys. The "relying party ID" is typically the domain name. |
| **Authenticator** | The device or software that creates and stores passkeys—your phone, computer, or hardware security key. |
| **Credential ID** | A unique identifier for each passkey. The server stores this to recognize your passkey during sign-in. |
| **Public Key** | The cryptographic key shared with the website. Can be safely stored on servers. |
| **Private Key** | The secret cryptographic key that never leaves your device. Used to prove your identity. |
| **Cross-device Authentication** | Using a passkey from one device to authenticate on another device via QR code and Bluetooth. Also called "hybrid transport." |
| **Secure Enclave / TPM** | Hardware security modules that store private keys in a tamper-resistant chip, separate from the main OS. |

---

## Additional Resources

- [FIDO Alliance](https://fidoalliance.org/) — The organization behind passkey standards
- [Passkeys.io](https://passkeys.io/) — Directory of sites supporting passkeys
- [WebAuthn Guide](https://webauthn.guide/) — Technical documentation for developers
- [Can I Use Passkeys?](https://passkeys.dev/) — Browser and platform support reference

---

{% hint style="info" %}
**Have more questions?** Contact our support team or visit our help center.
{% endhint %}
