from audit_common.finding import Finding, Severity
from audit_common.session import get_session


def check_users_without_mfa(session=None):
    session = session or get_session()
    iam = session.client("iam")
    findings = []

    paginator = iam.get_paginator("list_users")
    for page in paginator.paginate():
        for user in page["Users"]:
            username = user["UserName"]
            mfa_devices = iam.list_mfa_devices(UserName=username)["MFADevices"]
            if not mfa_devices:
                findings.append(
                    Finding(
                        resource=f"iam-user:{username}",
                        severity=Severity.HIGH,
                        message=f"IAM user '{username}' does not have MFA enabled",
                        check_id="iam-001-mfa-enabled",
                    )
                )
    return findings