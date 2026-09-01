# Research Evolution

This document records the economic and structural changes made during the project. It intentionally excludes local environment, package, editor, and dependency troubleshooting because those did not change the research design.

## Stage 1: Sentiment Weighted

The first experiment compared standard S&P 500 DCA with a contribution strategy driven only by Fear & Greed.

The predefined multipliers were:

| Regime | Multiplier |
|---|---:|
| Extreme Fear | 2.00x |
| Fear | 1.50x |
| Neutral | 1.00x |
| Greed | 0.75x |
| Extreme Greed | 0.50x |

Unused contributions remained as cash and rolled forward. The strategy never borrowed and therefore could not invest more than the cash already contributed.

### Finding

In the primary SPY sample, Standard DCA finished at $54,582.93 versus $54,151.47 for Sentiment Weighted. The sentiment strategy also accumulated fewer adjusted units and had a higher average adjusted purchase price.

### Structural lesson

Fear alone was not sufficient evidence that the asset was cheap. Withholding cash during persistent Greed also created opportunity cost.

## Stage 2: Sentiment + Drawdown

The next structural change added the selected asset's actual drawdown from its previous peak.

The central hypothesis became:

$$
\text{Fear alone} \neq \text{cheap market}
$$

while:

$$
\text{Fear} + \text{material drawdown}
$$

might identify more attractive accumulation periods.

The primary drawdown thresholds were fixed at 10% and 20% before results were evaluated.

### Finding

Sentiment + Drawdown improved the primary SPY final value from $54,151.47 to $54,284.09, recovering part of the gap to DCA, but still finished $298.84 below Standard DCA.

### Structural lesson

The stronger signal exposed an execution constraint. The strategy often wanted to invest more during strong fear-and-drawdown events but did not have enough accumulated cash to do so.

## Stage 3: Core + Tactical Reserve

The next change addressed cash availability directly instead of adding another indicator.

Each $500 monthly contribution was split into:

$$
C_t^{Core}=0.80C=\$400
$$

and:

$$
C_t^{Reserve}=0.20C=\$100
$$

The core contribution was invested every month. The reserve accumulated and was deployed only when Fear or Extreme Fear coincided with a 10% or 20% drawdown.

### Finding

The reserve structure reduced the primary SPY maximum drawdown to -21.75% and lowered the average adjusted purchase price to $460.65, but final wealth fell to $53,116.68.

The reserve received $6,700 of contributions, deployed roughly $2,692, and ended with about $4,008 still in cash. This means only about 40% of the reserve was used.

### Structural lesson

The dedicated reserve solved the problem of not having cash available, but over-solved it. Too much capital remained idle after the qualifying deployment events ended.

## Stage 4: Robustness and Cash Yield

The analysis was expanded without changing the core hypotheses.

1. The primary high-confidence Fear & Greed sample was retained.
2. A lower-confidence long-history sample beginning in 2011 was added.
3. Reserve allocations of 90/10, 80/20, and 70/30 were tested as predefined structural sensitivities.
4. Idle cash was allowed to earn a short-term Treasury proxy using `^IRX`.
5. Drawdown history was extended before the investment sample so the running peak would not reset artificially at the backtest start.

### Finding

Treasury yield improved the cash-holding strategies but did not overturn the primary SPY ranking. Larger reserve allocations reduced drawdown but also reduced final wealth. The 90/10 allocation was the strongest of the predefined reserve splits.

### Structural lesson

The underperformance was not solely caused by assuming a 0% return on cash. The larger issue remained the opportunity cost of capital held outside the market.

## Stage 5: Generalized Ticker Analyzer

The final structural change converted the S&P 500 research into a reusable tool.

The analyzer now:

1. Accepts a Yahoo Finance ticker as its main input.
2. Dynamically adjusts the feasible analysis history to the selected asset.
3. Uses the selected asset's own unadjusted close for drawdown calculations.
4. Uses adjusted prices as the portfolio total-return proxy.
5. Runs all four strategies under the same capital rules.
6. Includes primary and long-history analysis.
7. Includes Treasury cash-yield sensitivity.
8. Includes predefined reserve-allocation robustness.
9. Produces deterministic, rules-based interpretation from calculated metrics.
10. Warns when a non-US security is being tested with a US-market sentiment indicator.

## Why the project stopped here

The research did not continue adding thresholds or optimizing allocations after observing the results. The accumulated evidence supported a stronger conclusion than another round of tuning: simple systematic DCA is difficult to improve using these sentiment-timing overlays, while tactical cash can trade some wealth accumulation for lower drawdown.
