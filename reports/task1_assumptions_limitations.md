# Task 1: Detailed Assumptions and Limitations

## Critical Distinction: Correlation vs. Causation

### The Fundamental Challenge
In time series analysis of economic data, we face a critical methodological limitation:
**Temporal coincidence does not establish causation.**

### What We Can Say:
- "Event X occurred on Date Y"
- "Oil prices showed significant change around Date Y"
- "The statistical model detects a structural break near Date Y"

### What We Cannot Say:
- "Event X **caused** the price change"
- "Without Event X, prices would have been different"
- "The price change was **exclusively** due to Event X"

### Why This Matters:
1. **Multiple Concurrent Events:** Several events often occur simultaneously
2. **Market Anticipation:** Prices may move before official announcements
3. **Confounding Factors:** Unobserved variables influence prices
4. **Reverse Causality:** Price changes might influence events (e.g., high prices trigger policy responses)

## Specific Assumptions Requiring Validation

### Data Quality Assumptions
| Assumption | Validation Method | Risk if Invalid |
|------------|------------------|-----------------|
| Prices are closing prices | Compare with known market close times | Intraday volatility missed |
| No systematic reporting errors | Cross-check with alternative sources | Biased analysis results |
| Date format consistency | Manual sample verification | Incorrect time alignment |

### Modeling Assumptions
| Assumption | Justification | Alternatives if Invalid |
|------------|---------------|-------------------------|
| Single change point sufficient | Initial simplicity | Multiple change point model |
| Normal distribution of returns | Central Limit Theorem | Student-t or skewed distributions |
| Independent observations | Stationary returns | ARCH/GARCH for volatility clustering |

## Recommendations for Stakeholders

### For Decision-Making:
1. **Use results as one input** among many
2. **Consider confidence intervals**, not just point estimates
3. **Look for consistent patterns** across multiple events
4. **Test sensitivity** to different time windows

### For Further Research:
1. **Incorporate additional data sources** (inventories, production, demand)
2. **Use structural VAR models** for causal inference
3. **Implement machine learning approaches** for complex patterns
4. **Conduct event study methodology** with proper statistical tests

## Ethical Considerations

### Transparency Requirements:
1. Clearly communicate the correlation/causation distinction
2. Disclose all assumptions in reports and presentations
3. Provide access to data and code for reproducibility

### Responsible Communication:
1. Avoid definitive causal language without strong evidence
2. Present confidence intervals alongside estimates
3. Highlight limitations alongside findings
4. Acknowledge alternative explanations

## Document Version Control
- **Version:** 1.0
- **Created:** February 5, 2026
- **Author:** Task 1 Analysis Team
- **Status:** Approved for Task 1 submission