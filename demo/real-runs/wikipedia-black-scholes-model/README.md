# wikipedia-black-scholes-model

A complete run of the `kip` ingestion pipeline over `black scholes model`.

**73 knowledge units** · **125 citations** (125 verified) · **12 entries handed off** · run `bs` · schema `3.1.0`

---

## Reading this folder

**If you are a person:** the [entries](#the-knowledge-handed-off) below are the output — what a knowledge base would receive. The [assets](#assets) are the tables, formulas and page images recovered from the source, shown as they are stored.

**If you are a model asked to ingest this run, do not work from this file.** It is a rendering and it is lossy. Read, in order:

1. [`runs/bs/07_enqueue/enqueue.jsonl`](runs/bs/07_enqueue/enqueue.jsonl) — **the handoff.** One JSON event per approved entry, each with `payload.title`, `payload.assertions`, `payload.knowledge_state` and an `idempotency_key`. This is the only file you need in order to ingest; everything below is for checking what it says.
2. [`runs/bs/02_units/units.jsonl`](runs/bs/02_units/units.jsonl) — the evidence. Each unit carries verbatim excerpts with character offsets into `normalized.txt`, and `asset_ref` where the evidence is a table cell or a formula. Follow `payload.source_unit_ids` from an entry to get here.
3. `01_normalized/<source>/assets.jsonl` — the tables, formulas and figures. **Check `fidelity` before you trust a comparison:** `exact` came from the source's own markup and can be compared as a string; `transcribed` was read off an image and must not be.
4. `01_normalized/<source>/normalized.txt` — the flat text every non-asset citation resolves against, by character offset.
5. [`runs/bs/00_original_sources/`](runs/bs/00_original_sources) — the raw source, unmodified. Go here when you need to check the pipeline itself.

Everything else records how the output was arrived at: the routing, the judgments, the candidates before audit, and the audit findings.

## What is in each folder

| folder | contents |
|---|---|
| [`00_original_sources`](runs/bs/00_original_sources) | The source documents exactly as ingested, byte for byte. |
| [`01_normalized`](runs/bs/01_normalized) | One directory per source: `normalized.txt` (the flat text every citation resolves against), `assets.jsonl` (tables, formulas and figures the flat text could not hold), `manifest.json`, and `assets/` for any rendered page images. |
| [`02_units`](runs/bs/02_units) | `units.jsonl` — every extracted knowledge unit with its verbatim evidence and character offsets. `omissions.jsonl` — what the completeness check found missing. `rejects.jsonl` if any record failed materialization. |
| [`03_clusters`](runs/bs/03_clusters) | Which units were routed together for comparison, and why. |
| [`04_assessments`](runs/bs/04_assessments) | One judgment per claim: does the evidence support it, contradict it, or settle nothing, and how many INDEPENDENT sources it rests on. |
| [`05_candidates`](runs/bs/05_candidates) | Proposed knowledge-base entries, before audit. |
| [`06_audit`](runs/bs/06_audit) | `audits.jsonl` — the adversarial review of each candidate, with deterministic check results. `corpus_coverage.json` — whether the output fairly represents the whole corpus. |
| [`07_enqueue`](runs/bs/07_enqueue) | **`enqueue.jsonl` is the handoff.** One idempotent event per approved entry. This is the file a consuming knowledge base reads. |
| [`_handoff`](runs/bs/_handoff) | The complete record of every model call: `pending.jsonl` holds the requests, `responses.jsonl` the answers. Copying `responses.jsonl` into a fresh workspace replays the entire run from cache. |

## Does the output represent the corpus?

The run's own corpus-coverage audit returned **`gaps`**, with 1 gap(s) named.

- **The standard normal probability density function, which the source states as N'(x) = dN(x)/dx = (1/sqrt(2*pi)) e^{-x^2/2} (formula asset fml-src-black-scholes-model-fa32a5b3-0015). No unit was extracted for it, so it reached no assertion. Its cumulative counterpart N(x) WAS carried across; only the density is missing.** Gamma, vega and both thetas are written in terms of N'(d+) and cannot be evaluated from the output alone -- a reader has the shape of each Greek but not a number. This is the failure the [PROTECTED] marking exists to catch: the density asserts nothing to argue with, so nothing downstream noticed it was gone. It is not deduplication; the density is stated once in the source and appears nowhere in the output.

> Not loss: six of the seven tables recovered from this source are MediaWiki navigation boxes -- lists of related articles marked up as <table>. They produced no units and should not. The seventh is the Greeks table and every row of it reached an assertion.

> The Greeks are cited to table cells rather than to flattened rows, so the call and put columns are distinguishable in the record. That is the point of the cell citation and it held for all five Greeks.

> Twelve leaves for one article is close to the fragmentation limit, but each answers a distinct question and the two largest -- the Greeks and the interpretation dispute -- would each be too big to merge into anything else.

Full judgment: [`06_audit/corpus_coverage.json`](runs/bs/06_audit/corpus_coverage.json).

## What the checks found

- The completeness check reported **13 finding(s)** against the first extraction: [`02_units/omissions.jsonl`](runs/bs/02_units/omissions.jsonl).
- The adversarial audit reviewed **12 candidate(s)** and passed 2 without requiring a correction: [`06_audit/audits.jsonl`](runs/bs/06_audit/audits.jsonl).

## Assets

**119 assets** — 112 formula, 7 table. 33 cited by at least one unit, 86 not cited.

An uncited asset is not a failure. A source carries structure that is not content -- a navigation box marked up as a table, a page rendered to check one equation on it -- and capturing it losslessly while citing nothing from it is the correct outcome.

Fidelity is part of the record, because the kinds are not equally trustworthy:

- **exact** (119) — structure recovered from markup the source itself carried — citable as a quote

Evidence cites an asset with `asset_ref {asset_id, row, col}` for a table cell, or `{asset_id}` for a formula. A cell reference resolves to the value **and** the headers governing it, which is what makes a figure checkable rather than merely quoted.

### `src-black-scholes-model-fa32a5b3`

[`normalized.txt`](runs/bs/01_normalized/src-black-scholes-model-fa32a5b3/normalized.txt) · [`assets.jsonl`](runs/bs/01_normalized/src-black-scholes-model-fa32a5b3/assets.jsonl) · [`manifest.json`](runs/bs/01_normalized/src-black-scholes-model-fa32a5b3/manifest.json)

#### `tbl-src-black-scholes-model-fa32a5b3-0001`

table · **exact** · extractor `html_tables_v1` · cited by 8 units

|   |   | Call | Put |
|---|---|---|---|
| Delta | ∂ V ∂ S {\displaystyle {\frac {\partial V}{\partial S}}} | N ( d + ) {\displaystyle N(d_{+})\,} | − N ( − d + ) = N ( d + ) − 1 {\displaystyle -N(-d_{+})=N(d_{+})-1\,} |
| Gamma | ∂ 2 V ∂ S 2 {\displaystyle {\frac {\partial ^{2}V}{\partial S^{2}}}} | N ′ ( d + ) S σ T − t {\displaystyle {\frac {N'(d_{+})}{S\sigma {\sqrt {T-t}}}}\,} |   |
| Vega | ∂ V ∂ σ {\displaystyle {\frac {\partial V}{\partial \sigma }}} | S N ′ ( d + ) T − t {\displaystyle SN'(d_{+}){\sqrt {T-t}}\,} |   |
| Theta | ∂ V ∂ t {\displaystyle {\frac {\partial V}{\partial t}}} | − S N ′ ( d + ) σ 2 T − t − r K e − r ( T − t ) N ( d − ) {\displaystyle -{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}-rKe^{-r(T-t)}N(d_{-})\,} | − S N ′ ( d + ) σ 2 T − t + r K e − r ( T − t ) N ( − d − ) {\displaystyle -{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}+rKe^{-r(T-t)}N(-d_{-})\,} |
| Rho | ∂ V ∂ r {\displaystyle {\frac {\partial V}{\partial r}}} | K ( T − t ) e − r ( T − t ) N ( d − ) {\displaystyle K(T-t)e^{-r(T-t)}N(d_{-})\,} | − K ( T − t ) e − r ( T − t ) N ( − d − ) {\displaystyle -K(T-t)e^{-r(T-t)}N(-d_{-})\,} |

Related units: `u-src-black-scholes-model-fa32a5b3-0056`, `u-src-black-scholes-model-fa32a5b3-0056`, `u-src-black-scholes-model-fa32a5b3-0057`, `u-src-black-scholes-model-fa32a5b3-0058`, `u-src-black-scholes-model-fa32a5b3-0059`, `u-src-black-scholes-model-fa32a5b3-0059`, `u-src-black-scholes-model-fa32a5b3-0060`, `u-src-black-scholes-model-fa32a5b3-0060`

#### `tbl-src-black-scholes-model-fa32a5b3-0002`

table · **exact** · extractor `html_tables_v1` · not cited by any unit

| Terms | Delta neutral Exercise Expiration Moneyness Open interest Pin risk Risk-free interest rate Strike price Synthetic position the Greeks Volatility |
|---|---|
| Vanillas | American Bond option Call Employee stock option European Fixed income FX Option styles Put Warrants |
| Exotics | Asian Barrier Basket Binary Callable bull/bear contract Chooser Cliquet Compound Forward start Interest rate Lookback Mountain range Rainbow Spread Swaption |
| Strategies | Backspread Box spread Butterfly Calendar spread Collar Condor Covered option Credit spread Debit spread Diagonal spread Fence Intermarket spread Iron butterfly Iron condor Jelly roll Ladder Naked option Straddle Strangle Protective option Ratio spread Risk reversal Vertical spread (Bear, Bull) |
| Valuation | Valuation methods Continuous-time stochastic processes: • Arithmetic diffusion: Bachelier • Geometric diffusion: Black, Black–Scholes, Garman–Kohlhagen, Margrabe • Stochastic volatility: Heston • Jump processes: Jump diffusion • Multi-curve framework Multi-curve framework Discrete-time processes: • Binomial, Trinomial, Lattices Numerical methods: • Finite difference, MC Simulation, Real options Model-free:• Put–call parity, Vanna–Volga |

#### `tbl-src-black-scholes-model-fa32a5b3-0003`

table · **exact** · extractor `html_tables_v1` · not cited by any unit

| vteDerivatives market |   |
|---|---|
| Derivative (finance) * List of futures exchanges |   |
| Options |   |
| Swaps | Amortising Asset Basis Commodity Conditional variance Constant maturity Correlation Credit default Currency Dividend Equity Forex Forward Rate Agreement Inflation Interest rate Overnight indexed Total return Variance Volatility Year-on-year inflation-indexed Zero Coupon Zero-coupon inflation-indexed |
| ForwardsFutures | Contango Spot contract Backwardation Commodities future Currency future Dividend future Forward market Forward price Forwards pricing Forward rate Futures pricing Interest rate future Margin Perpetual futures Single-stock futures Slippage Stock market index future |
| Exotic derivatives | Energy derivative Freight derivative Inflation derivative Property derivative Weather derivative |
| Other derivatives | Collateralized debt obligation (CDO) Constant proportion portfolio insurance Contract for difference Credit-linked note (CLN) Credit default option Credit derivative Equity-linked note (ELN) Equity derivative Foreign exchange derivative Fund derivative Fund of funds Interest rate derivative Mortgage-backed security Power reverse dual-currency note (PRDC) |
| Market issues | Consumer debt Corporate debt Government debt Great Recession Municipal debt Tax policy |
| Business portal |   |

#### `tbl-src-black-scholes-model-fa32a5b3-0004`

table · **exact** · extractor `html_tables_v1` · not cited by any unit

| Arbitrage /relative value | Capital structure arbitrage Convertible arbitrage Equity market neutral Fixed income arbitrage / fixed-income relative-value investing (Treasury basis trade) Convergence trade Statistical arbitrage Volatility arbitrage |
|---|---|
| Event-driven | Shareholder activism Distressed securities Risk arbitrage Special situation |
| Directional | Commodity trading advisors / managed futures account Trend following Global macro Long/short equity Dedicated short |
| Other | Fund of hedge funds / Multi-manager |

#### `tbl-src-black-scholes-model-fa32a5b3-0005`

table · **exact** · extractor `html_tables_v1` · not cited by any unit

| Markets | Commodities Derivatives Equity Fixed income Foreign exchange Money markets Structured securities |
|---|---|
| Misc | Absolute return Arbitrage pricing theory Assets under management Black–Scholes model (Greeks: delta neutral) Capital asset pricing model (alpha / beta / security characteristic line) Fundamental analysis Hedge Securitization Short Taxation of private equity and hedge funds Technical analysis |

#### `tbl-src-black-scholes-model-fa32a5b3-0006`

table · **exact** · extractor `html_tables_v1` · not cited by any unit

| vteHedge funds |   |
|---|---|
| Investmentstrategy |   |
| Trading | Algorithmic trading Day trading High-frequency trading (List of electronic trading protocols) Prime brokerage Program trading Proprietary trading |
| Relatedterms |   |
| Investors | Vulture funds Family offices Financial endowments Fund of hedge funds High-net-worth individual Institutional investors Insurance companies Investment banks Merchant banks Pension funds Sovereign wealth funds |
| Governance | Fund governance Standards Board for Alternative Investments Managed Funds Association |
| Alternative investment management companies Hedge funds Hedge fund managers List of hedge funds |   |

#### `tbl-src-black-scholes-model-fa32a5b3-0007`

table · **exact** · extractor `html_tables_v1` · not cited by any unit

| vteStochastic processes |   |
|---|---|
| Discrete time | Bernoulli process Branching process Chinese restaurant process Galton–Watson process Independent and identically distributed random variables Markov chain Moran process Random walk Loop-erased Self-avoiding Biased Maximal entropy |
| Continuous time | Additive process Airy process Bessel process Birth–death process pure birth Brownian motion Bridge Dyson Excursion Fractional Geometric Meander Cauchy process Contact process Continuous-time random walk Cox process Diffusion process Empirical process Feller process Fleming–Viot process Gamma process Geometric process Hawkes process Hunt process Interacting particle systems Itô diffusion Itô process Jump diffusion Jump process Lévy process Local time Markov additive process McKean–Vlasov process Ornstein–Uhlenbeck process Poisson process Compound Non-homogeneous Quasimartingale Schramm–Loewner evolution Semimartingale Sigma-martingale Stable process Superprocess Telegraph process Variance gamma process Wiener process Wiener sausage |
| Both | Branching process Gaussian process Hidden Markov model (HMM) Markov process Martingale Differences Local Sub- Super- Random dynamical system Regenerative process Renewal process Stochastic chains with memory of variable length White noise |
| Fields and other | Dirichlet process Gaussian random field Gibbs measure Hopfield model Ising model Potts model Boolean network Markov random field Percolation Pitman–Yor process Point process Cox Determinantal Poisson Random field Random graph |
| Time series models | Autoregressive conditional heteroskedasticity (ARCH) model Autoregressive integrated moving average (ARIMA) model Autoregressive (AR) model Autoregressive moving-average (ARMA) model Generalized autoregressive conditional heteroskedasticity (GARCH) model Moving-average (MA) model |
| Financial models | Binomial options pricing model Black–Derman–Toy Black–Karasinski Black–Scholes Chan–Karolyi–Longstaff–Sanders (CKLS) Chen Constant elasticity of variance (CEV) Cox–Ingersoll–Ross (CIR) Garman–Kohlhagen Heath–Jarrow–Morton (HJM) Heston Ho–Lee Hull–White Korn-Kreer-Lenssen LIBOR market Rendleman–Bartter SABR volatility Vašíček Wilkie |
| Actuarial models | Bühlmann Cramér–Lundberg Risk process Sparre–Anderson |
| Queueing models | Bulk Fluid Generalized queueing network M/G/1 M/M/1 M/M/c |
| Properties | Càdlàg paths Continuous Continuous paths Ergodic Exchangeable Feller-continuous Gauss–Markov Markov Mixing Piecewise-deterministic Predictable Progressively measurable Self-similar Stationary Time-reversible |
| Limit theorems | Central limit theorem Donsker's theorem Doob's martingale convergence theorems Ergodic theorem Fisher–Tippett–Gnedenko theorem Large deviation principle Law of large numbers (weak/strong) Law of the iterated logarithm Maximal ergodic theorem Sanov's theorem Zero–one laws (Blumenthal, Borel–Cantelli, Engelbert–Schmidt, Hewitt–Savage, Kolmogorov, Lévy) |
| Inequalities | Burkholder–Davis–Gundy Doob's martingale Doob's upcrossing Kunita–Watanabe Marcinkiewicz–Zygmund |

*(3 further rows in the stored grid.)*

#### `fml-src-black-scholes-model-fa32a5b3-0008`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$C(S,t)$$

```latex
C(S,t)
```

> d ] and dividend payout. [ 19 ] Notation At time t, in particular: … is the price of a European call option and P ( S , t )

#### `fml-src-black-scholes-model-fa32a5b3-0009`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$P(S,t)$$

```latex
P(S,t)
```

> C ( S , t ) {\displaystyle C(S,t)} is the price of a European call option and … is the price of a European put option. T {\displaystyle T}

#### `fml-src-black-scholes-model-fa32a5b3-0010`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$\tau$$

```latex
\tau
```

> T {\displaystyle T} is the time of option expiration. … is the time until maturity: τ = T − t {\

#### `fml-src-black-scholes-model-fa32a5b3-0011`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$\tau =T-t$$

```latex
\tau =T-t
```

> τ {\displaystyle \tau } is the time until maturity: … . K {\displaystyle K}

Related units: `u-src-black-scholes-model-fa32a5b3-0017`

#### `fml-src-black-scholes-model-fa32a5b3-0012`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$N(x)$$

```latex
N(x)
```

> K {\displaystyle K} is the strike price of the option, also known as the exercise price. … denotes the standard normal cumulative distribution function :

#### `fml-src-black-scholes-model-fa32a5b3-0013`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$N(x)={\frac {1}{\sqrt {2\pi }}}\int _{-\infty }^{x}e^{-z^{2}/2}\,dz.$$

```latex
N(x)={\frac {1}{\sqrt {2\pi }}}\int _{-\infty }^{x}e^{-z^{2}/2}\,dz.
```

> denotes the standard normal cumulative distribution function : … N ′ ( x

Related units: `u-src-black-scholes-model-fa32a5b3-0016`

#### `fml-src-black-scholes-model-fa32a5b3-0014`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$N'(x)$$

```latex
N'(x)
```

> d z . {\displaystyle N(x)={\frac {1}{\sqrt {2\pi }}}\int _{-\infty }^{x}e^{-z^{2}/2}\,dz.} … denotes the standard normal probability density function :

#### `fml-src-black-scholes-model-fa32a5b3-0015`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$N'(x)={\frac {dN(x)}{dx}}={\frac {1}{\sqrt {2\pi }}}e^{-x^{2}/2}.$$

```latex
N'(x)={\frac {dN(x)}{dx}}={\frac {1}{\sqrt {2\pi }}}e^{-x^{2}/2}.
```

> ) {\displaystyle N'(x)} denotes the standard normal probability density function : … Black–Scholes equation

#### `fml-src-black-scholes-model-fa32a5b3-0016`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$V(S,t)$$

```latex
V(S,t)
```

> ted geometric Brownian motions with parameters from market data The Black–Scholes equation is a parabolic partial differential equation that describes the price … of the option, where S {\displaystyle S}

#### `fml-src-black-scholes-model-fa32a5b3-0017`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$${\frac {\partial V}{\partial t}}+{\frac {1}{2}}\sigma ^{2}S^{2}{\frac {\partial ^{2}V}{\partial S^{2}}}+rS{\frac {\partial V}{\partial S}}-rV=0$$

```latex
{\frac {\partial V}{\partial t}}+{\frac {1}{2}}\sigma ^{2}S^{2}{\frac {\partial ^{2}V}{\partial S^{2}}}+rS{\frac {\partial V}{\partial S}}-rV=0
```

> t {\displaystyle t} is time: … A key financial insight behind the equation is that one can perfectly hedge the

Related units: `u-src-black-scholes-model-fa32a5b3-0011`

#### `fml-src-black-scholes-model-fa32a5b3-0018`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$${\begin{aligned}C(0,t)&=0{\text{ for all }}t\\C(S,t)&\sim S-Ke^{-r(T-t)}{\text{ as }}S\rightarrow \infty \\C(S,T)&=\max\{S-K,0\}\end{aligned}}$$

```latex
{\begin{aligned}C(0,t)&=0{\text{ for all }}t\\C(S,t)&\sim S-Ke^{-r(T-t)}{\text{ as }}S\rightarrow \infty \\C(S,T)&=\max\{S-K,0\}\end{aligned}}
```

> boundary conditions : [ 20 ] … The value of a call option for a non-dividend-paying underlying stock in terms o

Related units: `u-src-black-scholes-model-fa32a5b3-0015`

#### `fml-src-black-scholes-model-fa32a5b3-0019`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$${\begin{aligned}C(S_{t},t)&=N(d_{+})S_{t}-N(d_{-})Ke^{-r(T-t)}\\d_{+}&={\frac {1}{\sigma {\sqrt {T-t}}}}\left[\ln \left({\frac {S_{t}}{K}}\right)+\left(r+{\frac {\sigma ^{2}}{2}}\right)(T-t)\right]\\d_{-}&=d_{+}-\sigma {\sqrt {T-t}}\\\end{aligned}}$$

```latex
{\begin{aligned}C(S_{t},t)&=N(d_{+})S_{t}-N(d_{-})Ke^{-r(T-t)}\\d_{+}&={\frac {1}{\sigma {\sqrt {T-t}}}}\left[\ln \left({\frac {S_{t}}{K}}\right)+\left(r+{\frac {\sigma ^{2}}{2}}\right)(T-t)\right]\\d_{-}&=d_{+}-\sigma {\sqrt {T-t}}\\\end{aligned}}
```

> fty \\C(S,T)&=\max\{S-K,0\}\end{aligned}}}"/> The value of a call option for a non-dividend-paying underlying stock in terms of the Black–Scholes parameters is: … The price of a corresponding put option based on put–call parity with discount f

Related units: `u-src-black-scholes-model-fa32a5b3-0013`

#### `fml-src-black-scholes-model-fa32a5b3-0020`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$e^{-r(T-t)}$$

```latex
e^{-r(T-t)}
```

> \right)(T-t)\right]\\d_{-}&=d_{+}-\sigma {\sqrt {T-t}}\\\end{aligned}}}"/> The price of a corresponding put option based on put–call parity with discount factor … is:

#### `fml-src-black-scholes-model-fa32a5b3-0021`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$${\begin{aligned}P(S_{t},t)&=Ke^{-r(T-t)}-S_{t}+C(S_{t},t)\\&=N(-d_{-})Ke^{-r(T-t)}-N(-d_{+})S_{t}\end{aligned}}\,$$

```latex
{\begin{aligned}P(S_{t},t)&=Ke^{-r(T-t)}-S_{t}+C(S_{t},t)\\&=N(-d_{-})Ke^{-r(T-t)}-N(-d_{+})S_{t}\end{aligned}}\,
```

> t ) {\displaystyle e^{-r(T-t)}} is: … Alternative formulation Introducing auxiliary variables allows for the formula t

Related units: `u-src-black-scholes-model-fa32a5b3-0014`

#### `fml-src-black-scholes-model-fa32a5b3-0022`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$${\begin{aligned}C(F,\tau )&=D\left[N(d_{+})F-N(d_{-})K\right]\\d_{+}&={\frac {1}{\sigma {\sqrt {\tau }}}}\left[\ln \left({\frac {F}{K}}\right)+{\frac {1}{2}}\sigma ^{2}\tau \right]\\d_{-}&=d_{+}-\sigma {\sqrt {\tau }}\end{aligned}}$$

```latex
{\begin{aligned}C(F,\tau )&=D\left[N(d_{+})F-N(d_{-})K\right]\\d_{+}&={\frac {1}{\sigma {\sqrt {\tau }}}}\left[\ln \left({\frac {F}{K}}\right)+{\frac {1}{2}}\sigma ^{2}\tau \right]\\d_{-}&=d_{+}-\sigma {\sqrt {\tau }}\end{aligned}}
```

> ary variables allows for the formula to be simplified and reformulated in a form that can be more convenient (this is a special case of the Black '76 formula ): … where:

Related units: `u-src-black-scholes-model-fa32a5b3-0018`

#### `fml-src-black-scholes-model-fa32a5b3-0023`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$D=e^{-r\tau }$$

```latex
D=e^{-r\tau }
```

> &=d_{+}-\sigma {\sqrt {\tau }}\end{aligned}}} where: … is the discount factor F = e

Related units: `u-src-black-scholes-model-fa32a5b3-0018`

#### `fml-src-black-scholes-model-fa32a5b3-0024`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$F=e^{r\tau }S={\frac {S}{D}}$$

```latex
F=e^{r\tau }S={\frac {S}{D}}
```

> e − r τ {\displaystyle D=e^{-r\tau }} is the discount factor … is the forward price of the underlying asset, and S = D F

Related units: `u-src-black-scholes-model-fa32a5b3-0018`

#### `fml-src-black-scholes-model-fa32a5b3-0025`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$S=DF$$

```latex
S=DF
```

> S D {\displaystyle F=e^{r\tau }S={\frac {S}{D}}} is the forward price of the underlying asset, and … Given put–call parity, which is expressed in these terms as: C − P =

#### `fml-src-black-scholes-model-fa32a5b3-0026`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$C-P=D(F-K)=S-DK$$

```latex
C-P=D(F-K)=S-DK
```

> S = D F {\displaystyle S=DF} Given put–call parity, which is expressed in these terms as: … the price of a put option is: P

Related units: `u-src-black-scholes-model-fa32a5b3-0019`

#### `fml-src-black-scholes-model-fa32a5b3-0027`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$P(F,\tau )=D\left[N(-d_{-})K-N(-d_{+})F\right]$$

```latex
P(F,\tau )=D\left[N(-d_{-})K-N(-d_{+})F\right]
```

> ) = S − D K {\displaystyle C-P=D(F-K)=S-DK} the price of a put option is: … Interpretation It is possible to have intuitive interpretations of the Black–Sch

Related units: `u-src-black-scholes-model-fa32a5b3-0019`

#### `fml-src-black-scholes-model-fa32a5b3-0028`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$d_{\pm }$$

```latex
d_{\pm }
```

> d_{+})F\right]} Interpretation It is possible to have intuitive interpretations of the Black–Scholes formula, with the main subtlety being the interpretation of … and why there are two different terms. [ 21 ] The formula can be interpreted by

#### `fml-src-black-scholes-model-fa32a5b3-0029`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$C=D\left[N(d_{+})F-N(d_{-})K\right]$$

```latex
C=D\left[N(d_{+})F-N(d_{-})K\right]
```

> o the values of the binary call options. These binary options are less frequently traded than vanilla call options, but are easier to analyze. Thus the formula: … breaks up as: C = D N

#### `fml-src-black-scholes-model-fa32a5b3-0030`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$C=DN(d_{+})F-DN(d_{-})K,$$

```latex
C=DN(d_{+})F-DN(d_{-})K,
```

> ) K ] {\displaystyle C=D\left[N(d_{+})F-N(d_{-})K\right]} breaks up as: … where D N ( d +

#### `fml-src-black-scholes-model-fa32a5b3-0031`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$DN(d_{+})F$$

```latex
DN(d_{+})F
```

> d − ) K , {\displaystyle C=DN(d_{+})F-DN(d_{-})K,} where … is the present value of an asset-or-nothing call and D N ( d

#### `fml-src-black-scholes-model-fa32a5b3-0032`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$DN(d_{-})K$$

```latex
DN(d_{-})K
```

> ( d + ) F {\displaystyle DN(d_{+})F} is the present value of an asset-or-nothing call and … is the present value of a cash-or-nothing call. The D factor is for discounting,

#### `fml-src-black-scholes-model-fa32a5b3-0033`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$N(d_{+})~F$$

```latex
N(d_{+})~F
```

> g call. The D factor is for discounting, because the expiration date is in future, and removing it changes present value to future value (value at expiry). Thus … is the future value of an asset-or-nothing call and N ( d −

#### `fml-src-black-scholes-model-fa32a5b3-0034`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$N(d_{-})~K$$

```latex
N(d_{-})~K
```

> d + ) F {\displaystyle N(d_{+})~F} is the future value of an asset-or-nothing call and … is the future value of a cash-or-nothing call. In risk-neutral terms, these are

#### `fml-src-black-scholes-model-fa32a5b3-0035`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$N(d_{+})F$$

```latex
N(d_{+})F
```

> pected value of the asset and the expected value of the cash in the risk-neutral measure. A naive, and slightly incorrect, interpretation of these terms is that … is the probability of the option expiring in the money N ( d +

#### `fml-src-black-scholes-model-fa32a5b3-0036`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$N(d_{+})$$

```latex
N(d_{+})
```

> ( d + ) F {\displaystyle N(d_{+})F} is the probability of the option expiring in the money … , multiplied by the value of the underlying at expiry F, while N ( d

#### `fml-src-black-scholes-model-fa32a5b3-0037`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$N(d_{-})K$$

```latex
N(d_{-})K
```

> ( d + ) {\displaystyle N(d_{+})} , multiplied by the value of the underlying at expiry F, while … is the probability of the option expiring in the money N ( d −

#### `fml-src-black-scholes-model-fa32a5b3-0038`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$N(d_{-}),$$

```latex
N(d_{-}),
```

> ( d − ) K {\displaystyle N(d_{-})K} is the probability of the option expiring in the money … multiplied by the value of the cash at expiry K. This interpretation is incorrec

#### `fml-src-black-scholes-model-fa32a5b3-0039`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$N(d_{-})$$

```latex
N(d_{-})
```

> N ( d + ) {\displaystyle N(d_{+})} and … are not equal. In fact, d ±

#### `fml-src-black-scholes-model-fa32a5b3-0040`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$N(d_{\pm })$$

```latex
N(d_{\pm })
```

> d ± {\displaystyle d_{\pm }} can be interpreted as measures of moneyness (in standard deviations) and … as probabilities of expiring ITM ( percent moneyness ), in the respective numéra

#### `fml-src-black-scholes-model-fa32a5b3-0041`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$${\textstyle {\frac {1}{2}}\sigma ^{2}}$$

```latex
{\textstyle {\frac {1}{2}}\sigma ^{2}}
```

> d ± {\displaystyle d_{\pm }} instead of the … term there is ( r ±

#### `fml-src-black-scholes-model-fa32a5b3-0042`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$${\textstyle \left(r\pm {\frac {1}{2}}\sigma ^{2}\right)\tau ,}$$

```latex
{\textstyle \left(r\pm {\frac {1}{2}}\sigma ^{2}\right)\tau ,}
```

> σ 2 {\textstyle {\frac {1}{2}}\sigma ^{2}} term there is … which can be interpreted as a drift factor (in the risk-neutral measure for appr

#### `fml-src-black-scholes-model-fa32a5b3-0043`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$${\textstyle m={\frac {1}{\sigma {\sqrt {\tau }}}}\ln \left({\frac {F}{K}}\right)}$$

```latex
{\textstyle m={\frac {1}{\sigma {\sqrt {\tau }}}}\ln \left({\frac {F}{K}}\right)}
```

> an be interpreted as a drift factor (in the risk-neutral measure for appropriate numéraire). The use of d − for moneyness rather than the standardized moneyness … – in other words, the reason for the

Related units: `u-src-black-scholes-model-fa32a5b3-0023`

#### `fml-src-black-scholes-model-fa32a5b3-0044`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$N(d_{+}),N(d_{-})$$

```latex
N(d_{+}),N(d_{-})
```

> [ 21 ] : 6 In detail, the terms … are the probabilities of the option expiring in-the-money under the equivalent e

#### `fml-src-black-scholes-model-fa32a5b3-0045`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$S_{T}\in (0,\infty )$$

```latex
S_{T}\in (0,\infty )
```

> ck) and the equivalent martingale probability measure (numéraire=risk free asset), respectively. [ 21 ] The risk neutral probability density for the stock price … is p (

#### `fml-src-black-scholes-model-fa32a5b3-0046`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$p(S,T)={\frac {N^{\prime }[d_{-}(S_{T})]}{S_{T}\sigma {\sqrt {T}}}}$$

```latex
p(S,T)={\frac {N^{\prime }[d_{-}(S_{T})]}{S_{T}\sigma {\sqrt {T}}}}
```

> ( 0 , ∞ ) {\displaystyle S_{T}\in (0,\infty )} is … where d −

#### `fml-src-black-scholes-model-fa32a5b3-0047`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$d_{-}=d_{-}(K)$$

```latex
d_{-}=d_{-}(K)
```

> {\displaystyle p(S,T)={\frac {N^{\prime }[d_{-}(S_{T})]}{S_{T}\sigma {\sqrt {T}}}}} where … is defined as above. Specifically, N ( d −

#### `fml-src-black-scholes-model-fa32a5b3-0048`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$SN(d_{+})$$

```latex
SN(d_{+})
```

> ( d + ) {\displaystyle N(d_{+})} , however, does not lend itself to a simple probability interpretation. … is correctly interpreted as the present value, using the risk-free interest rate

#### `fml-src-black-scholes-model-fa32a5b3-0049`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$${\frac {\partial V}{\partial S}}$$

```latex
{\frac {\partial V}{\partial S}}
```

> ice movements. The Greeks for Black–Scholes are given in closed form below. They can be obtained by differentiation of the Black–Scholes formula. Call Put Delta … N ( d +

#### `fml-src-black-scholes-model-fa32a5b3-0050`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$N(d_{+})\,$$

```latex
N(d_{+})\,
```

> V ∂ S {\displaystyle {\frac {\partial V}{\partial S}}} … − N ( − d

#### `fml-src-black-scholes-model-fa32a5b3-0051`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$-N(-d_{+})=N(d_{+})-1\,$$

```latex
-N(-d_{+})=N(d_{+})-1\,
```

> ( d + ) {\displaystyle N(d_{+})\,} … Gamma

#### `fml-src-black-scholes-model-fa32a5b3-0052`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$${\frac {\partial ^{2}V}{\partial S^{2}}}$$

```latex
{\frac {\partial ^{2}V}{\partial S^{2}}}
```

> ) − 1 {\displaystyle -N(-d_{+})=N(d_{+})-1\,} Gamma …

#### `fml-src-black-scholes-model-fa32a5b3-0053`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$${\frac {N'(d_{+})}{S\sigma {\sqrt {T-t}}}}\,$$

```latex
{\frac {N'(d_{+})}{S\sigma {\sqrt {T-t}}}}\,
```

> 2 {\displaystyle {\frac {\partial ^{2}V}{\partial S^{2}}}} … Vega

#### `fml-src-black-scholes-model-fa32a5b3-0054`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$${\frac {\partial V}{\partial \sigma }}$$

```latex
{\frac {\partial V}{\partial \sigma }}
```

> {\displaystyle {\frac {N'(d_{+})}{S\sigma {\sqrt {T-t}}}}\,} Vega … S N ′

#### `fml-src-black-scholes-model-fa32a5b3-0055`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$SN'(d_{+}){\sqrt {T-t}}\,$$

```latex
SN'(d_{+}){\sqrt {T-t}}\,
```

> ∂ σ {\displaystyle {\frac {\partial V}{\partial \sigma }}} … Theta

#### `fml-src-black-scholes-model-fa32a5b3-0056`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$${\frac {\partial V}{\partial t}}$$

```latex
{\frac {\partial V}{\partial t}}
```

> t {\displaystyle SN'(d_{+}){\sqrt {T-t}}\,} Theta … −

#### `fml-src-black-scholes-model-fa32a5b3-0057`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$-{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}-rKe^{-r(T-t)}N(d_{-})\,$$

```latex
-{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}-rKe^{-r(T-t)}N(d_{-})\,
```

> ∂ t {\displaystyle {\frac {\partial V}{\partial t}}} …

#### `fml-src-black-scholes-model-fa32a5b3-0058`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$-{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}+rKe^{-r(T-t)}N(-d_{-})\,$$

```latex
-{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}+rKe^{-r(T-t)}N(-d_{-})\,
```

> ) {\displaystyle -{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}-rKe^{-r(T-t)}N(d_{-})\,} … Rho

#### `fml-src-black-scholes-model-fa32a5b3-0059`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$${\frac {\partial V}{\partial r}}$$

```latex
{\frac {\partial V}{\partial r}}
```

> {\displaystyle -{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}+rKe^{-r(T-t)}N(-d_{-})\,} Rho … K ( T − t

#### `fml-src-black-scholes-model-fa32a5b3-0060`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$K(T-t)e^{-r(T-t)}N(d_{-})\,$$

```latex
K(T-t)e^{-r(T-t)}N(d_{-})\,
```

> ∂ r {\displaystyle {\frac {\partial V}{\partial r}}} … − K ( T −

#### `fml-src-black-scholes-model-fa32a5b3-0061`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$-K(T-t)e^{-r(T-t)}N(-d_{-})\,$$

```latex
-K(T-t)e^{-r(T-t)}N(-d_{-})\,
```

> − ) {\displaystyle K(T-t)e^{-r(T-t)}N(d_{-})\,} … Note that the gamma and vega are the same value for calls and puts. This can be

#### `fml-src-black-scholes-model-fa32a5b3-0062`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$\nu$$

```latex
\nu
```

> ys or trading days per year). Note that "Vega" is not a letter in the Greek alphabet; the name arises from misreading the Greek letter nu (variously rendered as … , ν , and ν) as a V. Extensions of the model The above model can be extended for

#### `fml-src-black-scholes-model-fa32a5b3-0063`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$[t,t+dt]$$

```latex
[t,t+dt]
```

> ion that dividends are paid continuously, and that the dividend amount is proportional to the level of the index. The dividend payment paid over the time period … is then modelled as: q S t

#### `fml-src-black-scholes-model-fa32a5b3-0064`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$qS_{t}\,dt$$

```latex
qS_{t}\,dt
```

> [ t , t + d t ] {\displaystyle [t,t+dt]} is then modelled as: … for some constant q {\displaystyle q}

#### `fml-src-black-scholes-model-fa32a5b3-0065`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$C(S_{t},t)=e^{-r(T-t)}[FN(d_{1})-KN(d_{2})]\,$$

```latex
C(S_{t},t)=e^{-r(T-t)}[FN(d_{1})-KN(d_{2})]\,
```

> {\displaystyle q} (the dividend yield ). Under this formulation the arbitrage-free price implied by the Black–Scholes model can be shown to be: … and P

Related units: `u-src-black-scholes-model-fa32a5b3-0031`

#### `fml-src-black-scholes-model-fa32a5b3-0066`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$P(S_{t},t)=e^{-r(T-t)}[KN(-d_{2})-FN(-d_{1})]\,$$

```latex
P(S_{t},t)=e^{-r(T-t)}[KN(-d_{2})-FN(-d_{1})]\,
```

> ) ] {\displaystyle C(S_{t},t)=e^{-r(T-t)}[FN(d_{1})-KN(d_{2})]\,} and … where now F = S

#### `fml-src-black-scholes-model-fa32a5b3-0067`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$F=S_{t}e^{(r-q)(T-t)}\,$$

```latex
F=S_{t}e^{(r-q)(T-t)}\,
```

> ) ] {\displaystyle P(S_{t},t)=e^{-r(T-t)}[KN(-d_{2})-FN(-d_{1})]\,} where now … is the modified forward price that occurs in the terms d 1

Related units: `u-src-black-scholes-model-fa32a5b3-0031`

#### `fml-src-black-scholes-model-fa32a5b3-0068`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$d_{1},d_{2}$$

```latex
d_{1},d_{2}
```

> t ) {\displaystyle F=S_{t}e^{(r-q)(T-t)}\,} is the modified forward price that occurs in the terms … :

#### `fml-src-black-scholes-model-fa32a5b3-0069`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$d_{1}={\frac {1}{\sigma {\sqrt {T-t}}}}\left[\ln \left({\frac {S_{t}}{K}}\right)+\left(r-q+{\frac {1}{2}}\sigma ^{2}\right)(T-t)\right]$$

```latex
d_{1}={\frac {1}{\sigma {\sqrt {T-t}}}}\left[\ln \left({\frac {S_{t}}{K}}\right)+\left(r-q+{\frac {1}{2}}\sigma ^{2}\right)(T-t)\right]
```

> 2 {\displaystyle d_{1},d_{2}} : … and

#### `fml-src-black-scholes-model-fa32a5b3-0070`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$d_{2}=d_{1}-\sigma {\sqrt {T-t}}={\frac {1}{\sigma {\sqrt {T-t}}}}\left[\ln \left({\frac {S_{t}}{K}}\right)+\left(r-q-{\frac {1}{2}}\sigma ^{2}\right)(T-t)\right]$$

```latex
d_{2}=d_{1}-\sigma {\sqrt {T-t}}={\frac {1}{\sigma {\sqrt {T-t}}}}\left[\ln \left({\frac {S_{t}}{K}}\right)+\left(r-q-{\frac {1}{2}}\sigma ^{2}\right)(T-t)\right]
```

> ght)(T-t)\right]} and … . [ 25 ]

#### `fml-src-black-scholes-model-fa32a5b3-0071`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$\delta$$

```latex
\delta
```

> n instruments paying discrete proportional dividends. This is useful when the option is struck on a single stock. A typical model is to assume that a proportion … of the stock price is paid out at pre-determined times t 1

#### `fml-src-black-scholes-model-fa32a5b3-0072`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$t_{1},t_{2},\ldots ,t_{n}$$

```latex
t_{1},t_{2},\ldots ,t_{n}
```

> δ {\displaystyle \delta } of the stock price is paid out at pre-determined times … . The price of the stock is then modelled as: S

#### `fml-src-black-scholes-model-fa32a5b3-0073`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$S_{t}=S_{0}(1-\delta )^{n(t)}e^{ut+\sigma W_{t}}$$

```latex
S_{t}=S_{0}(1-\delta )^{n(t)}e^{ut+\sigma W_{t}}
```

> t n {\displaystyle t_{1},t_{2},\ldots ,t_{n}} . The price of the stock is then modelled as: … where n ( t )

Related units: `u-src-black-scholes-model-fa32a5b3-0032`

#### `fml-src-black-scholes-model-fa32a5b3-0074`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$n(t)$$

```latex
n(t)
```

> W t {\displaystyle S_{t}=S_{0}(1-\delta )^{n(t)}e^{ut+\sigma W_{t}}} where … is the number of dividends that have been paid by time t {\displaystyle t}

#### `fml-src-black-scholes-model-fa32a5b3-0075`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$C(S_{0},T)=e^{-rT}[FN(d_{1})-KN(d_{2})]\,$$

```latex
C(S_{0},T)=e^{-rT}[FN(d_{1})-KN(d_{2})]\,
```

> t {\displaystyle t} . The price of a call option on such a stock is again: … where now F =

#### `fml-src-black-scholes-model-fa32a5b3-0076`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$F=S_{0}(1-\delta )^{n(T)}e^{rT}\,$$

```latex
F=S_{0}(1-\delta )^{n(T)}e^{rT}\,
```

> ) ] {\displaystyle C(S_{0},T)=e^{-rT}[FN(d_{1})-KN(d_{2})]\,} where now … is the forward price for the dividend paying stock. American options The problem

Related units: `u-src-black-scholes-model-fa32a5b3-0032`

#### `fml-src-black-scholes-model-fa32a5b3-0077`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$${\frac {\partial V}{\partial t}}+{\frac {1}{2}}\sigma ^{2}S^{2}{\frac {\partial ^{2}V}{\partial S^{2}}}+rS{\frac {\partial V}{\partial S}}-rV\leq 0$$

```latex
{\frac {\partial V}{\partial t}}+{\frac {1}{2}}\sigma ^{2}S^{2}{\frac {\partial ^{2}V}{\partial S^{2}}}+rS{\frac {\partial V}{\partial S}}-rV\leq 0
```

> ion. Since the American option can be exercised at any time before the expiration date, the Black–Scholes equation becomes a variational inequality of the form: … [ 26 ] together with

Related units: `u-src-black-scholes-model-fa32a5b3-0033`

#### `fml-src-black-scholes-model-fa32a5b3-0078`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$V(S,t)\geq H(S)$$

```latex
V(S,t)\geq H(S)
```

> tial V}{\partial t}}+{\frac {1}{2}}\sigma ^{2}S^{2}{\frac {\partial ^{2}V}{\partial S^{2}}}+rS{\frac {\partial V}{\partial S}}-rV\leq 0}"/> [ 26 ] together with … where H ( S ) {\displaystyle H(S)}

Related units: `u-src-black-scholes-model-fa32a5b3-0033`

#### `fml-src-black-scholes-model-fa32a5b3-0079`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$H(S)$$

```latex
H(S)
```

> ( S , t ) ≥ H ( S ) {\displaystyle V(S,t)\geq H(S)} where … denotes the payoff at stock price S {\displaystyle S}

#### `fml-src-black-scholes-model-fa32a5b3-0080`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$V(S,T)=H(S)$$

```latex
V(S,T)=H(S)
```

> S {\displaystyle S} and the terminal condition: … . In general this inequality does not have a closed form solution, though an Ame

Related units: `u-src-black-scholes-model-fa32a5b3-0033`

#### `fml-src-black-scholes-model-fa32a5b3-0081`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$S-X$$

```latex
S-X
```

> onding to a trigger price. Here, if the underlying asset price is greater than or equal to the trigger price it is optimal to exercise, and the value must equal … , otherwise the option "boils down to: (i) a European up-and-out call option...

#### `fml-src-black-scholes-model-fa32a5b3-0082`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$T\rightarrow \infty$$

```latex
T\rightarrow \infty
```

> cal solution for American put options, it is possible to derive such a formula for the case of a perpetual option – meaning that the option never expires (i.e., … ). [ 34 ] In this case, the time decay of the option is equal to zero, which lea

#### `fml-src-black-scholes-model-fa32a5b3-0083`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$${1 \over {2}}\sigma ^{2}S^{2}{d^{2}V \over {dS^{2}}}+(r-q)S{dV \over {dS}}-rV=0$$

```latex
{1 \over {2}}\sigma ^{2}S^{2}{d^{2}V \over {dS^{2}}}+(r-q)S{dV \over {dS}}-rV=0
```

> ). [ 34 ] In this case, the time decay of the option is equal to zero, which leads to the Black–Scholes PDE becoming an ODE: … Let S −

Related units: `u-src-black-scholes-model-fa32a5b3-0035`

#### `fml-src-black-scholes-model-fa32a5b3-0084`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$S_{-}$$

```latex
S_{-}
```

> − r V = 0 {\displaystyle {1 \over {2}}\sigma ^{2}S^{2}{d^{2}V \over {dS^{2}}}+(r-q)S{dV \over {dS}}-rV=0} Let … denote the lower exercise boundary, below which it is optimal to exercise the op

#### `fml-src-black-scholes-model-fa32a5b3-0085`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$V(S_{-})=K-S_{-},\quad {dV \over {dS}}(S_{-})=-1,\quad V(S)\leq K$$

```latex
V(S_{-})=K-S_{-},\quad {dV \over {dS}}(S_{-})=-1,\quad V(S)\leq K
```

> − {\displaystyle S_{-}} denote the lower exercise boundary, below which it is optimal to exercise the option. The boundary conditions are: … The solutions to the ODE are a linear combination of any two linearly independen

#### `fml-src-black-scholes-model-fa32a5b3-0086`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$V(S)=A_{1}S^{\lambda _{1}}+A_{2}S^{\lambda _{2}}$$

```latex
V(S)=A_{1}S^{\lambda _{1}}+A_{2}S^{\lambda _{2}}
```

> V(S_{-})=K-S_{-},\quad {dV \over {dS}}(S_{-})=-1,\quad V(S)\leq K} The solutions to the ODE are a linear combination of any two linearly independent solutions: … For S − ≤

#### `fml-src-black-scholes-model-fa32a5b3-0087`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$S_{-}\leq S$$

```latex
S_{-}\leq S
```

> λ 2 {\displaystyle V(S)=A_{1}S^{\lambda _{1}}+A_{2}S^{\lambda _{2}}} For … , substitution of this solution into the ODE for i = 1 , 2

#### `fml-src-black-scholes-model-fa32a5b3-0088`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$i={1,2}$$

```latex
i={1,2}
```

> S − ≤ S {\displaystyle S_{-}\leq S} , substitution of this solution into the ODE for … yields:

#### `fml-src-black-scholes-model-fa32a5b3-0089`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$\left[{1 \over {2}}\sigma ^{2}\lambda _{i}(\lambda _{i}-1)+(r-q)\lambda _{i}-r\right]S^{\lambda _{i}}=0$$

```latex
\left[{1 \over {2}}\sigma ^{2}\lambda _{i}(\lambda _{i}-1)+(r-q)\lambda _{i}-r\right]S^{\lambda _{i}}=0
```

> i = 1 , 2 {\displaystyle i={1,2}} yields: … Rearranging the terms gives:

#### `fml-src-black-scholes-model-fa32a5b3-0090`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$${1 \over {2}}\sigma ^{2}\lambda _{i}^{2}+\left(r-q-{1 \over {2}}\sigma ^{2}\right)\lambda _{i}-r=0$$

```latex
{1 \over {2}}\sigma ^{2}\lambda _{i}^{2}+\left(r-q-{1 \over {2}}\sigma ^{2}\right)\lambda _{i}-r=0
```

> {\displaystyle \left[{1 \over {2}}\sigma ^{2}\lambda _{i}(\lambda _{i}-1)+(r-q)\lambda _{i}-r\right]S^{\lambda _{i}}=0} Rearranging the terms gives: … Using the quadratic formula , the solutions for

Related units: `u-src-black-scholes-model-fa32a5b3-0072`

#### `fml-src-black-scholes-model-fa32a5b3-0091`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$\lambda _{i}$$

```latex
\lambda _{i}
```

> displaystyle {1 \over {2}}\sigma ^{2}\lambda _{i}^{2}+\left(r-q-{1 \over {2}}\sigma ^{2}\right)\lambda _{i}-r=0} Using the quadratic formula , the solutions for … are:

#### `fml-src-black-scholes-model-fa32a5b3-0092`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$${\begin{aligned}\lambda _{1}&={-\left(r-q-{1 \over {2}}\sigma ^{2}\right)+{\sqrt {\left(r-q-{1 \over {2}}\sigma ^{2}\right)^{2}+2\sigma ^{2}r}} \over {\sigma ^{2}}}\\\lambda _{2}&={-\left(r-q-{1 \over {2}}\sigma ^{2}\right)-{\sqrt {\left(r-q-{1 \over {2}}\sigma ^{2}\right)^{2}+2\sigma ^{2}r}} \over {\sigma ^{2}}}\end{aligned}}$$

```latex
{\begin{aligned}\lambda _{1}&={-\left(r-q-{1 \over {2}}\sigma ^{2}\right)+{\sqrt {\left(r-q-{1 \over {2}}\sigma ^{2}\right)^{2}+2\sigma ^{2}r}} \over {\sigma ^{2}}}\\\lambda _{2}&={-\left(r-q-{1 \over {2}}\sigma ^{2}\right)-{\sqrt {\left(r-q-{1 \over {2}}\sigma ^{2}\right)^{2}+2\sigma ^{2}r}} \over {\sigma ^{2}}}\end{aligned}}
```

> are: … In order to have a finite solution for the perpetual put, since the boundary con

#### `fml-src-black-scholes-model-fa32a5b3-0093`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$A_{1}=0$$

```latex
A_{1}=0
```

> have a finite solution for the perpetual put, since the boundary conditions imply upper and lower finite bounds on the value of the put, it is necessary to set … , leading to the solution V ( S ) =

Related units: `u-src-black-scholes-model-fa32a5b3-0072`

#### `fml-src-black-scholes-model-fa32a5b3-0094`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$V(S)=A_{2}S^{\lambda _{2}}$$

```latex
V(S)=A_{2}S^{\lambda _{2}}
```

> A 1 = 0 {\displaystyle A_{1}=0} , leading to the solution … . From the first boundary condition, it is known that:

Related units: `u-src-black-scholes-model-fa32a5b3-0072`

#### `fml-src-black-scholes-model-fa32a5b3-0095`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$V(S_{-})=A_{2}(S_{-})^{\lambda _{2}}=K-S_{-}\implies A_{2}={K-S_{-} \over {(S_{-})^{\lambda _{2}}}}$$

```latex
V(S_{-})=A_{2}(S_{-})^{\lambda _{2}}=K-S_{-}\implies A_{2}={K-S_{-} \over {(S_{-})^{\lambda _{2}}}}
```

> {\displaystyle V(S)=A_{2}S^{\lambda _{2}}} . From the first boundary condition, it is known that: … Therefore, the value of the perpetual put becomes:

#### `fml-src-black-scholes-model-fa32a5b3-0096`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$V(S)=(K-S_{-})\left({S \over {S_{-}}}\right)^{\lambda _{2}}$$

```latex
V(S)=(K-S_{-})\left({S \over {S_{-}}}\right)^{\lambda _{2}}
```

> laystyle V(S_{-})=A_{2}(S_{-})^{\lambda _{2}}=K-S_{-}\implies A_{2}={K-S_{-} \over {(S_{-})^{\lambda _{2}}}}} Therefore, the value of the perpetual put becomes: … The second boundary condition yields the location of the lower exercise boundary

#### `fml-src-black-scholes-model-fa32a5b3-0097`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$${dV \over {dS}}(S_{-})=\lambda _{2}{K-S_{-} \over {S_{-}}}=-1\implies S_{-}={\lambda _{2}K \over {\lambda _{2}-1}}$$

```latex
{dV \over {dS}}(S_{-})=\lambda _{2}{K-S_{-} \over {S_{-}}}=-1\implies S_{-}={\lambda _{2}K \over {\lambda _{2}-1}}
```

> {\displaystyle V(S)=(K-S_{-})\left({S \over {S_{-}}}\right)^{\lambda _{2}}} The second boundary condition yields the location of the lower exercise boundary: … To conclude, for

Related units: `u-src-black-scholes-model-fa32a5b3-0036`

#### `fml-src-black-scholes-model-fa32a5b3-0098`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$${\textstyle S\geq S_{-}={\lambda _{2}K \over {\lambda _{2}-1}}}$$

```latex
{\textstyle S\geq S_{-}={\lambda _{2}K \over {\lambda _{2}-1}}}
```

> {\displaystyle {dV \over {dS}}(S_{-})=\lambda _{2}{K-S_{-} \over {S_{-}}}=-1\implies S_{-}={\lambda _{2}K \over {\lambda _{2}-1}}} To conclude, for … , the perpetual American put option is worth:

#### `fml-src-black-scholes-model-fa32a5b3-0099`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$V(S)={K \over {1-\lambda _{2}}}\left({\lambda _{2}-1 \over {\lambda _{2}}}\right)^{\lambda _{2}}\left({S \over {K}}\right)^{\lambda _{2}}$$

```latex
V(S)={K \over {1-\lambda _{2}}}\left({\lambda _{2}-1 \over {\lambda _{2}}}\right)^{\lambda _{2}}\left({S \over {K}}\right)^{\lambda _{2}}
```

> {\textstyle S\geq S_{-}={\lambda _{2}K \over {\lambda _{2}-1}}} , the perpetual American put option is worth: … Binary options By solving the Black–Scholes differential equation with the Heavi

Related units: `u-src-black-scholes-model-fa32a5b3-0036`

#### `fml-src-black-scholes-model-fa32a5b3-0100`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$C=e^{-r(T-t)}N(d_{2}).\,$$

```latex
C=e^{-r(T-t)}N(d_{2}).\,
```

> two terms in the Black–Scholes formula. Cash-or-nothing call This pays out one unit of cash if the spot is above the strike at maturity. Its value is given by: … Cash-or-nothing put This pays out one unit of cash if the spot is below the stri

Related units: `u-src-black-scholes-model-fa32a5b3-0037`

#### `fml-src-black-scholes-model-fa32a5b3-0101`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$P=e^{-r(T-t)}N(-d_{2}).\,$$

```latex
P=e^{-r(T-t)}N(-d_{2}).\,
```

> {\displaystyle C=e^{-r(T-t)}N(d_{2}).\,} Cash-or-nothing put This pays out one unit of cash if the spot is below the strike at maturity. Its value is given by: … Asset-or-nothing call This pays out one unit of asset if the spot is above the s

#### `fml-src-black-scholes-model-fa32a5b3-0102`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$C=Se^{-q(T-t)}N(d_{1}).\,$$

```latex
C=Se^{-q(T-t)}N(d_{1}).\,
```

> isplaystyle P=e^{-r(T-t)}N(-d_{2}).\,} Asset-or-nothing call This pays out one unit of asset if the spot is above the strike at maturity. Its value is given by: … Asset-or-nothing put This pays out one unit of asset if the spot is below the st

Related units: `u-src-black-scholes-model-fa32a5b3-0037`

#### `fml-src-black-scholes-model-fa32a5b3-0103`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$P=Se^{-q(T-t)}N(-d_{1}),$$

```latex
P=Se^{-q(T-t)}N(-d_{1}),
```

> displaystyle C=Se^{-q(T-t)}N(d_{1}).\,} Asset-or-nothing put This pays out one unit of asset if the spot is below the strike at maturity. Its value is given by: … Foreign Exchange (FX)

#### `fml-src-black-scholes-model-fa32a5b3-0104`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$r_{f}$$

```latex
r_{f}
```

> unit of the foreign currency if the spot at maturity is above or below the strike is exactly like an asset-or nothing call and put respectively. Hence by taking … , the foreign interest rate, r d

#### `fml-src-black-scholes-model-fa32a5b3-0105`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$r_{d}$$

```latex
r_{d}
```

> r f {\displaystyle r_{f}} , the foreign interest rate, … , the domestic interest rate, and the rest as above, the following results can b

#### `fml-src-black-scholes-model-fa32a5b3-0106`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$C=e^{-r_{d}T}N(d_{2})\,$$

```latex
C=e^{-r_{d}T}N(d_{2})\,
```

> lowing results can be obtained: In the case of a digital call (this is a call FOR/put DOM) paying out one unit of the domestic currency gotten as present value: … In the case of a digital put (this is a put FOR/call DOM) paying out one unit of

Related units: `u-src-black-scholes-model-fa32a5b3-0042`

#### `fml-src-black-scholes-model-fa32a5b3-0107`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$P=e^{-r_{d}T}N(-d_{2})\,$$

```latex
P=e^{-r_{d}T}N(-d_{2})\,
```

> aystyle C=e^{-r_{d}T}N(d_{2})\,} In the case of a digital put (this is a put FOR/call DOM) paying out one unit of the domestic currency gotten as present value: … In the case of a digital call (this is a call FOR/put DOM) paying out one unit o

#### `fml-src-black-scholes-model-fa32a5b3-0108`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$C=Se^{-r_{f}T}N(d_{1})\,$$

```latex
C=Se^{-r_{f}T}N(d_{1})\,
```

> ystyle P=e^{-r_{d}T}N(-d_{2})\,} In the case of a digital call (this is a call FOR/put DOM) paying out one unit of the foreign currency gotten as present value: … In the case of a digital put (this is a put FOR/call DOM) paying out one unit of

Related units: `u-src-black-scholes-model-fa32a5b3-0042`

#### `fml-src-black-scholes-model-fa32a5b3-0109`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$P=Se^{-r_{f}T}N(-d_{1})\,$$

```latex
P=Se^{-r_{f}T}N(-d_{1})\,
```

> aystyle C=Se^{-r_{f}T}N(d_{1})\,} In the case of a digital put (this is a put FOR/call DOM) paying out one unit of the foreign currency gotten as present value: … Skew In the standard Black–Scholes model, one can interpret the premium of the b

#### `fml-src-black-scholes-model-fa32a5b3-0110`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$\sigma$$

```latex
\sigma
```

> the skewness of the distribution of the asset. Market makers adjust for such skewness by, instead of using a single standard deviation for the underlying asset … across all strikes, incorporating a variable one σ ( K )

#### `fml-src-black-scholes-model-fa32a5b3-0111`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$\sigma (K)$$

```latex
\sigma (K)
```

> σ {\displaystyle \sigma } across all strikes, incorporating a variable one … where volatility depends on strike price, thus incorporating the volatility skew

#### `fml-src-black-scholes-model-fa32a5b3-0112`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$C_{v}$$

```latex
C_{v}
```

> t call spread using two vanilla options. One can model the value of a binary cash-or-nothing option, C , at strike K , as an infinitesimally tight spread, where … is a vanilla European call: [ 36 ]

#### `fml-src-black-scholes-model-fa32a5b3-0113`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$C=\lim _{\epsilon \to 0}{\frac {C_{v}(K-\epsilon )-C_{v}(K)}{\epsilon }}$$

```latex
C=\lim _{\epsilon \to 0}{\frac {C_{v}(K-\epsilon )-C_{v}(K)}{\epsilon }}
```

> [ 36 ] [ 37 ] … Thus, the value of a binary call is the negative of the derivative of the price

Related units: `u-src-black-scholes-model-fa32a5b3-0038`

#### `fml-src-black-scholes-model-fa32a5b3-0114`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$C=-{\frac {dC_{v}}{dK}}$$

```latex
C=-{\frac {dC_{v}}{dK}}
```

> on )-C_{v}(K)}{\epsilon }}} Thus, the value of a binary call is the negative of the derivative of the price of a vanilla call with respect to strike price: … When one takes volatility skew into account, σ {\displaystyle \sigma }

Related units: `u-src-black-scholes-model-fa32a5b3-0038`

#### `fml-src-black-scholes-model-fa32a5b3-0115`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$C=-{\frac {dC_{v}(K,\sigma (K))}{dK}}=-{\frac {\partial C_{v}}{\partial K}}-{\frac {\partial C_{v}}{\partial \sigma }}{\frac {\partial \sigma }{\partial K}}$$

```latex
C=-{\frac {dC_{v}(K,\sigma (K))}{dK}}=-{\frac {\partial C_{v}}{\partial K}}-{\frac {\partial C_{v}}{\partial \sigma }}{\frac {\partial \sigma }{\partial K}}
```

> K {\displaystyle K} : … The first term is equal to the premium of the binary option ignoring skew:

#### `fml-src-black-scholes-model-fa32a5b3-0116`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$$-{\frac {\partial C_{v}}{\partial K}}=-{\frac {\partial (SN(d_{1})-Ke^{-r(T-t)}N(d_{2}))}{\partial K}}=e^{-r(T-t)}N(d_{2})=C_{\text{no skew}}$$

```latex
-{\frac {\partial C_{v}}{\partial K}}=-{\frac {\partial (SN(d_{1})-Ke^{-r(T-t)}N(d_{2}))}{\partial K}}=e^{-r(T-t)}N(d_{2})=C_{\text{no skew}}
```

> -{\frac {\partial C_{v}}{\partial \sigma }}{\frac {\partial \sigma }{\partial K}}}"/> The first term is equal to the premium of the binary option ignoring skew: …

#### `fml-src-black-scholes-model-fa32a5b3-0117`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$${\frac {\partial C_{v}}{\partial \sigma }}$$

```latex
{\frac {\partial C_{v}}{\partial \sigma }}
```

> {\displaystyle -{\frac {\partial C_{v}}{\partial K}}=-{\frac {\partial (SN(d_{1})-Ke^{-r(T-t)}N(d_{2}))}{\partial K}}=e^{-r(T-t)}N(d_{2})=C_{\text{no skew}}} … is the Vega of the vanilla call;

#### `fml-src-black-scholes-model-fa32a5b3-0118`

formula · **exact** · extractor `html_mathml_v1` · not cited by any unit

$${\frac {\partial \sigma }{\partial K}}$$

```latex
{\frac {\partial \sigma }{\partial K}}
```

> {\displaystyle {\frac {\partial C_{v}}{\partial \sigma }}} is the Vega of the vanilla call; … is sometimes called the "skew slope" or just "skew". If the skew is typically ne

#### `fml-src-black-scholes-model-fa32a5b3-0119`

formula · **exact** · extractor `html_mathml_v1` · cited by 1 unit

$$C=C_{\text{no skew}}-{\text{Vega}}_{v}\cdot {\text{Skew}}$$

```latex
C=C_{\text{no skew}}-{\text{Vega}}_{v}\cdot {\text{Skew}}
```

> is sometimes called the "skew slope" or just "skew". If the skew is typically negative, the value of a binary call will be higher when taking skew into account. … Relationship to vanilla options' Greeks Since a binary call is a mathematical de

Related units: `u-src-black-scholes-model-fa32a5b3-0039`

## Assets in text nobody read

119 asset(s) sit in a region of the source from which no unit was extracted, so nothing in the output points at them. This is a hole in the reading rather than a judgment about evidence: no unit was dropped here, none was ever made. They are shown because they are still the source's content.

### `tbl-src-black-scholes-model-fa32a5b3-0001`

table · **exact** · anchored by `none`

|   |   | Call | Put |
|---|---|---|---|
| Delta | ∂ V ∂ S {\displaystyle {\frac {\partial V}{\partial S}}} | N ( d + ) {\displaystyle N(d_{+})\,} | − N ( − d + ) = N ( d + ) − 1 {\displaystyle -N(-d_{+})=N(d_{+})-1\,} |
| Gamma | ∂ 2 V ∂ S 2 {\displaystyle {\frac {\partial ^{2}V}{\partial S^{2}}}} | N ′ ( d + ) S σ T − t {\displaystyle {\frac {N'(d_{+})}{S\sigma {\sqrt {T-t}}}}\,} |   |
| Vega | ∂ V ∂ σ {\displaystyle {\frac {\partial V}{\partial \sigma }}} | S N ′ ( d + ) T − t {\displaystyle SN'(d_{+}){\sqrt {T-t}}\,} |   |
| Theta | ∂ V ∂ t {\displaystyle {\frac {\partial V}{\partial t}}} | − S N ′ ( d + ) σ 2 T − t − r K e − r ( T − t ) N ( d − ) {\displaystyle -{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}-rKe^{-r(T-t)}N(d_{-})\,} | − S N ′ ( d + ) σ 2 T − t + r K e − r ( T − t ) N ( − d − ) {\displaystyle -{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}+rKe^{-r(T-t)}N(-d_{-})\,} |
| Rho | ∂ V ∂ r {\displaystyle {\frac {\partial V}{\partial r}}} | K ( T − t ) e − r ( T − t ) N ( d − ) {\displaystyle K(T-t)e^{-r(T-t)}N(d_{-})\,} | − K ( T − t ) e − r ( T − t ) N ( − d − ) {\displaystyle -K(T-t)e^{-r(T-t)}N(-d_{-})\,} |

### `tbl-src-black-scholes-model-fa32a5b3-0002`

table · **exact** · anchored by `none`

| Terms | Delta neutral Exercise Expiration Moneyness Open interest Pin risk Risk-free interest rate Strike price Synthetic position the Greeks Volatility |
|---|---|
| Vanillas | American Bond option Call Employee stock option European Fixed income FX Option styles Put Warrants |
| Exotics | Asian Barrier Basket Binary Callable bull/bear contract Chooser Cliquet Compound Forward start Interest rate Lookback Mountain range Rainbow Spread Swaption |
| Strategies | Backspread Box spread Butterfly Calendar spread Collar Condor Covered option Credit spread Debit spread Diagonal spread Fence Intermarket spread Iron butterfly Iron condor Jelly roll Ladder Naked option Straddle Strangle Protective option Ratio spread Risk reversal Vertical spread (Bear, Bull) |
| Valuation | Valuation methods Continuous-time stochastic processes: • Arithmetic diffusion: Bachelier • Geometric diffusion: Black, Black–Scholes, Garman–Kohlhagen, Margrabe • Stochastic volatility: Heston • Jump processes: Jump diffusion • Multi-curve framework Multi-curve framework Discrete-time processes: • Binomial, Trinomial, Lattices Numerical methods: • Finite difference, MC Simulation, Real options Model-free:• Put–call parity, Vanna–Volga |

### `tbl-src-black-scholes-model-fa32a5b3-0003`

table · **exact** · anchored by `none`

| vteDerivatives market |   |
|---|---|
| Derivative (finance) * List of futures exchanges |   |
| Options |   |
| Swaps | Amortising Asset Basis Commodity Conditional variance Constant maturity Correlation Credit default Currency Dividend Equity Forex Forward Rate Agreement Inflation Interest rate Overnight indexed Total return Variance Volatility Year-on-year inflation-indexed Zero Coupon Zero-coupon inflation-indexed |
| ForwardsFutures | Contango Spot contract Backwardation Commodities future Currency future Dividend future Forward market Forward price Forwards pricing Forward rate Futures pricing Interest rate future Margin Perpetual futures Single-stock futures Slippage Stock market index future |
| Exotic derivatives | Energy derivative Freight derivative Inflation derivative Property derivative Weather derivative |
| Other derivatives | Collateralized debt obligation (CDO) Constant proportion portfolio insurance Contract for difference Credit-linked note (CLN) Credit default option Credit derivative Equity-linked note (ELN) Equity derivative Foreign exchange derivative Fund derivative Fund of funds Interest rate derivative Mortgage-backed security Power reverse dual-currency note (PRDC) |
| Market issues | Consumer debt Corporate debt Government debt Great Recession Municipal debt Tax policy |
| Business portal |   |

### `tbl-src-black-scholes-model-fa32a5b3-0004`

table · **exact** · anchored by `none`

| Arbitrage /relative value | Capital structure arbitrage Convertible arbitrage Equity market neutral Fixed income arbitrage / fixed-income relative-value investing (Treasury basis trade) Convergence trade Statistical arbitrage Volatility arbitrage |
|---|---|
| Event-driven | Shareholder activism Distressed securities Risk arbitrage Special situation |
| Directional | Commodity trading advisors / managed futures account Trend following Global macro Long/short equity Dedicated short |
| Other | Fund of hedge funds / Multi-manager |

### `tbl-src-black-scholes-model-fa32a5b3-0005`

table · **exact** · anchored by `none`

| Markets | Commodities Derivatives Equity Fixed income Foreign exchange Money markets Structured securities |
|---|---|
| Misc | Absolute return Arbitrage pricing theory Assets under management Black–Scholes model (Greeks: delta neutral) Capital asset pricing model (alpha / beta / security characteristic line) Fundamental analysis Hedge Securitization Short Taxation of private equity and hedge funds Technical analysis |

### `tbl-src-black-scholes-model-fa32a5b3-0006`

table · **exact** · anchored by `none`

| vteHedge funds |   |
|---|---|
| Investmentstrategy |   |
| Trading | Algorithmic trading Day trading High-frequency trading (List of electronic trading protocols) Prime brokerage Program trading Proprietary trading |
| Relatedterms |   |
| Investors | Vulture funds Family offices Financial endowments Fund of hedge funds High-net-worth individual Institutional investors Insurance companies Investment banks Merchant banks Pension funds Sovereign wealth funds |
| Governance | Fund governance Standards Board for Alternative Investments Managed Funds Association |
| Alternative investment management companies Hedge funds Hedge fund managers List of hedge funds |   |

### `tbl-src-black-scholes-model-fa32a5b3-0007`

table · **exact** · anchored by `none`

| vteStochastic processes |   |
|---|---|
| Discrete time | Bernoulli process Branching process Chinese restaurant process Galton–Watson process Independent and identically distributed random variables Markov chain Moran process Random walk Loop-erased Self-avoiding Biased Maximal entropy |
| Continuous time | Additive process Airy process Bessel process Birth–death process pure birth Brownian motion Bridge Dyson Excursion Fractional Geometric Meander Cauchy process Contact process Continuous-time random walk Cox process Diffusion process Empirical process Feller process Fleming–Viot process Gamma process Geometric process Hawkes process Hunt process Interacting particle systems Itô diffusion Itô process Jump diffusion Jump process Lévy process Local time Markov additive process McKean–Vlasov process Ornstein–Uhlenbeck process Poisson process Compound Non-homogeneous Quasimartingale Schramm–Loewner evolution Semimartingale Sigma-martingale Stable process Superprocess Telegraph process Variance gamma process Wiener process Wiener sausage |
| Both | Branching process Gaussian process Hidden Markov model (HMM) Markov process Martingale Differences Local Sub- Super- Random dynamical system Regenerative process Renewal process Stochastic chains with memory of variable length White noise |
| Fields and other | Dirichlet process Gaussian random field Gibbs measure Hopfield model Ising model Potts model Boolean network Markov random field Percolation Pitman–Yor process Point process Cox Determinantal Poisson Random field Random graph |
| Time series models | Autoregressive conditional heteroskedasticity (ARCH) model Autoregressive integrated moving average (ARIMA) model Autoregressive (AR) model Autoregressive moving-average (ARMA) model Generalized autoregressive conditional heteroskedasticity (GARCH) model Moving-average (MA) model |
| Financial models | Binomial options pricing model Black–Derman–Toy Black–Karasinski Black–Scholes Chan–Karolyi–Longstaff–Sanders (CKLS) Chen Constant elasticity of variance (CEV) Cox–Ingersoll–Ross (CIR) Garman–Kohlhagen Heath–Jarrow–Morton (HJM) Heston Ho–Lee Hull–White Korn-Kreer-Lenssen LIBOR market Rendleman–Bartter SABR volatility Vašíček Wilkie |
| Actuarial models | Bühlmann Cramér–Lundberg Risk process Sparre–Anderson |
| Queueing models | Bulk Fluid Generalized queueing network M/G/1 M/M/1 M/M/c |
| Properties | Càdlàg paths Continuous Continuous paths Ergodic Exchangeable Feller-continuous Gauss–Markov Markov Mixing Piecewise-deterministic Predictable Progressively measurable Self-similar Stationary Time-reversible |
| Limit theorems | Central limit theorem Donsker's theorem Doob's martingale convergence theorems Ergodic theorem Fisher–Tippett–Gnedenko theorem Large deviation principle Law of large numbers (weak/strong) Law of the iterated logarithm Maximal ergodic theorem Sanov's theorem Zero–one laws (Blumenthal, Borel–Cantelli, Engelbert–Schmidt, Hewitt–Savage, Kolmogorov, Lévy) |
| Inequalities | Burkholder–Davis–Gundy Doob's martingale Doob's upcrossing Kunita–Watanabe Marcinkiewicz–Zygmund |

*(3 further rows in the stored grid.)*

### `fml-src-black-scholes-model-fa32a5b3-0008`

formula · **exact** · anchored by `none`

$$C(S,t)$$

```latex
C(S,t)
```

> d ] and dividend payout. [ 19 ] Notation At time t, in particular: … is the price of a European call option and P ( S , t )

### `fml-src-black-scholes-model-fa32a5b3-0009`

formula · **exact** · anchored by `none`

$$P(S,t)$$

```latex
P(S,t)
```

> C ( S , t ) {\displaystyle C(S,t)} is the price of a European call option and … is the price of a European put option. T {\displaystyle T}

### `fml-src-black-scholes-model-fa32a5b3-0010`

formula · **exact** · anchored by `none`

$$\tau$$

```latex
\tau
```

> T {\displaystyle T} is the time of option expiration. … is the time until maturity: τ = T − t {\

### `fml-src-black-scholes-model-fa32a5b3-0011`

formula · **exact** · anchored by `none`

$$\tau =T-t$$

```latex
\tau =T-t
```

> τ {\displaystyle \tau } is the time until maturity: … . K {\displaystyle K}

### `fml-src-black-scholes-model-fa32a5b3-0012`

formula · **exact** · anchored by `none`

$$N(x)$$

```latex
N(x)
```

> K {\displaystyle K} is the strike price of the option, also known as the exercise price. … denotes the standard normal cumulative distribution function :

### `fml-src-black-scholes-model-fa32a5b3-0013`

formula · **exact** · anchored by `none`

$$N(x)={\frac {1}{\sqrt {2\pi }}}\int _{-\infty }^{x}e^{-z^{2}/2}\,dz.$$

```latex
N(x)={\frac {1}{\sqrt {2\pi }}}\int _{-\infty }^{x}e^{-z^{2}/2}\,dz.
```

> denotes the standard normal cumulative distribution function : … N ′ ( x

### `fml-src-black-scholes-model-fa32a5b3-0014`

formula · **exact** · anchored by `none`

$$N'(x)$$

```latex
N'(x)
```

> d z . {\displaystyle N(x)={\frac {1}{\sqrt {2\pi }}}\int _{-\infty }^{x}e^{-z^{2}/2}\,dz.} … denotes the standard normal probability density function :

### `fml-src-black-scholes-model-fa32a5b3-0015`

formula · **exact** · anchored by `none`

$$N'(x)={\frac {dN(x)}{dx}}={\frac {1}{\sqrt {2\pi }}}e^{-x^{2}/2}.$$

```latex
N'(x)={\frac {dN(x)}{dx}}={\frac {1}{\sqrt {2\pi }}}e^{-x^{2}/2}.
```

> ) {\displaystyle N'(x)} denotes the standard normal probability density function : … Black–Scholes equation

### `fml-src-black-scholes-model-fa32a5b3-0016`

formula · **exact** · anchored by `none`

$$V(S,t)$$

```latex
V(S,t)
```

> ted geometric Brownian motions with parameters from market data The Black–Scholes equation is a parabolic partial differential equation that describes the price … of the option, where S {\displaystyle S}

### `fml-src-black-scholes-model-fa32a5b3-0017`

formula · **exact** · anchored by `none`

$${\frac {\partial V}{\partial t}}+{\frac {1}{2}}\sigma ^{2}S^{2}{\frac {\partial ^{2}V}{\partial S^{2}}}+rS{\frac {\partial V}{\partial S}}-rV=0$$

```latex
{\frac {\partial V}{\partial t}}+{\frac {1}{2}}\sigma ^{2}S^{2}{\frac {\partial ^{2}V}{\partial S^{2}}}+rS{\frac {\partial V}{\partial S}}-rV=0
```

> t {\displaystyle t} is time: … A key financial insight behind the equation is that one can perfectly hedge the

### `fml-src-black-scholes-model-fa32a5b3-0018`

formula · **exact** · anchored by `none`

$${\begin{aligned}C(0,t)&=0{\text{ for all }}t\\C(S,t)&\sim S-Ke^{-r(T-t)}{\text{ as }}S\rightarrow \infty \\C(S,T)&=\max\{S-K,0\}\end{aligned}}$$

```latex
{\begin{aligned}C(0,t)&=0{\text{ for all }}t\\C(S,t)&\sim S-Ke^{-r(T-t)}{\text{ as }}S\rightarrow \infty \\C(S,T)&=\max\{S-K,0\}\end{aligned}}
```

> boundary conditions : [ 20 ] … The value of a call option for a non-dividend-paying underlying stock in terms o

### `fml-src-black-scholes-model-fa32a5b3-0019`

formula · **exact** · anchored by `none`

$${\begin{aligned}C(S_{t},t)&=N(d_{+})S_{t}-N(d_{-})Ke^{-r(T-t)}\\d_{+}&={\frac {1}{\sigma {\sqrt {T-t}}}}\left[\ln \left({\frac {S_{t}}{K}}\right)+\left(r+{\frac {\sigma ^{2}}{2}}\right)(T-t)\right]\\d_{-}&=d_{+}-\sigma {\sqrt {T-t}}\\\end{aligned}}$$

```latex
{\begin{aligned}C(S_{t},t)&=N(d_{+})S_{t}-N(d_{-})Ke^{-r(T-t)}\\d_{+}&={\frac {1}{\sigma {\sqrt {T-t}}}}\left[\ln \left({\frac {S_{t}}{K}}\right)+\left(r+{\frac {\sigma ^{2}}{2}}\right)(T-t)\right]\\d_{-}&=d_{+}-\sigma {\sqrt {T-t}}\\\end{aligned}}
```

> fty \\C(S,T)&=\max\{S-K,0\}\end{aligned}}}"/> The value of a call option for a non-dividend-paying underlying stock in terms of the Black–Scholes parameters is: … The price of a corresponding put option based on put–call parity with discount f

### `fml-src-black-scholes-model-fa32a5b3-0020`

formula · **exact** · anchored by `none`

$$e^{-r(T-t)}$$

```latex
e^{-r(T-t)}
```

> \right)(T-t)\right]\\d_{-}&=d_{+}-\sigma {\sqrt {T-t}}\\\end{aligned}}}"/> The price of a corresponding put option based on put–call parity with discount factor … is:

### `fml-src-black-scholes-model-fa32a5b3-0021`

formula · **exact** · anchored by `none`

$${\begin{aligned}P(S_{t},t)&=Ke^{-r(T-t)}-S_{t}+C(S_{t},t)\\&=N(-d_{-})Ke^{-r(T-t)}-N(-d_{+})S_{t}\end{aligned}}\,$$

```latex
{\begin{aligned}P(S_{t},t)&=Ke^{-r(T-t)}-S_{t}+C(S_{t},t)\\&=N(-d_{-})Ke^{-r(T-t)}-N(-d_{+})S_{t}\end{aligned}}\,
```

> t ) {\displaystyle e^{-r(T-t)}} is: … Alternative formulation Introducing auxiliary variables allows for the formula t

### `fml-src-black-scholes-model-fa32a5b3-0022`

formula · **exact** · anchored by `none`

$${\begin{aligned}C(F,\tau )&=D\left[N(d_{+})F-N(d_{-})K\right]\\d_{+}&={\frac {1}{\sigma {\sqrt {\tau }}}}\left[\ln \left({\frac {F}{K}}\right)+{\frac {1}{2}}\sigma ^{2}\tau \right]\\d_{-}&=d_{+}-\sigma {\sqrt {\tau }}\end{aligned}}$$

```latex
{\begin{aligned}C(F,\tau )&=D\left[N(d_{+})F-N(d_{-})K\right]\\d_{+}&={\frac {1}{\sigma {\sqrt {\tau }}}}\left[\ln \left({\frac {F}{K}}\right)+{\frac {1}{2}}\sigma ^{2}\tau \right]\\d_{-}&=d_{+}-\sigma {\sqrt {\tau }}\end{aligned}}
```

> ary variables allows for the formula to be simplified and reformulated in a form that can be more convenient (this is a special case of the Black '76 formula ): … where:

### `fml-src-black-scholes-model-fa32a5b3-0023`

formula · **exact** · anchored by `none`

$$D=e^{-r\tau }$$

```latex
D=e^{-r\tau }
```

> &=d_{+}-\sigma {\sqrt {\tau }}\end{aligned}}} where: … is the discount factor F = e

### `fml-src-black-scholes-model-fa32a5b3-0024`

formula · **exact** · anchored by `none`

$$F=e^{r\tau }S={\frac {S}{D}}$$

```latex
F=e^{r\tau }S={\frac {S}{D}}
```

> e − r τ {\displaystyle D=e^{-r\tau }} is the discount factor … is the forward price of the underlying asset, and S = D F

### `fml-src-black-scholes-model-fa32a5b3-0025`

formula · **exact** · anchored by `none`

$$S=DF$$

```latex
S=DF
```

> S D {\displaystyle F=e^{r\tau }S={\frac {S}{D}}} is the forward price of the underlying asset, and … Given put–call parity, which is expressed in these terms as: C − P =

### `fml-src-black-scholes-model-fa32a5b3-0026`

formula · **exact** · anchored by `none`

$$C-P=D(F-K)=S-DK$$

```latex
C-P=D(F-K)=S-DK
```

> S = D F {\displaystyle S=DF} Given put–call parity, which is expressed in these terms as: … the price of a put option is: P

### `fml-src-black-scholes-model-fa32a5b3-0027`

formula · **exact** · anchored by `none`

$$P(F,\tau )=D\left[N(-d_{-})K-N(-d_{+})F\right]$$

```latex
P(F,\tau )=D\left[N(-d_{-})K-N(-d_{+})F\right]
```

> ) = S − D K {\displaystyle C-P=D(F-K)=S-DK} the price of a put option is: … Interpretation It is possible to have intuitive interpretations of the Black–Sch

### `fml-src-black-scholes-model-fa32a5b3-0028`

formula · **exact** · anchored by `none`

$$d_{\pm }$$

```latex
d_{\pm }
```

> d_{+})F\right]} Interpretation It is possible to have intuitive interpretations of the Black–Scholes formula, with the main subtlety being the interpretation of … and why there are two different terms. [ 21 ] The formula can be interpreted by

### `fml-src-black-scholes-model-fa32a5b3-0029`

formula · **exact** · anchored by `none`

$$C=D\left[N(d_{+})F-N(d_{-})K\right]$$

```latex
C=D\left[N(d_{+})F-N(d_{-})K\right]
```

> o the values of the binary call options. These binary options are less frequently traded than vanilla call options, but are easier to analyze. Thus the formula: … breaks up as: C = D N

### `fml-src-black-scholes-model-fa32a5b3-0030`

formula · **exact** · anchored by `none`

$$C=DN(d_{+})F-DN(d_{-})K,$$

```latex
C=DN(d_{+})F-DN(d_{-})K,
```

> ) K ] {\displaystyle C=D\left[N(d_{+})F-N(d_{-})K\right]} breaks up as: … where D N ( d +

### `fml-src-black-scholes-model-fa32a5b3-0031`

formula · **exact** · anchored by `none`

$$DN(d_{+})F$$

```latex
DN(d_{+})F
```

> d − ) K , {\displaystyle C=DN(d_{+})F-DN(d_{-})K,} where … is the present value of an asset-or-nothing call and D N ( d

### `fml-src-black-scholes-model-fa32a5b3-0032`

formula · **exact** · anchored by `none`

$$DN(d_{-})K$$

```latex
DN(d_{-})K
```

> ( d + ) F {\displaystyle DN(d_{+})F} is the present value of an asset-or-nothing call and … is the present value of a cash-or-nothing call. The D factor is for discounting,

### `fml-src-black-scholes-model-fa32a5b3-0033`

formula · **exact** · anchored by `none`

$$N(d_{+})~F$$

```latex
N(d_{+})~F
```

> g call. The D factor is for discounting, because the expiration date is in future, and removing it changes present value to future value (value at expiry). Thus … is the future value of an asset-or-nothing call and N ( d −

### `fml-src-black-scholes-model-fa32a5b3-0034`

formula · **exact** · anchored by `none`

$$N(d_{-})~K$$

```latex
N(d_{-})~K
```

> d + ) F {\displaystyle N(d_{+})~F} is the future value of an asset-or-nothing call and … is the future value of a cash-or-nothing call. In risk-neutral terms, these are

### `fml-src-black-scholes-model-fa32a5b3-0035`

formula · **exact** · anchored by `none`

$$N(d_{+})F$$

```latex
N(d_{+})F
```

> pected value of the asset and the expected value of the cash in the risk-neutral measure. A naive, and slightly incorrect, interpretation of these terms is that … is the probability of the option expiring in the money N ( d +

### `fml-src-black-scholes-model-fa32a5b3-0036`

formula · **exact** · anchored by `none`

$$N(d_{+})$$

```latex
N(d_{+})
```

> ( d + ) F {\displaystyle N(d_{+})F} is the probability of the option expiring in the money … , multiplied by the value of the underlying at expiry F, while N ( d

### `fml-src-black-scholes-model-fa32a5b3-0037`

formula · **exact** · anchored by `none`

$$N(d_{-})K$$

```latex
N(d_{-})K
```

> ( d + ) {\displaystyle N(d_{+})} , multiplied by the value of the underlying at expiry F, while … is the probability of the option expiring in the money N ( d −

### `fml-src-black-scholes-model-fa32a5b3-0038`

formula · **exact** · anchored by `none`

$$N(d_{-}),$$

```latex
N(d_{-}),
```

> ( d − ) K {\displaystyle N(d_{-})K} is the probability of the option expiring in the money … multiplied by the value of the cash at expiry K. This interpretation is incorrec

### `fml-src-black-scholes-model-fa32a5b3-0039`

formula · **exact** · anchored by `none`

$$N(d_{-})$$

```latex
N(d_{-})
```

> N ( d + ) {\displaystyle N(d_{+})} and … are not equal. In fact, d ±

### `fml-src-black-scholes-model-fa32a5b3-0040`

formula · **exact** · anchored by `none`

$$N(d_{\pm })$$

```latex
N(d_{\pm })
```

> d ± {\displaystyle d_{\pm }} can be interpreted as measures of moneyness (in standard deviations) and … as probabilities of expiring ITM ( percent moneyness ), in the respective numéra

### `fml-src-black-scholes-model-fa32a5b3-0041`

formula · **exact** · anchored by `none`

$${\textstyle {\frac {1}{2}}\sigma ^{2}}$$

```latex
{\textstyle {\frac {1}{2}}\sigma ^{2}}
```

> d ± {\displaystyle d_{\pm }} instead of the … term there is ( r ±

### `fml-src-black-scholes-model-fa32a5b3-0042`

formula · **exact** · anchored by `none`

$${\textstyle \left(r\pm {\frac {1}{2}}\sigma ^{2}\right)\tau ,}$$

```latex
{\textstyle \left(r\pm {\frac {1}{2}}\sigma ^{2}\right)\tau ,}
```

> σ 2 {\textstyle {\frac {1}{2}}\sigma ^{2}} term there is … which can be interpreted as a drift factor (in the risk-neutral measure for appr

### `fml-src-black-scholes-model-fa32a5b3-0043`

formula · **exact** · anchored by `none`

$${\textstyle m={\frac {1}{\sigma {\sqrt {\tau }}}}\ln \left({\frac {F}{K}}\right)}$$

```latex
{\textstyle m={\frac {1}{\sigma {\sqrt {\tau }}}}\ln \left({\frac {F}{K}}\right)}
```

> an be interpreted as a drift factor (in the risk-neutral measure for appropriate numéraire). The use of d − for moneyness rather than the standardized moneyness … – in other words, the reason for the

### `fml-src-black-scholes-model-fa32a5b3-0044`

formula · **exact** · anchored by `none`

$$N(d_{+}),N(d_{-})$$

```latex
N(d_{+}),N(d_{-})
```

> [ 21 ] : 6 In detail, the terms … are the probabilities of the option expiring in-the-money under the equivalent e

### `fml-src-black-scholes-model-fa32a5b3-0045`

formula · **exact** · anchored by `none`

$$S_{T}\in (0,\infty )$$

```latex
S_{T}\in (0,\infty )
```

> ck) and the equivalent martingale probability measure (numéraire=risk free asset), respectively. [ 21 ] The risk neutral probability density for the stock price … is p (

### `fml-src-black-scholes-model-fa32a5b3-0046`

formula · **exact** · anchored by `none`

$$p(S,T)={\frac {N^{\prime }[d_{-}(S_{T})]}{S_{T}\sigma {\sqrt {T}}}}$$

```latex
p(S,T)={\frac {N^{\prime }[d_{-}(S_{T})]}{S_{T}\sigma {\sqrt {T}}}}
```

> ( 0 , ∞ ) {\displaystyle S_{T}\in (0,\infty )} is … where d −

### `fml-src-black-scholes-model-fa32a5b3-0047`

formula · **exact** · anchored by `none`

$$d_{-}=d_{-}(K)$$

```latex
d_{-}=d_{-}(K)
```

> {\displaystyle p(S,T)={\frac {N^{\prime }[d_{-}(S_{T})]}{S_{T}\sigma {\sqrt {T}}}}} where … is defined as above. Specifically, N ( d −

### `fml-src-black-scholes-model-fa32a5b3-0048`

formula · **exact** · anchored by `none`

$$SN(d_{+})$$

```latex
SN(d_{+})
```

> ( d + ) {\displaystyle N(d_{+})} , however, does not lend itself to a simple probability interpretation. … is correctly interpreted as the present value, using the risk-free interest rate

### `fml-src-black-scholes-model-fa32a5b3-0049`

formula · **exact** · anchored by `none`

$${\frac {\partial V}{\partial S}}$$

```latex
{\frac {\partial V}{\partial S}}
```

> ice movements. The Greeks for Black–Scholes are given in closed form below. They can be obtained by differentiation of the Black–Scholes formula. Call Put Delta … N ( d +

### `fml-src-black-scholes-model-fa32a5b3-0050`

formula · **exact** · anchored by `none`

$$N(d_{+})\,$$

```latex
N(d_{+})\,
```

> V ∂ S {\displaystyle {\frac {\partial V}{\partial S}}} … − N ( − d

### `fml-src-black-scholes-model-fa32a5b3-0051`

formula · **exact** · anchored by `none`

$$-N(-d_{+})=N(d_{+})-1\,$$

```latex
-N(-d_{+})=N(d_{+})-1\,
```

> ( d + ) {\displaystyle N(d_{+})\,} … Gamma

### `fml-src-black-scholes-model-fa32a5b3-0052`

formula · **exact** · anchored by `none`

$${\frac {\partial ^{2}V}{\partial S^{2}}}$$

```latex
{\frac {\partial ^{2}V}{\partial S^{2}}}
```

> ) − 1 {\displaystyle -N(-d_{+})=N(d_{+})-1\,} Gamma …

### `fml-src-black-scholes-model-fa32a5b3-0053`

formula · **exact** · anchored by `none`

$${\frac {N'(d_{+})}{S\sigma {\sqrt {T-t}}}}\,$$

```latex
{\frac {N'(d_{+})}{S\sigma {\sqrt {T-t}}}}\,
```

> 2 {\displaystyle {\frac {\partial ^{2}V}{\partial S^{2}}}} … Vega

### `fml-src-black-scholes-model-fa32a5b3-0054`

formula · **exact** · anchored by `none`

$${\frac {\partial V}{\partial \sigma }}$$

```latex
{\frac {\partial V}{\partial \sigma }}
```

> {\displaystyle {\frac {N'(d_{+})}{S\sigma {\sqrt {T-t}}}}\,} Vega … S N ′

### `fml-src-black-scholes-model-fa32a5b3-0055`

formula · **exact** · anchored by `none`

$$SN'(d_{+}){\sqrt {T-t}}\,$$

```latex
SN'(d_{+}){\sqrt {T-t}}\,
```

> ∂ σ {\displaystyle {\frac {\partial V}{\partial \sigma }}} … Theta

### `fml-src-black-scholes-model-fa32a5b3-0056`

formula · **exact** · anchored by `none`

$${\frac {\partial V}{\partial t}}$$

```latex
{\frac {\partial V}{\partial t}}
```

> t {\displaystyle SN'(d_{+}){\sqrt {T-t}}\,} Theta … −

### `fml-src-black-scholes-model-fa32a5b3-0057`

formula · **exact** · anchored by `none`

$$-{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}-rKe^{-r(T-t)}N(d_{-})\,$$

```latex
-{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}-rKe^{-r(T-t)}N(d_{-})\,
```

> ∂ t {\displaystyle {\frac {\partial V}{\partial t}}} …

### `fml-src-black-scholes-model-fa32a5b3-0058`

formula · **exact** · anchored by `none`

$$-{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}+rKe^{-r(T-t)}N(-d_{-})\,$$

```latex
-{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}+rKe^{-r(T-t)}N(-d_{-})\,
```

> ) {\displaystyle -{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}-rKe^{-r(T-t)}N(d_{-})\,} … Rho

### `fml-src-black-scholes-model-fa32a5b3-0059`

formula · **exact** · anchored by `none`

$${\frac {\partial V}{\partial r}}$$

```latex
{\frac {\partial V}{\partial r}}
```

> {\displaystyle -{\frac {SN'(d_{+})\sigma }{2{\sqrt {T-t}}}}+rKe^{-r(T-t)}N(-d_{-})\,} Rho … K ( T − t

### `fml-src-black-scholes-model-fa32a5b3-0060`

formula · **exact** · anchored by `none`

$$K(T-t)e^{-r(T-t)}N(d_{-})\,$$

```latex
K(T-t)e^{-r(T-t)}N(d_{-})\,
```

> ∂ r {\displaystyle {\frac {\partial V}{\partial r}}} … − K ( T −

### `fml-src-black-scholes-model-fa32a5b3-0061`

formula · **exact** · anchored by `none`

$$-K(T-t)e^{-r(T-t)}N(-d_{-})\,$$

```latex
-K(T-t)e^{-r(T-t)}N(-d_{-})\,
```

> − ) {\displaystyle K(T-t)e^{-r(T-t)}N(d_{-})\,} … Note that the gamma and vega are the same value for calls and puts. This can be

### `fml-src-black-scholes-model-fa32a5b3-0062`

formula · **exact** · anchored by `none`

$$\nu$$

```latex
\nu
```

> ys or trading days per year). Note that "Vega" is not a letter in the Greek alphabet; the name arises from misreading the Greek letter nu (variously rendered as … , ν , and ν) as a V. Extensions of the model The above model can be extended for

### `fml-src-black-scholes-model-fa32a5b3-0063`

formula · **exact** · anchored by `none`

$$[t,t+dt]$$

```latex
[t,t+dt]
```

> ion that dividends are paid continuously, and that the dividend amount is proportional to the level of the index. The dividend payment paid over the time period … is then modelled as: q S t

### `fml-src-black-scholes-model-fa32a5b3-0064`

formula · **exact** · anchored by `none`

$$qS_{t}\,dt$$

```latex
qS_{t}\,dt
```

> [ t , t + d t ] {\displaystyle [t,t+dt]} is then modelled as: … for some constant q {\displaystyle q}

### `fml-src-black-scholes-model-fa32a5b3-0065`

formula · **exact** · anchored by `none`

$$C(S_{t},t)=e^{-r(T-t)}[FN(d_{1})-KN(d_{2})]\,$$

```latex
C(S_{t},t)=e^{-r(T-t)}[FN(d_{1})-KN(d_{2})]\,
```

> {\displaystyle q} (the dividend yield ). Under this formulation the arbitrage-free price implied by the Black–Scholes model can be shown to be: … and P

### `fml-src-black-scholes-model-fa32a5b3-0066`

formula · **exact** · anchored by `none`

$$P(S_{t},t)=e^{-r(T-t)}[KN(-d_{2})-FN(-d_{1})]\,$$

```latex
P(S_{t},t)=e^{-r(T-t)}[KN(-d_{2})-FN(-d_{1})]\,
```

> ) ] {\displaystyle C(S_{t},t)=e^{-r(T-t)}[FN(d_{1})-KN(d_{2})]\,} and … where now F = S

### `fml-src-black-scholes-model-fa32a5b3-0067`

formula · **exact** · anchored by `none`

$$F=S_{t}e^{(r-q)(T-t)}\,$$

```latex
F=S_{t}e^{(r-q)(T-t)}\,
```

> ) ] {\displaystyle P(S_{t},t)=e^{-r(T-t)}[KN(-d_{2})-FN(-d_{1})]\,} where now … is the modified forward price that occurs in the terms d 1

### `fml-src-black-scholes-model-fa32a5b3-0068`

formula · **exact** · anchored by `none`

$$d_{1},d_{2}$$

```latex
d_{1},d_{2}
```

> t ) {\displaystyle F=S_{t}e^{(r-q)(T-t)}\,} is the modified forward price that occurs in the terms … :

### `fml-src-black-scholes-model-fa32a5b3-0069`

formula · **exact** · anchored by `none`

$$d_{1}={\frac {1}{\sigma {\sqrt {T-t}}}}\left[\ln \left({\frac {S_{t}}{K}}\right)+\left(r-q+{\frac {1}{2}}\sigma ^{2}\right)(T-t)\right]$$

```latex
d_{1}={\frac {1}{\sigma {\sqrt {T-t}}}}\left[\ln \left({\frac {S_{t}}{K}}\right)+\left(r-q+{\frac {1}{2}}\sigma ^{2}\right)(T-t)\right]
```

> 2 {\displaystyle d_{1},d_{2}} : … and

### `fml-src-black-scholes-model-fa32a5b3-0070`

formula · **exact** · anchored by `none`

$$d_{2}=d_{1}-\sigma {\sqrt {T-t}}={\frac {1}{\sigma {\sqrt {T-t}}}}\left[\ln \left({\frac {S_{t}}{K}}\right)+\left(r-q-{\frac {1}{2}}\sigma ^{2}\right)(T-t)\right]$$

```latex
d_{2}=d_{1}-\sigma {\sqrt {T-t}}={\frac {1}{\sigma {\sqrt {T-t}}}}\left[\ln \left({\frac {S_{t}}{K}}\right)+\left(r-q-{\frac {1}{2}}\sigma ^{2}\right)(T-t)\right]
```

> ght)(T-t)\right]} and … . [ 25 ]

### `fml-src-black-scholes-model-fa32a5b3-0071`

formula · **exact** · anchored by `none`

$$\delta$$

```latex
\delta
```

> n instruments paying discrete proportional dividends. This is useful when the option is struck on a single stock. A typical model is to assume that a proportion … of the stock price is paid out at pre-determined times t 1

### `fml-src-black-scholes-model-fa32a5b3-0072`

formula · **exact** · anchored by `none`

$$t_{1},t_{2},\ldots ,t_{n}$$

```latex
t_{1},t_{2},\ldots ,t_{n}
```

> δ {\displaystyle \delta } of the stock price is paid out at pre-determined times … . The price of the stock is then modelled as: S

### `fml-src-black-scholes-model-fa32a5b3-0073`

formula · **exact** · anchored by `none`

$$S_{t}=S_{0}(1-\delta )^{n(t)}e^{ut+\sigma W_{t}}$$

```latex
S_{t}=S_{0}(1-\delta )^{n(t)}e^{ut+\sigma W_{t}}
```

> t n {\displaystyle t_{1},t_{2},\ldots ,t_{n}} . The price of the stock is then modelled as: … where n ( t )

### `fml-src-black-scholes-model-fa32a5b3-0074`

formula · **exact** · anchored by `none`

$$n(t)$$

```latex
n(t)
```

> W t {\displaystyle S_{t}=S_{0}(1-\delta )^{n(t)}e^{ut+\sigma W_{t}}} where … is the number of dividends that have been paid by time t {\displaystyle t}

### `fml-src-black-scholes-model-fa32a5b3-0075`

formula · **exact** · anchored by `none`

$$C(S_{0},T)=e^{-rT}[FN(d_{1})-KN(d_{2})]\,$$

```latex
C(S_{0},T)=e^{-rT}[FN(d_{1})-KN(d_{2})]\,
```

> t {\displaystyle t} . The price of a call option on such a stock is again: … where now F =

### `fml-src-black-scholes-model-fa32a5b3-0076`

formula · **exact** · anchored by `none`

$$F=S_{0}(1-\delta )^{n(T)}e^{rT}\,$$

```latex
F=S_{0}(1-\delta )^{n(T)}e^{rT}\,
```

> ) ] {\displaystyle C(S_{0},T)=e^{-rT}[FN(d_{1})-KN(d_{2})]\,} where now … is the forward price for the dividend paying stock. American options The problem

### `fml-src-black-scholes-model-fa32a5b3-0077`

formula · **exact** · anchored by `none`

$${\frac {\partial V}{\partial t}}+{\frac {1}{2}}\sigma ^{2}S^{2}{\frac {\partial ^{2}V}{\partial S^{2}}}+rS{\frac {\partial V}{\partial S}}-rV\leq 0$$

```latex
{\frac {\partial V}{\partial t}}+{\frac {1}{2}}\sigma ^{2}S^{2}{\frac {\partial ^{2}V}{\partial S^{2}}}+rS{\frac {\partial V}{\partial S}}-rV\leq 0
```

> ion. Since the American option can be exercised at any time before the expiration date, the Black–Scholes equation becomes a variational inequality of the form: … [ 26 ] together with

### `fml-src-black-scholes-model-fa32a5b3-0078`

formula · **exact** · anchored by `none`

$$V(S,t)\geq H(S)$$

```latex
V(S,t)\geq H(S)
```

> tial V}{\partial t}}+{\frac {1}{2}}\sigma ^{2}S^{2}{\frac {\partial ^{2}V}{\partial S^{2}}}+rS{\frac {\partial V}{\partial S}}-rV\leq 0}"/> [ 26 ] together with … where H ( S ) {\displaystyle H(S)}

### `fml-src-black-scholes-model-fa32a5b3-0079`

formula · **exact** · anchored by `none`

$$H(S)$$

```latex
H(S)
```

> ( S , t ) ≥ H ( S ) {\displaystyle V(S,t)\geq H(S)} where … denotes the payoff at stock price S {\displaystyle S}

### `fml-src-black-scholes-model-fa32a5b3-0080`

formula · **exact** · anchored by `none`

$$V(S,T)=H(S)$$

```latex
V(S,T)=H(S)
```

> S {\displaystyle S} and the terminal condition: … . In general this inequality does not have a closed form solution, though an Ame

### `fml-src-black-scholes-model-fa32a5b3-0081`

formula · **exact** · anchored by `none`

$$S-X$$

```latex
S-X
```

> onding to a trigger price. Here, if the underlying asset price is greater than or equal to the trigger price it is optimal to exercise, and the value must equal … , otherwise the option "boils down to: (i) a European up-and-out call option...

### `fml-src-black-scholes-model-fa32a5b3-0082`

formula · **exact** · anchored by `none`

$$T\rightarrow \infty$$

```latex
T\rightarrow \infty
```

> cal solution for American put options, it is possible to derive such a formula for the case of a perpetual option – meaning that the option never expires (i.e., … ). [ 34 ] In this case, the time decay of the option is equal to zero, which lea

### `fml-src-black-scholes-model-fa32a5b3-0083`

formula · **exact** · anchored by `none`

$${1 \over {2}}\sigma ^{2}S^{2}{d^{2}V \over {dS^{2}}}+(r-q)S{dV \over {dS}}-rV=0$$

```latex
{1 \over {2}}\sigma ^{2}S^{2}{d^{2}V \over {dS^{2}}}+(r-q)S{dV \over {dS}}-rV=0
```

> ). [ 34 ] In this case, the time decay of the option is equal to zero, which leads to the Black–Scholes PDE becoming an ODE: … Let S −

### `fml-src-black-scholes-model-fa32a5b3-0084`

formula · **exact** · anchored by `none`

$$S_{-}$$

```latex
S_{-}
```

> − r V = 0 {\displaystyle {1 \over {2}}\sigma ^{2}S^{2}{d^{2}V \over {dS^{2}}}+(r-q)S{dV \over {dS}}-rV=0} Let … denote the lower exercise boundary, below which it is optimal to exercise the op

### `fml-src-black-scholes-model-fa32a5b3-0085`

formula · **exact** · anchored by `none`

$$V(S_{-})=K-S_{-},\quad {dV \over {dS}}(S_{-})=-1,\quad V(S)\leq K$$

```latex
V(S_{-})=K-S_{-},\quad {dV \over {dS}}(S_{-})=-1,\quad V(S)\leq K
```

> − {\displaystyle S_{-}} denote the lower exercise boundary, below which it is optimal to exercise the option. The boundary conditions are: … The solutions to the ODE are a linear combination of any two linearly independen

### `fml-src-black-scholes-model-fa32a5b3-0086`

formula · **exact** · anchored by `none`

$$V(S)=A_{1}S^{\lambda _{1}}+A_{2}S^{\lambda _{2}}$$

```latex
V(S)=A_{1}S^{\lambda _{1}}+A_{2}S^{\lambda _{2}}
```

> V(S_{-})=K-S_{-},\quad {dV \over {dS}}(S_{-})=-1,\quad V(S)\leq K} The solutions to the ODE are a linear combination of any two linearly independent solutions: … For S − ≤

### `fml-src-black-scholes-model-fa32a5b3-0087`

formula · **exact** · anchored by `none`

$$S_{-}\leq S$$

```latex
S_{-}\leq S
```

> λ 2 {\displaystyle V(S)=A_{1}S^{\lambda _{1}}+A_{2}S^{\lambda _{2}}} For … , substitution of this solution into the ODE for i = 1 , 2

### `fml-src-black-scholes-model-fa32a5b3-0088`

formula · **exact** · anchored by `none`

$$i={1,2}$$

```latex
i={1,2}
```

> S − ≤ S {\displaystyle S_{-}\leq S} , substitution of this solution into the ODE for … yields:

### `fml-src-black-scholes-model-fa32a5b3-0089`

formula · **exact** · anchored by `none`

$$\left[{1 \over {2}}\sigma ^{2}\lambda _{i}(\lambda _{i}-1)+(r-q)\lambda _{i}-r\right]S^{\lambda _{i}}=0$$

```latex
\left[{1 \over {2}}\sigma ^{2}\lambda _{i}(\lambda _{i}-1)+(r-q)\lambda _{i}-r\right]S^{\lambda _{i}}=0
```

> i = 1 , 2 {\displaystyle i={1,2}} yields: … Rearranging the terms gives:

### `fml-src-black-scholes-model-fa32a5b3-0090`

formula · **exact** · anchored by `none`

$${1 \over {2}}\sigma ^{2}\lambda _{i}^{2}+\left(r-q-{1 \over {2}}\sigma ^{2}\right)\lambda _{i}-r=0$$

```latex
{1 \over {2}}\sigma ^{2}\lambda _{i}^{2}+\left(r-q-{1 \over {2}}\sigma ^{2}\right)\lambda _{i}-r=0
```

> {\displaystyle \left[{1 \over {2}}\sigma ^{2}\lambda _{i}(\lambda _{i}-1)+(r-q)\lambda _{i}-r\right]S^{\lambda _{i}}=0} Rearranging the terms gives: … Using the quadratic formula , the solutions for

### `fml-src-black-scholes-model-fa32a5b3-0091`

formula · **exact** · anchored by `none`

$$\lambda _{i}$$

```latex
\lambda _{i}
```

> displaystyle {1 \over {2}}\sigma ^{2}\lambda _{i}^{2}+\left(r-q-{1 \over {2}}\sigma ^{2}\right)\lambda _{i}-r=0} Using the quadratic formula , the solutions for … are:

### `fml-src-black-scholes-model-fa32a5b3-0092`

formula · **exact** · anchored by `none`

$${\begin{aligned}\lambda _{1}&={-\left(r-q-{1 \over {2}}\sigma ^{2}\right)+{\sqrt {\left(r-q-{1 \over {2}}\sigma ^{2}\right)^{2}+2\sigma ^{2}r}} \over {\sigma ^{2}}}\\\lambda _{2}&={-\left(r-q-{1 \over {2}}\sigma ^{2}\right)-{\sqrt {\left(r-q-{1 \over {2}}\sigma ^{2}\right)^{2}+2\sigma ^{2}r}} \over {\sigma ^{2}}}\end{aligned}}$$

```latex
{\begin{aligned}\lambda _{1}&={-\left(r-q-{1 \over {2}}\sigma ^{2}\right)+{\sqrt {\left(r-q-{1 \over {2}}\sigma ^{2}\right)^{2}+2\sigma ^{2}r}} \over {\sigma ^{2}}}\\\lambda _{2}&={-\left(r-q-{1 \over {2}}\sigma ^{2}\right)-{\sqrt {\left(r-q-{1 \over {2}}\sigma ^{2}\right)^{2}+2\sigma ^{2}r}} \over {\sigma ^{2}}}\end{aligned}}
```

> are: … In order to have a finite solution for the perpetual put, since the boundary con

### `fml-src-black-scholes-model-fa32a5b3-0093`

formula · **exact** · anchored by `none`

$$A_{1}=0$$

```latex
A_{1}=0
```

> have a finite solution for the perpetual put, since the boundary conditions imply upper and lower finite bounds on the value of the put, it is necessary to set … , leading to the solution V ( S ) =

### `fml-src-black-scholes-model-fa32a5b3-0094`

formula · **exact** · anchored by `none`

$$V(S)=A_{2}S^{\lambda _{2}}$$

```latex
V(S)=A_{2}S^{\lambda _{2}}
```

> A 1 = 0 {\displaystyle A_{1}=0} , leading to the solution … . From the first boundary condition, it is known that:

### `fml-src-black-scholes-model-fa32a5b3-0095`

formula · **exact** · anchored by `none`

$$V(S_{-})=A_{2}(S_{-})^{\lambda _{2}}=K-S_{-}\implies A_{2}={K-S_{-} \over {(S_{-})^{\lambda _{2}}}}$$

```latex
V(S_{-})=A_{2}(S_{-})^{\lambda _{2}}=K-S_{-}\implies A_{2}={K-S_{-} \over {(S_{-})^{\lambda _{2}}}}
```

> {\displaystyle V(S)=A_{2}S^{\lambda _{2}}} . From the first boundary condition, it is known that: … Therefore, the value of the perpetual put becomes:

### `fml-src-black-scholes-model-fa32a5b3-0096`

formula · **exact** · anchored by `none`

$$V(S)=(K-S_{-})\left({S \over {S_{-}}}\right)^{\lambda _{2}}$$

```latex
V(S)=(K-S_{-})\left({S \over {S_{-}}}\right)^{\lambda _{2}}
```

> laystyle V(S_{-})=A_{2}(S_{-})^{\lambda _{2}}=K-S_{-}\implies A_{2}={K-S_{-} \over {(S_{-})^{\lambda _{2}}}}} Therefore, the value of the perpetual put becomes: … The second boundary condition yields the location of the lower exercise boundary

### `fml-src-black-scholes-model-fa32a5b3-0097`

formula · **exact** · anchored by `none`

$${dV \over {dS}}(S_{-})=\lambda _{2}{K-S_{-} \over {S_{-}}}=-1\implies S_{-}={\lambda _{2}K \over {\lambda _{2}-1}}$$

```latex
{dV \over {dS}}(S_{-})=\lambda _{2}{K-S_{-} \over {S_{-}}}=-1\implies S_{-}={\lambda _{2}K \over {\lambda _{2}-1}}
```

> {\displaystyle V(S)=(K-S_{-})\left({S \over {S_{-}}}\right)^{\lambda _{2}}} The second boundary condition yields the location of the lower exercise boundary: … To conclude, for

### `fml-src-black-scholes-model-fa32a5b3-0098`

formula · **exact** · anchored by `none`

$${\textstyle S\geq S_{-}={\lambda _{2}K \over {\lambda _{2}-1}}}$$

```latex
{\textstyle S\geq S_{-}={\lambda _{2}K \over {\lambda _{2}-1}}}
```

> {\displaystyle {dV \over {dS}}(S_{-})=\lambda _{2}{K-S_{-} \over {S_{-}}}=-1\implies S_{-}={\lambda _{2}K \over {\lambda _{2}-1}}} To conclude, for … , the perpetual American put option is worth:

### `fml-src-black-scholes-model-fa32a5b3-0099`

formula · **exact** · anchored by `none`

$$V(S)={K \over {1-\lambda _{2}}}\left({\lambda _{2}-1 \over {\lambda _{2}}}\right)^{\lambda _{2}}\left({S \over {K}}\right)^{\lambda _{2}}$$

```latex
V(S)={K \over {1-\lambda _{2}}}\left({\lambda _{2}-1 \over {\lambda _{2}}}\right)^{\lambda _{2}}\left({S \over {K}}\right)^{\lambda _{2}}
```

> {\textstyle S\geq S_{-}={\lambda _{2}K \over {\lambda _{2}-1}}} , the perpetual American put option is worth: … Binary options By solving the Black–Scholes differential equation with the Heavi

### `fml-src-black-scholes-model-fa32a5b3-0100`

formula · **exact** · anchored by `none`

$$C=e^{-r(T-t)}N(d_{2}).\,$$

```latex
C=e^{-r(T-t)}N(d_{2}).\,
```

> two terms in the Black–Scholes formula. Cash-or-nothing call This pays out one unit of cash if the spot is above the strike at maturity. Its value is given by: … Cash-or-nothing put This pays out one unit of cash if the spot is below the stri

### `fml-src-black-scholes-model-fa32a5b3-0101`

formula · **exact** · anchored by `none`

$$P=e^{-r(T-t)}N(-d_{2}).\,$$

```latex
P=e^{-r(T-t)}N(-d_{2}).\,
```

> {\displaystyle C=e^{-r(T-t)}N(d_{2}).\,} Cash-or-nothing put This pays out one unit of cash if the spot is below the strike at maturity. Its value is given by: … Asset-or-nothing call This pays out one unit of asset if the spot is above the s

### `fml-src-black-scholes-model-fa32a5b3-0102`

formula · **exact** · anchored by `none`

$$C=Se^{-q(T-t)}N(d_{1}).\,$$

```latex
C=Se^{-q(T-t)}N(d_{1}).\,
```

> isplaystyle P=e^{-r(T-t)}N(-d_{2}).\,} Asset-or-nothing call This pays out one unit of asset if the spot is above the strike at maturity. Its value is given by: … Asset-or-nothing put This pays out one unit of asset if the spot is below the st

### `fml-src-black-scholes-model-fa32a5b3-0103`

formula · **exact** · anchored by `none`

$$P=Se^{-q(T-t)}N(-d_{1}),$$

```latex
P=Se^{-q(T-t)}N(-d_{1}),
```

> displaystyle C=Se^{-q(T-t)}N(d_{1}).\,} Asset-or-nothing put This pays out one unit of asset if the spot is below the strike at maturity. Its value is given by: … Foreign Exchange (FX)

### `fml-src-black-scholes-model-fa32a5b3-0104`

formula · **exact** · anchored by `none`

$$r_{f}$$

```latex
r_{f}
```

> unit of the foreign currency if the spot at maturity is above or below the strike is exactly like an asset-or nothing call and put respectively. Hence by taking … , the foreign interest rate, r d

### `fml-src-black-scholes-model-fa32a5b3-0105`

formula · **exact** · anchored by `none`

$$r_{d}$$

```latex
r_{d}
```

> r f {\displaystyle r_{f}} , the foreign interest rate, … , the domestic interest rate, and the rest as above, the following results can b

### `fml-src-black-scholes-model-fa32a5b3-0106`

formula · **exact** · anchored by `none`

$$C=e^{-r_{d}T}N(d_{2})\,$$

```latex
C=e^{-r_{d}T}N(d_{2})\,
```

> lowing results can be obtained: In the case of a digital call (this is a call FOR/put DOM) paying out one unit of the domestic currency gotten as present value: … In the case of a digital put (this is a put FOR/call DOM) paying out one unit of

### `fml-src-black-scholes-model-fa32a5b3-0107`

formula · **exact** · anchored by `none`

$$P=e^{-r_{d}T}N(-d_{2})\,$$

```latex
P=e^{-r_{d}T}N(-d_{2})\,
```

> aystyle C=e^{-r_{d}T}N(d_{2})\,} In the case of a digital put (this is a put FOR/call DOM) paying out one unit of the domestic currency gotten as present value: … In the case of a digital call (this is a call FOR/put DOM) paying out one unit o

### `fml-src-black-scholes-model-fa32a5b3-0108`

formula · **exact** · anchored by `none`

$$C=Se^{-r_{f}T}N(d_{1})\,$$

```latex
C=Se^{-r_{f}T}N(d_{1})\,
```

> ystyle P=e^{-r_{d}T}N(-d_{2})\,} In the case of a digital call (this is a call FOR/put DOM) paying out one unit of the foreign currency gotten as present value: … In the case of a digital put (this is a put FOR/call DOM) paying out one unit of

### `fml-src-black-scholes-model-fa32a5b3-0109`

formula · **exact** · anchored by `none`

$$P=Se^{-r_{f}T}N(-d_{1})\,$$

```latex
P=Se^{-r_{f}T}N(-d_{1})\,
```

> aystyle C=Se^{-r_{f}T}N(d_{1})\,} In the case of a digital put (this is a put FOR/call DOM) paying out one unit of the foreign currency gotten as present value: … Skew In the standard Black–Scholes model, one can interpret the premium of the b

### `fml-src-black-scholes-model-fa32a5b3-0110`

formula · **exact** · anchored by `none`

$$\sigma$$

```latex
\sigma
```

> the skewness of the distribution of the asset. Market makers adjust for such skewness by, instead of using a single standard deviation for the underlying asset … across all strikes, incorporating a variable one σ ( K )

### `fml-src-black-scholes-model-fa32a5b3-0111`

formula · **exact** · anchored by `none`

$$\sigma (K)$$

```latex
\sigma (K)
```

> σ {\displaystyle \sigma } across all strikes, incorporating a variable one … where volatility depends on strike price, thus incorporating the volatility skew

### `fml-src-black-scholes-model-fa32a5b3-0112`

formula · **exact** · anchored by `none`

$$C_{v}$$

```latex
C_{v}
```

> t call spread using two vanilla options. One can model the value of a binary cash-or-nothing option, C , at strike K , as an infinitesimally tight spread, where … is a vanilla European call: [ 36 ]

### `fml-src-black-scholes-model-fa32a5b3-0113`

formula · **exact** · anchored by `none`

$$C=\lim _{\epsilon \to 0}{\frac {C_{v}(K-\epsilon )-C_{v}(K)}{\epsilon }}$$

```latex
C=\lim _{\epsilon \to 0}{\frac {C_{v}(K-\epsilon )-C_{v}(K)}{\epsilon }}
```

> [ 36 ] [ 37 ] … Thus, the value of a binary call is the negative of the derivative of the price

### `fml-src-black-scholes-model-fa32a5b3-0114`

formula · **exact** · anchored by `none`

$$C=-{\frac {dC_{v}}{dK}}$$

```latex
C=-{\frac {dC_{v}}{dK}}
```

> on )-C_{v}(K)}{\epsilon }}} Thus, the value of a binary call is the negative of the derivative of the price of a vanilla call with respect to strike price: … When one takes volatility skew into account, σ {\displaystyle \sigma }

### `fml-src-black-scholes-model-fa32a5b3-0115`

formula · **exact** · anchored by `none`

$$C=-{\frac {dC_{v}(K,\sigma (K))}{dK}}=-{\frac {\partial C_{v}}{\partial K}}-{\frac {\partial C_{v}}{\partial \sigma }}{\frac {\partial \sigma }{\partial K}}$$

```latex
C=-{\frac {dC_{v}(K,\sigma (K))}{dK}}=-{\frac {\partial C_{v}}{\partial K}}-{\frac {\partial C_{v}}{\partial \sigma }}{\frac {\partial \sigma }{\partial K}}
```

> K {\displaystyle K} : … The first term is equal to the premium of the binary option ignoring skew:

### `fml-src-black-scholes-model-fa32a5b3-0116`

formula · **exact** · anchored by `none`

$$-{\frac {\partial C_{v}}{\partial K}}=-{\frac {\partial (SN(d_{1})-Ke^{-r(T-t)}N(d_{2}))}{\partial K}}=e^{-r(T-t)}N(d_{2})=C_{\text{no skew}}$$

```latex
-{\frac {\partial C_{v}}{\partial K}}=-{\frac {\partial (SN(d_{1})-Ke^{-r(T-t)}N(d_{2}))}{\partial K}}=e^{-r(T-t)}N(d_{2})=C_{\text{no skew}}
```

> -{\frac {\partial C_{v}}{\partial \sigma }}{\frac {\partial \sigma }{\partial K}}}"/> The first term is equal to the premium of the binary option ignoring skew: …

### `fml-src-black-scholes-model-fa32a5b3-0117`

formula · **exact** · anchored by `none`

$${\frac {\partial C_{v}}{\partial \sigma }}$$

```latex
{\frac {\partial C_{v}}{\partial \sigma }}
```

> {\displaystyle -{\frac {\partial C_{v}}{\partial K}}=-{\frac {\partial (SN(d_{1})-Ke^{-r(T-t)}N(d_{2}))}{\partial K}}=e^{-r(T-t)}N(d_{2})=C_{\text{no skew}}} … is the Vega of the vanilla call;

### `fml-src-black-scholes-model-fa32a5b3-0118`

formula · **exact** · anchored by `none`

$${\frac {\partial \sigma }{\partial K}}$$

```latex
{\frac {\partial \sigma }{\partial K}}
```

> {\displaystyle {\frac {\partial C_{v}}{\partial \sigma }}} is the Vega of the vanilla call; … is sometimes called the "skew slope" or just "skew". If the skew is typically ne

### `fml-src-black-scholes-model-fa32a5b3-0119`

formula · **exact** · anchored by `none`

$$C=C_{\text{no skew}}-{\text{Vega}}_{v}\cdot {\text{Skew}}$$

```latex
C=C_{\text{no skew}}-{\text{Vega}}_{v}\cdot {\text{Skew}}
```

> is sometimes called the "skew slope" or just "skew". If the skew is typically negative, the value of a binary call will be higher when taking skew into account. … Relationship to vanilla options' Greeks Since a binary call is a mathematical de

## The knowledge handed off

Rendered from [`07_enqueue/enqueue.jsonl`](runs/bs/07_enqueue/enqueue.jsonl) — 12 event(s), target `existing-leaf-engine`.

---

### 1. Black-Scholes: what the model is and the hedging argument behind it

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-001-r1` v2

**Slug** `black-scholes-what-the-model-is-and-the-hedging-argument-behind-it`

The Black-Scholes-Merton model prices European options by showing that the option can be replicated by continuously trading the underlying and cash, which forces a unique price. This leaf carries the definition, the hedging argument, the original 1973 claim, and the one parameter the model cannot observe.

**Assertions (5)**

1. The Black-Scholes (or Black-Scholes-Merton) model is a mathematical model of the dynamics of a financial market containing derivative instruments, from whose parabolic partial differential equation one deduces the Black-Scholes formula: a theoretical price for European-style options that is unique given the security's risk, with the security's expected return replaced by the risk-neutral rate.

   *backed by* `asmt-0001`

2. Black-Scholes prices an option by hedging it: buying and selling the underlying asset continuously so as to eliminate risk, a technique called continuously revised delta hedging, which is the basis of the more complicated hedging strategies used by investment banks and hedge funds.

   *backed by* `asmt-0002`

3. The financial insight behind the Black-Scholes equation is that the option can be perfectly hedged by trading the underlying asset and cash so as to eliminate risk, which is what implies a unique option price.

   *backed by* `asmt-0012`

4. The original Black-Scholes model assumes the stock pays no dividend, though trivial extensions of the model can accommodate a continuous dividend yield factor.

   *backed by* `asmt-0001`

5. Volatility is the only Black-Scholes parameter that cannot be observed directly in the market; because the option value rises with it for both puts and calls, the formula can be inverted on observed option prices to produce a volatility surface, which is then used to calibrate other models.

   *backed by* `asmt-0003`

**Related topics** `Black-Scholes: the equation and its closed-form solutions`

**Source units (5)** `u-src-black-scholes-model-fa32a5b3-0001`, `u-src-black-scholes-model-fa32a5b3-0002`, `u-src-black-scholes-model-fa32a5b3-0003`, `u-src-black-scholes-model-fa32a5b3-0012`, `u-src-black-scholes-model-fa32a5b3-0062`

**Traceability** — idempotency key `cf1a5e4d6ba1dbd17df2c0600ec74b81a25a6459c3ed540bdd7d89c4748854fe` · queue event `q-cf1a5e4d6ba1dbd1` · audits `audit-cand-001`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 2. Black-Scholes: the equation, its boundary conditions and its closed-form solutions

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-002-r1` v2

**Slug** `black-scholes-the-equation-its-boundary-conditions-and-its-closed-form-solutions`

The core mathematics: the partial differential equation, the terminal and boundary conditions that pick out the call, the resulting call and put prices, the forward-price reformulation, and the notation the formulas use. Every formula is stated in full so it can be applied without returning to the source.

**Assertions (8)**

1. The Black-Scholes equation is the parabolic partial differential equation governing the option price V(S,t), where S is the underlying price, t is time, sigma is volatility and r the risk-free rate: dV/dt + (1/2)sigma^2 S^2 d2V/dS2 + rS dV/dS - rV = 0.

   *backed by* `asmt-0011`

2. The Black-Scholes formula is obtained by solving the Black-Scholes equation subject to the terminal and boundary conditions C(0,t)=0 for all t, C(S,t) ~ S - K e^{-r(T-t)} as S goes to infinity, and C(S,T)=max{S-K,0}, which is why the formula and the equation are consistent with each other.

   *backed by* `asmt-0015`

3. The Black-Scholes call price for a non-dividend-paying stock is C(S_t,t) = N(d+)S_t - N(d-)K e^{-r(T-t)}, with d+ = [ln(S_t/K) + (r + sigma^2/2)(T-t)] / (sigma sqrt(T-t)) and d- = d+ - sigma sqrt(T-t).

   *backed by* `asmt-0013`

4. The Black-Scholes put price follows from put-call parity rather than a separate derivation: P(S_t,t) = K e^{-r(T-t)} - S_t + C(S_t,t) = N(-d-)K e^{-r(T-t)} - N(-d+)S_t.

   *backed by* `asmt-0014`

5. Introducing the discount factor D = e^{-r tau} and the forward price F = e^{r tau} S = S/D simplifies the Black-Scholes call to C(F,tau) = D[N(d+)F - N(d-)K], a special case of the Black '76 formula, in which d+ = [ln(F/K) + (1/2)sigma^2 tau] / (sigma sqrt(tau)).

   *backed by* `asmt-0018`

6. Put-call parity in forward terms is C - P = D(F - K) = S - DK, and it yields the put price P(F,tau) = D[N(-d-)K - N(-d+)F].

   *backed by* `asmt-0019`

7. In the Black-Scholes formula N(x) is the standard normal cumulative distribution function, N(x) = (1/sqrt(2 pi)) times the integral of e^{-z^2/2} from minus infinity to x.

   *backed by* `asmt-0016`

8. Time to maturity in the Black-Scholes notation is tau = T - t, the difference between the option's expiration time T and the current time t.

   *backed by* `asmt-0017`

**Related topics** `Black-Scholes: the Greeks in closed form`

**Source units (8)** `u-src-black-scholes-model-fa32a5b3-0011`, `u-src-black-scholes-model-fa32a5b3-0013`, `u-src-black-scholes-model-fa32a5b3-0014`, `u-src-black-scholes-model-fa32a5b3-0015`, `u-src-black-scholes-model-fa32a5b3-0016`, `u-src-black-scholes-model-fa32a5b3-0017`, `u-src-black-scholes-model-fa32a5b3-0018`, `u-src-black-scholes-model-fa32a5b3-0019`

**Traceability** — idempotency key `6e9fb658a84b08aabdd19e48c501affe5154a9232f82b4327719281220e9718c` · queue event `q-6e9fb658a84b08aa` · audits `audit-cand-002`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 3. Black-Scholes: the assumptions, and what each one costs to relax

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-003-r1` v2

**Slug** `black-scholes-the-assumptions-and-what-each-one-costs-to-relax`

The model's assumptions about the assets and about the market, together with the extensions that remove them. Kept as one leaf because the extensions are only meaningful against the assumption each one drops. [contains claims the source itself flags as unsourced]

**Assertions (5)**

1. Black-Scholes assumes the riskless asset earns a constant rate of return, the risk-free interest rate.

   *backed by* `asmt-0007`

2. Black-Scholes assumes the stock price follows a geometric Brownian motion with constant drift and volatility; if drift and volatility vary with time a modified formula can still be derived, provided the volatility is not random.

   *backed by* `asmt-0008`

3. The Black-Scholes market assumptions are: no arbitrage opportunity, unlimited borrowing and lending of fractional amounts of cash at the riskless rate, unlimited buying and selling of fractional amounts of the stock including short selling, and no fees or costs on any of those transactions.

   *backed by* `asmt-0009`

4. Several original Black-Scholes assumptions have been removed by later extensions: modern versions account for dynamic interest rates (Merton, 1976), transaction costs and taxes (Ingersoll, 1976), and dividend payout.

   *backed by* `asmt-0010`

5. The Black-Scholes model extends to variable but deterministic rates and volatilities and to European options on dividend-paying instruments, where closed-form solutions survive if the dividend is a known proportion of the stock price; American options and options on stocks paying a known cash dividend are the harder cases.

   *backed by* `asmt-0010`

**Source units (5)** `u-src-black-scholes-model-fa32a5b3-0007`, `u-src-black-scholes-model-fa32a5b3-0008`, `u-src-black-scholes-model-fa32a5b3-0009`, `u-src-black-scholes-model-fa32a5b3-0010`, `u-src-black-scholes-model-fa32a5b3-0070`

**Traceability** — idempotency key `845c113ecb65cefcff40bc0e013e52b43756455fe58ca50c07c93e40d2bd99aa` · queue event `q-845c113ecb65cefc` · audits `audit-cand-003`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 4. Black-Scholes: the Greeks in closed form

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-004-r1` v2

**Slug** `black-scholes-the-greeks-in-closed-form`

Every Black-Scholes sensitivity, stated as a formula rather than described, plus the conventions used to quote them and the reason delta dominates in practice. Recovered from the article's Greeks table, where each value is cited by its cell so the call and put columns cannot be confused.

**Assertions (12)**

1. The Black-Scholes delta, the partial derivative of the option value with respect to the underlying price, is N(d+) for a call and N(d+)-1 for a put -- equivalently -N(-d+) -- so a call's delta lies between 0 and 1 and a put's between -1 and 0.

   *backed by* `asmt-0056`

2. The Black-Scholes gamma, the second partial derivative of the option value with respect to the underlying price, is N'(d+)/(S sigma sqrt(T-t)), where N' is the standard normal density.

   *backed by* `asmt-0057`

3. The Black-Scholes vega, the partial derivative of the option value with respect to volatility, is S N'(d+) sqrt(T-t).

   *backed by* `asmt-0058`

4. The Black-Scholes theta, the partial derivative of the option value with respect to time, is -S N'(d+) sigma / (2 sqrt(T-t)) - r K e^{-r(T-t)} N(d-) for a call and -S N'(d+) sigma / (2 sqrt(T-t)) + r K e^{-r(T-t)} N(-d-) for a put: the two differ only in the sign of the second term.

   *backed by* `asmt-0059`

5. The Black-Scholes rho, the partial derivative of the option value with respect to the risk-free rate, is K(T-t) e^{-r(T-t)} N(d-) for a call and -K(T-t) e^{-r(T-t)} N(-d-) for a put.

   *backed by* `asmt-0060`

6. The Black-Scholes Greeks are available in closed form and are obtained by differentiating the Black-Scholes formula, which is why every sensitivity of the model is exactly computable rather than estimated numerically.

   *backed by* `asmt-0061`

7. Greeks are usually quoted scaled to the size of a likely parameter change: rho divided by 10,000 for a one-basis-point rate move, vega divided by 100 for a one-volatility-point move, and theta divided by 365 or 252 for one day of decay on calendar or trading days.

   *backed by* `asmt-0030`

8. For an instrument paying a continuous dividend yield q, the Black-Scholes call is C(S_t,t) = e^{-r(T-t)}[F N(d1) - K N(d2)] with forward F = S_t e^{(r-q)(T-t)}, an assumption that is reasonable for options on indices.

   *backed by* `asmt-0031`

9. Financial institutions typically set risk limits on each of the Greeks that their traders must not exceed, which is why the Greeks matter to trading and not only to the mathematical theory of finance.

   *backed by* `asmt-0028`

10. Gamma and vega take the same value for a call and a put on the same underlying, because the difference between a put and a call is a forward, which is linear in S and independent of sigma and therefore has zero gamma and zero vega.

   *backed by* `asmt-0029`

11. Delta is the most important Greek because it usually carries the largest risk, and many traders zero their delta at the end of the day when they are not speculating on market direction, following the delta-neutral hedging approach Black-Scholes defines.

   *backed by* `asmt-0063`

12. "Vega" is not a letter of the Greek alphabet; the name arose from misreading the Greek letter nu.

   *backed by* `asmt-0064`

**Source units (12)** `u-src-black-scholes-model-fa32a5b3-0028`, `u-src-black-scholes-model-fa32a5b3-0029`, `u-src-black-scholes-model-fa32a5b3-0030`, `u-src-black-scholes-model-fa32a5b3-0031`, `u-src-black-scholes-model-fa32a5b3-0056`, `u-src-black-scholes-model-fa32a5b3-0057`, `u-src-black-scholes-model-fa32a5b3-0058`, `u-src-black-scholes-model-fa32a5b3-0059`, `u-src-black-scholes-model-fa32a5b3-0060`, `u-src-black-scholes-model-fa32a5b3-0061`, `u-src-black-scholes-model-fa32a5b3-0063`, `u-src-black-scholes-model-fa32a5b3-0064`

**Traceability** — idempotency key `13a1a12f2ca3608626121644025164fd820de4fbfa413acc2d69d26733e1f01f` · queue event `q-13a1a12f2ca36086` · audits `audit-cand-004`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 5. Black-Scholes: how the two terms of the formula should and should not be read

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-005-r1` v2

**Slug** `black-scholes-how-the-two-terms-of-the-formula-should-and-should-not-be-read`

The article's most substantive argument: N(d+) and N(d-) are not both probabilities of expiring in the money, the naive reading produces a negative price for out-of-the-money calls, and the correct reading depends on which numeraire each term is expressed in.

**Assertions (9)**

1. The Black-Scholes call decomposes into two binary options -- long an asset-or-nothing call, short a cash-or-nothing call -- which is what the two terms of the formula are: a call exchanges cash for an asset at expiry, an asset-or-nothing call yields the asset with no cash exchanged, and a cash-or-nothing call yields cash with no asset delivered.

   *backed by* `asmt-0020`

2. Reading N(d+) and N(d-) as probabilities of the option expiring in the money is incorrect, because either both binaries expire in the money or neither does, so a single event cannot carry two different probabilities.

   *backed by* `asmt-0021`

3. Substituting N(d-) for N(d+) in the Black-Scholes formula yields a negative value for out-of-the-money call options, which is a direct demonstration that the naive reading of the two terms as one probability times one value is wrong.

   *backed by* `asmt-0021`

4. The cash-or-nothing term of the Black-Scholes formula does read as probability times value, because the cash payoff is independent of the underlying's movements; the asset-or-nothing term does not, because the probability of expiring in the money and the asset's value at expiry are not independent unless the numeraire is changed from cash to the asset.

   *backed by* `asmt-0022`

5. The (1/2)sigma^2 term that distinguishes d- from standardized moneyness m = ln(F/K)/(sigma sqrt(tau)) comes from the gap between the median and the mean of the log-normal distribution -- the same factor Ito's lemma produces for geometric Brownian motion.

   *backed by* `asmt-0023`

6. N(d-) is the probability that a Black-Scholes call is exercised when the asset is assumed to drift at the risk-free rate, whereas N(d+) has no simple probability interpretation; N(d+) is correctly read as the present value, at the risk-free rate, of the expected asset price at expiration conditional on that price exceeding the strike.

   *backed by* `asmt-0024`

7. d+ and d- are measures of moneyness expressed in standard deviations, and N(d+) and N(d-) are the probabilities of expiring in the money in their respective numeraires -- the stock for the first, the risk-free asset for the second.

   *backed by* `asmt-0024`

8. The probabilities appearing in the Black-Scholes formula are measure-theoretic probabilities under the equivalent martingale (risk-neutral) measure, and neither is the true probability of expiring in the money under the real physical measure; computing that requires additional information, the drift.

   *backed by* `asmt-0025`

9. The Feynman-Kac formula says the appropriately discounted solution of the Black-Scholes PDE is a martingale, so the option price is the expected value of its discounted payoff -- the risk-neutrality approach, which prices options without any knowledge of PDEs.

   *backed by* `asmt-0026`

**Source units (9)** `u-src-black-scholes-model-fa32a5b3-0020`, `u-src-black-scholes-model-fa32a5b3-0021`, `u-src-black-scholes-model-fa32a5b3-0022`, `u-src-black-scholes-model-fa32a5b3-0023`, `u-src-black-scholes-model-fa32a5b3-0024`, `u-src-black-scholes-model-fa32a5b3-0025`, `u-src-black-scholes-model-fa32a5b3-0026`, `u-src-black-scholes-model-fa32a5b3-0066`, `u-src-black-scholes-model-fa32a5b3-0067`

**Traceability** — idempotency key `2bc990e61b98797f368deb381f30364c7fb28850a0e4a7b94bf0747f6ff61aa7` · queue event `q-2bc990e61b98797f` · audits `audit-cand-005`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 6. Black-Scholes with dividends: continuous yield and discrete proportional payouts

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-006-r1` v2

**Slug** `black-scholes-with-dividends-continuous-yield-and-discrete-proportional-payouts`

Two extensions to dividend-paying instruments, each with the forward price that replaces the spot in the base formula.

**Assertions (2)**

1. Under discrete proportional dividends, where a fraction delta of the stock price is paid out at predetermined times, the stock is modelled as S_t = S_0 (1-delta)^{n(t)} e^{ut + sigma W_t} with n(t) the number of dividends paid by time t, and the call price keeps its usual form with forward F = S_0 (1-delta)^{n(T)} e^{rT}.

   *backed by* `asmt-0032`

2. Pricing an American option is the optimal stopping problem of choosing when to exercise, so the Black-Scholes equation becomes a variational inequality: the PDE expression is at most zero, the option value is at least the payoff H(S), and V(S,T) = H(S) at expiry.

   *backed by* `asmt-0033`

**Source units (2)** `u-src-black-scholes-model-fa32a5b3-0032`, `u-src-black-scholes-model-fa32a5b3-0033`

**Traceability** — idempotency key `ab1aac83d5efcdd53ce07a83a479f351b8d7c9f79d952869dc04a3906c4d93e5` · queue event `q-ab1aac83d5efcdd5` · audits `audit-cand-006`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 7. American options: no general closed form, and the approximations used instead

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-007-r1` v2

**Slug** `american-options-no-general-closed-form-and-the-approximations-used-instead`

The American case turns the equation into a variational inequality with no general closed-form solution. This leaf carries the inequality, the exceptions that do solve exactly, the named approximations, and the one American contract with an exact answer -- the perpetual put.

**Assertions (7)**

1. The American variational inequality generally has no closed-form solution, though an American call on a non-dividend-paying stock equals the European call, and the Roll-Geske-Whaley method solves the case of an American call with one dividend.

   *backed by* `asmt-0034`

2. For a perpetual American put the time decay is zero, so the Black-Scholes PDE collapses to the ordinary differential equation (1/2)sigma^2 S^2 d2V/dS2 + (r-q)S dV/dS - rV = 0, which does admit a closed-form solution even though the finite-maturity American put does not.

   *backed by* `asmt-0035`

3. Barone-Adesi and Whaley approximate the American option by splitting the stochastic differential equation into the European option value plus the early exercise premium, then solving a quadratic for the premium under some assumptions; the solution requires finding the critical underlying price at which one is indifferent between exercising early and holding to maturity.

   *backed by* `asmt-0035`

4. Bjerksund and Stensland approximate the American option with a trigger-price exercise strategy: exercise is optimal once the underlying reaches the trigger price, and below it the option reduces to a European up-and-out call plus a rebate paid if it is knocked out before maturity; the method is computationally inexpensive and fast.

   *backed by* `asmt-0035`

5. The perpetual American put is worth V(S) = K/(1-lambda2) [(lambda2-1)/lambda2]^{lambda2} (S/K)^{lambda2} above the exercise boundary S- = lambda2 K/(lambda2 - 1), below which exercising is optimal.

   *backed by* `asmt-0036`

6. The exponents of the perpetual American put solution are the roots of (1/2)sigma^2 lambda^2 + (r - q - (1/2)sigma^2) lambda - r = 0, and finiteness of the put's value forces the coefficient on the positive root to zero, leaving V(S) = A2 S^{lambda2}.

   *backed by* `asmt-0036`

7. A cash-or-nothing call, which pays one unit of cash if the spot is above the strike at maturity, is worth C = e^{-r(T-t)} N(d2); the corresponding asset-or-nothing call, paying one unit of asset, is worth C = S e^{-q(T-t)} N(d1).

   *backed by* `asmt-0037`

**Source units (7)** `u-src-black-scholes-model-fa32a5b3-0034`, `u-src-black-scholes-model-fa32a5b3-0035`, `u-src-black-scholes-model-fa32a5b3-0036`, `u-src-black-scholes-model-fa32a5b3-0037`, `u-src-black-scholes-model-fa32a5b3-0068`, `u-src-black-scholes-model-fa32a5b3-0069`, `u-src-black-scholes-model-fa32a5b3-0072`

**Traceability** — idempotency key `dd6b26dd0c3daa029a68a8346869fc2f106826440f8801fbf18241d502c2eede` · queue event `q-dd6b26dd0c3daa02` · audits `audit-cand-007`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 8. Binary options under Black-Scholes

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-008-r1` v2

**Slug** `binary-options-under-black-scholes`

Binary (digital) options priced in the same framework, their relation to the vanilla formula as a derivative with respect to strike, the skew correction, and the foreign-exchange case. [contains claims the source itself flags as unsourced]

**Assertions (6)**

1. A binary cash-or-nothing call is the limit of an infinitesimally tight call spread, so its value is the negative derivative of the vanilla call price with respect to strike: C = -dCv/dK.

   *backed by* `asmt-0038`

2. Taking the volatility skew into account, a binary call is worth C = C_no-skew - Vega_v * Skew, where the skew is the derivative of implied volatility with respect to strike; a typically negative skew therefore raises the binary call's value.

   *backed by* `asmt-0039`

3. Skew matters far more for binary options than for vanilla options, because the Black-Scholes model relies on a symmetric distribution and ignores the skewness of the asset's distribution.

   *backed by* `asmt-0040`

4. Because a binary call is the derivative of a vanilla call with respect to strike, the price of a binary call has the same shape as the delta of a vanilla call, and the delta of a binary call has the same shape as the gamma of a vanilla call.

   *backed by* `asmt-0041`

5. For foreign exchange, paying one unit of domestic currency when the spot is above or below the strike is exactly a cash-or-nothing call or put, and paying one unit of foreign currency is exactly an asset-or-nothing call or put, giving digital values C = e^{-r_d T} N(d2) for the domestic payout and C = S e^{-r_f T} N(d1) for the foreign payout.

   *backed by* `asmt-0042`

6. The Black-Scholes assumptions are not all empirically valid, and blindly following the model exposes the user to unexpected risk; its most significant limitations are underestimating extreme moves (tail risk), assuming instant cost-less trading (liquidity risk), assuming a stationary process (volatility risk), assuming continuous time and trading (gap risk), and underpricing deep out-of-the-money while overpricing deep in-the-money options.

   *backed by* `asmt-0043`

**Source units (6)** `u-src-black-scholes-model-fa32a5b3-0038`, `u-src-black-scholes-model-fa32a5b3-0039`, `u-src-black-scholes-model-fa32a5b3-0040`, `u-src-black-scholes-model-fa32a5b3-0041`, `u-src-black-scholes-model-fa32a5b3-0042`, `u-src-black-scholes-model-fa32a5b3-0043`

**Traceability** — idempotency key `5c2a8d3c76ee952dc1c35634dcba8afed8aad6c664289a865a8f3419fad353ae` · queue event `q-5c2a8d3c76ee952d` · audits `audit-cand-008`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 9. Where Black-Scholes fails, and which failures can be hedged

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-009-r1` v2

**Slug** `where-black-scholes-fails-and-which-failures-can-be-hedged`

The model's empirical limitations, each paired with the risk it leaves behind and whether that risk is hedgeable. Kept together because the article's position is that the model is a useful approximation whose failures must be known, and a limitation quoted without that framing misrepresents the source.

**Assertions (6)**

1. Delta hedging alone suffices to hedge an option inside the Black-Scholes model, but in practice there are many other sources of risk.

   *backed by* `asmt-0044`

2. The normality assumption of the Black-Scholes model does not capture extreme movements such as stock market crashes.

   *backed by* `asmt-0055`

3. Black-Scholes pricing remains widely used because it is a useful approximation for the direction prices move when crossing critical points, a robust basis for more refined models, and reversible -- price can be treated as an input and volatility solved for, giving the implied volatility used as a quoting convention.

   *backed by* `asmt-0045`

4. Black-Scholes cannot be applied directly to bonds because of pull-to-par: as the bond approaches maturity all its prices become known and its volatility falls, which the model does not reflect.

   *backed by* `asmt-0049`

5. Interest rate volatility can contribute significantly to an option's price, especially a long-dated one, because rates vary by tenor and over time while Black-Scholes takes a single constant rate.

   *backed by* `asmt-0050`

6. Black-Scholes assumes positive underlying prices and does not work directly when the underlying can go negative; practitioners then use a different model such as Bachelier's, or add a constant offset to the prices.

   *backed by* `asmt-0051`

**Source units (6)** `u-src-black-scholes-model-fa32a5b3-0044`, `u-src-black-scholes-model-fa32a5b3-0045`, `u-src-black-scholes-model-fa32a5b3-0049`, `u-src-black-scholes-model-fa32a5b3-0050`, `u-src-black-scholes-model-fa32a5b3-0051`, `u-src-black-scholes-model-fa32a5b3-0055`

**Traceability** — idempotency key `cc6621060834389638ef43e4b14e1c07619f68bd37df728369c2de9643774551` · queue event `q-cc66210608343896` · audits `audit-cand-009`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 10. Implied volatility: the smile, the surface, and using the wrong number

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-010-r1` v2

**Slug** `implied-volatility-the-smile-the-surface-and-using-the-wrong-number`

Constant volatility is the assumption the market most visibly violates. This leaf carries the test, its result, the shape the surface takes by asset class, and the practice that survives the failure.

**Assertions (5)**

1. If the Black-Scholes model held, a stock's implied volatility would be identical across all strikes and maturities; in practice the volatility surface is not flat, which is how the model can be tested and found wanting.

   *backed by* `asmt-0046`

2. The shape of the implied volatility curve depends on the underlying: equities are skewed, with implied volatility substantially higher for low strikes and slightly lower for high strikes than at-the-money; currencies are more symmetrical, lowest at-the-money and higher in both wings; commodities often behave the reverse of equities.

   *backed by* `asmt-0047`

3. The standard practice despite the volatility smile is to treat the volatility surface as a fact about the market and feed an implied volatility from it into a Black-Scholes valuation, an approach described as using "the wrong number in the wrong formula to get the right price".

   *backed by* `asmt-0048`

4. Solving the Black-Scholes model for volatility across a set of durations and strike prices constructs the implied volatility surface, an application that amounts to a coordinate transformation from the price domain to the volatility domain.

   *backed by* `asmt-0046`

5. Haug and Taleb argue that Black-Scholes merely recasts existing widely used models in terms of practically impossible dynamic hedging rather than risk, to make them compatible with mainstream neoclassical economic theory, and assert that Boness published an actually identical formula in 1964.

   *backed by* `asmt-0052`

**Source units (5)** `u-src-black-scholes-model-fa32a5b3-0046`, `u-src-black-scholes-model-fa32a5b3-0047`, `u-src-black-scholes-model-fa32a5b3-0048`, `u-src-black-scholes-model-fa32a5b3-0052`, `u-src-black-scholes-model-fa32a5b3-0071`

**Traceability** — idempotency key `e2698fb96aa919a3ff1fbe23650c83160433b4a827bb5d97fecc1677ceb01328` · queue event `q-e2698fb96aa919a3` · audits `audit-cand-010`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 11. Black-Scholes: history, reception and criticism

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-011-r1` v2

**Slug** `black-scholes-history-reception-and-criticism`

Who established the result and when, the prize it won, the trading it enabled, and the published objections to it -- including a priority claim that it was not new.

**Assertions (6)**

1. Louis Bachelier's 1900 thesis was the earliest publication to apply Brownian motion to derivative pricing, but it had little impact for many years and carried important limitations for application to modern markets.

   *backed by* `asmt-0004`

2. Black and Scholes invented the risk-neutral argument in 1968 by showing that dynamically revising a portfolio removes the security's expected return; they then lost money trying to trade the formula for lack of risk management, returned to academia in 1970, and published it in 1973 as "The Pricing of Options and Corporate Liabilities" in the Journal of Political Economy.

   *backed by* `asmt-0005`

3. Merton and Scholes received the 1997 Nobel Memorial Prize in Economic Sciences for the risk-neutral dynamic revision, which the committee credited with separating the option from the risk of the underlying security; Black, who died in 1995, was ineligible but named as a contributor.

   *backed by* `asmt-0006`

4. The Black-Scholes formula led to a boom in options trading and gave mathematical legitimacy to the activity, led by Cboe Global Markets.

   *backed by* `asmt-0004`

5. Warren Buffett wrote in his 2008 letter to Berkshire Hathaway shareholders that the Black-Scholes formula, though the standard for establishing the dollar liability for options, produces strange and even absurd results when applied to long-dated valuations.

   *backed by* `asmt-0053`

6. Ian Stewart said Black-Scholes had underpinned massive economic growth and that by 2007 the international financial system was trading derivatives valued at one quadrillion dollars per year, calling the equation the mathematical justification for that trading.

   *backed by* `asmt-0054`

**Labels**

- Attach the label(s) named in the findings.

**Source units (6)** `u-src-black-scholes-model-fa32a5b3-0004`, `u-src-black-scholes-model-fa32a5b3-0005`, `u-src-black-scholes-model-fa32a5b3-0006`, `u-src-black-scholes-model-fa32a5b3-0053`, `u-src-black-scholes-model-fa32a5b3-0054`, `u-src-black-scholes-model-fa32a5b3-0073`

**Traceability** — idempotency key `1f547975b90d71bf2055bd7ed34aa9047a4e9fca91ef4ea244d67a936e68a43f` · queue event `q-1f547975b90d71bf` · audits `audit-cand-011`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>

---

### 12. Black-Scholes: the risk-neutral measure and the Feynman-Kac route to the price

`create_or_update` · knowledge state **supported** · status `ready` · candidate `cand-012-r1` v2

**Slug** `black-scholes-the-risk-neutral-measure-and-the-feynman-kac-route-to-the-price`

The probabilistic reading of the model: the option price as an expectation under the equivalent martingale measure, reached without solving a PDE at all.

**Assertions (2)**

1. The Greeks measure the sensitivity of a derivative's or portfolio's value to a change in one parameter with the others held fixed; they are the partial derivatives of the price with respect to those parameters, and one Greek may be the partial derivative of another, as gamma is of delta.

   *backed by* `asmt-0027`

2. Black and Scholes showed for the European call and put that it is possible to create a hedged position -- long the stock, short the option -- whose value does not depend on the price of the stock, which is the result the whole model rests on.

   *backed by* `asmt-0027`

**Source units (2)** `u-src-black-scholes-model-fa32a5b3-0027`, `u-src-black-scholes-model-fa32a5b3-0065`

**Traceability** — idempotency key `a5125959ca143527501f40e03b4fe2700678130a2a68c2d7ef487845c2da84ee` · queue event `q-a5125959ca143527` · audits `audit-cand-012`

<details><summary>Provenance chain</summary>

- `approved_candidates` → `06_audit/candidates.approved.jsonl`
- `assessments` → `04_assessments/claim_assessments.jsonl`
- `audits` → `06_audit/audits.jsonl`
- `clusters` → `03_clusters/clusters.jsonl`
- `initial_candidates` → `05_candidates/candidates.initial.jsonl`
- `omissions` → `02_units/omissions.jsonl`
- `source_registry` → `01_normalized/source_registry.jsonl`
- `units` → `02_units/units.jsonl`

</details>
