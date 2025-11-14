"""Performance Reporter - Generate detailed performance reports from tracked data.

Generates comprehensive performance reports including:
- Run summaries with timing metrics
- Step-by-step breakdowns
- Browser performance metrics
- Action-level details
- Trend analysis
- Export to multiple formats (text, JSON, HTML)
"""

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

from core.performance import performance_tracker


@dataclass
class RunSummary:
    """Summary of a single automation run."""
    run_id: int
    session_id: str
    script_name: str
    started_at: datetime
    completed_at: Optional[datetime]
    total_duration: float
    status: str
    total_steps: int
    failed_steps: int
    success_rate: float
    environment: Optional[str]
    browser_type: Optional[str]
    tags: Optional[List[str]]


@dataclass
class StepSummary:
    """Summary of a single step."""
    step_id: int
    name: str
    type: str
    duration: float
    status: str
    order_index: int
    error_message: Optional[str]


class PerformanceReporter:
    """Generate and export performance reports."""

    def __init__(self, db_path: Optional[Path] = None):
        """Initialize performance reporter.

        Args:
            db_path: Path to performance database (defaults to tracker's db)
        """
        self.db_path = db_path or performance_tracker.db_path
        self.console = Console()

    def get_latest_run(self) -> Optional[RunSummary]:
        """Get the most recent automation run."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT
                    id, session_id, script_name, started_at, completed_at,
                    total_duration, status, total_steps, failed_steps,
                    environment, browser_type, tags
                FROM automation_runs
                ORDER BY started_at DESC
                LIMIT 1
            """)
            row = cursor.fetchone()

            if not row:
                return None

            return RunSummary(
                run_id=row['id'],
                session_id=row['session_id'],
                script_name=row['script_name'],
                started_at=datetime.fromisoformat(row['started_at']),
                completed_at=datetime.fromisoformat(row['completed_at']) if row['completed_at'] else None,
                total_duration=row['total_duration'] or 0.0,
                status=row['status'],
                total_steps=row['total_steps'],
                failed_steps=row['failed_steps'],
                success_rate=(row['total_steps'] - row['failed_steps']) / row['total_steps'] * 100 if row['total_steps'] > 0 else 0.0,
                environment=row['environment'],
                browser_type=row['browser_type'],
                tags=json.loads(row['tags']) if row['tags'] else []
            )

    def get_run_steps(self, run_id: int) -> List[StepSummary]:
        """Get all steps for a specific run."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT
                    id, step_name, step_type, duration, status, step_order, error_message
                FROM step_metrics
                WHERE run_id = ?
                ORDER BY step_order ASC
            """, (run_id,))

            steps = []
            for row in cursor.fetchall():
                steps.append(StepSummary(
                    step_id=row['id'],
                    name=row['step_name'],
                    type=row['step_type'],
                    duration=row['duration'] or 0.0,
                    status=row['status'],
                    order_index=row['step_order'] or 0,
                    error_message=row['error_message']
                ))

            return steps

    def get_browser_metrics(self, run_id: int) -> List[Dict[str, Any]]:
        """Get browser metrics for a specific run."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT *
                FROM browser_metrics
                WHERE run_id = ?
                ORDER BY recorded_at ASC
            """, (run_id,))

            return [dict(row) for row in cursor.fetchall()]

    def get_action_metrics(self, run_id: int) -> List[Dict[str, Any]]:
        """Get action metrics for a specific run."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT *
                FROM action_metrics
                WHERE run_id = ?
                ORDER BY started_at ASC
            """, (run_id,))

            return [dict(row) for row in cursor.fetchall()]

    def generate_summary_report(self, run_id: Optional[int] = None) -> str:
        """Generate a summary report for a run.

        Args:
            run_id: Specific run ID (None = latest run)

        Returns:
            Formatted summary report as string
        """
        if run_id is None:
            run = self.get_latest_run()
            if not run:
                return "No automation runs found in database."
            run_id = run.run_id
        else:
            run = self._get_run_by_id(run_id)
            if not run:
                return f"Run {run_id} not found."

        steps = self.get_run_steps(run_id)

        # Build report
        lines = []
        lines.append("=" * 80)
        lines.append(f"AUTOMATION RUN SUMMARY")
        lines.append("=" * 80)
        lines.append(f"")
        lines.append(f"Script Name:      {run.script_name}")
        lines.append(f"Session ID:       {run.session_id}")
        lines.append(f"Status:           {run.status.upper()}")
        lines.append(f"Environment:      {run.environment or 'N/A'}")
        lines.append(f"Browser:          {run.browser_type or 'N/A'}")
        lines.append(f"")
        lines.append(f"Started:          {run.started_at.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"Completed:        {run.completed_at.strftime('%Y-%m-%d %H:%M:%S') if run.completed_at else 'N/A'}")
        lines.append(f"Total Duration:   {run.total_duration:.2f}s")
        lines.append(f"")
        lines.append(f"Total Steps:      {run.total_steps}")
        lines.append(f"Failed Steps:     {run.failed_steps}")
        lines.append(f"Success Rate:     {run.success_rate:.1f}%")
        lines.append(f"")

        if run.tags:
            lines.append(f"Tags:             {', '.join(run.tags)}")
            lines.append(f"")

        # Step breakdown
        if steps:
            lines.append("=" * 80)
            lines.append("STEP BREAKDOWN")
            lines.append("=" * 80)
            lines.append(f"")

            for step in steps:
                status_icon = "✓" if step.status == "success" else "✗"
                lines.append(f"{status_icon} [{step.order_index + 1}] {step.name}")
                lines.append(f"    Type: {step.type} | Duration: {step.duration:.2f}s | Status: {step.status}")
                if step.error_message:
                    lines.append(f"    Error: {step.error_message}")
                lines.append(f"")

        # Performance metrics
        browser_metrics = self.get_browser_metrics(run_id)
        if browser_metrics:
            lines.append("=" * 80)
            lines.append("BROWSER PERFORMANCE METRICS")
            lines.append("=" * 80)
            lines.append(f"")

            total_page_loads = len([m for m in browser_metrics if m.get('page_load_time')])
            avg_page_load = sum(m.get('page_load_time', 0) for m in browser_metrics) / total_page_loads if total_page_loads > 0 else 0

            lines.append(f"Total Page Loads:     {total_page_loads}")
            lines.append(f"Avg Page Load Time:   {avg_page_load:.2f}s")
            lines.append(f"")

        # Action metrics summary
        actions = self.get_action_metrics(run_id)
        if actions:
            lines.append("=" * 80)
            lines.append("ACTION METRICS")
            lines.append("=" * 80)
            lines.append(f"")

            action_types = {}
            for action in actions:
                action_type = action.get('action_type', 'unknown')
                if action_type not in action_types:
                    action_types[action_type] = {'count': 0, 'total_duration': 0, 'success': 0}
                action_types[action_type]['count'] += 1
                action_types[action_type]['total_duration'] += action.get('duration', 0)
                if action.get('success'):
                    action_types[action_type]['success'] += 1

            for action_type, stats in action_types.items():
                avg_duration = stats['total_duration'] / stats['count'] if stats['count'] > 0 else 0
                success_rate = stats['success'] / stats['count'] * 100 if stats['count'] > 0 else 0
                lines.append(f"{action_type.upper()}:")
                lines.append(f"  Count: {stats['count']} | Avg Duration: {avg_duration:.3f}s | Success Rate: {success_rate:.1f}%")
            lines.append(f"")

        lines.append("=" * 80)

        return "\n".join(lines)

    def generate_detailed_report(self, run_id: Optional[int] = None) -> str:
        """Generate a detailed report with all metrics.

        Args:
            run_id: Specific run ID (None = latest run)

        Returns:
            Formatted detailed report as string
        """
        summary = self.generate_summary_report(run_id)

        # Get run_id if not provided
        if run_id is None:
            run = self.get_latest_run()
            if not run:
                return summary
            run_id = run.run_id

        # Add detailed action breakdown
        actions = self.get_action_metrics(run_id)

        if actions:
            lines = [summary, "", "=" * 80, "DETAILED ACTION LOG", "=" * 80, ""]

            for i, action in enumerate(actions, 1):
                lines.append(f"[{i}] {action.get('action_type', 'unknown').upper()}")
                lines.append(f"    Target: {action.get('target_element', 'N/A')}")
                lines.append(f"    Duration: {action.get('duration', 0):.3f}s")
                lines.append(f"    Success: {'Yes' if action.get('success') else 'No'}")
                if action.get('action_value'):
                    lines.append(f"    Value: {action.get('action_value')}")
                if action.get('retry_count', 0) > 0:
                    lines.append(f"    Retries: {action.get('retry_count')}")
                if action.get('error_details'):
                    lines.append(f"    Error: {action.get('error_details')}")
                lines.append("")

            return "\n".join(lines)

        return summary

    def generate_json_report(self, run_id: Optional[int] = None) -> str:
        """Generate JSON report with all data.

        Args:
            run_id: Specific run ID (None = latest run)

        Returns:
            JSON string with complete report data
        """
        if run_id is None:
            run = self.get_latest_run()
            if not run:
                return json.dumps({"error": "No runs found"}, indent=2)
            run_id = run.run_id
        else:
            run = self._get_run_by_id(run_id)
            if not run:
                return json.dumps({"error": f"Run {run_id} not found"}, indent=2)

        steps = self.get_run_steps(run_id)
        browser_metrics = self.get_browser_metrics(run_id)
        actions = self.get_action_metrics(run_id)

        report = {
            "run": asdict(run),
            "steps": [asdict(step) for step in steps],
            "browser_metrics": browser_metrics,
            "actions": actions
        }

        # Convert datetime objects to strings
        report['run']['started_at'] = run.started_at.isoformat()
        report['run']['completed_at'] = run.completed_at.isoformat() if run.completed_at else None

        return json.dumps(report, indent=2, default=str)

    def export_report(self, output_path: Path, format: str = "text", run_id: Optional[int] = None):
        """Export report to file.

        Args:
            output_path: Path to save report
            format: Report format ('text', 'json', 'detailed')
            run_id: Specific run ID (None = latest run)
        """
        if format == "json":
            content = self.generate_json_report(run_id)
        elif format == "detailed":
            content = self.generate_detailed_report(run_id)
        else:
            content = self.generate_summary_report(run_id)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content)

        print(f"Report exported to: {output_path}")

    def print_rich_summary(self, run_id: Optional[int] = None):
        """Print a beautifully formatted summary using rich.

        Args:
            run_id: Specific run ID (None = latest run)
        """
        if run_id is None:
            run = self.get_latest_run()
            if not run:
                self.console.print("[red]No automation runs found in database.[/]")
                return
            run_id = run.run_id
        else:
            run = self._get_run_by_id(run_id)
            if not run:
                self.console.print(f"[red]Run {run_id} not found.[/]")
                return

        steps = self.get_run_steps(run_id)

        # Header
        self.console.print("\n")
        self.console.print(Panel.fit(
            f"[bold cyan]Automation Run Summary[/]\n"
            f"[yellow]{run.script_name}[/]",
            border_style="cyan"
        ))

        # Overview table
        overview = Table(show_header=False, box=None, padding=(0, 2))
        overview.add_column("Key", style="cyan")
        overview.add_column("Value", style="white")

        status_color = "green" if run.status == "success" else "red"
        overview.add_row("Status", f"[{status_color}]{run.status.upper()}[/]")
        overview.add_row("Session ID", run.session_id)
        overview.add_row("Environment", run.environment or "N/A")
        overview.add_row("Browser", run.browser_type or "N/A")
        overview.add_row("Started", run.started_at.strftime("%Y-%m-%d %H:%M:%S"))
        overview.add_row("Duration", f"{run.total_duration:.2f}s")
        overview.add_row("Total Steps", str(run.total_steps))
        overview.add_row("Failed Steps", f"[red]{run.failed_steps}[/]" if run.failed_steps > 0 else "0")
        overview.add_row("Success Rate", f"[green]{run.success_rate:.1f}%[/]")

        self.console.print(overview)

        # Steps table
        if steps:
            self.console.print("\n[bold cyan]Step Breakdown[/]\n")

            steps_table = Table(show_header=True, header_style="bold magenta")
            steps_table.add_column("#", style="dim", width=4)
            steps_table.add_column("Step Name", style="cyan")
            steps_table.add_column("Type", style="yellow")
            steps_table.add_column("Duration", style="green", justify="right")
            steps_table.add_column("Status", justify="center")

            for step in steps:
                status_icon = "✓" if step.status == "success" else "✗"
                status_color = "green" if step.status == "success" else "red"

                steps_table.add_row(
                    str(step.order_index + 1),
                    step.name,
                    step.type,
                    f"{step.duration:.2f}s",
                    f"[{status_color}]{status_icon}[/]"
                )

            self.console.print(steps_table)

        self.console.print("\n")

    def get_recent_runs(self, limit: int = 10) -> List[RunSummary]:
        """Get recent automation runs.

        Args:
            limit: Maximum number of runs to retrieve

        Returns:
            List of run summaries
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT
                    id, session_id, script_name, started_at, completed_at,
                    total_duration, status, total_steps, failed_steps,
                    environment, browser_type, tags
                FROM automation_runs
                ORDER BY started_at DESC
                LIMIT ?
            """, (limit,))

            runs = []
            for row in cursor.fetchall():
                runs.append(RunSummary(
                    run_id=row['id'],
                    session_id=row['session_id'],
                    script_name=row['script_name'],
                    started_at=datetime.fromisoformat(row['started_at']),
                    completed_at=datetime.fromisoformat(row['completed_at']) if row['completed_at'] else None,
                    total_duration=row['total_duration'] or 0.0,
                    status=row['status'],
                    total_steps=row['total_steps'],
                    failed_steps=row['failed_steps'],
                    success_rate=(row['total_steps'] - row['failed_steps']) / row['total_steps'] * 100 if row['total_steps'] > 0 else 0.0,
                    environment=row['environment'],
                    browser_type=row['browser_type'],
                    tags=json.loads(row['tags']) if row['tags'] else []
                ))

            return runs

    def _get_run_by_id(self, run_id: int) -> Optional[RunSummary]:
        """Get a specific run by ID."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("""
                SELECT
                    id, session_id, script_name, started_at, completed_at,
                    total_duration, status, total_steps, failed_steps,
                    environment, browser_type, tags
                FROM automation_runs
                WHERE id = ?
            """, (run_id,))
            row = cursor.fetchone()

            if not row:
                return None

            return RunSummary(
                run_id=row['id'],
                session_id=row['session_id'],
                script_name=row['script_name'],
                started_at=datetime.fromisoformat(row['started_at']),
                completed_at=datetime.fromisoformat(row['completed_at']) if row['completed_at'] else None,
                total_duration=row['total_duration'] or 0.0,
                status=row['status'],
                total_steps=row['total_steps'],
                failed_steps=row['failed_steps'],
                success_rate=(row['total_steps'] - row['failed_steps']) / row['total_steps'] * 100 if row['total_steps'] > 0 else 0.0,
                environment=row['environment'],
                browser_type=row['browser_type'],
                tags=json.loads(row['tags']) if row['tags'] else []
            )
