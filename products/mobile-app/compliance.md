---
description: >-
  How ROZO Wallet handles sanctions screening, and what ROZO can and cannot do
  with a non-custodial wallet.
icon: shield-check
---

<!-- DRAFT. Not approved for publication. External wording requires founder approval. Remove all HTML comments before merge. -->

# Compliance

This page describes the sanctions compliance policy for ROZO Wallet.

## How ROZO Wallet works

ROZO Wallet is a non-custodial smart wallet on Stellar. You sign in with a passkey, and your passkey controls your wallet. ROZO does not hold your funds or your keys.

ROZO does not collect identity information, such as your name or ID documents, and does not verify the identity of wallet users. For this reason, ROZO screens wallet addresses, not people.

## Sanctions screening

ROZO screens the following addresses against the digital currency addresses that the U.S. Treasury's Office of Foreign Assets Control (OFAC) publishes on the Specially Designated Nationals and Blocked Persons List (SDN List):

* ROZO wallet addresses.
* Addresses that send funds to ROZO wallets on Stellar.

<!-- TODO: once screening of cross-chain deposit source addresses is active, add this bullet: "* Addresses that fund ROZO wallets through ROZO cross-chain deposits." Do not add it before it is active. -->

ROZO re-checks known addresses as the SDN List is updated.

## Sanctioned jurisdictions

ROZO blocks requests from comprehensively sanctioned jurisdictions. ROZO determines the location of a request from its IP address.

## ROZO blocklist

ROZO keeps its own blocklist. It can include wallet addresses, users and IP addresses.

## Monitoring and review

ROZO monitors wallet activity with its own rules. Flagged activity is reviewed by a person. ROZO keeps a record of screening results and review decisions.

## What ROZO can and cannot do

ROZO Wallet is non-custodial. ROZO cannot freeze, seize or move the assets in your wallet.

ROZO may deny ROZO services to an address, user or IP address that matches the SDN List, comes from a comprehensively sanctioned jurisdiction, is on the ROZO blocklist, or is flagged in review. ROZO services include:

* Deploying a new ROZO wallet.
* Transactions sponsored by ROZO, where ROZO pays the network fee.

If ROZO denies a service, the app shows that the service is unavailable. ROZO may not give a reason.

## Cash-out

When you cash out through a ROZO partner, identity verification (KYC) is performed by that cash-out partner, not by ROZO. The partner's own terms and checks apply.

<!-- FOUNDER DECISION: (1) name the cash-out partner (MoneyGram) here or keep it generic; (2) cash-out is not live yet, so decide whether to keep this section before launch or add it when cash-out ships. -->

## Questions

Contact [hi@rozo.ai](mailto:hi@rozo.ai).
