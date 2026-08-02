from s3_auditor.checks import check_placeholder


def main():
    findings = check_placeholder()
    if not findings:
        print("No findings.")
        return

    for f in findings:
        print(f"[{f.severity.value.upper()}] {f.check_id} - {f.resource}: {f.message}")


if __name__ == "__main__":
    main()
