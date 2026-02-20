from typing import List, Dict, Any


def summarize_if_large(data: List[Dict]) -> List[Dict]:
    if len(data) > 10:
        return [{"summary": f"{len(data)} records found. Showing first 10."}]
    return data


def summarize_analytics(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """For analytics with >5 points: return summary (total, avg, trend) for voice."""
    if not data:
        return [{"summary": "No data", "total": 0, "avg": 0, "trend": "0%"}]
    values = [float(d.get("value", 0)) for d in data if isinstance(d.get("value"), (int, float))]
    if not values:
        return [{"summary": "No numeric values", "total": 0, "avg": 0, "trend": "0%"}]
    total = sum(values)
    avg = total / len(values)
    # Simple trend: compare first half avg to second half avg
    mid = len(values) // 2
    first_avg = sum(values[:mid]) / mid if mid else values[0]
    second_avg = sum(values[mid:]) / (len(values) - mid) if (len(values) - mid) else values[-1]
    pct = ((second_avg - first_avg) / first_avg * 100) if first_avg else 0
    trend = f"{pct:+.0f}%"
    return [
        {
            "summary": f"{len(data)} points: total={total:.0f}, avg={avg:.1f}, trend={trend}",
            "total": round(total, 2),
            "avg": round(avg, 2),
            "trend": trend,
            "data_type": "time-series",
        }
    ]
