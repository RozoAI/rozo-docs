# Passkey FAQ

Everything you need to know about passkeys—a modern, secure way to sign in without passwords.

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

**Best practices for protection:**
- Register multiple passkeys on different devices
- Use passkeys in multiple ecosystems
- Keep alternative sign-in methods enabled

---

### What if I lose access to my cloud account (Apple ID or Google)?

This is a critical scenario. If you lose access to your iCloud or Google account, you may lose access to your synced passkeys.

**Protect yourself:**

- Set up recovery contacts or recovery keys for your cloud accounts
- Register passkeys in multiple ecosystems
- Use a cross-platform password manager
- Keep backup codes from websites in a secure location
- Maintain a recovery email/phone number

---

### Can I export or backup my passkeys manually?

**Generally, no.** Passkeys are designed so the private key never leaves the secure enclave of your device. This is a security feature—it prevents theft.

Your "backup" is the cloud sync:
- iCloud Keychain for Apple
- Google Password Manager for Google/Android
- Password manager's encrypted cloud

{% hint style="info" %}
Some password managers may offer their own encrypted export options, but this varies by provider.
{% endhint %}

---

### What recovery options should apps provide?

Well-designed apps should offer:

- ✅ Multiple passkeys per account
- ✅ Backup codes during setup
- ✅ Alternative verification (email, phone)
- ✅ Account recovery through identity verification
- ✅ Clear documentation on recovery procedures

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

### I use both iPhone and Android. What should I do?

**Register a passkey on each device:**

1. Create your account on iPhone → passkey saved to iCloud Keychain
2. Go to account settings on Android → add another passkey → saved to Google Password Manager

Both will work independently.

**Alternative:** Use a cross-platform password manager like 1Password that syncs passkeys across all your devices.

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
