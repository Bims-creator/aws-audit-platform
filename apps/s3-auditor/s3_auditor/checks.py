from botocore.exceptions import ClientError

from audit_common.finding import Finding, Severity
from audit_common.session import get_session


def check_public_buckets(session=None):
    session = session or get_session()
    s3 = session.client("s3")
    findings = []

    for bucket in s3.list_buckets()["Buckets"]:
        name = bucket["Name"]
        try:
            status = s3.get_bucket_policy_status(Bucket=name)
            is_public = status["PolicyStatus"]["IsPublic"]
        except ClientError as e:
            if e.response["Error"]["Code"] == "NoSuchBucketPolicy":
                is_public = False
            else:
                raise

        if is_public:
            findings.append(
                Finding(
                    resource=f"s3-bucket:{name}",
                    severity=Severity.CRITICAL,
                    message=f"S3 bucket '{name}' has a policy that makes it publicly accessible",
                    check_id="s3-001-public-bucket-policy",
                )
            )
    return findings


def check_unencrypted_buckets(session=None):
    session = session or get_session()
    s3 = session.client("s3")
    findings = []

    for bucket in s3.list_buckets()["Buckets"]:
        name = bucket["Name"]
        try:
            s3.get_bucket_encryption(Bucket=name)
        except ClientError as e:
            if e.response["Error"]["Code"] == "ServerSideEncryptionConfigurationNotFoundError":
                findings.append(
                    Finding(
                        resource=f"s3-bucket:{name}",
                        severity=Severity.MEDIUM,
                        message=f"S3 bucket '{name}' has no default encryption configured",
                        check_id="s3-002-bucket-encryption",
                    )
                )
            else:
                raise
    return findings
