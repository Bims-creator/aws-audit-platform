from s3_auditor.checks import check_placeholder


def test_placeholder_returns_list():
    findings = check_placeholder(session=object())
    assert isinstance(findings, list)
