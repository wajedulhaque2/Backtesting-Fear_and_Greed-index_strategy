# Sentiment Weighted S&P 500 Research

## Research question

Does changing the size of monthly S&P 500 purchases using the Fear & Greed Index improve long-term investment outcomes relative to standard dollar cost averaging when both strategies receive exactly the same external capital?

## Structure

Standard DCA invests the full monthly contribution:

$$
I_t^{DCA}=C
$$

The sentiment strategy uses predefined multipliers:

| Fear & Greed regime | Multiplier |
|---|---:|
| Extreme Fear | 2.00x |
| Fear | 1.50x |
| Neutral | 1.00x |
| Greed | 0.75x |
| Extreme Greed | 0.50x |

The target investment is:

$$
T_t^{S}=C\times m_t
$$

Actual investment cannot exceed available contributed cash. Any unused capital rolls forward as cash.

## Controls

1. Each strategy receives $500 on the first SPY trading day of every month.
2. No selling, borrowing, or leverage is allowed.
3. Fractional adjusted investment units are allowed.
4. Fear & Greed must be known before the purchase date.
5. The high-confidence sample begins on 1 February 2021.
6. The earlier Fear & Greed archive is used only as a lower-confidence robustness sample.
7. Strategy thresholds are fixed before results are evaluated.

## Primary result

For 1 February 2021 through 31 August 2026, both strategies received $33,500.

| Metric | Standard DCA | Sentiment Weighted |
|---|---:|---:|
| Final portfolio value | **$54,582.93** | $54,151.47 |
| Adjusted units | **71.1595** | 70.5971 |
| Average adjusted purchase price | **$470.77** | $474.52 |
| XIRR | **17.44%** | 17.15% |
| Annualized TWR | **15.15%** | 14.95% |
| Maximum drawdown | -24.50% | **-24.31%** |

The sentiment strategy finished $431.46, or about 0.79%, below Standard DCA.

## Structural lesson

Fear alone did not reliably identify attractive entry prices. The strategy also withheld capital during Greed, creating opportunity cost during persistent market advances. This motivated adding an independent valuation-state proxy based on the market's actual drawdown from its prior peak.
