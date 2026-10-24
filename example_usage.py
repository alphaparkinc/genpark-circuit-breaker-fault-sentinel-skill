"""Example usage for GenPark Circuit Breaker Fault Sentinel."""
from client import CircuitBreakerFaultSentinel

def main():
    sentinel = CircuitBreakerFaultSentinel(failure_threshold=3, recovery_timeout_seconds=5.0)
    service = "external_search_api"

    print(f"Can execute initially: {sentinel.can_execute(service)}")

    print("
Simulating 3 consecutive failures...")
    for i in range(3):
        res = sentinel.record_result(service, success=False)
        print(f" - Failure #{i+1} recorded -> Circuit state: {res['state']}")

    print(f"
Can execute after tripping: {sentinel.can_execute(service)} (Fails fast)")
    print("Circuit details:", sentinel.get_state(service))

if __name__ == "__main__":
    main()
