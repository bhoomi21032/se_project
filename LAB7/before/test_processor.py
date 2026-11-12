from hypothesis import given, strategies as st
from processor import decode_promo_voucher, calculate_seat_tier_price, parse_attendee_badge


# ---------- 1. Fuzz: must never crash ----------
@given(st.text() | st.none())
def test_decode_promo_voucher_no_crash(s):
    try:
        decode_promo_voucher(s)
    except Exception as e:
        assert False, f"decode_promo_voucher crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_calculate_seat_tier_price_safe(s):
    try:
        calculate_seat_tier_price(s)
    except Exception as e:
        assert False, f"calculate_seat_tier_price crashed with: {e!r} on input {s!r}"


@given(st.text() | st.none())
def test_parse_attendee_badge_safe(s):
    try:
        parse_attendee_badge(s)
    except Exception as e:
        assert False, f"parse_attendee_badge crashed with: {e!r} on input {s!r}"


# ---------- 2. Extra properties: valid inputs still give correct output ----------
@given(st.from_regex(r"[A-Za-z0-9]{1,10}", fullmatch=True), st.integers(0, 100))
def test_valid_voucher_roundtrip(prefix, pct):
    assert decode_promo_voucher(f"{prefix}-{pct}") == f"Valid {prefix.upper()}: {pct}% OFF"


@given(st.sampled_from(["VIP", "PREMIUM", "GENERAL"]), st.integers(1, 1000))
def test_valid_tier_price(tier, row):
    rates = {"VIP": 150.0, "PREMIUM": 90.0, "GENERAL": 45.0}
    assert calculate_seat_tier_price(f"{tier}@{row}") == rates[tier] + row * 2.0


@given(st.from_regex(r"[A-Za-z]{1,10}", fullmatch=True), st.integers(0, 120),
       st.from_regex(r"[A-Z][0-9]{1,3}", fullmatch=True))
def test_valid_badge(name, age, seat):
    cat = "Child" if age < 18 else "Adult"
    assert parse_attendee_badge(f"{name},{age},{seat}") == f"{name} [{cat}] - Seat {seat}"


@given(st.text() | st.none())
def test_invalid_inputs_return_str(s):
    # hardened functions always return something printable, never raise
    assert isinstance(decode_promo_voucher(s), str)
    assert isinstance(parse_attendee_badge(s), str)
    assert isinstance(calculate_seat_tier_price(s), (str, float))
