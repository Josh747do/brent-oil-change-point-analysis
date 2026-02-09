# Task 1: Analysis Workflow and Documentation
## Brent Oil Price Change Point Analysis

**Date:** February 5, 2026  
**Analyst:** [Your Name/Team]  
**Project:** 10 Academy - KAIM - Week 11 Challenge  
**Git Branch:** `task-1-foundation-analysis`

---

## 1. Analysis Workflow Outline

### Phase 1: Data Foundation (Completed)
- **1.1 Data Acquisition**
  - Load historical Brent oil prices (May 20, 1987 - November 14, 2022)
  - Validate data structure and quality
  - Handle date parsing (day-month-year format)

- **1.2 Initial Exploration**
  - Basic statistics and data quality assessment
  - Time series visualization
  - Missing value and outlier detection

### Phase 2: Time Series Analysis (Completed)
- **2.1 Trend Analysis**
  - Long-term trend identification (1-year moving average)
  - Medium-term trends (30-day moving average)
  - Regime change identification

- **2.2 Stationarity Testing**
  - Augmented Dickey-Fuller test (ADF)
  - KPSS test
  - Log returns transformation for stationarity

- **2.3 Volatility Analysis**
  - Rolling volatility calculation (30-day, 90-day)
  - Volatility clustering detection
  - ACF/PACF analysis of returns

### Phase 3: Event Research (Completed)
- **3.1 Historical Event Identification**
  - Research 15+ geopolitical/economic events
  - Compile structured dataset with dates and descriptions
  - Categorize by event type (Geopolitical, OPEC, Economic Crisis, etc.)

- **3.2 Event-Price Correlation**
  - Map events to price timeline
  - Calculate price changes around events
  - Preliminary impact assessment

### Phase 4: Modeling Preparation (Upcoming - Task 2)
- **4.1 Data Preparation for Change Point Detection**
  - Log returns calculation
  - Outlier handling
  - Data segmentation if needed

- **4.2 Bayesian Change Point Model**
  - PyMC model specification
  - Prior distributions definition
  - MCMC sampling

- **4.3 Model Interpretation**
  - Change point identification
  - Impact quantification
  - Event association

### Phase 5: Dashboard Development (Task 3)
- **5.1 Backend API Development**
  - Flask API endpoints
  - Data serving infrastructure

- **5.2 Frontend Visualization**
  - React dashboard
  - Interactive visualizations
  - Event highlighting functionality

---

## 2. Assumptions and Limitations

### 2.1 Key Assumptions

**Data Quality Assumptions:**
1. The provided Brent oil price data is accurate and representative of market prices
2. Daily closing prices capture relevant market movements
3. Date parsing with `dayfirst=True` correctly interprets the "day-month-year" format
4. No systematic biases in data collection or reporting

**Modeling Assumptions:**
1. Price changes can be modeled as having distinct regimes with different statistical properties
2. Structural breaks correspond to identifiable external events
3. Bayesian inference with MCMC sampling will converge to meaningful posterior distributions
4. A single change point model (initially) can capture major structural shifts

**Event Analysis Assumptions:**
1. Major geopolitical/economic events have measurable impacts on oil prices
2. Event dates from historical records are accurately recorded
3. Price movements around event dates are primarily driven by those events
4. 5-day windows around events capture immediate market reactions

### 2.2 Important Limitations

**Causality Limitation:**
> **Critical Distinction:** Identifying statistical correlation in time ≠ Proving causal impact
> - Our analysis identifies price changes that coincide temporally with events
> - We cannot prove events *caused* price changes without controlled experiments
> - Multiple confounding factors may influence prices simultaneously
> - Market anticipation may cause price movements before official event dates

**Data Limitations:**
1. **Time Period:** Data ends in November 2022, missing recent developments
2. **Frequency:** Daily data may miss intraday volatility and reactions
3. **Scope:** Only Brent crude prices, not other oil benchmarks or energy markets
4. **Exogenous Factors:** No direct data on supply/demand fundamentals, inventory levels, or production costs

**Methodological Limitations:**
1. **Model Simplicity:** Initial single change point model may oversimplify complex market dynamics
2. **Event Selection Bias:** Researcher-selected events may miss important but less-publicized factors
3. **Window Sensitivity:** Price change calculations depend on chosen time windows
4. **Stationarity Assumption:** While returns are stationary, volatility clustering violates i.i.d. assumptions

**Practical Limitations:**
1. **Black Swan Events:** Unprecedented events (COVID-19) challenge historical patterns
2. **Market Evolution:** Changing market structure over 35+ years affects price dynamics
3. **Policy Responses:** Government interventions can mute or amplify event impacts
4. **Global Interconnectedness:** Increasing global integration makes isolation of single factors difficult

---

## 3. Communication Channels and Formats

### 3.1 Primary Stakeholders and Their Needs

**1. Investors & Traders**
- **Needs:** Actionable trading signals, risk management insights
- **Preferred Format:** Interactive dashboard, real-time alerts, concise reports
- **Key Metrics:** Expected price changes, volatility forecasts, regime probabilities

**2. Policymakers & Government Agencies**
- **Needs:** Policy impact assessment, economic stability planning
- **Preferred Format:** Executive summaries, policy briefs, scenario analysis
- **Key Metrics:** Market resilience, shock propagation, intervention effectiveness

**3. Energy Companies**
- **Needs:** Strategic planning, hedging decisions, supply chain management
- **Preferred Format:** Technical reports, scenario modeling, risk assessments
- **Key Metrics:** Price forecasting, volatility patterns, event sensitivity

**4. Research & Academic Community**
- **Needs:** Methodological rigor, reproducibility, theoretical contributions
- **Preferred Format:** Academic papers, code repositories, conference presentations
- **Key Metrics:** Model performance, statistical significance, novelty of findings

### 3.2 Communication Formats and Channels

**A. Interactive Dashboard (Primary Channel)**
- **Technology Stack:** React frontend + Flask backend
- **Key Features:**
  - Historical price visualization with event overlays
  - Change point detection results
  - Event impact quantification
  - Filtering by event type/time period
- **Access:** Web-based, responsive design

**B. Technical Reports**
- **Format:** Jupyter notebooks → PDF/HTML reports
- **Content:** Full methodological details, code, results, interpretations
- **Distribution:** GitHub repository, internal knowledge base

**C. Executive Summaries**
- **Format:** 1-2 page briefs with key insights
- **Visualizations:** Simplified charts, key metrics dashboards
- **Frequency:** Monthly updates + ad-hoc event analysis

**D. API Endpoints**
- **Purpose:** Programmatic access to analysis results
- **Endpoints:**
  - `/api/prices` - Historical price data
  - `/api/events` - Event dataset
  - `/api/change-points` - Model results
  - `/api/forecasts` - Short-term projections

**E. Alert System (Future Enhancement)**
- **Triggers:** Significant price movements, detected change points
- **Channels:** Email, Slack/Teams integration, SMS
- **Content:** Event context, historical parallels, recommended actions

### 3.3 Delivery Schedule

| Deliverable | Format | Audience | Due Date |
|------------|--------|----------|----------|
| Task 1: Foundation | Markdown report + CSV dataset | Tutors/Reviewers | Feb 8, 2026 |
| Task 2: Change Point Analysis | Jupyter notebook + visualizations | Technical stakeholders | Feb 10, 2026 |
| Task 3: Dashboard | Web application + API | All stakeholders | Feb 10, 2026 |
| Final Report | Blog post (Medium-style) | General audience | Feb 10, 2026 |

---

## 4. Next Steps and Dependencies

### Immediate Next Steps (Task 2)
1. **Implement Bayesian change point model** using PyMC
2. **Run MCMC sampling** and assess convergence
3. **Identify significant change points** in the data
4. **Quantify impacts** of detected change points
5. **Associate change points** with researched events

### Dependencies and Requirements
- **Computational:** Adequate memory for MCMC sampling (8GB+ recommended)
- **Data:** Cleaned dataset with log returns (`brent_prices_with_features.csv`)
- **Events:** Validated event dataset (`key_events.csv`)
- **Software:** PyMC, ArviZ, and dependencies from `requirements.txt`

### Risk Mitigation
- **Model Convergence:** Multiple chains, convergence diagnostics (R-hat)
- **Computational Intensity:** Start with subset of data if needed
- **Interpretation Complexity:** Visualize posterior distributions thoroughly
- **Event Association:** Maintain clear distinction between correlation and causation

---

## 5. Files Generated in Task 1

### Data Files
- `data/raw/BrentOilPrices.csv` - Original dataset
- `data/processed/brent_prices_cleaned.csv` - Cleaned price data
- `data/processed/brent_prices_with_features.csv` - Data with calculated features
- `data/processed/key_events.csv` - 15 key events dataset
- `data/processed/events_with_analysis.csv` - Events with price change analysis

### Analysis Files
- `notebooks/01_task1_foundation_analysis.ipynb` - Time series analysis
- `notebooks/02_task1_event_research.ipynb` - Event research and analysis

### Reports and Visualizations
- `reports/figures/full_time_series.html` - Interactive price chart
- `reports/figures/trend_analysis.png` - Trend decomposition
- `reports/figures/stationarity_analysis.png` - Stationarity tests
- `reports/figures/volatility_analysis.png` - Volatility patterns
- `reports/figures/events_on_timeline.png` - Events mapped to prices
- `reports/figures/event_timeline.png` - Event chronology
- `reports/task1_initial_findings.txt` - Summary statistics
- `reports/key_events.md` - Event documentation
- `reports/task1_analysis_workflow.md` - This document

### Code
- `src/data_loader.py` - Data loading and validation module

---

**Prepared by:** [Your Name/Team]  
**Review Status:** Ready for Task 2 Implementation  
**Git Status:** On branch `task-1-foundation-analysis`  
**Last Updated:** February 5, 2026