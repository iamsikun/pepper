# Literature Survey: Deep Learning-Based Latent Factor Models for Asset Pricing

**Date:** 2026-03-04
**Query:** Deep latent factor models for asset pricing; neural autoencoder factor models; conditional factor models with time-varying loadings; machine learning for cross-sectional asset pricing

## Key Themes

- **From linear to nonlinear factor models.** The literature has progressed from PCA and linear factor models (Fama-French, IPCA) toward neural network-based architectures that capture nonlinear interactions between characteristics and factor exposures.
- **Autoencoder architectures as the dominant paradigm.** Following Gu, Kelly, and Xiu (2021), conditional autoencoders that map characteristics to factor loadings via neural networks have become the standard deep learning approach.
- **Tension between flexibility and interpretability.** Deep models achieve superior Sharpe ratios and OOS R², but their black-box nature is a concern. Recent bottleneck models try to bridge this gap.
- **Portfolio-based factor construction.** A key economic restriction is that factors should be tradable portfolios. Models that enforce this constraint have a structural advantage.
- **Extension beyond equities.** Most deep factor models are tested on U.S. equities. Application to mutual funds and multi-asset universes remains underexplored.

---

## Seminal Works

| Paper | Venue | Year | Key Contribution |
|---|---|---|---|
| Ross, "The Arbitrage Theory of Capital Asset Pricing" | J. Economic Theory | 1976 | Introduced APT |
| Chamberlain & Rothschild, "Arbitrage, Factor Structure, and Mean-Variance Analysis" | Econometrica | 1983 | Formalized approximate factor structure under no-arbitrage |
| Fama & French, "Common Risk Factors" | J. Financial Economics | 1993 | Three-factor model |
| Carhart, "On Persistence in Mutual Fund Performance" | J. Finance | 1997 | Four-factor model with momentum |
| Connor & Korajczyk, "Performance Measurement with APT" | J. Financial Economics | 1986 | Portfolio-based factor estimation |
| Bai & Ng, "Determining the Number of Factors" | Econometrica | 2002 | Information criteria for number of factors |
| Kingma & Welling, "Auto-Encoding Variational Bayes" | ICLR | 2014 | VAE framework |

---

## Recent Work (Last 3 Years)

| Paper | Venue | Year | Key Contribution |
|---|---|---|---|
| Gu, Kelly, Xiu, "Autoencoder Asset Pricing Models" | J. Econometrics | 2021 | Conditional autoencoder with characteristic-driven nonlinear loadings; Sharpe 2.16 |
| Gu, Kelly, Xiu, "Empirical Asset Pricing via ML" | RFS | 2020 | Comprehensive ML benchmark for return prediction |
| Kelly, Pruitt, Su, "Characteristics Are Covariances" | JFE | 2019 | IPCA: characteristics instrument for time-varying loadings |
| Chen, Pelger, Zhu, "Deep Learning in Asset Pricing" | Management Science | 2024 | GAN-based SDF estimation with LSTM macro state |
| Lettau, Pelger, "Factors That Fit the TS and CS" | RFS | 2020 | RP-PCA penalizing pricing errors |
| Kozak, Nagel, Santosh, "Shrinking the Cross-Section" | JFE | 2020 | Bayesian SDF with shrinkage |
| Feng, Giglio, Xiu, "Taming the Factor Zoo" | J. Finance | 2020 | Model selection for factors |
| Kaniel et al., "ML the Skill of Mutual Fund Managers" | JFE | 2023 | NN prediction of fund alpha |
| Guijarro-Ordonez, Pelger, Zanotti, "Deep Learning Statistical Arbitrage" | Management Science | 2025 | Conditional latent factors + convolutional transformer |
| Kelly et al., "Large and Deep Factor Models" | arXiv | 2024 | Portfolio Tangent Kernel for DNN-SDF |
| Epstein et al., "Attention Factors for Statistical Arbitrage" | ICAIF | 2025 | Attention-based conditional latent factors; Sharpe >4 gross |
| Duan et al., "FactorVAE" | AAAI | 2022 | VAE-based factor model with prior-posterior learning |
| Wang & Guo, "RVRAE" | arXiv | 2024 | VRAE + dynamic factor model |
| Zhao et al., "STORM" | arXiv | 2024 | Dual VQ-VAE for spatial/temporal factors |
| Wang & Singh, "KAN based Autoencoders" | arXiv | 2024 | KAN encoder for interpretable loadings |
| Gopal, "NeuralFactors" | ICAIF | 2024 | VAE-trained factor exposures and returns |
| Jang et al., "Consensus-Bottleneck APM" | arXiv | 2025 | Analyst consensus as structural bottleneck |
| Bagnara, "Asset Pricing and ML: A Critical Review" | J. Economic Surveys | 2024 | Survey of ML methods for asset pricing |

---

## Research Gaps

1. **Application to mutual funds rather than individual equities** — nearly all deep factor models operate on individual stock returns.
2. **Multi-asset factor learning** — existing work focuses almost exclusively on U.S. equities.
3. **Explicit portfolio tradability as architectural constraint** — most subsequent work relaxes the tradability constraint from Gu et al. (2021).
4. **Interpretability via fund characteristics** — conditioning on fund-level characteristics provides more directly interpretable variation.
5. **Joint evaluation on pricing accuracy and portfolio performance** — rare in the literature.
6. **Scalable models for moderate cross-sections** — most models designed for thousands of stocks, not hundreds of funds.
