# Weather Derivative Product Design Proposal
## OTC Precipitation Risk Transfer Instrument
**Cliff Horizon Pte. Ltd.**

Date: November 18, 2025  
Prepared by: Claude (AI Assistant)

---

## EXECUTIVE SUMMARY

This document outlines the design of a standalone OTC weather derivative product derived from Cliff Horizon's successful precipitation warranty offering. The proposed instrument will provide pure financial protection against rainfall-related business disruption without bundled analytics services, structured under Singapore law using ISDA documentation.

**Key Differentiators:**
- **Unbundled**: Pure financial instrument (no analytics included)
- **Scalable**: Can be offered through financial intermediaries/brokers
- **Standardised**: ISDA-based for institutional acceptance
- **Data-driven**: Uses independently verifiable satellite data (GPM IMERG)
- **Emerging Markets Focus**: Designed for Asian infrastructure/agriculture sectors

---

## PART 1: PRODUCT ARCHITECTURE

### 1.1 Product Overview

**Product Name**: Cliff Horizon Precipitation Swap (CHPS)  
**Classification**: Weather Derivative / Commodity Derivative  
**Underlying Index**: Monthly Precipitation Threshold Exceedance Index (MPTEI)  
**Settlement**: Cash-settled, financially settled  
**Jurisdiction**: Singapore law (ISDA Master Agreement)

### 1.2 Core Structure Options

#### **OPTION A: Precipitation Excess Swap**
*Most Similar to Current Warranty*

**Structure:**
- **Type**: Digital (Binary) Swap
- **Parties**: 
  - Protection Buyer (Client) - pays fixed premium
  - Protection Seller (Cliff Horizon/Hedge Fund) - receives premium, pays on trigger
  
**Mechanics:**
```
IF: Actual Rainy Days > Threshold Rainy Days
THEN: Seller pays: (Actual Days - Threshold Days) Ã— Payout Rate
ELSE: No payment (Buyer loses premium)

Subject to: Monthly Cap on payout days
```

**Example Terms:**
- **Location**: Bankot, India (17.895N, 73.052E)
- **Observation Period**: October 2025
- **Threshold**: 11 rainy days (>25mm rainfall/day)
- **Payout Rate**: USD 14,000 per excess day
- **Maximum Days**: 7 days (cap at USD 98,000)
- **Premium**: USD 15,000 (buyer pays upfront)
- **Data Source**: NASA GPM IMERG Late Run v07
- **Settlement**: T+30 days after period end

#### **OPTION B: Cumulative Rainfall Swap**
*More Aligned with CME Standard Practices*

**Structure:**
- **Type**: Linear Payout Swap
- **Index**: Cumulative Monthly Rainfall (mm)

**Mechanics:**
```
Payout = MAX[0, (Actual Rainfall - Strike Rainfall) Ã— Tick Size]
Subject to: Maximum Cap
```

**Example Terms:**
- **Strike**: 280mm cumulative rainfall
- **Tick Size**: USD 500 per mm
- **Cap**: USD 100,000 (200mm above strike)
- **Premium**: USD 12,000

#### **OPTION C: Rainfall Put Option**
*Provides Optionality to Buyer*

**Structure:**
- **Type**: European-style Put Option on Rainfall Days
- **Buyer**: Purchases right but not obligation to exercise

**Mechanics:**
```
At Expiry:
Buyer can choose to exercise if:
  Actual Rainy Days > Strike Days
  
If exercised:
  Payout = (Actual Days - Strike Days) Ã— Notional per Day
  
Buyer pays: Premium (regardless of exercise)
```

**Advantage**: More flexibility, lower premium than swap

---

### 1.3 Recommended Primary Structure

**RECOMMENDATION: OPTION A - Precipitation Excess Swap (Digital)**

**Rationale:**
1. **Client familiarity**: Directly matches existing warranty structure
2. **Simple**: Clear trigger, easy to understand and price
3. **Hedgeable**: Can be reinsured or hedged with parametric insurers
4. **Emerging market fit**: Binary payouts match construction/agriculture business interruption losses

---

## PART 2: LEGAL & DOCUMENTATION FRAMEWORK

### 2.1 ISDA Master Agreement Structure

**Documentation Hierarchy:**

```
1. ISDA Master Agreement (Singapore Law version)
   â””â”€ Elections: Singapore law, Singapore courts, SGD or USD

2. Schedule to ISDA
   â””â”€ Credit Support Annex (CSA) - if required
   â””â”€ Definitions incorporated by reference

3. Confirmation (per trade)
   â””â”€ Weather Derivative Confirmation Template
   â””â”€ Incorporates:
      â€¢ ISDA 2006 Commodity Definitions (adapted)
      â€¢ Custom Weather Index Definitions
      â€¢ Data Source Specifications
```

### 2.2 Key Contractual Provisions

#### **Trade Confirmation Template Structure**

```
WEATHER DERIVATIVE TRANSACTION
Confirmation Date: [DATE]
Effective Date: [START DATE]
Termination Date: [END DATE]

GENERAL TERMS:
- Trade Type: Precipitation Excess Swap
- Notional Amount: [CURRENCY + AMOUNT]
- Calculation Agent: Cliff Horizon Pte. Ltd.

FIXED AMOUNTS:
- Fixed Amount Payer: [CLIENT NAME]
- Fixed Amount: [PREMIUM AMOUNT]
- Payment Date: Effective Date
- Business Day Convention: Following

FLOATING AMOUNTS:
- Floating Amount Payer: Cliff Horizon Pte. Ltd.
- Calculation: See Weather Index Provisions
- Payment Date: 30 days after Final Index Level determination

WEATHER INDEX PROVISIONS:
- Index Name: Monthly Precipitation Threshold Exceedance Index
- Reference Location: [LAT/LONG or Station ID]
- Observation Period: [MONTH YEAR]
- Rainy Day Threshold: 25mm precipitation per day
- Strike Level: [X] rainy days
- Payout Rate: USD [Y] per excess day
- Maximum Payout Days: [Z] days
- Data Source: NASA GPM IMERG Late Run v07
- Disruption Events: See Schedule A

DATA SOURCE FALLBACK HIERARCHY:
1. NASA GPM IMERG Late Run v07
2. NASA GPM IMERG Final Run v07
3. Local Weather Station [STATION ID]
4. Mutual Agreement or Postponement
```

#### **Critical Definitions**

**"Rainy Day"**: A calendar day during the Observation Period where total accumulated precipitation at the Reference Location equals or exceeds 25 millimeters, as measured by the Data Source.

**"Actual Rainy Days"**: The total count of Rainy Days during the Observation Period as determined by the Calculation Agent using the Data Source.

**"Floating Amount"**: 
```
IF Actual Rainy Days â‰¤ Strike Level:
   Floating Amount = ZERO

IF Actual Rainy Days > Strike Level:
   Excess Days = MIN(Actual Rainy Days - Strike Level, Maximum Payout Days)
   Floating Amount = Excess Days Ã— Payout Rate
```

**"Calculation Agent"**: Cliff Horizon Pte. Ltd., with disputes subject to Independent Expert determination.

**"Disruption Events"**:
1. Data Source Unavailability (>7 days)
2. Material Error in Data Source (published correction >10%)
3. Discontinuation of Data Source
4. Force Majeure at Reference Location

**Disruption Fallbacks**:
- Use alternative data source per fallback hierarchy
- Postponement (up to 60 days)
- Cancellation (both parties agree)

### 2.3 Singapore Law Considerations

**Key Legal Aspects:**

1. **Contractual Freedom**: Singapore law provides strong contractual freedom - parties can freely structure derivatives

2. **Enforceability**: 
   - Weather derivatives are "commodity derivatives" under Securities and Futures Act (SFA)
   - No specific prohibition on weather derivatives
   - Financial settlement permissible

3. **Netting**: 
   - Close-out netting under ISDA Master Agreement enforceable
   - Supported by Singapore courts

4. **Collateral**: 
   - CSA (Credit Support Annex) enforceable under Singapore law
   - Security interests registrable under Personal Property Securities Act

5. **Regulatory Classification**:
   - **If Cliff Horizon acts as counterparty (principal)**: Likely requires Capital Markets Services License
   - **If Cliff Horizon acts as calculation agent only**: No license required
   - **Alternative**: Use licensed intermediary as counterparty, Cliff Horizon provides index calculation

**Recommended Structure**: Cliff Horizon provides index calculation services to licensed dealer who acts as counterparty

---

## PART 3: PRODUCT VARIANTS & CUSTOMISATION

### 3.1 Geographical Variants

**India Focus (Primary)**
- Monsoon Season Products (June-September)
- Non-Monsoon Products (October-May)
- Specific exclusions: July (high variability)

**Locations:**
1. Mumbai Metropolitan Region
2. Pune Infrastructure Corridor
3. Bangalore Tech Hub
4. NCR Construction Belt

**Southeast Asia Expansion**
- Singapore
- Malaysia (Kuala Lumpur, Johor)
- Indonesia (Jakarta, Surabaya)
- Thailand (Bangkok)
- Philippines (Manila)

### 3.2 Tenor Variants

**Short-term Products:**
- **Monthly**: Single month protection
- **Seasonal**: 3-month monsoon/non-monsoon packages
- **Event-specific**: Specific project phase protection (e.g., foundation work Oct-Dec)

**Medium-term Products:**
- **Annual**: 12-month rolling protection (excludes high-variability months)
- **Multi-year**: 2-3 year programs for long infrastructure projects

### 3.3 Industry-Specific Variants

**Construction/Infrastructure:**
- Focus: Working day loss
- Trigger: Rainy days >25mm
- Payout: Fixed per day (covers machinery, labour costs)

**Agriculture:**
- Focus: Planting/harvest disruption
- Trigger: Rainfall excess during critical windows
- Payout: Per mm over threshold (crop damage correlation)

**Events/Tourism:**
- Focus: Revenue protection
- Trigger: Number of wet days (>10mm)
- Payout: Per affected day

**Renewable Energy (Solar/Wind):**
- Focus: Generation shortfall
- Trigger: Cloud cover index / wind speed
- Payout: Per unit generation shortfall

---

## PART 4: PRICING & RISK MANAGEMENT

### 4.1 Pricing Methodology

**Component Breakdown:**

```
Premium = Expected Loss + Risk Loading + Operating Cost + Profit Margin

Where:
Expected Loss = P(trigger) Ã— E[Payout | Trigger]
Risk Loading = Î» Ã— Ïƒ(Payout)  
Operating Cost = Fixed costs / Expected Volume
Profit Margin = Target ROE Ã— Allocated Capital
```

**Historical Data Analysis:**
1. Minimum 20 years GPM IMERG data
2. Statistical distribution fitting (Poisson for count, Gamma for volume)
3. Trend analysis (climate change adjustment)
4. Seasonality factors

**Example Calculation (October, Bankot):**

```
Historical Data (2004-2024): October rainy days (>25mm)
Mean: 11.2 days
Std Dev: 3.1 days
Strike: 11 days
Payout Rate: USD 14,000/day
Maximum Days: 7 days

Probability Analysis:
P(Actual > 11) â‰ˆ 48%
E[Excess Days | Trigger] â‰ˆ 2.3 days
Expected Payout = 0.48 Ã— 2.3 Ã— USD 14,000 = USD 15,456

Premium Components:
- Expected Loss: USD 15,456
- Risk Loading (30%): USD 4,637
- Operating Cost: USD 2,000
- Profit Margin (15%): USD 3,314
-----------------------------------
TOTAL PREMIUM: USD 25,407

Client Quote: USD 25,000 - USD 26,000 (rounded)
```

### 4.2 Risk Management & Hedging

**Cliff Horizon's Risk Exposure:**
- **Short Position**: Sold protection, exposed to precipitation excess
- **Concentration Risk**: Geographic and temporal correlation

**Hedging Strategies:**

**1. Reinsurance/Retrocession:**
- Partner with parametric reinsurers (Swiss Re, Munich Re Cat Bonds)
- Purchase protection for extreme tail risk (>5 excess days)
- Cost: ~40-50% of premium for tail protection

**2. Portfolio Diversification:**
- Geographic diversification (low correlation locations)
- Temporal diversification (different monsoon seasons)
- Opposite hedges (sell rainfall deficiency protection for agriculture)

**3. Capital Markets Hedge:**
- Issue parametric cat bonds for rainfall risk
- Use hedge funds as counterparties for back-to-back trades
- Access CME weather derivatives market for temperature correlation

**4. Dynamic Hedging:**
- Adjust pricing based on accumulating positions
- Seasonal position limits
- Geographic concentration limits

---

## PART 5: DISTRIBUTION STRATEGY

### 5.1 Distribution Channels

**Primary Channel: Institutional Brokers**

**Target Brokers:**
1. **TP ICAP Weather Desk** (global leader)
2. **Speedwell Weather** (specialised broker)
3. **BGC Partners** (Asia focus)
4. **TFS Energy** (regional)

**Value Proposition to Brokers:**
- Unique Asian rainfall product (underserved market)
- Verified data source (NASA GPM IMERG)
- Institutional-grade documentation (ISDA)
- Client education support from Cliff Horizon

**Broker Compensation:**
- 3-5% commission on premium
- Revenue share on portfolio growth

**Secondary Channel: Direct to Corporates**

**Target Segments:**
1. **Infrastructure/Construction** (Primary)
   - Large EPC contractors (L&T, Larsen & Toubro, GMR, etc.)
   - Government infrastructure agencies (NHAI, MSRDC)
   - Real estate developers

2. **Agriculture** (Secondary)
   - Large plantation companies
   - Agricultural cooperatives
   - Food processing companies

3. **Events/Tourism**
   - IPL franchises
   - Event management companies
   - Tourism boards

**Sales Approach:**
- CFO/Treasurer level engagement
- Risk management workshops
- Integration with existing insurance programs

### 5.2 Market Positioning

**Competitive Positioning:**

| Competitor | Product | Geography | Cliff Horizon Advantage |
|------------|---------|-----------|-------------------------|
| Parametric Insurers (Swiss Re) | Weather Insurance | Global | Pure derivative (no insurance license), faster settlement |
| CME Weather Futures | Temperature contracts | 18 cities (no India) | Rainfall focus, Asian locations, bespoke |
| Traditional Reinsurers | Cat bonds | Global | Lower minimum size, construction-specific |
| Index-based insurance | Crop insurance | India | Institutional-grade, non-indemnity |

**Key Messages:**
1. **"Asia's First Institutional Rainfall Derivative"**
2. **"NASA-verified, Singapore-regulated"**
3. **"Built for Infrastructure, Designed for Scale"**

---

## PART 6: REGULATORY COMPLIANCE

### 6.1 Singapore Regulatory Requirements

**MAS Reporting Obligations:**

If Cliff Horizon acts as principal (counterparty):
1. **Trade Reporting**: Report all OTC commodity derivatives to DTCC GTR within T+2
2. **License**: May require Capital Markets Services License (depends on volume/counterparty type)
3. **Risk Mitigation**: Margin requirements for non-cleared OTC derivatives

**Recommended Structure to Minimise Regulatory Burden:**

```
CLIENT â†’ Licensed Dealer (Counterparty) â†’ Cliff Horizon (Calculation Agent + Hedger)

Licensed Dealer: Licensed bank or CMS license holder
Cliff Horizon Role: 
- Calculation Agent (no license required)
- Index provider (no license required)
- Optional: back-to-back hedge counterparty to dealer
```

**Benefits:**
- Dealer handles MAS reporting
- Dealer manages client onboarding/KYC
- Cliff Horizon focuses on risk management and product design
- Scalable model

**Potential Partners:**
- **DBS Bank** (Asia's safest bank)
- **UOB** (strong corporate relationships)
- **Standard Chartered** (emerging markets expertise)
- **JP Morgan Singapore** (derivatives expertise)

### 6.2 India Regulatory Considerations

**For Indian Corporate Clients:**

**FEMA Regulations (Foreign Exchange Management Act):**
- Weather derivatives for hedging purposes permitted
- Must demonstrate "underlying exposure" to weather risk
- Documentation: Board resolution, RBI reporting

**SEBI Regulations:**
- Weather derivatives not yet regulated by SEBI
- Falls under RBI jurisdiction for corporates
- Insurance regulator (IRDAI) if structured as insurance

**Tax Treatment:**
- Hedge accounting possible if proper documentation
- Premium may be tax-deductible as business expense
- Payouts may be taxable income (consult tax advisor)

**Compliance Checklist for Indian Clients:**
1. Board approval for derivative transactions
2. Risk management policy documentation
3. FEMA compliance certification
4. RBI reporting (if amount exceeds threshold)

---

## PART 7: OPERATIONAL FRAMEWORK

### 7.1 Data Infrastructure

**Primary Data Source: NASA GPM IMERG**

**Access:**
- Public data: https://gpm.nasa.gov/data/imerg
- API access: Giovanni interface or direct FTP
- Update frequency: Daily (Late Run), Monthly (Final Run)
- Historical archive: 2000-present

**Data Processing Pipeline:**

```
1. AUTOMATED DAILY EXTRACTION
   - FTP download from NASA servers
   - Time: 02:00 SGT (after Late Run publication)
   
2. QUALITY ASSURANCE
   - Verify file integrity (checksums)
   - Check completeness (no missing days)
   - Flag anomalies (>3 sigma from historical)

3. INDEX CALCULATION
   - Extract precipitation data for reference locations
   - Apply rainy day threshold (25mm)
   - Calculate cumulative metrics
   
4. VALIDATION
   - Cross-check with alternative sources (if available)
   - Compare to historical patterns
   - Manual review for material deviations

5. PUBLICATION
   - Daily dashboard update
   - Client portal access
   - Calculation agent records
```

**Backup Data Sources:**
1. **GPM IMERG Final Run** (3-month lag, higher accuracy)
2. **Local Weather Stations** (for specific validation)
3. **ERA5 Reanalysis** (ECMWF) - extreme fallback

**Data SLA:**
- Calculation published within 24 hours of period end
- Dispute resolution within 7 business days
- Final settlement within 30 days

### 7.2 Settlement Process

**Timeline:**

```
Day 0: Observation Period Ends (e.g., Oct 31, 2025 23:59)
Day 1-7: Data Collection & Verification
         - Download complete dataset
         - Calculate index
         - Preliminary calculation notice

Day 7: Preliminary Settlement Amount Notice
        - Sent to both parties
        - Dispute period opens

Day 7-17: Dispute Period (10 business days)
          - Parties may dispute calculation
          - Provide alternative data/methodology
          - Independent Expert if needed

Day 18-28: Final Calculation
           - Resolve disputes (if any)
           - Issue Final Settlement Amount Notice

Day 30: Payment Due
        - Wire transfer by Protection Seller
        - If no trigger: No payment
```

**Dispute Resolution Process:**

1. **Calculation Agent Recalculation** (5 days)
   - Review counterparty objections
   - Re-verify data sources
   - Provide detailed explanation

2. **Independent Expert** (if unresolved)
   - Appointed from pre-agreed panel
   - Meteorologist or weather derivatives expert
   - Decision binding on both parties
   - Costs shared 50/50

3. **Arbitration** (last resort)
   - Singapore International Arbitration Centre (SIAC)
   - Rules: UNCITRAL
   - Language: English

### 7.3 Technology Stack

**Core Systems:**

1. **Data Platform:**
   - Cloud: AWS Asia Pacific (Singapore) - ap-southeast-1
   - Database: PostgreSQL with PostGIS (geospatial)
   - Storage: S3 for historical archive

2. **Calculation Engine:**
   - Python-based (NumPy, Pandas, Xarray for NetCDF)
   - Automated daily runs (cron + Lambda)
   - Audit trail (all calculations logged)

3. **Client Portal:**
   - Real-time index monitoring
   - Historical data visualization
   - Document repository (confirmations, notices)
   - Mobile-responsive design

4. **Risk Management System:**
   - Portfolio monitoring
   - Real-time P&L
   - VaR calculations
   - Concentration reports

---

## PART 8: GO-TO-MARKET ROADMAP

### Phase 1: Foundation (Months 1-3)

**Objectives:**
- Finalize product design
- Establish legal framework
- Build MVP technology

**Deliverables:**
1. ISDA Master Agreement template (Singapore law)
2. Confirmation template
3. Data infrastructure MVP
4. Pricing model (Excel + Python)

**Partners:**
- **Legal**: Singapore law firm (Rajah & Tann, Allen & Gledhill)
- **Data**: NASA GPM IMERG access established
- **Technology**: AWS infrastructure setup

**Budget**: USD 50,000-75,000

### Phase 2: Pilot Program (Months 4-9)

**Objectives:**
- Pilot trades with 2-3 clients
- Validate operations
- Refine pricing

**Target Clients:**
- **Client 1**: MSRDC (existing warranty client) - convert to derivative
- **Client 2**: Large EPC contractor (e.g., L&T)
- **Client 3**: Infrastructure developer (new client)

**Volume Target:** 5-10 trades, USD 500,000-1,000,000 notional

**Success Metrics:**
- Zero operational errors
- Settlement within SLA
- Client satisfaction >8/10
- Profitable on risk-adjusted basis

### Phase 3: Scale Distribution (Months 10-18)

**Objectives:**
- Onboard broker partnerships
- Expand geography
- Build reinsurance capacity

**Distribution:**
- Partner with TP ICAP Weather Desk (exclusive 12 months)
- Provide broker training
- Co-marketing campaigns

**Geography Expansion:**
- India: Expand to 10 cities
- Southeast Asia: Launch Singapore, KL, Jakarta products

**Reinsurance:**
- Swiss Re/Munich Re Cat Bond desk discussions
- Structure tail risk hedge

**Volume Target:** 50+ trades, USD 10-20 million notional

### Phase 4: Institutional Platform (Months 19-24+)

**Objectives:**
- Establish as market standard for Asian rainfall derivatives
- Technology platform licensing
- Secondary market liquidity

**Initiatives:**
1. **White-label platform** for banks
2. **API access** for institutional clients
3. **Market making**: Provide two-way quotes
4. **CME listing**: Explore listed contract (if volume sufficient)

**Volume Target:** 200+ trades, USD 100+ million notional

---

## PART 9: FINANCIAL PROJECTIONS

### 9.1 Revenue Model

**Revenue Streams:**

1. **Trading P&L** (Primary)
   - Premium income minus claims and hedging costs
   - Target: 15-25% ROE

2. **Calculation Agent Fees** (if using dealer model)
   - 0.5-1% of notional per transaction
   - Recurring annual fees

3. **Data Licensing**
   - Index methodology licensing to brokers/banks
   - USD 25,000-50,000 per institution per year

4. **Technology Platform Fees** (Phase 4)
   - SaaS model for white-label deployment
   - USD 10,000-20,000 per month per institution

### 9.2 Cost Structure

**Year 1 Costs:**

| Category | Amount (USD) |
|----------|--------------|
| Legal & Documentation | 75,000 |
| Technology Development | 50,000 |
| Data & Infrastructure | 20,000 |
| Personnel (2 FTE) | 200,000 |
| Marketing & Business Development | 30,000 |
| Regulatory & Compliance | 25,000 |
| **TOTAL OPEX** | **400,000** |

**Ongoing Costs (Year 2+):**
- Personnel: USD 300,000 (4-5 FTE)
- Technology: USD 50,000
- Data: USD 30,000
- Other: USD 50,000
- **Total**: USD 430,000/year

### 9.3 Profitability Scenarios

**Conservative Scenario (Year 2):**
- Volume: 30 trades Ã— USD 25,000 avg premium = USD 750,000
- Loss Ratio: 65% (USD 487,500)
- Operating Costs: USD 430,000
- **Net Profit**: -USD 167,500 (Loss - Investment Phase)

**Base Case (Year 3):**
- Volume: 80 trades Ã— USD 30,000 avg premium = USD 2,400,000
- Loss Ratio: 60% (USD 1,440,000)
- Operating Costs: USD 450,000
- **Net Profit**: USD 510,000 (21% margin)

**Bull Case (Year 4-5):**
- Volume: 200 trades Ã— USD 35,000 avg premium = USD 7,000,000
- Loss Ratio: 55% (USD 3,850,000)
- Operating Costs: USD 600,000
- **Net Profit**: USD 2,550,000 (36% margin)

---

## PART 10: RISK FACTORS & MITIGATION

### 10.1 Key Risks

**1. Basis Risk**
- **Definition**: Mismatch between derivative payout and actual client loss
- **Example**: Rainfall occurs but doesn't disrupt client operations
- **Mitigation**: 
  - Careful strike/threshold calibration with clients
  - Historical correlation analysis
  - Pilot testing

**2. Data Risk**
- **Definition**: Data source error, discontinuation, or unavailability
- **Mitigation**:
  - Multiple data source fallbacks
  - Long history of GPM IMERG (20+ years proven)
  - Regular data quality audits

**3. Model Risk**
- **Definition**: Pricing model underestimates risk
- **Mitigation**:
  - Conservative assumptions
  - Backtesting (out-of-sample)
  - Regular model validation
  - Climate change adjustment factors

**4. Correlation Risk**
- **Definition**: Multiple contracts trigger simultaneously
- **Mitigation**:
  - Geographic diversification
  - Position limits
  - Tail risk reinsurance

**5. Legal/Regulatory Risk**
- **Definition**: Enforceability, regulatory changes
- **Mitigation**:
  - Use well-established ISDA framework
  - Regular legal reviews
  - Monitor regulatory developments

**6. Counterparty Credit Risk**
- **Definition**: Client defaults on premium or Cliff Horizon defaults on payout
- **Mitigation**:
  - Credit assessment (KYC/AML)
  - Collateral/margin requirements for large exposures
  - Reinsurance for tail risk

**7. Reputational Risk**
- **Definition**: Dispute over calculation or settlement
- **Mitigation**:
  - Transparent methodology
  - Independent expert panel
  - Strong operational controls

### 10.2 Success Factors

**Critical Success Factors:**

1. **Data Credibility**
   - NASA GPM IMERG is gold-standard
   - Independently verifiable
   - Long track record

2. **Client Trust**
   - Existing warranty relationships
   - Transparent pricing
   - Fast, fair settlement

3. **Partnerships**
   - Licensed dealer for distribution
   - Reinsurer for tail risk
   - Brokers for scale

4. **Operational Excellence**
   - Zero errors in calculation
   - Timely settlement
   - Responsive client service

5. **Regulatory Compliance**
   - Proactive MAS engagement
   - Clean audit trail
   - Strong governance

---

## CONCLUSIONS & NEXT STEPS

### Key Takeaways

1. **Market Opportunity**: 
   - Underserved market for Asian rainfall derivatives
   - Growing demand (climate change, infrastructure boom)
   - Limited competition

2. **Product Design**: 
   - Digital precipitation excess swap is optimal starting point
   - Leverages existing warranty expertise
   - ISDA-based for institutional credibility

3. **Go-to-Market**: 
   - Phased approach: Pilot â†’ Scale â†’ Platform
   - Partner with licensed dealer to minimize regulatory burden
   - Target brokers for distribution

4. **Economics**: 
   - Attractive margins (20-35% in steady state)
   - Manageable startup costs (USD 400K Year 1)
   - Break-even by Year 3 in base case

5. **Risks**: 
   - Manageable with proper hedging and diversification
   - Data source is robust (NASA GPM IMERG)
   - ISDA framework provides legal certainty

### Immediate Next Steps

**WEEK 1-2:**
1. Validate product design assumptions with potential clients
2. Engage Singapore law firm for ISDA template drafting
3. Meet with potential dealer partners (DBS, UOB, SC)

**WEEK 3-4:**
4. Build pricing model (Python)
5. Set up AWS infrastructure for data processing
6. Draft pitch materials for brokers

**MONTH 2:**
7. Complete legal documentation
8. Pilot trade with MSRDC (convert warranty to derivative)
9. Engage TP ICAP or Speedwell for partnership discussions

**MONTH 3:**
10. Launch MVP client portal
11. Complete first 2-3 pilot trades
12. Begin broker outreach

---

## APPENDICES

*The following appendices would be developed in detail:*

**Appendix A**: Sample ISDA Confirmation (Full Template)  
**Appendix B**: Pricing Model Specification (Python Implementation)  
**Appendix C**: Data Processing Technical Specifications  
**Appendix D**: Client Education Materials  
**Appendix E**: Regulatory Compliance Checklist  
**Appendix F**: Risk Management Framework  
**Appendix G**: Broker Partnership Terms Sheet  

---

**END OF DOCUMENT**

---

**Document Control:**
- Version: 1.0 Draft
- Date: November 18, 2025
- Classification: Confidential
- Distribution: Internal Use Only

