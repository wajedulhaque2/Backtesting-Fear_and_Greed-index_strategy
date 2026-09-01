# Fear & Greed Ticker Strategy Analyzer

A reproducible backtesting project that asks a simple question: can investor sentiment improve long-term monthly accumulation relative to standard dollar cost averaging?

The project began as a fixed S&P 500 experiment and developed into a reusable Yahoo Finance ticker analyzer. The research progression is preserved in `research/`, while the portfolio-ready analyzer is in `notebooks/` and the reusable strategy engine is in `src/`.

## Research question

Does changing monthly investment size using the Fear & Greed Index, asset drawdown confirmation, or a dedicated tactical reserve improve long-term outcomes relative to investing the same external capital systematically?

## Strategy framework

1. **Standard DCA** invests the full monthly contribution.
2. **Sentiment Weighted** changes the monthly target using predefined Fear & Greed multipliers.
3. **Sentiment + Drawdown** increases the target when Fear or Extreme Fear coincides with a material asset drawdown.
4. **Core + Tactical Reserve** keeps most capital continuously invested while accumulating a dedicated reserve for confirmed fear-and-drawdown events.
5. **Cash Yield Sensitivity** tests whether allowing idle balances to earn a short-term Treasury proxy changes the conclusions.

## Research evolution

The project developed through structural stages rather than post-hoc parameter tuning.

1. **Sentiment weighting:** tested whether Fear & Greed alone could improve monthly S&P 500 contribution timing.
2. **Drawdown confirmation:** added market drawdown after the sentiment-only strategy showed that fear does not necessarily mean the market is cheap.
3. **Dedicated reserve:** changed the capital-management structure after the drawdown strategy frequently lacked cash when its strongest signals arrived.
4. **Robustness and cash yield:** tested longer history, predefined reserve allocations, and a Treasury cash-rate proxy without changing the central hypothesis.
5. **Generalized analyzer:** converted the S&P 500 research into a reusable Yahoo Finance ticker tool with deterministic interpretation and market-context warnings for non-US securities.

See [`docs/RESEARCH_EVOLUTION.md`](docs/RESEARCH_EVOLUTION.md) for the full rationale and evidence chain.

## Primary SPY finding

For the high-confidence Fear & Greed sample from 1 February 2021 through 31 August 2026, each strategy received the same $33,500 of external capital.

| Metric | Standard DCA | Sentiment Weighted | Sentiment + Drawdown | Core + Tactical Reserve |
|---|---:|---:|---:|---:|
| Final portfolio value | **$54,582.93** | $54,151.47 | $54,284.09 | $53,116.68 |
| XIRR | **17.44%** | 17.15% | 17.24% | 16.45% |
| Annualized volatility | 16.72% | 16.56% | 16.59% | **15.35%** |
| Maximum drawdown | -24.50% | -24.31% | -24.31% | **-21.75%** |
| Average adjusted purchase price | $470.77 | $474.52 | $473.36 | **$460.65** |

The main result is a disciplined negative finding: the timing overlays changed entry price and risk characteristics, but standard monthly DCA produced the highest final wealth in the primary SPY sample.

## What changed structurally

1. Sentiment alone withheld capital during Greed and attempted to deploy more during Fear.
2. Drawdown confirmation improved the signal but exposed an execution problem because the strategy often had insufficient accumulated cash during strong signals.
3. The tactical reserve solved the cash-availability problem by deliberately creating dry powder every month, but too much reserve remained idle and reduced long-term wealth accumulation.
4. Treasury cash yield narrowed the gap but did not overturn the primary SPY ranking.
5. The final analyzer generalized the framework to arbitrary Yahoo Finance symbols and added deterministic rules-based summaries rather than AI-generated interpretation.

## Ticker analyzer

Open:

`notebooks/Fear_Greed_Ticker_Strategy_Analyzer.ipynb`

Change only:

```python
asset_ticker = "SPY"
```

Examples:

```text
AAPL
MSFT
NVDA
SHEL.L
RR.L
SPY
QQQ
```

Then run the notebook from top to bottom.

The core simulation and performance calculations are separated into `src/fear_greed_engine.py` so the strategy logic can be reviewed independently of the notebook presentation layer.

## Non-US market context

Fear & Greed is a broad US-market sentiment indicator. For symbols such as `SHEL.L` and `RR.L`, the analyzer explicitly treats the exercise as a cross-market sentiment test rather than a local-market or company-specific sentiment measure.

## Data

1. Asset prices are downloaded through Yahoo Finance using `yfinance`.
2. Fear & Greed history uses the maintained `whit3rabbit/fear-greed-data` dataset.
3. The primary sample begins on 1 February 2021 because the maintained dataset identifies the later CNN-derived history as the higher-confidence period.
4. Earlier Fear & Greed observations are retained only for extended robustness analysis.
5. `^IRX` is used as an approximate 13-week Treasury bill cash-rate proxy in the cash-yield sensitivity.

## Methodological controls

1. Every strategy receives the same external monthly contribution.
2. The purchase date is the first trading day of each month.
3. Fear & Greed and drawdown signals must be known strictly before the purchase date.
4. No strategy sells, borrows, or uses leverage.
5. Fractional adjusted investment units are allowed.
6. Strategy thresholds are specified before evaluating ticker-level results.
7. Drawdown history begins before the analysis window so the running market peak is not artificially reset.

## Validation

The generalized analyzer was run successfully on:

1. `SPY`, a US ETF.
2. `AAPL`, a US individual equity.
3. `SHEL.L`, a London-listed equity.
4. `RR.L`, a London-listed equity.

The validation runs confirm that the ticker engine, Yahoo suffix handling, strategy comparison, robustness tests, and deterministic summary logic operate across both US and UK-listed securities. See [`docs/VALIDATION.md`](docs/VALIDATION.md).

## Repository structure

```text
.
├── README.md
├── requirements.txt
├── notebooks/
│   └── Fear_Greed_Ticker_Strategy_Analyzer.ipynb
├── src/
│   ├── __init__.py
│   └── fear_greed_engine.py
├── research/
│   ├── 01_sentiment_weighted.md
│   ├── 02_sentiment_drawdown.md
│   └── 03_core_tactical_reserve.md
└── docs/
    ├── RESEARCH_EVOLUTION.md
    └── VALIDATION.md
```

## Key takeaway

Across the research progression, increasingly sophisticated sentiment timing rules improved some aspects of execution, purchase price, or downside risk, but simple systematic monthly investing remained difficult to beat on final wealth. The project therefore emphasizes research discipline, no-lookahead implementation, robustness checks, and transparent negative results rather than strategy optimization after observing the outcome.
