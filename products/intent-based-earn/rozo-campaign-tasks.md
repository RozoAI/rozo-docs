# [Draft] ROZO Earn Points Calculation Rules & User Simulations

> Version: v4.0
> Updated: 2026/01/03

---

## 1. Dual-Track Incentive System

| System | Purpose | Calculation | Distribution |
|--------|---------|-------------|--------------|
| **Cash Back** | Instant Rewards | Bridge: Fee×2 / Payment: 1%-20% | Real-time |
| **Point** | Leaderboard + Lucky Draw | √(Balance) + Task Points + Referral Bonus | Daily Snapshot |

---

## 2. Point Calculation Formula

### Total Points Formula

```
Weekly Total Points = Σ(Daily √Balance) + One-Time Task Points + Referral Bonus
```

### 1. Daily Base Points (Core)

```
Daily Points = √(Daily Minimum Balance)
```

| Balance | Daily Points |
|---------|--------------|
| $1 | 1.00 |
| $5 | 2.24 |
| $10 | 3.16 |
| $25 | 5.00 |
| $50 | 7.07 |
| $100 | 10.00 |
| $200 | 14.14 |
| $500 | 22.36 |
| $1,000 | 31.62 |
| $2,000 | 44.72 |
| $5,000 | 70.71 |
| $10,000 | 100.00 (cap) |

### 2. One-Time Task Points (New User Only)

These are claimed **ONCE per user** in their first participating week:

| Task | Points | Trigger Condition | Frequency |
|------|--------|-------------------|-----------|
| First Deposit | +20 | Deposit ≥ $1 | Once per user |
| Bind Twitter | +15 | Complete OAuth Authorization | Once per user |
| Bind Discord | +15 | Complete OAuth Authorization | Once per user |
| First Successful Referral | +20 | Invite 1 person to deposit ≥ $1 | Once per user |

**Maximum One-Time Task Points: 70** (only in your first week)

### 3. Referral Bonus (Recalculated Weekly)

```
Referral Bonus = Σ(Referred User's Weekly Balance Points × 20%)
```

**What contributes to referrer's points:**

| Counts ✓ | Does NOT Count ✗ |
|----------|------------------|
| Referred user's balance points (√balance × days) | Referred user's one-time task points (+70) |
| | Referred user's own referral bonus |

**Cap Rules**:
- If you have deposits: Cap = Your own total points
- If you have no deposits: Cap = 100 points

---

## 3. Points Cycle Explanation

**Important: 5-Week Campaign = 5 Independent Weekly Competitions, Points Do NOT Accumulate!**

| Point Type | Cycle | Description |
|------------|-------|-------------|
| **One-time Tasks** | Once per user | Claimed in user's first participating week only |
| **Daily Balance Points** | Weekly | Resets to zero each week, recalculated |
| **Referral Bonus** | Weekly | Based on referred users' weekly balance points |

**Draw Announcement Time**: Every Monday 00:00 UTC
- Singapore/Hong Kong: Monday 08:00
- London: Monday 00:00
- Los Angeles: Sunday 16:00

---

## 4. User Simulation Examples

### User A: New Beginner (Deposits $50, Completes Tasks)

**Background**: Student, deposits $50, completes all simple tasks

#### Activity Log

| Day | Action | Balance | Daily Points |
|-----|--------|---------|--------------|
| Day 1 | Deposit $50, Bind Twitter | $50 | √50 = 7.07 |
| Day 2 | Bind Discord | $50 | 7.07 |
| Day 3 | Successfully refer Friend B | $50 | 7.07 |
| Day 4 | No action | $50 | 7.07 |
| Day 5 | No action | $50 | 7.07 |
| Day 6 | No action | $50 | 7.07 |
| Day 7 | No action | $50 | 7.07 |

#### Points Calculation

```
Daily Balance Points: 7.07 × 7 = 49.49 pts

One-Time Tasks:
  - First Deposit: +20
  - Bind Twitter: +15
  - Bind Discord: +15
  - First Successful Referral: +20
  Subtotal: +70 pts

Referral Bonus: Friend B's balance points 49.49 × 20% = 9.9 pts
  (Note: Only counts balance points, not one-time tasks)

───────────────────────────
Weekly Total Points: 49.49 + 70 + 9.9 = 129.39 pts
```

**Result**: Eligible for weekly lucky draw, chance to win $25!

---

### User B: Regular User (Deposits $500, Refers 2 People)

**Background**: Office worker, deposits $500, referred by A, also refers 2 people

#### Activity Log

| Day | Action | Balance | Daily Points |
|-----|--------|---------|--------------|
| Day 1 | Deposit $500 via A's link | $500 | √500 = 22.36 |
| Day 2 | Bind Twitter + Discord | $500 | 22.36 |
| Day 3 | Refer Friend C ($100) | $500 | 22.36 |
| Day 4 | Refer Friend D ($50) | $500 | 22.36 |
| Day 5 | No action | $500 | 22.36 |
| Day 6 | No action | $500 | 22.36 |
| Day 7 | No action | $500 | 22.36 |

#### Points Calculation

```
Daily Balance Points: 22.36 × 7 = 156.52 pts

One-Time Tasks:
  - First Deposit: +20
  - Bind Twitter: +15
  - Bind Discord: +15
  - First Successful Referral: +20
  Subtotal: +70 pts

Referral Bonus (balance points only):
  - Friend C ($100) balance points 70 × 20% = 14 pts
  - Friend D ($50) balance points 49.49 × 20% = 9.9 pts
  Subtotal: 23.9 pts

───────────────────────────
Weekly Total Points: 156.52 + 70 + 23.9 = 250.42 pts
```

**Result**: Strong chance to enter Top 30 leaderboard!

---

### User C: Whale User (Deposits $5,000, Aims for Top)

**Background**: DeFi veteran, deposits $5,000, focuses on yield + leaderboard ranking

#### Activity Log

| Day | Action | Balance | Daily Points |
|-----|--------|---------|--------------|
| Day 1 | Deposit $5,000 | $5,000 | √5000 = 70.71 |
| Day 2 | Bind Twitter + Discord | $5,000 | 70.71 |
| Day 3 | Refer 5 friends | $5,000 | 70.71 |
| Day 4 | No action | $5,000 | 70.71 |
| Day 5 | No action | $5,000 | 70.71 |
| Day 6 | No action | $5,000 | 70.71 |
| Day 7 | No action | $5,000 | 70.71 |

#### Points Calculation

```
Daily Balance Points: 70.71 × 7 = 494.97 pts

One-Time Tasks:
  - First Deposit: +20
  - Bind Twitter: +15
  - Bind Discord: +15
  - First Successful Referral: +20
  Subtotal: +70 pts

Referral Bonus (balance points only):
  - 5 friends, assume each has 70 balance points
  - Theoretical bonus: 70 × 20% × 5 = 70 pts
  - Cap check: min(70, 494.97+70) = 70 pts

───────────────────────────
Weekly Total Points: 494.97 + 70 + 70 = 634.97 pts
```

**Result**: Guaranteed Top 10, strong contender for Top 3!

---

### User D: Pure Referrer (No Deposits, Only Referrals)

**Background**: KOL, doesn't deposit, but refers many people

#### Points Calculation

```
Own Balance Points: 0 pts (no deposits)

Referral Bonus (balance points only):
  - Referred 10 new users, each with ~50 balance points
  - Theoretical bonus: 50 × 20% × 10 = 100 pts
  - Cap check (no deposits, cap = 100): min(100, 100) = 100 pts

───────────────────────────
Weekly Total Points: 0 + 0 + 100 = 100 pts
```

**Result**: Pure referrers can earn max 100 points, eligible for lucky draw!

*Note: Referral bonus only counts referred users' balance points, not one-time tasks*

---

## 5. New vs. Returning User Comparison

| User Type | Deposit | Weekly Points | Notes |
|-----------|---------|---------------|-------|
| New User | $10 | 22 + 70 = **92 pts** | Has one-time task bonus |
| Returning User (to match) | **$173** | 92 pts | Only balance points |

New user with $10 = Returning user with $173 (from Week 2 onwards)

---

## 6. Strategy Comparison

| User | Deposit | Weekly Points | Goal | Expected Reward | How to Win |
|------|---------|---------------|------|-----------------|------------|
| A | $50 | ~129 pts | Lucky Draw | $25 | Probability (higher points = better odds) |
| B | $500 | ~250 pts | Top 30 | $12-50 | **Guaranteed** (by ranking) |
| C | $5,000 | ~635 pts | Top 3 | $80-150 | **Guaranteed** (by ranking) |
| D | $0 (referrals only) | 100 pts | Lucky Draw | $25 | Probability (higher points = better odds) |

### Key Observations

1. **Small Depositors**: Rely on task points + lucky draw, low investment but still have chances
2. **Medium Depositors**: Tasks + referrals together, best value for effort
3. **Large Depositors**: Balance points dominate, but √n formula limits whale advantage
4. **Pure Referrers**: Max 100 points, encourages participation but prevents pure arbitrage

---

## 7. Quick Start Roadmap

### First Week Task Checklist for Beginners

- [ ] Day 1: Deposit $1 or more (Earn +20 first deposit points)
- [ ] Day 1: Bind Twitter (+15)
- [ ] Day 1: Bind Discord (+15)
- [ ] Day 2: Successfully refer 1 friend (+20)
- [ ] Day 3-7: Keep balance, don't withdraw

**Expected Points**: ~90-140 pts (depending on deposit amount)

---

*Document Version: v4.0*
*Last Updated: 2026/01/03*
