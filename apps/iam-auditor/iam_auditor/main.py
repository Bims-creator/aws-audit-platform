from iam_auditor.checks import check_users_without_mfa


def main():
    findings = check_users_without_mfa()
    if not findings:
        print("No findings.")
        return

    for f in findings:
        print(f"[{f.severity.value.upper()}] {f.check_id} - {f.resource}: {f.message}")


if __name__ == "__main__":
    main()