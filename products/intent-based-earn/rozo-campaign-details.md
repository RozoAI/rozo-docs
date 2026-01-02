# [Draft] ROZO Earn Campaign Incentive Rules

> Version: v9.0
> Updated: 2026/01/03
> Protocol provides the yield, ROZO provides fairness, engagement, and growth.

---

## 1. Campaign Overview

| Item | Details |
|------|---------|
| Campaign Name | ROZO Earn January Incentive Program |
| Total Prize Pool | $10,000 ROZO Subsidy |
| Protocol Yield | 15% APY (Native Protocol) |
| Supported Chains | Solana / Base |
| Campaign Duration | 5 Weeks (5 Independent Weekly Competitions, Points Reset Weekly) |

### Core Highlights

- **Protocol Yield**: 15% APY, unlimited deposits, start earning instantly
- **Cash Back**: Real-time rewards (Bridge: 2x fee refund, Payment: 1%-20% back)
- **ROZO Ensures Fairness**: √n square root scoring prevents whale domination
- **Everyone Can Win**: Leaderboard + Lucky Draw, rewards for all participants
- **Ultra-Low Barrier**: Start with just $1, beginner tasks are easy to complete

---

## 2. Dual-Track Incentive System

ROZO uses a **Cash Back + Point** dual-track incentive system:

| System | Purpose | Calculation | Distribution |
|--------|---------|-------------|--------------|
| **Cash Back** | Instant Rewards (Guaranteed) | Based on transaction type | Real-time |
| **Point** | Leaderboard + Lucky Draw (Gamified Competition) | √(Balance) + Task Points | Daily Snapshot |

```
User Interface View:
┌─────────────────────────┐
│  Cash Back: $0.50       │  ← Transaction Rewards
│  Points: 156 pts        │  ← For Leaderboard/Lucky Draw
│  Rank: #42              │
└─────────────────────────┘
```

### Why Two Separate Systems?

1. **Mental Account Separation**: Cash Back = "Guaranteed money in pocket", Points = "Gamified competition"
2. **Dual Motivation**: Satisfaction when depositing (cashback), satisfaction while holding (points grow)
3. **Reduced Cognitive Load**: Cash Back = Money, Point = Score, no confusion

---

## 3. Cash Back Mechanism

### Rules

| Transaction Type | Cash Back Calculation | Description |
|------------------|----------------------|-------------|
| **Bridge (Cross-chain)** | Fee × 2 | Double refund on cross-chain fees |
| **Payment** | 1% - 20% | Specific cashback rate shown on merchant page before checkout |

### Features

- **Real-time**: Credited immediately upon successful transaction
- **Withdrawable**: Cash Back goes directly to balance, withdraw anytime
- **Independent**: Cash Back and Points are calculated separately

---

## 4. Point System

### Core Formula

```
Daily Points = √(Minimum Balance at UTC 00:00 Snapshot)
```

**Minimum Participation Amount: $1 USDC** (or €1 EU)

### Points Reference Table

| Deposit Amount | Daily Points |
|----------------|--------------|
| $1 | 1 point |
| $10 | 3.16 points |
| $50 | 7.07 points |
| $100 | 10 points |
| $500 | 22.4 points |
| $1,000 | 31.6 points |
| $5,000 | 70.7 points |
| $10,000 | 100 points (calculation cap) |

### Points Cycle Explanation

**Important: 5-Week Campaign = 5 Independent Weekly Competitions, Points Do NOT Accumulate!**

| Point Type | Cycle | Description |
|------------|-------|-------------|
| **One-time Tasks** (First deposit, binding, etc.) | Only once | Claimed in Week 1, not available after |
| **Daily Balance Points** | Recalculated weekly | Resets to zero each week |
| **Referral Bonus** | Recalculated weekly | Follows weekly points |

**Example**:
- Week 1: Balance Points + One-time Tasks + Referrals = **High Score** (New user bonus)
- Week 2+: Only Balance Points + Referrals = **Lower Score** (Sustained deposits)

---

## 5. Beginner Task System (Simple & Easy)

### A. One-Time Tasks (Can Only Be Claimed Once)

| Task | Points | Condition |
|------|--------|-----------|
| First Deposit | **+20 pts** | Deposit ≥ $1 |
| Bind Twitter | +15 pts | OAuth Authorization |
| Bind Discord | +15 pts | OAuth Authorization |
| First Successful Referral | +20 pts | Invite 1 person who deposits ≥ $1 |

**Total One-Time Task Bonus: Up to 70 points**

### B. Daily Tasks (Recalculated Weekly)

| Task | Point Calculation | Frequency | Condition |
|------|-------------------|-----------|-----------|
| Balance Points | √(Daily Minimum Balance) | Daily Snapshot | Balance ≥ $1 |

**Important Rule**: Daily points are calculated based on **minimum balance that day** (prevents flash deposits).

### C. Referral Bonus (Recalculated Weekly)

| Type | Bonus | Condition |
|------|-------|-----------|
| Level-1 Referral | +20% | Referred user deposits ≥ $1 |

**Referral Bonus Formula**:
```
Referral Bonus = Σ(Referred User's Balance Points × 20%)
```

**Notes**:
- Only counts referred user's **balance points**, not one-time task points
- Based on referred user's actual weekly points, recalculated weekly

**Cap Rules**:
- If you have deposits: Cap = Your own points
- If you have no deposits: Cap = 100 points

**Example**:
- User A (no deposits) refers new User B ($50 deposit, 49.49 balance points)
- A's referral bonus = min(49.49 × 20%, 100) = **9.9 points**
- If A refers 10 people (each with 50 balance points), theoretical 100 pts, actual cap **100 points**

---

## 6. Point Rewards Mechanism

### Weekly $1,500 Prize Pool

```
Weekly $1,500 Prize Pool
├── Leaderboard Top 30: $1,000 (By points ranking)
└── Lucky Draw 20 Winners: $500 (Users outside Top 30)
```

### 6.1 Leaderboard Rewards ($1,000/week)

| Rank | Reward |
|------|--------|
| 1 | $150 |
| 2 | $100 |
| 3 | $80 |
| 4-10 | $50 each ($350) |
| 11-20 | $20 each ($200) |
| 21-30 | $12 each ($120) |

**No Threshold**: All users ranked by points, highest scores enter Top 30.

### 6.2 Lucky Draw ($500/week)

| Item | Details |
|------|---------|
| Prize Pool | $500/week |
| Winners | 20 people |
| Prize per Winner | $25 |

**Lucky Draw Conditions**:
- Not in Top 30 leaderboard
- Must have points to participate

**Draw Rules**: Weighted lottery, higher points = higher winning probability.

---

## 7. Quick Reference Table

### Cash Back Rules

| Rule | Value |
|------|-------|
| Bridge Cashback | Fee × 2 |
| Payment Cashback | 1% - 20% |
| Distribution | Real-time |

### Point Rules

| Rule | Value |
|------|-------|
| Minimum Valid Deposit | **$1** |
| Points Calculation Balance Cap | $10,000 |
| Valid Referral Threshold | Referred user deposits ≥ $1 |
| Referral Bonus Cap (With Deposit) | Cannot exceed own points |
| Referral Bonus Cap (No Deposit) | 100 points |
| Daily Snapshot Time | UTC 00:00 |
| Points Cycle | Weekly reset (except one-time tasks) |
| Draw Announcement Time | Monday 00:00 UTC (Singapore/HK 08:00 / London 00:00 / LA Sunday 16:00) |

---

## 8. User Earnings Examples

### New User Week 1 (Deposit $100)

| Earnings Source | Amount/Points |
|-----------------|---------------|
| **Cash Back** | Based on transaction type |
| Protocol Yield (15% APY) | ~$0.29/week |
| Daily Balance Points | 10 × 7 = 70 pts |
| One-time Tasks | +70 pts (First deposit + bindings, etc.) |
| **Weekly Total Points** | **140 pts** |

### Returning User Week 2 (Same $100)

| Earnings Source | Amount/Points |
|-----------------|---------------|
| Protocol Yield (15% APY) | ~$0.29/week |
| Daily Balance Points | 10 × 7 = 70 pts |
| One-time Tasks | 0 (Already claimed) |
| **Weekly Total Points** | **70 pts** |

### Referral-Only User (No Deposit, Refers 5 New Users)

| Earnings Source | Points |
|-----------------|--------|
| Own Balance Points | 0 pts |
| Referral Bonus (5 × 50 × 20%) | Theoretical 50 pts |
| Actual | **50 pts** |

*Note: Referral bonus only counts referred users' balance points, not one-time tasks*

### New vs. Returning User Comparison

New user deposits $10 (one week): 22 + 70 = **92 pts**
Returning user needs to match: **$173** (√173 × 7 ≈ 92)

---

## 9. Anti-Abuse Mechanisms

| Layer | Mechanism | Effect |
|-------|-----------|--------|
| Registration | Passkey device binding | High cost for batch registration |
| Points | √n square root formula | Splitting accounts reduces returns |
| Snapshot | Uses daily minimum balance | Prevents flash deposit farming |
| Cap | $10,000 points calculation cap | Diminishing returns for whales |
| Referral | Bonus capped at own points | Prevents infinite pyramid schemes |

---

*Document Version: v9.0*
*Last Updated: 2026/01/03*
