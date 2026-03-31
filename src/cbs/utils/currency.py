"""Supported currencies and FX helpers."""

SUPPORTED_CURRENCIES = {"EUR", "USD", "GBP", "CZK", "PLN", "HUF", "CHF", "SEK", "NOK", "DKK", "JPY"}

# Simplified FX rates against EUR for demonstration purposes.
FX_RATES: dict[str, float] = {
    "EUR/USD": 1.08,
    "EUR/GBP": 0.86,
    "EUR/CZK": 25.30,
    "EUR/PLN": 4.33,
    "EUR/HUF": 395.0,
    "EUR/CHF": 0.96,
    "EUR/SEK": 11.40,
    "EUR/NOK": 11.70,
    "EUR/DKK": 7.46,
    "EUR/JPY": 163.0,
}


def get_fx_rate(source: str, target: str) -> float | None:
    """Return a simplified FX rate between two currencies."""
    if source == target:
        return 1.0
    pair = f"{source}/{target}"
    if pair in FX_RATES:
        return FX_RATES[pair]
    inverse = f"{target}/{source}"
    if inverse in FX_RATES:
        return round(1.0 / FX_RATES[inverse], 6)
    return None
