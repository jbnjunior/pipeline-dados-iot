"""Lê o CSV do Kaggle, padroniza os campos e grava no PostgreSQL."""
import argparse
from pathlib import Path
import pandas as pd
from sqlalchemy import text
from src.db import ROOT, get_engine

DEFAULT_CSV = ROOT / "data" / "temperature-readings-iot-devices.csv"

def find_column(df, candidates, required=True):
    normalized = {str(col).strip().lower(): col for col in df.columns}
    for candidate in candidates:
        if candidate in normalized:
            return normalized[candidate]
    if required:
        raise ValueError(
            f"Não encontrei nenhuma coluna entre {candidates}. "
            f"Colunas encontradas: {list(df.columns)}"
        )
    return None

def transform_csv(csv_path: Path) -> pd.DataFrame:
    """Normaliza nomes comuns do dataset do Kaggle para um esquema consistente."""
    if not csv_path.exists():
        raise FileNotFoundError(
            f"CSV não encontrado: {csv_path}\n"
            "Baixe o CSV do Kaggle e coloque-o em data/temperature-readings-iot-devices.csv"
        )
    raw = pd.read_csv(csv_path)
    raw.columns = [str(c).strip() for c in raw.columns]

    temp_col = find_column(raw, ["temp", "temperature", "temperature_c", "temperatura"])
    date_col = find_column(raw, ["noted_date", "timestamp", "datetime", "date", "created_at"])
    device_col = find_column(raw, ["room_id/id", "room_id", "device_id", "sensor_id", "device"], required=False)
    location_col = find_column(raw, ["out/in", "location", "room_type", "environment"], required=False)

    result = pd.DataFrame()
    result["device_id"] = raw[device_col].astype("string").fillna("desconhecido") if device_col else "desconhecido"
    result["recorded_at"] = pd.to_datetime(raw[date_col], errors="coerce", dayfirst=True)
    result["temperature"] = pd.to_numeric(raw[temp_col], errors="coerce")
    result["location"] = raw[location_col].astype("string") if location_col else pd.NA

    result = result.dropna(subset=["recorded_at", "temperature"])
    result = result.drop_duplicates(subset=["device_id", "recorded_at", "temperature"])
    result["device_id"] = result["device_id"].astype(str)
    result["location"] = result["location"].astype("string").fillna("não informado")
    if result.empty:
        raise ValueError("Nenhuma linha válida restou após a limpeza do CSV.")
    return result

def main():
    parser = argparse.ArgumentParser(description="Ingestão do CSV de temperaturas IoT.")
    parser.add_argument("--csv", default=str(DEFAULT_CSV), help="Caminho do CSV do Kaggle.")
    args = parser.parse_args()

    df = transform_csv(Path(args.csv))
    engine = get_engine()
    with engine.begin() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS temperature_readings (
                reading_id BIGSERIAL PRIMARY KEY,
                device_id VARCHAR(100) NOT NULL,
                recorded_at TIMESTAMP NOT NULL,
                temperature DOUBLE PRECISION NOT NULL,
                location VARCHAR(100) NOT NULL DEFAULT 'não informado',
                ingested_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (device_id, recorded_at, temperature)
            )
        """))
        # Insert em lotes; ON CONFLICT impede duplicar leituras em reexecuções.
        for start in range(0, len(df), 1000):
            batch = df.iloc[start:start + 1000]
            for row in batch.itertuples(index=False):
                conn.execute(text("""
                    INSERT INTO temperature_readings
                        (device_id, recorded_at, temperature, location)
                    VALUES
                        (:device_id, :recorded_at, :temperature, :location)
                    ON CONFLICT (device_id, recorded_at, temperature) DO NOTHING
                """), {
                    "device_id": row.device_id,
                    "recorded_at": row.recorded_at.to_pydatetime(),
                    "temperature": float(row.temperature),
                    "location": str(row.location),
                })

    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM temperature_readings")).scalar_one()
    print(f"CSV processado: {len(df):,} linhas válidas.")
    print(f"Total atualmente no PostgreSQL: {total:,} leituras.")

if __name__ == "__main__":
    main()
