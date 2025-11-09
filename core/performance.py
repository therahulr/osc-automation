"""
Performance Tracking System for Automation Scripts

Comprehensive performance monitoring with SQLite storage for tracking:
- Complete automation runs with metadata
- Individual step timings and outcomes  
- Browser/page performance metrics
- Micro-level action details (clicks, waits, navigations)

Features:
- Local SQLite database storage
- Context managers for session tracking
- Enhanced decorators for action monitoring
- Automatic browser integration
- Optional metadata support
- Backward compatible with existing code
"""

import sqlite3
import time
import uuid
import threading
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict

from core.utils import ensure_dir


@dataclass
class RunMetadata:
    """Metadata for automation runs - all optional except run basics"""
    script_name: str
    environment: Optional[str] = None
    browser_type: Optional[str] = None
    headless: Optional[bool] = None
    viewport_size: Optional[str] = None
    user_agent: Optional[str] = None
    tags: Optional[List[str]] = None
    notes: Optional[str] = None


@dataclass
class StepMetrics:
    """Detailed metrics for individual automation steps"""
    step_name: str
    step_type: str  # 'action', 'verification', 'navigation', 'wait'
    duration: float
    status: str  # 'success', 'failed', 'timeout'
    page_url: Optional[str] = None
    element_selector: Optional[str] = None
    error_message: Optional[str] = None
    screenshot_path: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class PerformanceTracker:
    """Central performance tracking system with SQLite storage"""
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self.db_path = Path.cwd() / "data" / "performance.db"
        ensure_dir(self.db_path.parent)
        self._init_database()
        self._current_session = None
        self._initialized = True
    
    def _init_database(self):
        """Initialize SQLite database with performance tracking schema"""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                -- Main automation runs tracking
                CREATE TABLE IF NOT EXISTS automation_runs (
                    id TEXT PRIMARY KEY,
                    session_id TEXT UNIQUE,
                    script_name TEXT NOT NULL,
                    started_at TIMESTAMP NOT NULL,
                    completed_at TIMESTAMP,
                    total_duration REAL,
                    status TEXT NOT NULL DEFAULT 'running',
                    total_steps INTEGER DEFAULT 0,
                    failed_steps INTEGER DEFAULT 0,
                    
                    -- Environment & Browser Info
                    environment TEXT,
                    browser_type TEXT,
                    headless BOOLEAN,
                    viewport_size TEXT,
                    user_agent TEXT,
                    
                    -- Optional Metadata
                    tags TEXT,  -- JSON array of tags
                    notes TEXT,
                    
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                -- Individual step performance metrics
                CREATE TABLE IF NOT EXISTS step_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    
                    -- Step Identification
                    step_name TEXT NOT NULL,
                    step_type TEXT NOT NULL,  -- action, verification, navigation, wait
                    step_order INTEGER,
                    parent_step_id INTEGER,  -- For nested steps
                    
                    -- Timing Data
                    started_at TIMESTAMP NOT NULL,
                    completed_at TIMESTAMP,
                    duration REAL,
                    
                    -- Outcome
                    status TEXT NOT NULL,  -- success, failed, timeout, skipped
                    error_message TEXT,
                    
                    -- Context Data
                    page_url TEXT,
                    page_title TEXT,
                    element_selector TEXT,
                    element_text TEXT,
                    
                    -- Performance Data
                    wait_time REAL,
                    response_time REAL,
                    
                    -- Optional Metadata
                    screenshot_path TEXT,
                    metadata TEXT,  -- JSON for additional data
                    
                    FOREIGN KEY (run_id) REFERENCES automation_runs(id),
                    FOREIGN KEY (parent_step_id) REFERENCES step_metrics(id)
                );
                
                -- Browser and page performance metrics
                CREATE TABLE IF NOT EXISTS browser_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_id TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    -- Page Performance
                    page_load_time REAL,
                    dom_content_loaded_time REAL,
                    first_paint_time REAL,
                    page_size_kb REAL,
                    
                    -- Network Metrics
                    network_requests INTEGER,
                    network_failed_requests INTEGER,
                    total_transfer_size_kb REAL,
                    
                    -- Browser Resource Usage
                    memory_usage_mb REAL,
                    cpu_usage_percent REAL,
                    
                    -- Context
                    page_url TEXT,
                    viewport_size TEXT,
                    
                    FOREIGN KEY (run_id) REFERENCES automation_runs(id)
                );
                
                -- Action-level micro metrics (clicks, typing, waits)
                CREATE TABLE IF NOT EXISTS action_metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    step_id INTEGER NOT NULL,
                    run_id TEXT NOT NULL,
                    
                    -- Action Details
                    action_type TEXT NOT NULL,  -- click, type, wait, navigate, verify
                    target_element TEXT,
                    action_value TEXT,  -- text typed, URL navigated, etc.
                    
                    -- Timing
                    started_at TIMESTAMP NOT NULL,
                    duration REAL NOT NULL,
                    
                    -- Outcome
                    success BOOLEAN NOT NULL,
                    retry_count INTEGER DEFAULT 0,
                    error_details TEXT,
                    
                    FOREIGN KEY (step_id) REFERENCES step_metrics(id),
                    FOREIGN KEY (run_id) REFERENCES automation_runs(id)
                );
                
                -- Indexes for performance
                CREATE INDEX IF NOT EXISTS idx_runs_script_date ON automation_runs(script_name, started_at);
                CREATE INDEX IF NOT EXISTS idx_steps_run_order ON step_metrics(run_id, step_order);
                CREATE INDEX IF NOT EXISTS idx_steps_duration ON step_metrics(duration);
                CREATE INDEX IF NOT EXISTS idx_actions_type ON action_metrics(action_type);
            """)
    
    def start_session(self, metadata: RunMetadata) -> str:
        """Start a new performance tracking session"""
        session_id = str(uuid.uuid4())
        run_id = str(uuid.uuid4())
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO automation_runs (
                    id, session_id, script_name, started_at, status,
                    environment, browser_type, headless, viewport_size, 
                    user_agent, tags, notes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                run_id, session_id, metadata.script_name, datetime.now(),
                'running', metadata.environment, metadata.browser_type,
                metadata.headless, metadata.viewport_size, metadata.user_agent,
                str(metadata.tags) if metadata.tags else None, metadata.notes
            ))
        
        self._current_session = {
            'run_id': run_id,
            'session_id': session_id,
            'started_at': time.time(),
            'step_counter': 0
        }
        
        return session_id
    
    def end_session(self, status: str = 'success'):
        """End the current performance tracking session"""
        if not self._current_session:
            return
        
        duration = time.time() - self._current_session['started_at']
        
        with sqlite3.connect(self.db_path) as conn:
            # Get step counts
            cursor = conn.execute("""
                SELECT COUNT(*) as total, 
                       SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed
                FROM step_metrics WHERE run_id = ?
            """, (self._current_session['run_id'],))
            
            total_steps, failed_steps = cursor.fetchone()
            
            # Update run completion
            conn.execute("""
                UPDATE automation_runs 
                SET completed_at = ?, total_duration = ?, status = ?,
                    total_steps = ?, failed_steps = ?
                WHERE id = ?
            """, (
                datetime.now(), duration, status, 
                total_steps or 0, failed_steps or 0,
                self._current_session['run_id']
            ))
        
        self._current_session = None
    
    def track_step(self, metrics: StepMetrics) -> int:
        """Record metrics for an individual step"""
        if not self._current_session:
            return 0
        
        self._current_session['step_counter'] += 1
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                INSERT INTO step_metrics (
                    run_id, session_id, step_name, step_type, step_order,
                    started_at, completed_at, duration, status, error_message,
                    page_url, element_selector, screenshot_path, metadata
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self._current_session['run_id'],
                self._current_session['session_id'],
                metrics.step_name,
                metrics.step_type,
                self._current_session['step_counter'],
                datetime.now(),
                datetime.now(),
                metrics.duration,
                metrics.status,
                metrics.error_message,
                metrics.page_url,
                metrics.element_selector,
                metrics.screenshot_path,
                str(metrics.metadata) if metrics.metadata else None
            ))
            
            return cursor.lastrowid
    
    def track_action(self, step_id: int, action_type: str, target: str, 
                    duration: float, success: bool, **kwargs):
        """Track micro-level actions within steps"""
        if not self._current_session:
            return
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO action_metrics (
                    step_id, run_id, action_type, target_element, action_value,
                    started_at, duration, success, retry_count, error_details
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                step_id,
                self._current_session['run_id'],
                action_type,
                target,
                kwargs.get('value', ''),
                datetime.now(),
                duration,
                success,
                kwargs.get('retry_count', 0),
                kwargs.get('error', '')
            ))
    
    def get_current_session(self) -> Optional[Dict]:
        """Get current session info"""
        return self._current_session


# Global instance
performance_tracker = PerformanceTracker()