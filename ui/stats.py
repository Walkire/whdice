"""Summary statistics computation for simulation results."""

import statistics
from typing import List, Dict, Optional


def compute_summary_stats(
    raw_results: List[Dict],
    simulations: int,
) -> Optional[Dict[str, Dict[str, float]]]:
    """Compute average, median, min, max for wounds, kills, and damage.

    Args:
        raw_results: List of per-weapon result dicts from simulate().
        simulations: Number of simulation iterations used.

    Returns:
        Dict mapping metric names to their summary stats, or None if no results.
        Each metric has keys: average, median, min, max, count.
    """
    if not raw_results or simulations <= 0:
        return None

    # Aggregate totals across all weapons per metric
    total_wounds = sum(r.get("wounds", 0) for r in raw_results)
    total_kills = sum(r.get("kills", 0) for r in raw_results)
    total_damage = sum(r.get("damage", 0) for r in raw_results)
    total_fnp = sum(r.get("fnp", 0) for r in raw_results)

    # Per-weapon averages (the simulation already aggregates across iterations)
    wounds_per_weapon = [r.get("wounds", 0) / simulations for r in raw_results]
    kills_per_weapon = [r.get("kills", 0) / simulations for r in raw_results]
    damage_per_weapon = [r.get("damage", 0) / simulations for r in raw_results]
    fnp_per_weapon = [r.get("fnp", 0) / simulations for r in raw_results]

    def _stats_for(values: List[float]) -> Dict[str, float]:
        if not values:
            return {"average": 0, "median": 0, "min": 0, "max": 0, "count": 0}
        return {
            "average": round(statistics.mean(values), 2),
            "median": round(statistics.median(values), 2),
            "min": round(min(values), 2),
            "max": round(max(values), 2),
            "count": len(values),
        }

    return {
        "wounds": _stats_for(wounds_per_weapon),
        "kills": _stats_for(kills_per_weapon),
        "damage": _stats_for(damage_per_weapon),
        "after_fnp": _stats_for(fnp_per_weapon),
        "totals": {
            "wounds": round(total_wounds / simulations, 2),
            "kills": round(total_kills / simulations, 2),
            "damage": round(total_damage / simulations, 2),
            "after_fnp": round(total_fnp / simulations, 2),
        },
    }
