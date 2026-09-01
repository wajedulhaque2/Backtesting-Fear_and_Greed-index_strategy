# Sentiment + Drawdown Research

## Research question

Does combining the Fear & Greed Index with the actual S&P 500 drawdown improve long-term contribution timing relative to Standard DCA and the sentiment-only strategy?

The structural hypothesis became:

$$
\text{Fear alone} \neq \text{cheap market}
$$

while:

$$
\text{Fear}+\text{material drawdown}
$$

may identify more attractive accumulation periods.

## Structural change

The strategy kept the original sentiment multipliers but increased the target when Fear or Extreme Fear coincided with a material prior market drawdown.

| Sentiment | Prior drawdown | Multiplier |
|---|---:|---:|
| Extreme Fear | less than 10% | 2.00x |
| Extreme Fear | 10% to less than 20% | 2.50x |
| Extreme Fear | 20% or more | 3.00x |
| Fear | less than 10% | 1.50x |
| Fear | 10% to less than 20% | 1.75x |
| Fear | 20% or more | 2.00x |
| Neutral | any | 1.00x |
| Greed | any | 0.75x |
| Extreme Greed | any | 0.50x |

The primary thresholds were fixed at 10% and 20% before the result was observed.

## No-lookahead control

The purchase occurs on the first SPY trading day of the month. Both signals must be strictly earlier than the purchase date:

$$
SignalDate_t^{FGI}<PurchaseDate_t
$$

$$
SignalDate_t^{DD}<PurchaseDate_t
$$

Market drawdown is:

$$
DD_t=\frac{P_t}{\max_{s\leq t}P_s}-1
$$

## Primary result

| Metric | Standard DCA | Sentiment Weighted | Sentiment + Drawdown |
|---|---:|---:|---:|
| Final portfolio value | **$54,582.93** | $54,151.47 | $54,284.09 |
| Adjusted units | **71.1595** | 70.5971 | 70.7699 |
| Average adjusted purchase price | **$470.77** | $474.52 | $473.36 |
| XIRR | **17.44%** | 17.15% | 17.24% |
| Annualized TWR | **15.15%** | 14.95% | 15.02% |
| Maximum drawdown | -24.50% | **-24.31%** | **-24.31%** |

Sentiment + Drawdown improved the sentiment-only final value by $132.62 and recovered part of the gap to DCA, but still finished $298.84 below Standard DCA.

## Structural lesson

The stronger signal exposed an execution constraint. Drawdown-confirmed opportunities occurred when the strategy often wanted to invest more than the cash it had accumulated. The next change therefore addressed capital availability directly rather than adding another signal threshold.
