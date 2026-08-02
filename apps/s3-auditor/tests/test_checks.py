from unittest.mock import MagicMock

from botocore.exceptions import ClientError

from audit_common.finding import Severity
from s3_auditor.checks import check_public_buckets, check_unencrypted_buckets


def _client_error(code):
    return ClientError({"Error": {"Code": code, "Message": "test"}}, "TestOperation")


def test_flags_public_bucket():
    mock_session = MagicMock()
    mock_s3 = mock_session.client.return_value
    mock_s3.list_buckets.return_value = {"Buckets": [{"Name": "my-bucket"}]}
    mock_s3.get_bucket_policy_status.return_value = {"PolicyStatus": {"IsPublic": True}}

    findings = check_public_buckets(session=mock_session)

    assert len(findings) == 1
    assert findings[0].severity == Severity.CRITICAL


def test_no_finding_when_bucket_private():
    mock_session = MagicMock()
    mock_s3 = mock_session.client.return_value
    mock_s3.list_buckets.return_value = {"Buckets": [{"Name": "my-bucket"}]}
    mock_s3.get_bucket_policy_status.side_effect = _client_error("NoSuchBucketPolicy")

    findings = check_public_buckets(session=mock_session)

    assert findings == []


def test_flags_unencrypted_bucket():
    mock_session = MagicMock()
    mock_s3 = mock_session.client.return_value
    mock_s3.list_buckets.return_value = {"Buckets": [{"Name": "my-bucket"}]}
    mock_s3.get_bucket_encryption.side_effect = _client_error("ServerSideEncryptionConfigurationNotFoundError")

    findings = check_unencrypted_buckets(session=mock_session)

    assert len(findings) == 1
    assert findings[0].severity == Severity.MEDIUM


def test_no_finding_when_bucket_encrypted():
    mock_session = MagicMock()
    mock_s3 = mock_session.client.return_value
    mock_s3.list_buckets.return_value = {"Buckets": [{"Name": "my-bucket"}]}
    mock_s3.get_bucket_encryption.return_value = {"ServerSideEncryptionConfiguration": {}}

    findings = check_unencrypted_buckets(session=mock_session)

    assert findings == []
