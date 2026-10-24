"""Circuit Breaker Fault Sentinel.
100% Python Standard Library.
"""
import time
from typing import Dict, Any

class CircuitBreakerFaultSentinel:
    """3-state circuit breaker (CLOSED, OPEN, HALF_OPEN) with failure rate tripping."""
    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout_seconds: float = 30.0,
        half_open_success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout_seconds = recovery_timeout_seconds
        self.half_open_success_threshold = half_open_success_threshold
        self.circuits: Dict[str, Dict[str, Any]] = {}

    def _get_circuit(self, service: str) -> Dict[str, Any]:
        if service not in self.circuits:
            self.circuits[service] = {
                "state": "CLOSED",
                "failure_count": 0,
                "consecutive_successes": 0,
                "last_state_change": time.time(),
                "total_calls": 0,
                "total_failures": 0
            }
        return self.circuits[service]

    def can_execute(self, service: str) -> bool:
        c = self._get_circuit(service)
        now = time.time()
        if c["state"] == "CLOSED":
            return True
        elif c["state"] == "OPEN":
            if now - c["last_state_change"] >= self.recovery_timeout_seconds:
                c["state"] = "HALF_OPEN"
                c["consecutive_successes"] = 0
                c["last_state_change"] = now
                return True
            return False
        elif c["state"] == "HALF_OPEN":
            return True
        return False

    def record_result(self, service: str, success: bool = True, latency_ms: float = 0.0) -> Dict[str, Any]:
        c = self._get_circuit(service)
        now = time.time()
        c["total_calls"] += 1

        if success:
            if c["state"] == "HALF_OPEN":
                c["consecutive_successes"] += 1
                if c["consecutive_successes"] >= self.half_open_success_threshold:
                    c["state"] = "CLOSED"
                    c["failure_count"] = 0
                    c["consecutive_successes"] = 0
                    c["last_state_change"] = now
            elif c["state"] == "CLOSED":
                c["failure_count"] = max(0, c["failure_count"] - 1)
        else:
            c["total_failures"] += 1
            if c["state"] == "CLOSED":
                c["failure_count"] += 1
                if c["failure_count"] >= self.failure_threshold:
                    c["state"] = "OPEN"
                    c["last_state_change"] = now
            elif c["state"] == "HALF_OPEN":
                c["state"] = "OPEN"
                c["last_state_change"] = now

        return {
            "service": service,
            "state": c["state"],
            "failure_count": c["failure_count"],
            "total_calls": c["total_calls"],
            "total_failures": c["total_failures"]
        }

    def get_state(self, service: str) -> Dict[str, Any]:
        c = self._get_circuit(service)
        now = time.time()
        time_to_half_open = 0.0
        if c["state"] == "OPEN":
            elapsed = now - c["last_state_change"]
            time_to_half_open = max(0.0, self.recovery_timeout_seconds - elapsed)

        return {
            "service": service,
            "state": c["state"],
            "failure_count": c["failure_count"],
            "time_to_half_open_seconds": round(time_to_half_open, 2),
            "total_calls": c["total_calls"],
            "total_failures": c["total_failures"]
        }

    def reset(self, service: str) -> Dict[str, Any]:
        if service in self.circuits:
            c = self.circuits[service]
            c["state"] = "CLOSED"
            c["failure_count"] = 0
            c["consecutive_successes"] = 0
            c["last_state_change"] = time.time()
        return {"status": "reset", "service": service, "state": "CLOSED"}
