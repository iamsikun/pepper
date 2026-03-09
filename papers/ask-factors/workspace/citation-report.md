# Citation Report

## Summary
- Total unique citation keys used in .tex files: 28
- Citations found in original BibTeX: 26
- Missing citations added: 2
- Unused entries removed from bib: 49
- Entries fixed: 1 (title capitalization protection)

## Changes Made

### 1. Missing Citations Added

- `Kingma2015Adam`: Used in `methodology.tex` (line 143) for the Adam optimizer. Added as `@inproceedings` at ICLR 2015 (Kingma and Ba).
- `BrandtSantaClaraValkanov2009`: Used in `methodology.tex` (line 154). This is the same paper as `Brandt2009parametric` (Brandt, Santa-Clara, Valkanov 2009, Review of Financial Studies) but cited under a different key. Added a duplicate entry with the `BrandtSantaClaraValkanov2009` key so both citation keys resolve correctly. Note: the paper also uses `Brandt2009parametric` in `introduction.tex` (line 11) and `related_work.tex` (line 13), so both keys must be present.

### 2. Unused Entries Removed (49 entries)

The following entries were present in `references.bib` but never cited in any .tex file:

- `Chamberlain1983arbitrage`
- `ConnorKorajczyk1986performance`
- `FamaFrench1993threefactor`
- `Ferson1999conditioning`
- `Markowitz1952portfolio`
- `StockWatson2002forecasting`
- `BerkGreen2004flows`
- `Cochrane2005asset`
- `HintonSalakhutdinov2006autoencoder`
- `Cremers2009active`
- `Asness2013value`
- `Bengio2013representation`
- `KingmaWelling2014vae`
- `Bali2014macro`
- `Higgins2017betavae`
- `Locatello2019challenging`
- `Elmachtoub2022smart`
- `Ban2018machine`
- `Buehler2019deep`
- `Zhang2021universal`
- `Uysal2021endtoend`
- `Cong2020alphaportfolio`
- `LettauPelger2020estimating`
- `KozakNagelSantosh2020shrinking`
- `FengGiglioXiu2020zoo`
- `GiglioLiaoXiu2021alpha`
- `Haddad2020timing`
- `Daniel2020crosssection`
- `Freyberger2020dissecting`
- `Ehsani2022momentum`
- `Jensen2023replication`
- `Avramov2023mlvs`
- `Avramov2023integrating`
- `Bryzgalova2025forest`
- `Dixon2020deep`
- `FengHePolsonXu2024deep`
- `Bagnara2024review`
- `Nakagawa2018deep`
- `GuijarroOrdonez2025arbitrage`
- `Zhao2024storm`
- `GraphVAE2024cikm`
- `Li2022d3vae`
- `Koa2023dva`
- `Cong2021sequence`
- `Li2021selecting`
- `vanBrakel2024holdings`
- `Tedongap2024wisdom`
- `Gao2024nextportfolio`
- `Kelly2025AIPM`

### 3. BibTeX Quality Fixes

- Protected capitalization in `KellyPruittSu2019ipca` title: added `{A}` for "A Unified Model".
- All entry types verified as correct (articles use `@article` with `journal`/`volume`/`pages`; conference papers use `@inproceedings` with `booktitle`; arXiv preprints use `@misc` with `howpublished`).
- Venue names verified as unabbreviated where applicable.
- Author names verified in "Lastname, Firstname" format throughout.

## Citation Keys by Section

### abstract.tex
- (no citations)

### introduction.tex (10 unique keys)
- `GuKellyXiu2021autoencoder`, `ChenPelgerZhu2024deep`, `LettauPelger2020factors`, `KellyPruittSu2019ipca`, `Duan2022factorvae`, `Epstein2025attention`, `Huberman1987mimicking`, `Brandt2009parametric`, `FamaFrench2015fivefactor`, `Carhart1997persistence`

### related_work.tex (23 unique keys)
- `Ross1976apt`, `FamaFrench2015fivefactor`, `Carhart1997persistence`, `BaiNg2002factors`, `LettauPelger2020factors`, `KellyPruittSu2019ipca`, `GuKellyXiu2021autoencoder`, `ChenPelgerZhu2024deep`, `Epstein2025attention`, `Kelly2024large`, `Duan2022factorvae`, `WangGuo2024rvrae`, `WangSingh2024kan`, `Gopal2024neuralfactors`, `Engel2025scaling`, `Jang2025consensus`, `Huberman1987mimicking`, `Brandt2009parametric`, `Amos2017optnet`, `Donti2017taskbased`, `Zhang2020portfolio`, `Sharpe1992style`, `Kaniel2023skill`, `DeMiguel2023fund`

### methodology.tex (6 unique keys)
- `Kingma2015Adam`, `GuKellyXiu2021autoencoder`, `Huberman1987mimicking`, `Donti2017taskbased`, `Agrawal2019differentiable`, `BrandtSantaClaraValkanov2009`

### experiments.tex (4 unique keys)
- `Carhart1997persistence`, `FamaFrench2015fivefactor`, `GuKellyXiu2020empirical`, `GuKellyXiu2021autoencoder`

### conclusion.tex (1 unique key)
- `Duan2022factorvae`

## Potential Issues

- **Duplicate key for same paper**: `Brandt2009parametric` and `BrandtSantaClaraValkanov2009` refer to the same paper but are used under two different keys in different .tex files. Consider standardizing to `Brandt2009parametric` across all .tex files (would require changing one citation in `methodology.tex` line 154) to avoid a duplicate entry in the bibliography.
- **Missing pages field**: `DeMiguel2023fund` is missing `pages` field. This may cause incomplete rendering in some BibTeX styles.
- **ArXiv papers that may have been published**: `Kelly2024large`, `WangGuo2024rvrae`, `WangSingh2024kan`, `Jang2025consensus`, and `Zhang2020portfolio` are listed as arXiv preprints. Check whether they have been formally published before camera-ready submission.

## Files Written

- Paper-specific BibTeX: `/home/iamsikun/research/paper-writer/papers/ask-factors/references.bib`
- This report: `/home/iamsikun/research/paper-writer/papers/ask-factors/workspace/citation-report.md`
