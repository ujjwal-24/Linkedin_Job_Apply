"""Location preferences and optional numeric application answers."""
import re


def excluded_location(location, exclusions):
    """Match city names as whole phrases, ignoring case and extra whitespace."""
    normalized = " ".join(location.split())
    for city in exclusions:
        city = " ".join(city.split())
        if city and re.search(r"(?<!\w)" + re.escape(city) + r"(?!\w)", normalized, re.I):
            return city
    return None


def numeric_answers(value, *, salary=False):
    """Return base/monthly/lakh salary or base/month/week notice; None stays blank."""
    if value is None:
        return "", "", ""
    if salary:
        return str(value), str(round(value / 12, 2)), str(round(value / 100000, 2))
    return str(value), str(value // 30), str(value // 7)
