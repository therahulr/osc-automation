"""
Performance Analysis Utilities

Tools for analyzing automation performance data, generating reports,
and identifying bottlenecks and trends in automation execution.
"""

import sqlite3
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import json

from core.performance import PerformanceTracker


class PerformanceAnalyzer:
    """Utilities for analyzing automation performance data"""
    
    def __init__(self):
        self.tracker = PerformanceTracker()
        self.db_path = self.tracker.db_path
    
    def get_recent_runs(self, days: int = 7, script_name: Optional[str] = None) -> List[Dict]:
        """Get recent automation runs with basic metrics
        
        Args:
            days: Number of days to look back
            script_name: Filter by specific script name
            
        Returns:
            List of run dictionaries with metrics
        """
        since_date = datetime.now() - timedelta(days=days)
        
        query = """
            SELECT 
                id, session_id, script_name, started_at, completed_at,
                total_duration, status, total_steps, failed_steps,
                environment, browser_type, headless
            FROM automation_runs 
            WHERE started_at >= ?
        """
        params = [since_date]
        
        if script_name:
            query += " AND script_name = ?"
            params.append(script_name)
        
        query += " ORDER BY started_at DESC"
        
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def get_run_details(self, run_id: str) -> Dict:
        """Get detailed information about a specific run
        
        Args:
            run_id: The run ID to analyze
            
        Returns:
            Dictionary with run details and step breakdown
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            
            # Get run info
            run_cursor = conn.execute("""
                SELECT * FROM automation_runs WHERE id = ?
            """, (run_id,))
            run_info = dict(run_cursor.fetchone() or {})
            
            # Get step metrics
            steps_cursor = conn.execute("""
                SELECT 
                    step_name, step_type, duration, status, 
                    error_message, page_url, element_selector
                FROM step_metrics 
                WHERE run_id = ? 
                ORDER BY step_order
            """, (run_id,))
            steps = [dict(row) for row in steps_cursor.fetchall()]
            
            # Get browser metrics
            browser_cursor = conn.execute("""
                SELECT 
                    page_load_time, dom_content_loaded_time, page_url,
                    network_requests, memory_usage_mb
                FROM browser_metrics 
                WHERE run_id = ?
                ORDER BY recorded_at
            """, (run_id,))
            browser_metrics = [dict(row) for row in browser_cursor.fetchall()]
            
            return {
                'run_info': run_info,
                'steps': steps,
                'browser_metrics': browser_metrics
            }
    
    def get_performance_trends(self, script_name: str, days: int = 30) -> Dict:
        """Analyze performance trends for a specific script
        
        Args:
            script_name: Name of the script to analyze
            days: Number of days to analyze
            
        Returns:
            Dictionary with trend analysis
        """
        since_date = datetime.now() - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            # Get run duration trends
            duration_cursor = conn.execute("""
                SELECT 
                    DATE(started_at) as run_date,
                    AVG(total_duration) as avg_duration,
                    MIN(total_duration) as min_duration,
                    MAX(total_duration) as max_duration,
                    COUNT(*) as run_count,
                    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count
                FROM automation_runs 
                WHERE script_name = ? AND started_at >= ?
                GROUP BY DATE(started_at)
                ORDER BY run_date
            """, (script_name, since_date))
            
            daily_trends = []
            for row in duration_cursor.fetchall():
                daily_trends.append({
                    'date': row[0],
                    'avg_duration': round(row[1], 2) if row[1] else 0,
                    'min_duration': round(row[2], 2) if row[2] else 0,
                    'max_duration': round(row[3], 2) if row[3] else 0,
                    'run_count': row[4],
                    'success_rate': round((row[5] / row[4]) * 100, 1) if row[4] > 0 else 0
                })
            
            # Get step performance analysis
            step_cursor = conn.execute("""
                SELECT 
                    sm.step_name,
                    AVG(sm.duration) as avg_duration,
                    MAX(sm.duration) as max_duration,
                    COUNT(*) as execution_count,
                    SUM(CASE WHEN sm.status = 'success' THEN 1 ELSE 0 END) as success_count
                FROM step_metrics sm
                JOIN automation_runs ar ON sm.run_id = ar.id
                WHERE ar.script_name = ? AND ar.started_at >= ?
                GROUP BY sm.step_name
                ORDER BY avg_duration DESC
            """, (script_name, since_date))
            
            step_analysis = []
            for row in step_cursor.fetchall():
                step_analysis.append({
                    'step_name': row[0],
                    'avg_duration': round(row[1], 3) if row[1] else 0,
                    'max_duration': round(row[2], 3) if row[2] else 0,
                    'execution_count': row[3],
                    'success_rate': round((row[4] / row[3]) * 100, 1) if row[3] > 0 else 0
                })
            
            return {
                'script_name': script_name,
                'analysis_period': f"{days} days",
                'daily_trends': daily_trends,
                'step_analysis': step_analysis
            }
    
    def identify_bottlenecks(self, script_name: Optional[str] = None, min_duration: float = 5.0) -> List[Dict]:
        """Identify performance bottlenecks
        
        Args:
            script_name: Optional script to analyze
            min_duration: Minimum duration (seconds) to consider a bottleneck
            
        Returns:
            List of potential bottlenecks
        """
        query = """
            SELECT 
                ar.script_name,
                sm.step_name,
                sm.step_type,
                AVG(sm.duration) as avg_duration,
                MAX(sm.duration) as max_duration,
                COUNT(*) as occurrences,
                SUM(CASE WHEN sm.status = 'failed' THEN 1 ELSE 0 END) as failure_count
            FROM step_metrics sm
            JOIN automation_runs ar ON sm.run_id = ar.id
            WHERE sm.duration >= ?
        """
        params = [min_duration]
        
        if script_name:
            query += " AND ar.script_name = ?"
            params.append(script_name)
        
        query += """
            GROUP BY ar.script_name, sm.step_name, sm.step_type
            ORDER BY avg_duration DESC
        """
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(query, params)
            bottlenecks = []
            
            for row in cursor.fetchall():
                bottlenecks.append({
                    'script_name': row[0],
                    'step_name': row[1],
                    'step_type': row[2],
                    'avg_duration': round(row[3], 2),
                    'max_duration': round(row[4], 2),
                    'occurrences': row[5],
                    'failure_count': row[6],
                    'failure_rate': round((row[6] / row[5]) * 100, 1) if row[5] > 0 else 0
                })
            
            return bottlenecks
    
    def generate_summary_report(self, days: int = 7) -> Dict:
        """Generate a comprehensive summary report
        
        Args:
            days: Number of days to include in report
            
        Returns:
            Dictionary with summary statistics
        """
        since_date = datetime.now() - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            # Overall statistics
            overall_cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total_runs,
                    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_runs,
                    AVG(total_duration) as avg_duration,
                    SUM(total_steps) as total_steps,
                    COUNT(DISTINCT script_name) as unique_scripts
                FROM automation_runs 
                WHERE started_at >= ?
            """, (since_date,))
            
            overall_stats = overall_cursor.fetchone()
            
            # Script performance
            script_cursor = conn.execute("""
                SELECT 
                    script_name,
                    COUNT(*) as run_count,
                    AVG(total_duration) as avg_duration,
                    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as success_count
                FROM automation_runs 
                WHERE started_at >= ?
                GROUP BY script_name
                ORDER BY run_count DESC
            """, (since_date,))
            
            script_stats = []
            for row in script_cursor.fetchall():
                script_stats.append({
                    'script_name': row[0],
                    'run_count': row[1],
                    'avg_duration': round(row[2], 2) if row[2] else 0,
                    'success_rate': round((row[3] / row[1]) * 100, 1) if row[1] > 0 else 0
                })
            
            return {
                'report_period': f"{days} days",
                'generated_at': datetime.now().isoformat(),
                'overall_statistics': {
                    'total_runs': overall_stats[0] or 0,
                    'successful_runs': overall_stats[1] or 0,
                    'success_rate': round((overall_stats[1] / overall_stats[0]) * 100, 1) if overall_stats[0] > 0 else 0,
                    'avg_duration': round(overall_stats[2], 2) if overall_stats[2] else 0,
                    'total_steps': overall_stats[3] or 0,
                    'unique_scripts': overall_stats[4] or 0
                },
                'script_performance': script_stats
            }
    
    def export_data(self, output_file: str, format: str = 'json', days: int = 30):
        """Export performance data to file
        
        Args:
            output_file: Path to output file
            format: Export format ('json', 'csv')
            days: Number of days of data to export
        """
        data = {
            'summary': self.generate_summary_report(days),
            'recent_runs': self.get_recent_runs(days),
            'bottlenecks': self.identify_bottlenecks()
        }
        
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        if format.lower() == 'json':
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported export format: {format}")


# Convenience functions for quick analysis
def quick_summary(days: int = 7) -> Dict:
    """Quick summary of recent performance"""
    analyzer = PerformanceAnalyzer()
    return analyzer.generate_summary_report(days)


def analyze_script(script_name: str, days: int = 30) -> Dict:
    """Analyze performance trends for a specific script"""
    analyzer = PerformanceAnalyzer()
    return analyzer.get_performance_trends(script_name, days)


def find_bottlenecks(min_duration: float = 5.0) -> List[Dict]:
    """Find performance bottlenecks across all scripts"""
    analyzer = PerformanceAnalyzer()
    return analyzer.identify_bottlenecks(min_duration=min_duration)


# Example usage functions
def print_summary_report(days: int = 7):
    """Print a formatted summary report to console"""
    report = quick_summary(days)
    
    print(f"\n{'='*60}")
    print(f"AUTOMATION PERFORMANCE SUMMARY ({report['report_period']})")
    print(f"{'='*60}")
    
    stats = report['overall_statistics']
    print(f"Total Runs: {stats['total_runs']}")
    print(f"Success Rate: {stats['success_rate']}%")
    print(f"Average Duration: {stats['avg_duration']}s")
    print(f"Total Steps Executed: {stats['total_steps']}")
    print(f"Unique Scripts: {stats['unique_scripts']}")
    
    print(f"\n{'Script Performance:'}")
    print(f"{'Name':<30} {'Runs':<8} {'Avg Duration':<12} {'Success Rate':<12}")
    print(f"{'-'*62}")
    
    for script in report['script_performance']:
        print(f"{script['script_name']:<30} {script['run_count']:<8} "
              f"{script['avg_duration']:<12.2f} {script['success_rate']:<12.1f}%")


if __name__ == "__main__":
    # Example: Print summary report
    print_summary_report()