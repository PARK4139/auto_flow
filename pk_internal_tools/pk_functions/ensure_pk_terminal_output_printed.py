def ensure_pk_terminal_output_printed(command: str, stdout_lines: list, stderr_lines: list):
    """
    Formats and prints command output in a structured and colored terminal-like a way using rich.Panel.
    """

    from rich.console import Console
    from rich.panel import Panel

    console = Console()

    output_content = []

    # Add command to panel content
    output_content.append("_" * 55)
    output_content.append(f"[bold white] # COMMAND:\n[/bold white] [white]{command}[/white]")

    if stdout_lines:
        output_content.append("_" * 55)
        output_content.append("# OUTPUT:\n")
        for line in stdout_lines:
            output_content.append(f"{line}")

    if stderr_lines:
        output_content.append("\n[red]Errors:[/red]")
        for line in stderr_lines:
            output_content.append(f"[red]{line}[/red]")

    if not stdout_lines and not stderr_lines:
        output_content.append("\n(No output was produced by the command.)")

    panel_content = "\n".join(output_content)
    panel = Panel(
        panel_content,
        title="[bold #e69dfc]PK Terminal Output[/bold #e69dfc]",
        border_style="white",
        expand=True
    )
    console.print(panel)
    # The `ensure_paused()` is handled in ensure_pk_terminal_executed.py
