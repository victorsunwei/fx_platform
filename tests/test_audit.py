from fx_platform.audit import AuditTrail

def test_audit_log_and_list():
    audit = AuditTrail()

    audit.log(
        actor="test_user",
        action="price_forward",
        payload={"pair": "EURUSD", "spot": "1.10"}
    )

    records = audit.list_records()

    assert len(records) == 1
    assert records[0].actor == "test_user"
    assert records[0].action == "price_forward"
    assert records[0].payload["pair"] == "EURUSD"
