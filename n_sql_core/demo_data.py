from __future__ import annotations
from typing import List, Dict, Any


def get_demo_routes() -> List[Dict[str, Any]]:
    """
    Returns a small in-memory "network.routes" table.

    In a real Law-N system, this would be fed by live telemetry from:
    - towers
    - devices
    - satellites
    - CLSI cloud
    """
    return [
        {
            "device": "0xA4C1",
            "channel": "Delta.Freq(42)",
            "frequency": 3600.0,  # MHz
            "g_layer": "5G",
            "tower_id": "TWR-001",
            "latency_ms": 32.4,
            "signal_quality": 0.92,
        },
        {
            "device": "0xA4C1",
            "channel": "Delta.Freq(21)",
            "frequency": 1800.0,
            "g_layer": "4G",
            "tower_id": "TWR-002",
            "latency_ms": 58.1,
            "signal_quality": 0.81,
        },
        {
            "device": "0xB9F0",
            "channel": "Gamma.Freq(11)",
            "frequency": 900.0,
            "g_layer": "3G",
            "tower_id": "TWR-003",
            "latency_ms": 95.7,
            "signal_quality": 0.66,
        },
        {
            "device": "0xC7AA",
            "channel": "Omega.Freq(88)",
            "frequency": 2600.0,
            "g_layer": "4G",
            "tower_id": "TWR-004",
            "latency_ms": 45.3,
            "signal_quality": 0.88,
        },
        {
            "device": "0xD123",
            "channel": "Theta.Freq(5)",
            "frequency": 700.0,
            "g_layer": "5G",
            "tower_id": "TWR-005",
            "latency_ms": 12.9,
            "signal_quality": 0.97,
        },
    ]
