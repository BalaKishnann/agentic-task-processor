import logging
import time
from collections import defaultdict
from contextlib import contextmanager
from threading import Lock

logger = logging.getLogger("tool_metrics")


class ToolMetrics:
    """
    In-memory counters for tool execution: call count, success/failure
    count, and cumulative/average duration per tool. Thread-safe via a
    simple lock, since FastAPI can handle concurrent requests.

    Note: this resets on every process restart. Fine for a single-instance
    dev/small deployment; for anything running multiple workers or needing
    persistence across restarts, this should be swapped for a real metrics
    backend (Prometheus, StatsD, etc.) rather than extended in place.
    """

    def __init__(self):
        self._lock = Lock()
        self._counts = defaultdict(lambda: {"success": 0, "failed": 0})
        self._durations = defaultdict(list)

    @contextmanager
    def track(self, tool_name: str):

        start_time = time.perf_counter()
        status = "failed"

        try:
            yield
            status = "success"
        finally:
            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)

            with self._lock:
                self._counts[tool_name][status] += 1
                self._durations[tool_name].append(duration_ms)

            logger.info(
                "Tool execution finished",
                extra={
                    "tool": tool_name,
                    "status": status,
                    "duration_ms": duration_ms,
                },
            )

    def snapshot(self) -> dict:
        """Returns a summary suitable for a /metrics endpoint."""

        with self._lock:
            summary = {}

            for tool_name, counts in self._counts.items():
                durations = self._durations[tool_name]
                total_calls = counts["success"] + counts["failed"]

                summary[tool_name] = {
                    "total_calls": total_calls,
                    "success_count": counts["success"],
                    "failed_count": counts["failed"],
                    "success_rate": (
                        round(counts["success"] / total_calls, 3)
                        if total_calls
                        else None
                    ),
                    "avg_duration_ms": (
                        round(sum(durations) / len(durations), 2) if durations else None
                    ),
                    "max_duration_ms": round(max(durations), 2) if durations else None,
                }

            return summary


tool_metrics = ToolMetrics()
