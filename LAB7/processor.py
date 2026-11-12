"""Hardened version of processor.py (Lab 7).

Every function validates its input and returns an "Invalid ..." message
instead of raising. Valid inputs behave exactly as before.
"""

TIER_RATES = {
    "VIP": 150.0,
    "PREMIUM": 90.0,
    "GENERAL": 45.0,
}
MAX_ROW = 1000
MAX_AGE = 120


def _is_ascii_int(s, max_len):
    """True only for a short string of plain ASCII digits (no signs, no unicode digits)."""
    return isinstance(s, str) and s.isascii() and s.isdigit() and len(s) <= max_len


def decode_promo_voucher(voucher_code):
    if not isinstance(voucher_code, str):
        return "Invalid voucher: input must be a string"
    parts = voucher_code.strip().split('-')
    if len(parts) != 2:
        return "Invalid voucher: expected format PREFIX-PERCENT"
    prefix, pct_str = parts[0].strip(), parts[1].strip()
    if not prefix or not prefix.isalnum():
        return "Invalid voucher: prefix must be non-empty letters/digits"
    if not _is_ascii_int(pct_str, 3):
        return "Invalid voucher: percentage must be a whole number"
    percentage = int(pct_str)
    if percentage > 100:
        return "Invalid voucher: percentage must be 0-100"
    return f"Valid {prefix.upper()}: {percentage}% OFF"


def calculate_seat_tier_price(tier_spec):
    if not isinstance(tier_spec, str):
        return "Invalid tier spec: input must be a string"
    parts = tier_spec.split('@')
    if len(parts) != 2:
        return "Invalid tier spec: expected format TIER@ROW"
    tier, row_str = parts[0].strip().upper(), parts[1].strip()
    if tier not in TIER_RATES:
        return "Invalid tier spec: unknown tier (VIP, PREMIUM, GENERAL)"
    if not _is_ascii_int(row_str, 4):
        return "Invalid tier spec: row must be a whole number"
    row = int(row_str)
    if not 1 <= row <= MAX_ROW:
        return f"Invalid tier spec: row must be 1-{MAX_ROW}"
    return TIER_RATES[tier] + (row * 2.0)


def parse_attendee_badge(badge_csv):
    if not isinstance(badge_csv, str):
        return "Invalid badge: input must be a string"
    tokens = badge_csv.split(',')
    if len(tokens) != 3:
        return "Invalid badge: expected format Name,Age,Seat"
    name, age_str, seat = (t.strip() for t in tokens)
    if not name:
        return "Invalid badge: name is empty"
    if not seat:
        return "Invalid badge: seat is empty"
    if not _is_ascii_int(age_str, 3):
        return "Invalid badge: age must be a whole number"
    age = int(age_str)
    if age > MAX_AGE:
        return f"Invalid badge: age must be 0-{MAX_AGE}"
    category = "Child" if age < 18 else "Adult"
    return f"{name} [{category}] - Seat {seat}"


def main():
    print("==== Running decode_promo_voucher ====")
    v_input = input("Enter voucher (e.g. EARLY-20): ")
    print("Voucher:", decode_promo_voucher(v_input))

    print("\n==== Running calculate_seat_tier_price ====")
    t_input = input("Enter tier spec (e.g. VIP@4): ")
    print("Seat Price: $", calculate_seat_tier_price(t_input))

    print("\n==== Running parse_attendee_badge ====")
    b_input = input("Enter badge CSV (Name,Age,Seat): ")
    print("Badge:", parse_attendee_badge(b_input))


if __name__ == "__main__":
    main()
