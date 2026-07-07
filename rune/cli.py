import sys

from rune.stats import compute_stats, format_report, load_ledger


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv

    if argv and argv[0] == "stats":
        rows = load_ledger()
        print(format_report(compute_stats(rows)))
        return 0

    print("usage: python -m rune.cli stats")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
