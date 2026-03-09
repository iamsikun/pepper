# Literature Survey: Portfolio-Based Factor Construction and Tradable Factor Models Using ML

**Date:** 2026-03-04
**Query:** Tradable factor construction, mimicking portfolios, portfolio optimization with neural networks, end-to-end portfolio learning, no-arbitrage constraints in factor models

## Key Themes

- **Deep latent factor models for asset pricing**: Neural networks (autoencoders, transformers, LSTMs) learn latent factors from stock characteristics and returns, with no-arbitrage constraints as training objective.
- **Tradability gap**: Most deep factor models learn factors as abstract statistical objects. Very few enforce that each factor corresponds to the return of a real, investable portfolio.
- **End-to-end / decision-focused portfolio learning**: A parallel thread bypasses predict-then-optimize, learning portfolio weights directly from features by differentiating through optimization layers.
- **Conditional and time-varying factor structure**: Modern models condition factor loadings and/or factor returns on observable characteristics and macroeconomic states.
- **Interpretability vs. flexibility tradeoff**: Tension between black-box deep models and interpretable factor structures; bottleneck architectures attempt to bridge this gap.

---

## Seminal Works

| Paper | Venue | Year | Key Contribution |
|---|---|---|---|
| Markowitz, "Portfolio Selection" | J. Finance | 1952 | Founded modern portfolio theory |
| Ross, "The Arbitrage Theory of Capital Asset Pricing" | J. Economic Theory | 1976 | Introduced APT |
| Huberman, Kandel, Stambaugh, "Mimicking Portfolios and Exact Arbitrage Pricing" | J. Finance | 1987 | Foundational for factor-mimicking portfolios |
| Fama & French, "A Five-Factor Asset Pricing Model" | JFE | 2015 | Dominant baseline for cross-sectional pricing |

---

## Recent Work: Deep Factor Models

| Paper | Venue | Year | Key Contribution |
|---|---|---|---|
| Chen, Pelger, Zhu, "Deep Learning in Asset Pricing" | Management Science | 2024 | GAN-based SDF with adversarial test assets |
| Gu, Kelly, Xiu, "Autoencoder Asset Pricing Models" | J. Econometrics | 2021 | Conditional autoencoder; Sharpe 2.16 |
| Kelly, Pruitt, Su, "IPCA" | JFE | 2019 | Linear conditional baseline |
| Lettau, Pelger, "Factors That Fit" | RFS | 2020 | RP-PCA detecting weak high-Sharpe factors |
| Kelly et al., "Large and Deep Factor Models" | arXiv | 2024 | Portfolio Tangent Kernel decomposition |
| Feng et al., "Deep Learning in Characteristics-Sorted Factor Models" | JFQA | 2024 | Structural deep learning for risk factors |
| Epstein et al., "Attention Factors" | ICAIF | 2025 | Attention-based tradable arbitrage factors |
| Engel et al., "Scaling Conditional Autoencoders" | arXiv | 2025 | Uncertainty-driven factor pruning for K=50 |
| Bryzgalova, Pelger, Zhu, "Forest Through the Trees" | J. Finance | 2025 | ML-based cross-section construction |

---

## End-to-End Portfolio Learning

| Paper | Venue | Year | Key Contribution |
|---|---|---|---|
| Zhang, Zohren, Roberts, "Deep Learning for Portfolio Optimization" | arXiv | 2020 | End-to-end Sharpe ratio optimization |
| Uysal, Li, Mulvey, "End-to-End Risk Budgeting" | arXiv | 2021 | Differentiable optimization for risk budgeting |
| Amos & Kolter, "OptNet" | ICML | 2017 | QPs as differentiable NN layers |
| Agrawal et al., "Differentiable Convex Optimization Layers" | NeurIPS | 2019 | General framework; cvxpylayers |
| Donti, Amos, Kolter, "Task-based End-to-end Model Learning" | NeurIPS | 2017 | End-to-end learning with downstream optimization |
| Elmachtoub & Grigas, "Smart Predict, then Optimize" | Management Science | 2022 | SPO loss for decision error |
| Cong et al., "AlphaPortfolio" | SSRN | 2020 | Transformer-based RL for portfolio construction |

---

## Research Gaps

1. **Tradability of latent factors** — no existing work embeds tradability directly into the autoencoder architecture as a structural constraint ("portfolio bottleneck").
2. **Cross-asset factor learning** — virtually all deep asset pricing papers focus on individual US equities.
3. **Alternative data as conditioning information** — no work uses fund-level portfolio holdings as conditioning information for factor construction.
4. **Simultaneous interpretability and tradability** — the portfolio bottleneck naturally provides both.
5. **Connection between end-to-end portfolio learning and factor models** — our work bridges these streams.
