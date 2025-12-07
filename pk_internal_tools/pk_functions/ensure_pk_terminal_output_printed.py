
import logging
from rich.console import Console
from rich.panel import Panel
from pk_internal_tools.pk_objects.pk_colors import PK_ANSI_COLOR_MAP
from pk_internal_tools.pk_objects.pk_etc import PK_UNDERLINE # Keep for general logging, not for panel

console = Console()

def ensure_pk_terminal_output_printed(command: str, stdout_lines: list, stderr_lines: list):
    """
    Formats and prints command output in a structured and colored terminal-like a way using rich.Panel.
    """
    output_content = []

    # Add command to panel content
    output_content.append(f"[bold white]Command:[/bold white] [white]{command}[/white]")

    if stdout_lines:
        output_content.append("\n[green]Output:[/green]")
        for line in stdout_lines:
            output_content.append(f"[green]{line}[/green]")
    
    if stderr_lines:
        output_content.append("\n[red]Errors:[/red]")
        for line in stderr_lines:
            output_content.append(f"[red]{line}[/red]")

    if not stdout_lines and not stderr_lines:
        output_content.append("\n(No output was produced by the command.)")

    panel_content = "\n".join(output_content)
    panel = Panel(
        panel_content, 
        title="[bold blue]PK Terminal Output[/bold blue]", 
        border_style="blue",
        expand=True
    )
    console.print(panel)
    # The `input("continue:enter")` is handled in ensure_pk_terminal_executed.py

