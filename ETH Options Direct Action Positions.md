# ETH Options Direct Action Positions
## Immediate Trading Opportunities - August 6, 2025

**Current Market Context:**
- ETH Spot: $3,614.96
- ATM IV: 65.4%
- VRP: +6.4%
- Put Skew: 13%

---

## POSITION 1: SHORT PUT SPREAD (HIGH PRIORITY)
**Strategy:** Monetize elevated put skew and positive VRP

### Exact Position Structure:
- **SELL:** ETH $3,400 Put (20 delta) - September 6 expiry (31 DTE)
- **BUY:** ETH $3,200 Put (10 delta) - September 6 expiry (31 DTE)
- **Net Credit:** ~$45-55 per spread
- **Max Risk:** $145-155 per spread
- **Breakeven:** ~$3,345

### Entry Criteria:
- Execute when ETH IV Rank > 0.35 ✓ (Current: 0.39)
- Put skew > 10% ✓ (Current: 13%)
- ETH trading above $3,500 ✓

### Position Sizing:
- **Conservative:** 10-15 spreads ($1,000-1,500 risk)
- **Moderate:** 20-30 spreads ($2,000-3,000 risk)
- **Aggressive:** 40-50 spreads ($4,000-5,000 risk)

### Exit Strategy:
- **Profit Target:** 60% of max profit (~$27-33 credit)
- **Stop Loss:** 150% of credit received (~$68-83 debit)
- **Time Exit:** Close at 7 DTE regardless of P&L

---

## POSITION 2: SHORT STRADDLE (MEDIUM PRIORITY)
**Strategy:** Capture volatility risk premium with delta-neutral exposure

### Exact Position Structure:
- **SELL:** ETH $3,600 Call - September 6 expiry (31 DTE)
- **SELL:** ETH $3,600 Put - September 6 expiry (31 DTE)
- **Net Credit:** ~$180-220 total
- **Breakevens:** ~$3,380 and ~$3,820

### Entry Criteria:
- Execute when ATM IV > 60% ✓ (Current: 65.4%)
- VRP > 5% ✓ (Current: 6.4%)
- ETH within 2% of strike price ✓

### Position Sizing:
- **Conservative:** 1-2 straddles ($180-440 credit)
- **Moderate:** 3-5 straddles ($540-1,100 credit)

### Delta Hedging Protocol:
- Hedge when delta exceeds ±15
- Use ETH futures or spot for hedging
- Rebalance daily during first 2 weeks

### Exit Strategy:
- **Profit Target:** 50% of max profit
- **Stop Loss:** 200% of credit received
- **Volatility Exit:** Close if IV exceeds 80%

---

## POSITION 3: CALENDAR SPREAD (LOWER PRIORITY)
**Strategy:** Exploit term structure backwardation

### Exact Position Structure:
- **SELL:** ETH $3,600 Call - August 20 expiry (14 DTE)
- **BUY:** ETH $3,600 Call - September 6 expiry (31 DTE)
- **Net Debit:** ~$25-35
- **Max Profit:** ~$50-70 (at expiry near $3,600)

### Entry Criteria:
- Front month IV > back month IV ✓
- ETH trading within 5% of strike ✓
- Front month IV > 60% ✓

### Position Sizing:
- **Conservative:** 5-10 calendars ($125-350 risk)
- **Moderate:** 15-25 calendars ($375-875 risk)

---

## POSITION 4: PROTECTIVE PUT BUYING (HEDGE)
**Strategy:** Portfolio protection given bearish options flow

### Exact Position Structure:
- **BUY:** ETH $3,200 Put - September 20 expiry (45 DTE)
- **Cost:** ~$85-105 per contract
- **Protection Level:** 11.5% below current price

### Sizing for Portfolio Protection:
- Buy 1 put per 1 ETH held in portfolio
- For $100k ETH exposure: ~28 puts ($2,380-2,940 cost)

---

## EXECUTION GUIDELINES

### Order Management:
1. **Use Limit Orders Only** - Never market orders in ETH options
2. **Start with Mid-Market** - Begin at bid-ask midpoint
3. **Work Orders Patiently** - Allow 15-30 minutes for fills
4. **Split Large Orders** - Break >20 contracts into smaller pieces

### Timing Considerations:
- **Best Execution Times:** 10:00-16:00 UTC (peak liquidity)
- **Avoid:** First/last hour of trading day
- **Monitor:** ETH spot volatility during execution

### Risk Management Rules:
1. **Maximum Single Position Risk:** 5% of portfolio
2. **Maximum ETH Options Allocation:** 15% of portfolio
3. **Daily P&L Limit:** -2% of portfolio (close all positions)
4. **Volatility Circuit Breaker:** Close all if IV >100%

---

## MARKET MONITORING CHECKLIST

### Daily Monitoring:
- [ ] ETH spot price vs position strikes
- [ ] Current implied volatility levels
- [ ] Delta exposure across all positions
- [ ] P&L vs profit targets and stop losses

### Weekly Review:
- [ ] IV Rank and percentile changes
- [ ] Volatility risk premium evolution
- [ ] Put-call skew changes
- [ ] Cross-asset volatility relationships

### Exit Triggers (Close ALL Positions):
- ETH 1-day realized vol >40%
- VIX >35 (macro stress)
- ETH options bid-ask spreads >10%
- Major regulatory announcement affecting ETH

---

## POSITION PRIORITY RANKING

**IMMEDIATE ACTION (Next 24-48 Hours):**
1. **Position 1:** Short Put Spread - Highest risk-adjusted return
2. **Position 4:** Protective Puts - If holding ETH spot

**SECONDARY (This Week):**
3. **Position 2:** Short Straddle - If comfortable with gamma risk
4. **Position 3:** Calendar Spread - Lowest priority, smallest allocation

**Expected Returns (30-day horizon):**
- Position 1: 15-25% return on risk
- Position 2: 10-20% return on risk  
- Position 3: 8-15% return on risk
- Position 4: Insurance cost (negative carry)

