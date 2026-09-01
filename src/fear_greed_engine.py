import numpy as np
import pandas as pd
from scipy.optimize import brentq

sentiment_multipliers = {
    "extreme fear": 2.00,
    "fear": 1.50,
    "neutral": 1.00,
    "greed": 0.75,
    "extreme greed": 0.50,
}

drawdown_thresholds = {
    "moderate": 0.10,
    "deep": 0.20,
}

def build_monthly_schedule(asset_data, fgi_data, yield_data, start_date, end_date):
    asset_data = asset_data.copy()
    fgi_data = fgi_data.copy()
    yield_data = yield_data.copy()

    for dataframe in [asset_data, fgi_data, yield_data]:
        dataframe["date"] = (
            pd.to_datetime(dataframe["date"])
            .astype("datetime64[ns]")
        )

    prices = asset_data.loc[
        asset_data["date"].between(start_date, end_date),
        ["date", "price"],
    ].copy()

    prices["month"] = prices["date"].dt.to_period("M")
    schedule = prices.groupby("month", as_index=False).first()[["date", "price"]]

    fgi_signal = fgi_data[
        ["date", "fear_greed", "rating"]
    ].rename(columns={"date": "fgi_date"})

    schedule = pd.merge_asof(
        schedule.sort_values("date"),
        fgi_signal.sort_values("fgi_date"),
        left_on="date",
        right_on="fgi_date",
        direction="backward",
        allow_exact_matches=False,
    )

    asset_signal = asset_data[
        ["date", "close", "market_peak", "asset_drawdown"]
    ].rename(columns={"date": "asset_signal_date"})

    schedule = pd.merge_asof(
        schedule.sort_values("date"),
        asset_signal.sort_values("asset_signal_date"),
        left_on="date",
        right_on="asset_signal_date",
        direction="backward",
        allow_exact_matches=False,
    )

    yield_signal = yield_data[
        ["date", "cash_yield_decimal"]
    ].rename(columns={"date": "yield_date"})

    schedule = pd.merge_asof(
        schedule.sort_values("date"),
        yield_signal.sort_values("yield_date"),
        left_on="date",
        right_on="yield_date",
        direction="backward",
        allow_exact_matches=True,
    )

    schedule = schedule.dropna(
        subset=[
            "fear_greed",
            "rating",
            "asset_drawdown",
        ]
    ).reset_index(drop=True)

    schedule["cash_yield_decimal"] = (
        schedule["cash_yield_decimal"]
        .ffill()
        .fillna(0.0)
        .clip(lower=0.0)
    )

    return schedule

def get_drawdown_multiplier(rating, asset_drawdown, thresholds):
    moderate = thresholds["moderate"]
    deep = thresholds["deep"]

    if rating == "extreme fear":
        if asset_drawdown <= -deep:
            return 3.00
        if asset_drawdown <= -moderate:
            return 2.50
        return 2.00

    if rating == "fear":
        if asset_drawdown <= -deep:
            return 2.00
        if asset_drawdown <= -moderate:
            return 1.75
        return 1.50

    return sentiment_multipliers[rating]


def get_reserve_deploy_fraction(rating, asset_drawdown, thresholds):
    moderate = thresholds["moderate"]
    deep = thresholds["deep"]

    if rating == "extreme fear":
        if asset_drawdown <= -deep:
            return 1.00
        if asset_drawdown <= -moderate:
            return 0.50

    if rating == "fear":
        if asset_drawdown <= -deep:
            return 0.50
        if asset_drawdown <= -moderate:
            return 0.25

    return 0.00

def simulate_portfolios(
    asset_data,
    schedule,
    start_date,
    end_date,
    contribution,
    core_share,
    use_treasury_cash=False,
):
    daily = asset_data.loc[
        asset_data["date"].between(start_date, end_date),
        ["date", "price"],
    ].copy().reset_index(drop=True)

    schedule_map = schedule.set_index("date").to_dict("index")

    state = {
        "dca": {"units": 0.0, "cash": 0.0, "invested": 0.0},
        "sentiment": {"units": 0.0, "cash": 0.0, "invested": 0.0},
        "drawdown": {"units": 0.0, "cash": 0.0, "invested": 0.0},
        "reserve": {"units": 0.0, "cash": 0.0, "invested": 0.0},
    }

    records = []
    transactions = []
    previous_date = None
    previous_cash_yield = 0.0

    for row in daily.itertuples(index=False):
        date = row.date
        price = row.price

        if previous_date is not None and use_treasury_cash:
            elapsed_days = (date - previous_date).days
            growth_factor = (1 + previous_cash_yield) ** (elapsed_days / 365.25)

            for strategy in ["sentiment", "drawdown", "reserve"]:
                state[strategy]["cash"] *= growth_factor

        contribution_flow = 0.0

        if date in schedule_map:
            signal = schedule_map[date]
            contribution_flow = contribution

            dca_purchase = contribution
            state["dca"]["units"] += dca_purchase / price
            state["dca"]["invested"] += dca_purchase

            state["sentiment"]["cash"] += contribution
            sentiment_multiplier = sentiment_multipliers[signal["rating"]]
            sentiment_target = contribution * sentiment_multiplier
            sentiment_purchase = min(
                sentiment_target,
                state["sentiment"]["cash"],
            )
            sentiment_constrained = sentiment_purchase + 1e-9 < sentiment_target
            state["sentiment"]["units"] += sentiment_purchase / price
            state["sentiment"]["cash"] -= sentiment_purchase
            state["sentiment"]["invested"] += sentiment_purchase

            state["drawdown"]["cash"] += contribution
            drawdown_multiplier = get_drawdown_multiplier(
                signal["rating"],
                signal["asset_drawdown"],
                drawdown_thresholds,
            )
            drawdown_target = contribution * drawdown_multiplier
            drawdown_purchase = min(
                drawdown_target,
                state["drawdown"]["cash"],
            )
            drawdown_constrained = drawdown_purchase + 1e-9 < drawdown_target
            state["drawdown"]["units"] += drawdown_purchase / price
            state["drawdown"]["cash"] -= drawdown_purchase
            state["drawdown"]["invested"] += drawdown_purchase

            core_purchase = contribution * core_share
            reserve_contribution = contribution * (1 - core_share)
            state["reserve"]["cash"] += reserve_contribution
            reserve_before_deploy = state["reserve"]["cash"]
            deploy_fraction = get_reserve_deploy_fraction(
                signal["rating"],
                signal["asset_drawdown"],
                drawdown_thresholds,
            )
            reserve_deploy = reserve_before_deploy * deploy_fraction
            reserve_purchase = core_purchase + reserve_deploy
            state["reserve"]["units"] += reserve_purchase / price
            state["reserve"]["cash"] -= reserve_deploy
            state["reserve"]["invested"] += reserve_purchase

            transactions.append(
                {
                    "date": date,
                    "price": price,
                    "fear_greed": signal["fear_greed"],
                    "rating": signal["rating"],
                    "fgi_date": signal["fgi_date"],
                    "asset_signal_date": signal["asset_signal_date"],
                    "asset_drawdown": signal["asset_drawdown"],
                    "cash_yield_decimal": signal["cash_yield_decimal"],
                    "contribution": contribution,
                    "dca_purchase": dca_purchase,
                    "sentiment_multiplier": sentiment_multiplier,
                    "sentiment_target": sentiment_target,
                    "sentiment_purchase": sentiment_purchase,
                    "sentiment_cash_constrained": sentiment_constrained,
                    "drawdown_multiplier": drawdown_multiplier,
                    "drawdown_target": drawdown_target,
                    "drawdown_purchase": drawdown_purchase,
                    "drawdown_cash_constrained": drawdown_constrained,
                    "reserve_core_purchase": core_purchase,
                    "reserve_contribution": reserve_contribution,
                    "reserve_before_deploy": reserve_before_deploy,
                    "reserve_deploy_fraction": deploy_fraction,
                    "reserve_deploy": reserve_deploy,
                    "reserve_purchase": reserve_purchase,
                }
            )

            previous_cash_yield = signal["cash_yield_decimal"]

        values = {}

        for strategy in state:
            values[f"{strategy}_units"] = state[strategy]["units"]
            values[f"{strategy}_cash"] = state[strategy]["cash"]
            values[f"{strategy}_invested"] = state[strategy]["invested"]
            values[f"{strategy}_value"] = (
                state[strategy]["units"] * price
                + state[strategy]["cash"]
            )

        records.append(
            {
                "date": date,
                "price": price,
                "contribution": contribution_flow,
                **values,
            }
        )

        previous_date = date

    daily_results = pd.DataFrame(records)
    transaction_results = pd.DataFrame(transactions)

    daily_results["cumulative_contributions"] = (
        daily_results["contribution"].cumsum()
    )

    for strategy in state:
        value = daily_results[f"{strategy}_value"]
        prior_value = value.shift(1)

        daily_results[f"{strategy}_daily_return"] = np.where(
            prior_value > 0,
            (value - daily_results["contribution"]) / prior_value - 1,
            np.nan,
        )

        daily_results[f"{strategy}_growth_index"] = (
            1 + daily_results[f"{strategy}_daily_return"].fillna(0.0)
        ).cumprod()

        running_peak = daily_results[f"{strategy}_growth_index"].cummax()
        daily_results[f"{strategy}_portfolio_drawdown"] = (
            daily_results[f"{strategy}_growth_index"]
            / running_peak
            - 1
        )

    return transaction_results, daily_results

def calculate_xirr(dates, cash_flows):
    dates = pd.to_datetime(pd.Series(dates))
    cash_flows = np.asarray(cash_flows, dtype=float)
    years = (dates - dates.iloc[0]).dt.days.to_numpy() / 365.25

    def npv(rate):
        return np.sum(cash_flows / np.power(1 + rate, years))

    return brentq(npv, -0.9999, 100.0)


def calculate_metrics(transactions, daily_results, strategy):
    final_value = daily_results[f"{strategy}_value"].iloc[-1]
    total_contributions = transactions["contribution"].sum()
    total_units = daily_results[f"{strategy}_units"].iloc[-1]
    total_invested = daily_results[f"{strategy}_invested"].iloc[-1]
    final_cash = daily_results[f"{strategy}_cash"].iloc[-1]

    average_purchase_price = (
        total_invested / total_units
        if total_units > 0
        else np.nan
    )

    units_per_1000 = total_units / total_contributions * 1000

    returns = daily_results[f"{strategy}_daily_return"].dropna()
    growth_index = daily_results[f"{strategy}_growth_index"]
    elapsed_years = (
        daily_results["date"].iloc[-1]
        - daily_results["date"].iloc[0]
    ).days / 365.25

    twr_total = growth_index.iloc[-1] - 1
    twr_annualized = growth_index.iloc[-1] ** (1 / elapsed_years) - 1
    annualized_volatility = returns.std(ddof=1) * np.sqrt(252)
    sharpe = (
        returns.mean() / returns.std(ddof=1) * np.sqrt(252)
        if returns.std(ddof=1) > 0
        else np.nan
    )
    max_drawdown = daily_results[
        f"{strategy}_portfolio_drawdown"
    ].min()

    cash_flow_dates = transactions["date"].tolist() + [
        daily_results["date"].iloc[-1]
    ]
    cash_flows = (
        (-transactions["contribution"]).tolist()
        + [final_value]
    )
    xirr = calculate_xirr(cash_flow_dates, cash_flows)

    if strategy == "sentiment":
        constrained_months = int(
            transactions["sentiment_cash_constrained"].sum()
        )
    elif strategy == "drawdown":
        constrained_months = int(
            transactions["drawdown_cash_constrained"].sum()
        )
    else:
        constrained_months = 0

    return {
        "Total contributions": total_contributions,
        "Total invested in asset": total_invested,
        "Final cash or reserve": final_cash,
        "Final portfolio value": final_value,
        "Total adjusted investment units": total_units,
        "Average adjusted purchase price": average_purchase_price,
        "Units per $1,000 contributed": units_per_1000,
        "Cash-constrained months": constrained_months,
        "Money-weighted return (XIRR)": xirr,
        "Time-weighted total return": twr_total,
        "Time-weighted annualized return": twr_annualized,
        "Annualized volatility": annualized_volatility,
        "Sharpe ratio": sharpe,
        "Maximum drawdown": max_drawdown,
    }


strategy_names = {
    "dca": "Standard DCA",
    "sentiment": "Sentiment Weighted",
    "drawdown": "Sentiment + Drawdown",
    "reserve": "Core + Tactical Reserve",
}
