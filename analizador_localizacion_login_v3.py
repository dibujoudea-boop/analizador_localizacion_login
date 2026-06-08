
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd


CONFIG = {
    "weights": {
        "location_not_home": 20,
        "country_change": 12,
        "new_device": 8,
        "risky_network": 18,
        "timezone_mismatch": 8,
        "off_hours": 7,
        "high_speed_travel": 20,
        "medium_speed_travel": 10,
        "high_ip_reputation": 12,
        "medium_ip_reputation": 6,
    },
    "thresholds": {
        "high_speed_kmh": 900,
        "medium_speed_kmh": 300,
        "risk_medium": 25,
        "risk_high": 50,
    },
    "off_hours": set([0, 1, 2, 3, 4, 5, 23]),
    "risky_networks": {"proxy", "hosting", "tor", "vpn"},
}


@dataclass
class ScoreResult:
    score: int
    level: str
    reasons: List[str]


def load_dataset(csv_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.sort_values(["user_id", "timestamp"]).reset_index(drop=True)
    return df


def score_event(row: pd.Series, previous_row: pd.Series | None, config: Dict) -> ScoreResult:
    w = config["weights"]
    t = config["thresholds"]

    score = 0
    reasons: List[str] = []

    if str(row["declared_city"]).lower() != str(row["known_location"]).lower():
        score += w["location_not_home"]
        reasons.append("localizacion_distinta_a_la_habitual")

    if int(row.get("country_change", 0)) == 1:
        score += w["country_change"]
        reasons.append("cambio_de_pais")

    if int(row.get("is_new_device", 0)) == 1:
        score += w["new_device"]
        reasons.append("nuevo_dispositivo")

    if str(row.get("network_type", "")).lower() in config["risky_networks"]:
        score += w["risky_network"]
        reasons.append(f"red_sospechosa:{row.get('network_type')}")

    if int(row.get("timezone_mismatch", 0)) == 1:
        score += w["timezone_mismatch"]
        reasons.append("desajuste_de_zona_horaria")

    hour = row["timestamp"].hour
    if hour in config["off_hours"]:
        score += w["off_hours"]
        reasons.append("horario_atipico")

    travel_speed = float(row.get("travel_speed_kmh", 0) or 0)
    if travel_speed >= t["high_speed_kmh"]:
        score += w["high_speed_travel"]
        reasons.append("viaje_imposible")
    elif travel_speed >= t["medium_speed_kmh"]:
        score += w["medium_speed_travel"]
        reasons.append("desplazamiento_poco_plausible")

    ip_rep = str(row.get("ip_reputation", "")).lower()
    if ip_rep == "high":
        score += w["high_ip_reputation"]
        reasons.append("reputacion_ip_alta")
    elif ip_rep == "medium":
        score += w["medium_ip_reputation"]
        reasons.append("reputacion_ip_media")

    # Small sequential coherence penalty
    if previous_row is not None:
        if row["declared_city"] != previous_row["declared_city"] and float(row.get("time_since_prev_min", 0) or 0) < 60:
            score += 10
            reasons.append("cambio_geografico_brusco_respecto_al_evento_anterior")

    if score >= t["risk_high"]:
        level = "alto"
    elif score >= t["risk_medium"]:
        level = "medio"
    else:
        level = "bajo"

    return ScoreResult(score=score, level=level, reasons=reasons)


def compare_expected_vs_obtained(expected: str, obtained: str) -> str:
    order = {"bajo": 1, "medio": 2, "alto": 3}
    if expected == obtained:
        return "acierto"
    if order[obtained] < order[expected]:
        return "subestimacion"
    return "sobrestimacion"


def run_analysis(df: pd.DataFrame, config: Dict = CONFIG) -> pd.DataFrame:
    results = []

    for user_id, group in df.groupby("user_id", sort=False):
        previous_row = None
        for _, row in group.iterrows():
            score_result = score_event(row, previous_row, config)
            comparison = compare_expected_vs_obtained(
                str(row["expected_result"]).lower(),
                score_result.level,
            )
            enriched = row.to_dict()
            enriched["risk_score"] = score_result.score
            enriched["risk_level"] = score_result.level
            enriched["risk_reasons"] = "; ".join(score_result.reasons)
            enriched["comparison_result"] = comparison
            results.append(enriched)
            previous_row = row

    return pd.DataFrame(results)


def build_summary_tables(df_results: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summary_risk = (
        df_results["risk_level"]
        .value_counts()
        .rename_axis("risk_level")
        .reset_index(name="count")
    )

    summary_comparison = (
        df_results["comparison_result"]
        .value_counts()
        .rename_axis("comparison_result")
        .reset_index(name="count")
    )

    summary_by_scenario = pd.crosstab(df_results["scenario_type"], df_results["risk_level"]).reset_index()

    return summary_risk, summary_comparison, summary_by_scenario


def export_outputs(df_results: pd.DataFrame, output_dir: str | Path) -> None:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    summary_risk, summary_comparison, summary_by_scenario = build_summary_tables(df_results)

    df_results.to_csv(output_dir / "resultados_v3_analizador_localizacion_login.csv", index=False)
    summary_risk.to_csv(output_dir / "resumen_riesgo_v3.csv", index=False)
    summary_comparison.to_csv(output_dir / "resumen_comparacion_v3.csv", index=False)
    summary_by_scenario.to_csv(output_dir / "resumen_escenario_vs_riesgo_v3.csv", index=False)


def main() -> None:
    csv_path = Path("logins_sinteticos_v3_analizador_localizacion_login.csv")
    output_dir = Path("output")

    df = load_dataset(csv_path)
    df_results = run_analysis(df, CONFIG)
    export_outputs(df_results, output_dir)

    print("Proceso completado.")
    print(f"Eventos procesados: {len(df_results)}")
    print("Archivos generados en /output")


if __name__ == "__main__":
    main()
