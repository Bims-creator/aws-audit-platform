from unittest.mock import MagicMock

from audit_common.finding import Severity
from iam_auditor.checks import check_users_without_mfa


def test_flags_user_without_mfa():
    mock_session = MagicMock()
    mock_iam = mock_session.client.return_value
    mock_paginator = mock_iam.get_paginator.return_value
    mock_paginator.paginate.return_value = [
        {"Users": [{"UserName": "no-mfa-user"}]}
    ]
    mock_iam.list_mfa_devices.return_value = {"MFADevices": []}

    findings = check_users_without_mfa(session=mock_session)

    assert len(findings) == 1
    assert findings[0].resource == "iam-user:no-mfa-user"
    assert findings[0].severity == Severity.HIGH


def test_no_finding_when_mfa_enabled():
    mock_session = MagicMock()
    mock_iam = mock_session.client.return_value
    mock_paginator = mock_iam.get_paginator.return_value
    mock_paginator.paginate.return_value = [
        {"Users": [{"UserName": "mfa-user"}]}
    ]
    mock_iam.list_mfa_devices.return_value = {
        "MFADevices": [{"SerialNumber": "arn:aws:iam::123:mfa/mfa-user"}]
    }

    findings = check_users_without_mfa(session=mock_session)

    assert findings == []