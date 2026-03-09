# Literature Survey: Alternative Data, Fund Characteristics, and Conditional Factor Models

**Date:** 2026-03-04
**Query:** Alternative data in asset pricing; fund characteristics as conditioning variables; mutual fund holdings-based analysis; characteristic-managed portfolios; cross-asset factor models

## Key Themes

- **Characteristic-conditioned factor models**: Growing body of work conditions factor portfolio weights and loadings on observable asset/fund characteristics, moving from static (Fama-French) to dynamic, data-driven factor structures (IPCA, conditional autoencoders).
- **Deep learning in asset pricing**: Neural networks increasingly replace linear models for extracting latent factors.
- **Mutual fund characteristics and ML**: Recent work demonstrates that fund-level characteristics predict fund performance when combined with flexible ML methods.
- **Cross-asset factor structures**: Value and momentum premia exist across asset classes, and recent models attempt unified factor structures.
- **Interpretability and tradability**: Tension between flexible deep models and interpretable, tradable factor constructions.

---

## Seminal Works

| Paper | Venue | Year | Key Contribution |
|---|---|---|---|
| Sharpe, "Asset Allocation: Management Style and Performance Measurement" | J. Portfolio Management | 1992 | Returns-based style analysis using asset class indices |
| Carhart, "On Persistence in Mutual Fund Performance" | J. Finance | 1997 | Four-factor model for fund returns |
| Ferson & Harvey, "Conditioning Variables and the Cross Section" | J. Finance | 1999 | Conditioning variables predict returns and explain cross-section |
| Brandt, Santa-Clara, Valkanov, "Parametric Portfolio Policies" | RFS | 2009 | Portfolio weights as functions of asset characteristics |
| Cremers & Petajisto, "How Active Is Your Fund Manager?" | RFS | 2009 | Active Share predicts fund performance |
| Asness, Moskowitz, Pedersen, "Value and Momentum Everywhere" | J. Finance | 2013 | Cross-asset value and momentum premia |
| Fama & French, "A Five-Factor Asset Pricing Model" | JFE | 2015 | Standard five-factor benchmark |

---

## Recent Work

| Paper | Venue | Year | Key Contribution |
|---|---|---|---|
| Gu, Kelly, Xiu, "Autoencoder Asset Pricing Models" | J. Econometrics | 2021 | Conditional autoencoder with no-arbitrage constraint |
| Kelly, Pruitt, Su, "Instrumented PCA" | JFE | 2020 | Observable instruments for dynamic factor loadings |
| Chen, Pelger, Zhu, "Deep Learning in Asset Pricing" | Management Science | 2024 | GAN-based SDF with LSTM macro states |
| Kaniel et al., "ML the Skill of Mutual Fund Managers" | JFE | 2023 | NNs exploit fund characteristics to identify skilled managers |
| DeMiguel et al., "ML and Fund Characteristics" | JFE | 2023 | ML methods exploit large set of fund characteristics; 4.2% annual alpha |
| Jensen, Kelly, Pedersen, "Is There a Replication Crisis in Finance?" | J. Finance | 2023 | 153 factors cluster into 13 themes; majority replicate |
| Avramov, Cheng, Metzker, "ML vs. Economic Restrictions" | Management Science | 2023 | Economic restrictions improve ML predictions |
| Ehsani & Linnainmaa, "Factor Momentum and the Momentum Factor" | J. Finance | 2022 | Factor momentum in high-eigenvalue PCs |
| Kelly et al., "Artificial Intelligence Asset Pricing Models" | NBER WP | 2025 | Transformer-based SDF with cross-asset attention |
| Li & Rossi, "Selecting Mutual Funds from the Stocks They Hold" | SSRN | 2021 | 94 stock characteristics aggregated to fund-level features |
| Haddad, Kozak, Santosh, "Factor Timing" | RFS | 2020 | Optimal factor timing portfolio equals the SDF |
| Daniel et al., "The Cross-Section of Risk and Returns" | RFS | 2020 | Characteristic Efficient Portfolios removing unpriced risk |
| Freyberger, Neuhierl, Weber, "Dissecting Characteristics Nonparametrically" | RFS | 2020 | Adaptive group LASSO for nonparametric characteristic selection |

---

## Research Gaps

1. **Fund-level characteristics as factor conditioning variables** — no prior work conditions factor portfolio weights on mutual fund-level characteristics (sector allocations, asset class holdings).
2. **Explicit tradability constraint in deep factor models** — the portfolio bottleneck architecture fills this gap.
3. **Cross-asset factor learning from fund holdings** — no ML model learns unified latent factors across equities, bonds, REITs, and emerging markets using fund-level alternative data.
4. **Interpretability of deep asset pricing models** — conditioning on economically meaningful fund characteristics for interpretation remains unexplored.
5. **Alternative data beyond stock-level characteristics** — fund-level data from SEC N-PORT filings represents a largely untapped alternative data source.
6. **Factor models for non-equity asset classes** — existing models perform poorly on bonds, REITs, and EM where traditional equity factors have limited explanatory power.
