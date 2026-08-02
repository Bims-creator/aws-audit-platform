from s3_auditor.checks import check_public_buckets, check_unencrypted_buckets


def main():
    findings = check_public_buckets() + check_unencrypted_buckets()
    if not findings:
        print("No findings.")
        return

    for f in findings:
        print(f"[{f.severity.value.upper()}] {f.check_id} - {f.resource}: {f.message}")


if __name__ == "__main__":
    main()
