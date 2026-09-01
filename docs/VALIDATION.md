# Analyzer Validation

The generalized notebook was tested on multiple Yahoo Finance symbols to confirm that the research engine works beyond its original SPY use case.

The purpose of these runs was software and methodology validation, not ticker-specific strategy optimization.

## SPY

SPY reproduced the established S&P 500 baseline.

| Strategy | Final value | XIRR | Maximum drawdown |
|---|---:|---:|---:|
| Standard DCA | $54,582.93 | 17.44% | -24.50% |
| Sentiment Weighted | $54,151.47 | 17.15% | -24.31% |
| Sentiment + Drawdown | $54,284.09 | 17.24% | -24.31% |
| Core + Tactical Reserve | $53,116.68 | 16.45% | -21.75% |

The generalized implementation therefore reproduced the known research benchmark before being tested on other assets.

## AAPL

The analyzer completed successfully on an individual US equity. Standard DCA produced the highest final value in the high-confidence sample, while Sentiment + Drawdown was the strongest timing strategy. The tactical reserve reduced drawdown and slightly improved average purchase price but held cash outside the asset.

This run confirmed that the framework can use an individual stock's own drawdown history while retaining Fear & Greed as a broad US-market sentiment signal.

## SHEL.L

The analyzer completed successfully on a London-listed equity using the Yahoo Finance `.L` suffix.

Standard DCA led the high-confidence sample, while the extended-history result changed the strategy ranking. The deterministic summary correctly identified the conclusion as sample-dependent rather than forcing the primary-sample winner into every period.

This is useful because it validates both non-US ticker handling and the rules-based interpretation logic when robustness tests disagree.

## RR.L

The analyzer also completed successfully on Rolls-Royce Holdings using the `.L` suffix.

Standard DCA remained the strongest wealth-accumulation strategy in the main sample, Treasury sensitivity, and extended history. The deterministic summary therefore correctly identified a more consistent ranking than in the Shell test.

## Cross-market interpretation

Fear & Greed is a US-market sentiment indicator. For London-listed securities, the notebook explicitly labels the experiment as a cross-market sentiment test rather than a local UK sentiment measure or company-specific signal.

## Validation conclusion

Across SPY, AAPL, SHEL.L, and RR.L, the analyzer demonstrated:

1. Yahoo Finance ticker flexibility.
2. US and London-listed suffix handling.
3. Asset-specific drawdown calculation.
4. Equal-capital strategy accounting.
5. Long-history robustness handling.
6. Treasury cash-yield sensitivity.
7. Reserve-allocation sensitivity.
8. Deterministic interpretation that adapts when the strategy ranking changes.
