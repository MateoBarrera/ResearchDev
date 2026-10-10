import argparse
from pathlib import Path

from synergy.runner import run_case


CASES = {
    "jamundi": "case_studies/jamundi/definition.yaml",
    "santa_rosalia": "case_studies/santa_rosalia/definition.yaml",
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a ResearchDev case study")
    parser.add_argument(
        "--case",
        choices=sorted(CASES),
        help="Named case study to execute",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to a case definition YAML file",
    )
    parser.add_argument(
        "--seed",
        nargs="+",
        type=float,
        help="Capacity-share values used to generate alternatives",
    )
    args = parser.parse_args()

    if bool(args.case) == bool(args.config):
        parser.error("Choose exactly one of --case or --config")

    config_path = CASES[args.case] if args.case else args.config
    result = run_case(config_path=config_path, seed=args.seed)
    print(f"Case study: {result['case_study']}")
    print(f"Alternatives: {result['alternative_count']}")
    print(f"Alternatives file: {result['alternatives_path']}")
    print(f"Ranking file: {result['ranking_path']}")


if __name__ == "__main__":
    main()
