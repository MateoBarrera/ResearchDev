import argparse
from pathlib import Path

from synergy.console import (
    console,
    show_hashes,
    show_outputs,
    show_rank_chart,
    show_resource_mix,
    show_resource_termgraph,
    show_summary,
    show_termgraph,
)
from synergy.runner import run_case
from synergy.validation import validate_case


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
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate the case configuration without running the analysis",
    )
    parser.add_argument(
        "--termgraph",
        action="store_true",
        help="Show the robustness profile with termgraph after the run",
    )
    args = parser.parse_args()

    if bool(args.case) == bool(args.config):
        parser.error("Choose exactly one of --case or --config")

    config_path = CASES[args.case] if args.case else args.config
    if args.validate:
        validate_case(config_path, Path.cwd())
        console.print(f"[bold green]Configuración válida:[/bold green] {config_path}")
        return
    result = run_case(config_path=config_path, seed=args.seed)
    show_summary(result)
    show_resource_mix(result)
    show_rank_chart(result)
    if args.termgraph:
        show_termgraph(result)
        show_resource_termgraph(result)
    show_outputs(result)
    show_hashes(result["manifest"])


if __name__ == "__main__":
    main()
