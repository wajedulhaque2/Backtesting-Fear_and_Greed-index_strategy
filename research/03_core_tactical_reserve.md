# Core + Tactical Reserve Research

## Research question

Can a long-term investor improve on Standard DCA by keeping most monthly capital continuously invested while building a dedicated tactical reserve that is deployed only when investor fear coincides with a meaningful market drawdown?

## Structural change

The prior strategies created dry powder indirectly by investing less during Greed and Extreme Greed. This stage created dry powder deliberately every month.

Each $500 monthly contribution was split into:

$$
C_t^{Core}=0.80C=\$400
$$

and:

$$
C_t^{Reserve}=0.20C=\$100
$$

The core contribution was always invested. The reserve accumulated until a qualifying fear-and-drawdown event occurred.

| Sentiment | Prior drawdown | Reserve deployed |
|---|---:|---:|
| Extreme Fear | 20% or more | 100% |
| Extreme Fear | 10% to less than 20% | 50% |
| Fear | 20% or more | 50% |
| Fear | 10% to less than 20% | 25% |
| Any other condition | any | 0% |

The reserve consists only of contributed capital. The strategy does not borrow.

## Why this is structurally different

The economic question changed from:

> Can sentiment decide how much of each monthly contribution should be invested?

To:

> Can a mostly invested portfolio benefit from maintaining a small dedicated reserve for confirmed periods of fear?

This stage therefore tests capital management rather than another sentiment threshold.

## Primary result

| Metric | Standard DCA | Sentiment Weighted | Sentiment + Drawdown | Core + Tactical Reserve |
|---|---:|---:|---:|---:|
| Final portfolio value | **$54,582.93** | $54,151.47 | $54,284.09 | $53,116.68 |
| Final cash or reserve | $0 | $0 | $0 | $4,007.81 |
| Average adjusted purchase price | $470.77 | $474.52 | $473.36 | **$460.65** |
| XIRR | **17.44%** | 17.15% | 17.24% | 16.45% |
| Annualized volatility | 16.72% | 16.56% | 16.59% | **15.35%** |
| Maximum drawdown | -24.50% | -24.31% | -24.31% | **-21.75%** |

## Reserve utilization

The reserve received $6,700 of contributions and deployed roughly $2,692 across seven qualifying events. About $4,008 remained undeployed at the end of the primary sample, so only about 40% of reserve contributions were used.

## Allocation robustness

| Core / reserve | Final value | Ending reserve | XIRR | Maximum drawdown |
|---|---:|---:|---:|---:|
| 90 / 10 | **$53,849.81** | $2,003.91 | **16.95%** | -23.14% |
| 80 / 20 | $53,116.68 | $4,007.81 | 16.45% | -21.75% |
| 70 / 30 | $52,383.56 | $6,011.72 | 15.95% | **-20.33%** |

Higher core allocation improved final wealth, while larger reserves reduced drawdown.

## Structural lesson

The dedicated reserve solved the earlier cash-availability problem, but it over-solved it. Too much capital remained idle after qualifying events stopped. This motivated testing realistic cash yield and then generalizing the full framework into a reusable ticker analyzer rather than continuing to tune thresholds after observing the results.
