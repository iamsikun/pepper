# Paper Outline: Interpretable and Tradable Factors from Mutual Funds via Deep Autoencoding with Alternative Data
Venue: NeurIPS 2026
Target Length: 8 pages + unlimited references (double-column)

## Narrative Arc (2--3 sentences)

Traditional factor models (Fama-French) explain equity returns well but fail on non-equity assets, while deep latent factor models learn abstract, non-tradable representations that resist economic interpretation. We propose an Autoencoding Factor Model (AFM) with a portfolio bottleneck that forces each latent factor to be the return of an explicit, tradable portfolio whose weights are conditioned on mutual fund characteristics (sector holdings, asset class allocations). Trained across 10 asset classes spanning equities, bonds, REITs, and emerging markets, the AFM achieves 85.0% average out-of-sample R-squared -- a 16.6 percentage point improvement over Fama-French -- with the largest gains on non-equity assets where traditional factors have near-zero explanatory power.

## Contributions (to appear in Introduction)

1. **Portfolio bottleneck architecture.** We propose a neural autoencoder where each latent factor is constrained to be the return of a tradable portfolio with explicit, no-look-ahead weights, bridging deep latent factor models and traditional portfolio-based factor construction.
2. **Conditional factor structure via fund-level alternative data.** Factor portfolio weights and loadings are conditioned on mutual fund characteristics (economic sector holdings, asset class allocations) derived from regulatory filings, enabling interpretable, time-varying factor exposures.
3. **Cross-asset factor learning.** Multi-asset training across 10 categories (equities, bonds, REITs, EM) achieves 85.0% average OOS R-squared vs. 68.4% for Fama-French 4-factor, with the largest gains on non-equity assets (US aggregate bonds: 84% vs. 11%; EM debt: 44% vs. 11%).
4. **Comprehensive ablation study.** We systematically evaluate architecture choices (MLP vs. residual MLP), training universes (single-asset vs. multi-asset), and number of factors, demonstrating that simpler architectures and broader training universes yield superior generalization.

## Section Plan

### Abstract (~150 words)
- Sentence 1: Factor models are central to asset pricing and portfolio construction, but traditional models fail on non-equity assets.
- Sentence 2: Deep latent factor models improve fit but produce abstract, non-tradable factors that resist interpretation.
- Sentence 3: We propose the Autoencoding Factor Model (AFM), a neural autoencoder with a portfolio bottleneck that constrains each factor to be the return of an explicit, tradable portfolio.
- Sentence 4: Portfolio weights and factor loadings are conditioned on fund-level characteristics (sector holdings, asset class allocations) and a learned market-state embedding from past returns.
- Sentence 5: Trained on ~1,000 US mutual funds across 10 asset classes, the AFM with 5 factors achieves 85.0% average OOS R-squared, a 16.6pp improvement over Fama-French 4-factor.
- Sentence 6: The largest gains are on non-equity assets (US aggregate bonds: 84% vs. 11%; EM debt: 44% vs. 11%), where traditional equity factors have near-zero explanatory power.
- Sentence 7: Ablations show that simpler architectures and multi-asset training are key to generalization, and that the portfolio bottleneck produces factors that are simultaneously tradable, interpretable, and predictive.

### 1. Introduction (~1.5 pages)

- **Para 1: Hook.** Factor models are the workhorse of asset pricing, risk management, and portfolio construction. Practitioners and academics rely on a small number of common factors to explain the cross-section of returns. Yet the dominant models (Fama-French, Carhart) are designed for equities and perform poorly on bonds, REITs, and emerging market assets -- asset classes that collectively represent trillions in AUM.
  - Key citations: \citep{fama1993common, carhart1997persistence, asness2013value}

- **Para 2: What is known.** Deep learning has transformed factor modeling. Conditional autoencoders \citep{gu2021autoencoder} learn nonlinear mappings from characteristics to factor loadings. GAN-based SDF estimation \citep{chen2024deep}, attention-based factors \citep{epstein2025attention}, and VAE extensions \citep{duan2022factorvae} push predictive boundaries further. These models achieve impressive Sharpe ratios and R-squared on US equity returns.

- **Para 3: What is NOT known / what fails.** Two critical gaps remain. First, most deep factor models produce latent factors that are abstract statistical objects -- they cannot be directly traded or economically interpreted. The tradability constraint from \citet{gu2021autoencoder} is often relaxed in subsequent work. Second, virtually all models are trained and evaluated exclusively on US equities; their performance on bonds, REITs, and EM assets is unknown. Fund-level alternative data (portfolio holdings, sector allocations) remains unexploited as conditioning information.
  - Key citations: \citep{gu2021autoencoder, kelly2019ipca, bagnara2024review}

- **Para 4: Our approach.** We propose the Autoencoding Factor Model (AFM), which addresses both gaps simultaneously. The key architectural innovation is a portfolio bottleneck: each latent factor is defined as the return of an explicit portfolio whose weights are produced by a neural network (ScoreNet) and mapped to valid allocations via softmax (long-only) or softmax-minus-softmax (market-neutral). Factor loadings and intercepts are produced by separate networks (BetaNet, AlphaNet) conditioned on fund characteristics and a learned market-state embedding (ReturnEncoder). The entire system is trained end-to-end via reconstruction loss.

- **Para 5: Contributions.** Bulleted list of the 4 contributions above.

- **Para 6: Paper roadmap.** Section 2 reviews related work. Section 3 formalizes the model. Section 4 describes experiments. Section 5 concludes.

### 2. Related Work (~1 page)

- **2.1 Deep Latent Factor Models for Asset Pricing**
  - Gu, Kelly, Xiu (2021) conditional autoencoder; Chen, Pelger, Zhu (2024) GAN-SDF; Lettau and Pelger (2020) RP-PCA; Kelly, Pruitt, Su (2019) IPCA; Feng et al. (2024) characteristics-sorted deep factors; Kelly et al. (2024) large and deep factor models; Epstein et al. (2025) attention factors.
  - **How we differ:** These models operate on individual stock returns and produce non-tradable latent factors. Our portfolio bottleneck enforces tradability by construction; we operate on mutual fund returns across multiple asset classes.

- **2.2 Autoencoder and VAE Extensions**
  - Duan et al. (2022) FactorVAE; Wang and Guo (2024) RVRAE; Wang and Singh (2024) KAN autoencoders; Jang et al. (2025) consensus-bottleneck; Engel et al. (2025) scaling conditional autoencoders; Gopal (2024) NeuralFactors.
  - **How we differ:** These extensions focus on probabilistic modeling, alternative network architectures, or analyst consensus as bottleneck information. None enforces portfolio tradability or conditions on fund-level characteristics. Our bottleneck is a portfolio return, not an information bottleneck.

- **2.3 Portfolio-Based Factor Construction and End-to-End Portfolio Learning**
  - Huberman, Kandel, Stambaugh (1987) mimicking portfolios; Brandt, Santa-Clara, Valkanov (2009) parametric portfolio policies; Zhang, Zohren, Roberts (2020) end-to-end Sharpe optimization; Amos and Kolter (2017) OptNet; Cong et al. (2020) AlphaPortfolio.
  - **How we differ:** Classical mimicking portfolios use linear projections; end-to-end portfolio methods optimize trading performance, not factor structure. Our model bridges these two streams: it learns factor-mimicking portfolios via neural networks while optimizing for cross-sectional explanatory power.

- **2.4 Mutual Fund Analysis and Alternative Data**
  - Sharpe (1992) returns-based style analysis; Kaniel et al. (2023) ML for fund manager skill; DeMiguel et al. (2023) ML and fund characteristics; Li and Rossi (2021) fund selection from holdings; Cremers and Petajisto (2009) Active Share.
  - **How we differ:** Existing ML fund analysis uses characteristics for fund selection or alpha prediction. We use fund-level characteristics (sector holdings, asset class allocations from N-PORT filings) as conditioning variables for factor construction -- a fundamentally different task.

- **Key differentiator paragraph:** To our knowledge, no prior work combines (i) a portfolio bottleneck enforcing tradability, (ii) conditioning on fund-level alternative data, and (iii) multi-asset training across equities, bonds, REITs, and EM in a unified autoencoder framework.

### 3. Method (~2.5 pages)

- **3.1 Problem Setup and Notation (~0.3 pages)**
  - Define returns $r_{i,t}$, characteristics $x_{i,t}$, lookback window $R_{t-1}^{(L-1)}$, information set $\mathcal{F}_{t-1}$
  - State the goal: learn $F$ latent factors that admit a conditional linear representation $r_t \approx \alpha_{t-1} + B_{t-1} f_t$ where factors are tradable portfolios $f_t = W_{t-1}^\top r_t$
  - Notation table (see below)

- **3.2 Architecture Overview (~0.3 pages)**
  - Present the autoencoder interpretation: encoder maps $\mathcal{F}_{t-1}$ to portfolio weights $W_{t-1}$ and exposures $(\alpha_{t-1}, B_{t-1})$; bottleneck is $f_t = W_{t-1}^\top r_t$; decoder reconstructs $\hat{r}_t = \alpha_{t-1} + B_{t-1} f_t$
  - Reference Figure 1 (architecture diagram)
  - Four sub-networks: ReturnEncoder, ScoreNet, BetaNet, AlphaNet

- **3.3 Sub-Network Details (~1.0 pages)**
  - **ReturnEncoder:** $s_{t-1} = g_\psi(\text{vec}(R_{t-1}^{(L-1)})) \in \mathbb{R}^S$ -- compresses 252-day return panel into state vector; captures time-varying market regimes
  - **ScoreNet and Portfolio Weight Construction:** $h_\phi(x_{i,t-1}, s_{t-1})$ produces raw scores; long-only factors via softmax; long-short market-neutral via softmax-minus-softmax with gross leverage normalization; mixing $k_0$ long-only and $F - k_0$ long-short factors
  - **BetaNet:** $\beta_{i,t-1} = b_\theta(x_{i,t-1}, s_{t-1}) \in \mathbb{R}^F$ -- conditional factor loadings
  - **AlphaNet:** $\alpha_{i,t-1} = a_\eta(x_{i,t-1}, s_{t-1}) \in \mathbb{R}$ -- asset-specific intercepts
  - Emphasize no-look-ahead: all weights and exposures are $\mathcal{F}_{t-1}$-measurable

- **3.4 Training Objective (~0.5 pages)**
  - Reconstruction loss: $\ell_\text{rec}(t) = \frac{1}{N}\sum_i (\hat{r}_{i,t} - r_{i,t})^2$
  - Orthogonality penalty: $\ell_\text{orth} = \|\hat{\Sigma}_f - \text{diag}(\hat{\Sigma}_f)\|_F^2$ -- prevents factor collapse
  - L2 regularization on loadings and weights
  - Total: $\mathcal{L} = \mathbb{E}_t[\ell_\text{rec} + \lambda_\text{orth}\ell_\text{orth} + \lambda_\beta\ell_\beta + \lambda_w\ell_w]$
  - Training procedure: Adam, mini-batches of time indices, early stopping

- **3.5 Discussion: Why the Portfolio Bottleneck Matters (~0.4 pages)**
  - Comparison to free latent codes in standard autoencoders
  - Tradability: each factor is a live trading strategy
  - Interpretability: factor weights reveal which funds drive each factor; betas reveal fund exposures
  - Regularization effect: constraining factors to be portfolio returns acts as implicit regularizer
  - Connection to classical mimicking portfolios (Huberman et al. 1987) and parametric portfolio policies (Brandt et al. 2009)

### 4. Experiments (~2.5 pages)

- **4.1 Setup (~0.5 pages)**
  - **Data:** ~1,000 US mutual funds from 10 asset classes (large cap, mid cap, small cap, EM equity, non-US equity, US REIT, US aggregate bonds, US high yield, EM debt, municipal debt); daily returns; characteristics from N-PORT filings (economic sector holdings, asset class allocations); cross-sectionally normalized per date
  - **Baselines:** Fama-French 4-factor (MKT-RF, SMB, HML, UMD)
  - **Evaluation metric:** Cross-sectional OLS R-squared on held-out validation period (last 10% of dates), computed per fund then averaged
  - **Model configurations:** (i) AFM MLP All (single-layer MLP, all 10 asset classes, 34.8M params); (ii) AFM Residual MLP All (residual MLP, all classes, 69.8M params); (iii) AFM MLP Large Cap (MLP, large cap only, 13.8M params); (iv) AFM Residual MLP Large Cap (residual MLP, large cap only, 27.7M params)
  - **Hyperparameters:** 5 factors (2 long-only, 3 long-short), lookback 252 days, state dim 16, hidden dim 128, GELU activation, layer norm, dropout 0.3--0.5, Adam lr=0.01, batch size 128, 150 epochs

- **4.2 Main Results (~0.7 pages)**
  - Reference Table 1: Full comparison across all models and 10 asset classes
  - Headline: Best AFM achieves 85.0% avg OOS R-squared vs. 68.4% for FF -- 16.6pp improvement
  - Equity categories: all models achieve >82% R-squared; AFM and FF are competitive
  - Non-equity: AFM dramatically outperforms (US agg 84% vs. 11%; EM debt 44% vs. 11%; high yield 53% vs. 35%; REIT 66% vs. 55%)
  - Reference Figure 2: R-squared comparison bar chart across categories
  - Discussion: traditional equity factors have near-zero explanatory power for bond and EM returns; the portfolio bottleneck learns cross-asset factors that capture these dynamics

- **4.3 Ablation: Architecture Complexity (~0.4 pages)**
  - MLP (34.8M params, 85.0% R-squared) vs. Residual MLP (69.8M params, 82.7% R-squared)
  - Simpler architecture wins despite half the parameters
  - Holds across both training universes (large-cap-only: 73.0% vs. 70.7%)
  - Interpretation: mutual fund returns have smoother cross-sectional structure than individual stocks; additional depth adds capacity without useful expressiveness
  - Reference Table 2 (ablation summary)

- **4.4 Ablation: Training Universe (~0.4 pages)**
  - Multi-asset training (85.0%) vs. large-cap-only (73.0%) -- 12pp improvement
  - Per-category analysis: multi-asset training improves every non-equity category dramatically (e.g., US agg: 84% vs. 11%)
  - Even equity categories benefit modestly from cross-asset training signal
  - Interpretation: cross-asset training enables transfer learning of shared factor structure; bond and equity returns share common drivers (rates, credit, macro) that single-asset training cannot discover
  - Reference Figure 2 (grouped bars showing universe effect)

- **4.5 Training Dynamics (~0.3 pages)**
  - All models converge within 10--15 epochs; best validation loss at epochs 84--114
  - No overfitting observed across any configuration
  - Reference Figure 3: Training loss curves for all AFM variants
  - Discussion: the portfolio bottleneck constrains the model sufficiently to prevent overfitting despite large parameter counts

- **4.6 Limitations and Failure Modes (~0.2 pages)**
  - Municipal debt: R-squared peaks at 30% -- likely requires richer characteristics (credit quality, duration, tax status)
  - EM debt: 44% R-squared is a large improvement but still moderate
  - No out-of-sample portfolio performance evaluation (Sharpe ratios, turnover) -- left to future work
  - Single evaluation split; no cross-validation due to computational cost

### 5. Conclusion (~0.5 pages)
- Summary: We proposed the AFM, a portfolio bottleneck autoencoder that produces tradable, interpretable factors conditioned on fund characteristics. Across 10 asset classes, it achieves 85% OOS R-squared, with massive gains on non-equity assets.
- **Limitations:**
  1. Evaluation is limited to explanatory R-squared; portfolio-level metrics (Sharpe, turnover, transaction costs) are not evaluated.
  2. Municipal and EM debt remain challenging; richer characteristics may be needed.
  3. The model is evaluated on a single train/validation split.
- **Future work:**
  1. Portfolio performance evaluation and live trading simulation
  2. Incorporation of additional characteristics (credit ratings, duration, macro indicators)
  3. Extension to individual securities (stocks, bonds) and larger cross-sections
  4. Theoretical analysis of the portfolio bottleneck as regularizer

### Appendix
- **A: Implementation Details** -- Full hyperparameter table, compute requirements, software stack
- **B: Additional Per-Category Results** -- In-sample R-squared, median R-squared, per-fund R-squared distributions
- **C: Characteristic Description** -- Full list of economic sector and asset allocation features from N-PORT filings
- **D: Factor Portfolio Analysis** -- Sample factor portfolio weights, turnover statistics, concentration metrics
- **E: Sensitivity to Number of Factors** -- Results with 3, 5, 7 factors (if available)

## Figure & Table Plan

| # | Type | Title | What it Shows | Section |
|---|------|-------|---------------|---------|
| Fig 1 | Diagram | AFM Architecture | Full architecture with ReturnEncoder, ScoreNet (softmax/softmax-minus-softmax), BetaNet, AlphaNet, portfolio bottleneck, and reconstruction. Show data flow with no-look-ahead boundary. | S3.2 |
| Fig 2 | Grouped bar chart | OOS R-squared by Asset Class | Per-category OOS R-squared for AFM MLP All, AFM ResMLP All, AFM MLP LC, FF. Grouped by category, color-coded by model. Highlights non-equity gains. | S4.2 |
| Fig 3 | Line plot | Training Loss Trajectories | Epoch vs. training/validation loss for all 4 AFM variants. Shows fast convergence and no overfitting. | S4.5 |
| Tab 1 | Results table | Main Results: OOS R-squared Across Models and Asset Classes | 5 models (rows) x 10 asset classes + avg + median (columns). Bold best per column. | S4.2 |
| Tab 2 | Ablation table | Ablation: Architecture and Training Universe | 2x2 grid (MLP vs ResMLP) x (All vs Large Cap). Shows avg R-squared, median R-squared, param count. | S4.3--4.4 |

## Notation to Define

| Symbol | Meaning |
|--------|---------|
| $N$ | Number of assets (mutual funds) |
| $T$ | Number of time periods |
| $F$ | Number of latent factors |
| $D$ | Dimension of characteristic vector per asset |
| $S$ | Dimension of learned state vector |
| $L$ | Lookback window length (252 trading days) |
| $r_{i,t}$ | Excess return of asset $i$ at time $t$ |
| $r_t$ | $N$-vector of returns at time $t$ |
| $x_{i,t}$ | Characteristic vector of asset $i$ at time $t$ |
| $X_t$ | $N \times D$ characteristic matrix at time $t$ |
| $R_{t-1}^{(L-1)}$ | $N \times (L-1)$ lagged return window |
| $\mathcal{F}_{t-1}$ | Information set at $t-1$ |
| $s_{t-1}$ | Learned market state vector at $t-1$ |
| $W_{t-1}$ | $N \times F$ portfolio weight matrix (encoder) |
| $w_{t-1}^{(k)}$ | $N$-vector of weights for factor $k$ |
| $f_t$ | $F$-vector of realized factor returns |
| $B_{t-1}$ | $N \times F$ conditional factor loading matrix |
| $\beta_{i,t-1}$ | $F$-vector of factor loadings for asset $i$ |
| $\alpha_{t-1}$ | $N$-vector of asset intercepts |
| $g_\psi$ | ReturnEncoder network |
| $h_\phi$ | ScoreNet network |
| $b_\theta$ | BetaNet network |
| $a_\eta$ | AlphaNet network |
| $\Theta$ | All learnable parameters $(\psi, \eta, \theta, \phi)$ |
| $\lambda_\text{orth}, \lambda_\beta, \lambda_w$ | Regularization hyperparameters |
| $k_0$ | Number of long-only factors (2) |

## Writing Notes for Section Agents

1. **Venue style:** NeurIPS 2026 double-column, 8 pages + unlimited references. Use `neurips_2025.sty` (or 2026 when available). Contributions in Introduction as a bulleted list, not prose.

2. **Citations:** Use `\citep{}` for parenthetical citations (e.g., "prior work has shown X \citep{gu2021autoencoder}") and `\citet{}` for textual citations (e.g., "\citet{gu2021autoencoder} proposed...").

3. **Math environments:** Use `\theorem`, `\proposition`, `\remark` environments sparingly -- this is primarily an empirical/methodology paper, not a theory paper. No formal theorems needed, but the portfolio bottleneck construction should be presented with definition-level rigor.

4. **Tables:** Bold the best result in each column of Table 1. Use `\textbf{}` for bolding. Include standard errors or confidence intervals if available.

5. **Figures:** Figure 1 (architecture) is critical -- it should be placed at the top of page 2 or 3 and span the full column width. Use TikZ or a clean PDF import. Figure 2 should use a colorblind-friendly palette.

6. **Terminology consistency:** Always say "portfolio bottleneck" (not "portfolio constraint" or "tradability constraint"). Always say "fund characteristics" or "fund-level characteristics" (not "features" or "covariates" -- to distinguish from stock-level characteristics in prior work). Always say "OOS R-squared" (not "test R-squared" or "validation R-squared").

7. **Key narrative beats:**
   - Introduction must establish that the problem is not just about beating Fama-French on equities (everyone does that) but about building factors that work across asset classes.
   - Related Work must clearly distinguish the portfolio bottleneck from free latent codes in standard autoencoders -- this is the core architectural novelty.
   - Method section should emphasize the no-look-ahead guarantee early and prominently.
   - Experiments should lead with the headline number (85% vs 68.4%) but spend more space on the cross-asset story and ablations than on the headline comparison.

8. **Proofs and derivations:** No formal proofs needed. The softmax-minus-softmax market neutrality property ($\sum_i w_i = 0$) is trivial and can be stated inline.

9. **Model details in appendix:** Full hyperparameter tables, training details, and characteristic descriptions should go in the appendix to save main-body space.

10. **Source files:** Section drafters should read `projects/ask-factors/docs/model.md` for precise mathematical notation and `projects/ask-factors/docs/analysis.md` for result numbers. Write section drafts to `papers/ask-factors/workspace/sections/`.
