from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd

from src.risk_engine import score_login_event, compare_expected_vs_obtained


def load_dataset(csv_path: str | Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    df = df.sort_values(["user_id", "timestamp"]).reset_index(drop=True)
    return df


def run_batch_analysis(df: pd.DataFrame) -> pd.DataFrame:
    results = []

    for _, row in df.iterrows():
        event = row.to_dict()
        result = score_login_event(event)

        enriched = row.to_dict()
        enriched["risk_score"] = result.score
        enriched["risk_level"] = result.level
        enriched["recommended_action"] = result.recommended_action
        enriched["risk_reasons"] = "; ".join(result.reasons)

        if "expected_result" in enriched and pd.notna(enriched["expected_result"]):
            enriched["comparison_result"] = compare_expected_vs_obtained(
                str(enriched["expected_result"]),
                result.level,
            )
        else:
            enriched["comparison_result"] = "no_aplica"

        results.append(enriched)

    return pd.DataFrame(results)


def build_summary_tables(
    df_results: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    summary_risk = (
        df_results["risk_level"]
        .value_counts()
        .reindex(["bajo", "medio", "alto"])
        .fillna(0)
        .astype(int)
        .rename_axis("risk_level")
        .reset_index(name="count")
    )

    summary_action = (
        df_results["recommended_action"]
        .value_counts()
        .rename_axis("recommended_action")
        .reset_index(name="count")
    )

    summary_comparison = (
        df_results["comparison_result"]
        .value_counts()
        .reindex(["acierto", "subestimacion", "sobrestimacion"])
        .fillna(0)
        .astype(int)
        .rename_axis("comparison_result")
        .reset_index(name="count")
    )

    summary_by_scenario = pd.crosstab(
        df_results["scenario_type"],
        df_results["risk_level"],
    ).reset_index()

    return summary_risk, summary_action, summary_comparison, summary_by_scenario


def main() -> None:
    input_path = Path("data/logins_sinteticos_v4_analizador_localizacion_login.csv")
    output_dir = Path("outputs")
    output_dir.mkdir(parents=True, exist_ok=True)

    df = load_dataset(input_path)
    df_results = run_batch_analysis(df)

    df_results.to_csv(
        output_dir / "resultados_detallados_v4.csv",
        index=False,
    )

    summary_risk, summary_action, summary_comparison, summary_by_scenario = build_summary_tables(df_results)

    summary_risk.to_csv(output_dir / "tabla_riesgo_v4.csv", index=False)
    summary_action.to_csv(output_dir / "tabla_acciones_v4.csv", index=False)
    summary_comparison.to_csv(output_dir / "tabla_comparacion_v4.csv", index=False)
    summary_by_scenario.to_csv(output_dir / "tabla_escenario_vs_riesgo_v4.csv", index=False)

    print("Análisis batch completado.")
    print(f"Eventos procesados: {len(df_results)}")
    print("Resultados guardados en outputs/")


if __name__ == "__main__":
    main()
