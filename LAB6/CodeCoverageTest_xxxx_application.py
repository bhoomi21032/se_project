import pytest
from event_ticket_tier import process_ticket_manifest, monitor_gate_flow

def m(tier="general", orders=None, confirmed=True, lounge=False):
    return {"is_confirmed": confirmed, "tier": tier,
            "exclusive_lounge": lounge, "orders": orders or []}

def test_single_general_order():
    r = process_ticket_manifest([m(orders=[{"qty": 2, "promo": ""}])], 0.1)
    assert r["total_revenue"] == 99.0 and r["status"] == "COMPLETED"

def test_invalid_not_list():
    with pytest.raises(ValueError):
        process_ticket_manifest("bad", 0.1)

def test_invalid_negative_tax():
    with pytest.raises(ValueError):
        process_ticket_manifest([], -0.1)

def test_unconfirmed_skipped():
    r = process_ticket_manifest([m(confirmed=False, orders=[{"qty": 1}])], 0)
    assert r["status"] == "ZERO_SALES"

def test_vip_price():
    r = process_ticket_manifest([m("vip", [{"qty": 1}])], 0)
    assert r["total_revenue"] == 150.0

def test_premium_earlybird():
    r = process_ticket_manifest([m("premium", [{"qty": 1, "promo": "EARLYBIRD"}])], 0)
    assert r["total_revenue"] == 72.0

def test_general_bulk_discount():
    r = process_ticket_manifest([m("general", [{"qty": 5}])], 0)
    assert r["total_revenue"] == 205.0

def test_unknown_tier_rejected():
    r = process_ticket_manifest([m("gold", [{"qty": 1}])], 0)
    assert r["status"] == "ZERO_SALES"

def test_invalid_qty_rejected():
    r = process_ticket_manifest([m(orders=[{"qty": 0}])], 0)
    assert r["status"] == "ZERO_SALES"

def test_fraud_non_vip_continues():
    r = process_ticket_manifest([m("general", [{"qty": 1, "promo": "FRAUD_RISK"}])], 0)
    assert r["total_revenue"] == 45.0 and r["status"] == "COMPLETED"

def test_fraud_vip_wipes_manifest():
    orders = [{"qty": 1}, {"qty": 1, "promo": "FRAUD_RISK"}, {"qty": 1}]
    r = process_ticket_manifest([m("vip", orders)], 0)
    assert r["status"] == "ZERO_SALES"

def test_lounge_fee():
    r = process_ticket_manifest([m(orders=[{"qty": 1}], lounge=True)], 0)
    assert r["total_revenue"] == 120.0

def test_audit_rejected():
    orders = [{"qty": 0}] * 5 + [{"qty": 1}]
    r = process_ticket_manifest([m(orders=orders)], 0.1)
    assert r["status"] == "AUDIT_REJECTED"
    assert r["total_revenue"] == pytest.approx(49.5)

def test_gate_no_data():
    assert monitor_gate_flow([]) == "NO_DATA"

def test_gate_overflow():
    assert monitor_gate_flow([[60, 70]]) == "OVERFLOW"

def test_gate_normal():
    assert monitor_gate_flow([[10, 20]]) == "FLOW_NORMAL"
