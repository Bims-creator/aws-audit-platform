from __APP_MODULE__.checks import check_placeholder


def test_placeholder_returns_list():
    findings = check_placeholder(session=object())
    assert isinstance(findings, list)
