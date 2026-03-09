# Literature Survey: Autoencoders and Representation Learning for Financial Factor Models

**Date:** 2026-03-04
**Query:** Autoencoders for financial time series/returns, representation learning for financial data, interpretable deep learning factor models, disentangled representations for factor discovery, neural network factor models, NeurIPS/ICML/ICLR financial ML papers (2022-2025)

## Key Themes

- **Autoencoder-based factor models** have emerged as the dominant nonlinear extension of classical linear factor models (PCA, IPCA), with Gu, Kelly, and Xiu (2021) establishing the conditional autoencoder as the key baseline that all subsequent work compares against.
- **Variational and probabilistic extensions** (FactorVAE, RVRAE, GraphVAE) address the low signal-to-noise ratio of financial data by modeling latent factors as distributions rather than point estimates, enabling uncertainty quantification alongside return prediction.
- **Interpretability-performance tradeoff** is a central tension: deep models (Chen, Pelger, Zhu 2024; Feng et al. 2024) achieve superior predictive performance but sacrifice economic interpretability; recent work (consensus-bottleneck, KAN-autoencoders) seeks to recover interpretability without sacrificing accuracy.
- **Disentanglement and factor discovery**: While disentangled representation learning (beta-VAE, Locatello et al. 2019) is mature in computer vision, its application to financial factor discovery remains largely unexplored -- a significant gap.
- **Mutual fund-specific ML** is growing (Kaniel et al. 2023; DeMiguel et al. 2023) but existing work uses standard ML for fund selection rather than autoencoder-based factor models tailored to fund return structure, leaving a clear opening.

---

## Seminal Works

| Paper | Venue | Year | Key Contribution |
|---|---|---|---|
| Ross, "The Arbitrage Theory of Capital Asset Pricing" | J. Economic Theory | 1976 | Introduced APT: expected returns are linearly related to factor loadings under no-arbitrage. |
| Fama & French, "Common Risk Factors in the Returns on Stocks and Bonds" | J. Financial Economics | 1993 | Three-factor model (market, size, value) -- standard benchmark for cross-sectional returns. |
| Carhart, "On Persistence in Mutual Fund Performance" | J. Finance | 1997 | Extended FF3 with momentum; showed fund persistence is explained by common factors and expenses, not skill. |
| Bai & Ng, "Determining the Number of Factors in Approximate Factor Models" | Econometrica | 2002 | Information criteria for consistently estimating the number of latent factors in large panels. |
| Hinton & Salakhutdinov, "Reducing the Dimensionality of Data with Neural Networks" | Science | 2006 | Seminal deep autoencoder paper; pretrained deep networks learn better representations than PCA. |
| Kingma & Welling, "Auto-Encoding Variational Bayes" | ICLR | 2014 | Introduced VAEs and reparameterization trick -- foundation for all VAE-based factor models. |
| Fama & French, "A Five-Factor Asset Pricing Model" | J. Financial Economics | 2015 | Extended with profitability and investment factors; current standard linear benchmark. |
| Higgins et al., "beta-VAE" | ICLR | 2017 | Introduced beta-VAE for disentangled representations via information bottleneck control. |

---

## Recent Work (Last 3 Years)

| Paper | Venue | Year | Key Contribution |
|---|---|---|---|
| Gu, Kelly, & Xiu, "Autoencoder Asset Pricing Models" | J. Econometrics | 2021 | Conditional autoencoder for asset pricing; covariates guide nonlinear dimension reduction into latent factors under no-arbitrage. **Primary baseline.** |
| Gu, Kelly, & Xiu, "Empirical Asset Pricing via Machine Learning" | Rev. Financial Studies | 2020 | Comprehensive ML comparison; neural nets and trees dominate via nonlinear predictor interactions. |
| Chen, Pelger, & Zhu, "Deep Learning in Asset Pricing" | Management Science | 2024 | Deep NNs with adversarial no-arbitrage training and macro state extraction; outperforms benchmarks. |
| Feng, He, Polson, & Xu, "Deep Learning in Characteristics-Sorted Factor Models" | JFQA | 2024 | Treats characteristic sorting as nonlinear activation; unified factor generation and pricing. |
| Duan et al., "FactorVAE" | AAAI | 2022 | First VAE-based dynamic factor model for stocks; prior-posterior learning for noisy data. |
| Wang & Guo, "RVRAE" | arXiv | 2024 | Extended FactorVAE with recurrence for temporal factor dynamics. |
| Wang & Singh, "KAN based Autoencoders for Factor Models" | arXiv | 2024 | KAN layers replace MLPs in conditional autoencoders; improved interpretability. |
| Jang, Jeong, & Kim, "Consensus-Bottleneck Asset Pricing Model" | arXiv | 2025 | Analyst consensus as structural bottleneck; interpretability acts as regularizer. |
| Engel et al., "Scaling Conditional Autoencoders" | ICAIF | 2025 | High-dimensional CAEs with uncertainty-aware factor pruning outperform low-dimensional ones. |
| Li et al., "D3VAE" | NeurIPS | 2022 | Bidirectional VAE with diffusion, denoising, and disentanglement for time series. |
| Kaniel et al., "Machine-Learning the Skill of Mutual Fund Managers" | JFE | 2023 | Neural networks predict fund alpha from stock/fund/macro characteristics. |
| DeMiguel et al., "ML and Fund Characteristics for Fund Selection" | JFE | 2023 | ML exploits fund characteristics for 2.4% annual alpha net of costs. |
| Kelly, Pruitt, & Su, "Instrumented PCA" | JFE | 2019 | Characteristics instrument for time-varying loadings; five IPCA factors explain cross section. |
| Lettau & Pelger, "Estimating Latent Asset-Pricing Factors" | J. Econometrics | 2020 | RP-PCA penalizes pricing errors; detects weak high-Sharpe factors. |
| Kozak, Nagel, & Santosh, "Shrinking the Cross-Section" | JFE | 2020 | Robust SDF from many predictors via economically motivated shrinkage. |
| Locatello et al., "Challenging Common Assumptions in Unsupervised Disentanglement" | ICML | 2019 | Proved unsupervised disentanglement impossible without inductive biases. |

---

## Research Gaps Identified

1. **No autoencoder factor model for mutual fund returns.** All existing autoencoder asset pricing models target individual stock returns. Mutual funds have distinct characteristics that are not addressed.
2. **Disentanglement for financial factor discovery is unexplored.** Despite mature disentangled representation learning, no work applies disentanglement objectives to discover interpretable financial factors.
3. **No integration of fund-level and holding-level characteristics.** Existing ML fund models use fund characteristics as flat features; no work uses autoencoders to jointly learn latent factors from both fund-level attributes and portfolio holdings.
4. **Temporal factor dynamics in autoencoders are underexplored.** No model explicitly captures regime-dependent factor structure within the autoencoder architecture.
5. **Lack of uncertainty quantification in conditional autoencoders.** The dominant Gu et al. (2021) autoencoder produces point estimates.
6. **Interpretability gap.** Deep factor models achieve strong predictive performance but learned factors lack economic meaning.
