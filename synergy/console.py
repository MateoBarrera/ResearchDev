from __future__ import annotations

from contextlib import contextmanager
import subprocess
import sys
from pathlib import Path
from typing import Iterator

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table
from rich.text import Text

console = Console()


@contextmanager
def pipeline_progress() -> Iterator[Progress]:
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
    )
    with progress:
        yield progress


def show_run_header(case_study: str, capacity: float, seed_size: int) -> None:
    body = Text.assemble(
        ("Case study  ", "bold cyan"),
        (case_study, "white"),
        ("\nCapacity    ", "bold cyan"),
        (f"{capacity:g} kW", "white"),
        ("\nSeed values ", "bold cyan"),
        (str(seed_size), "white"),
    )
    console.print(Panel(body, title="ResearchDev / MCDA", border_style="cyan"))


def show_summary(result: dict) -> None:
    manifest = result["manifest"]
    robust = manifest["robust_alternative"]
    table = Table(box=box.ROUNDED, show_header=True, header_style="bold cyan")
    table.add_column("Resultado")
    table.add_column("Valor", justify="right")
    table.add_row("Alternativas", f"{manifest['alternative_count']:,}")
    table.add_row("Indicadores", str(manifest["indicator_count"]))
    table.add_row("Escenarios TOPSIS", str(manifest["topsis_scenario_count"]))
    table.add_row("Alternativa robusta", robust["alternative"])
    table.add_row("Permanencia top 5", f"{robust['top_5_rate']:.0%}")
    table.add_row("Puesto medio", f"{robust['mean_rank']:.2f}")
    table.add_row("Desviación del puesto", f"{robust['rank_std']:.2f}")
    console.print(table)


def show_hashes(manifest: dict) -> None:
    table = Table(box=box.SIMPLE_HEAVY, header_style="bold green")
    table.add_column("Hash")
    table.add_column("SHA-256")
    for name, digest in manifest["hashes"].items():
        table.add_row(name, digest)
    console.print(Panel(table, title="Reproducibilidad", border_style="green"))


def show_rank_chart(result: dict) -> None:
    robust = result["manifest"]["robust_alternative"]
    metrics = {
        "Top 5 %": robust["top_5_rate"] * 100,
        "Mejor puesto": robust["best_rank"],
        "Puesto medio": robust["mean_rank"],
        "Peor puesto": robust["worst_rank"],
    }
    maximum = max(metrics.values(), default=1) or 1
    chart = Table(title="Perfil de alternativa robusta", box=box.SIMPLE)
    chart.add_column("Métrica")
    chart.add_column("Valor", justify="right")
    chart.add_column("Escala")
    for label, value in metrics.items():
        bar_length = max(1, round((value / maximum) * 40))
        chart.add_row(label, f"{value:.2f}", "█" * bar_length)
    console.print(chart)


def show_resource_mix(result: dict) -> None:
    """Show the robust alternative composition with readable resource bars."""
    robust = result["manifest"]["robust_alternative"]
    percentages = robust["resource_mix_percent"]
    capacities = robust["resource_mix_kw"]
    table = Table(
        title=f"Composición de alternativa {robust['alternative']}",
        box=box.ROUNDED,
        header_style="bold yellow",
    )
    table.add_column("Recurso")
    table.add_column("Capacidad", justify="right")
    table.add_column("Participación", justify="right")
    table.add_column("Indicador")
    for resource_name, percentage in percentages.items():
        table.add_row(
            resource_name.upper(),
            f"{capacities[resource_name]:.1f} kW",
            f"{percentage:.1f}%",
            "█" * max(1, round(percentage / 2)),
        )
    console.print(table)


def show_termgraph(result: dict) -> None:
    """Render the robustness profile with termgraph when it is available."""
    robust = result["manifest"]["robust_alternative"]
    data = "\n".join(
        [
            f"top_5_rate {robust['top_5_rate'] * 100:.2f}",
            f"best_rank {robust['best_rank']}",
            f"mean_rank {robust['mean_rank']:.2f}",
            f"worst_rank {robust['worst_rank']}",
        ]
    )
    try:
        executable = Path(sys.executable).with_name("termgraph")
        command = str(executable) if executable.is_file() else "termgraph"
        subprocess.run(
            [command, "--title", "Perfil robusto (termgraph)", "--color", "cyan"],
            input=data,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        console.print("[yellow]termgraph no está disponible; se conserva el gráfico Rich.[/yellow]")


def show_resource_termgraph(result: dict) -> None:
    """Render the robust resource mix with termgraph when available."""
    robust = result["manifest"]["robust_alternative"]
    data = "\n".join(
        f"{name} {value:.2f}"
        for name, value in robust["resource_mix_percent"].items()
    )
    try:
        executable = Path(sys.executable).with_name("termgraph")
        command = str(executable) if executable.is_file() else "termgraph"
        subprocess.run(
            [command, "--title", "Recursos de la alternativa robusta", "--color", "yellow"],
            input=data,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        console.print("[yellow]termgraph no está disponible para la mezcla de recursos.[/yellow]")


def show_outputs(result: dict) -> None:
    table = Table(box=box.MINIMAL, header_style="bold magenta")
    table.add_column("Salida")
    table.add_column("Ruta")
    table.add_row("Alternativas", str(result["alternatives_path"]))
    table.add_row("Ranking", str(result["ranking_path"]))
    table.add_row("Sensibilidad", str(result["sensitivity_path"]))
    table.add_row("Manifiesto", str(result["manifest_path"]))
    console.print(Panel(table, title="Artefactos generados", border_style="magenta"))
