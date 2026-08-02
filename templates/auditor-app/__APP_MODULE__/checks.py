from audit_common.finding import Finding, Severity
from audit_common.session import get_session


def check_placeholder(session=None):
    """TODO: replace with a real check for __APP_NAME__."""
    session = session or get_session()
    findings = []
    return findings
