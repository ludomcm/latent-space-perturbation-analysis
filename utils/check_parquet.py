import pandas as pd
import pyarrow.parquet as pq
from pyarrow.parquet import ParquetFile
import argparse
from pathlib import Path

def check_parquet(parquet_file: str):
    print(f"--- Controllo file: {parquet_file} ---")

    print("\n--- Controllo Metadati (Zero consumo RAM) ---")
    metadata = pq.read_metadata(parquet_file)
    print(f"Numero totale di righe: {metadata.num_rows}")
    print(f"Numero di colonne: {metadata.num_columns}")

    print("\n--- Struttura Colonne ---")
    schema = pq.read_schema(parquet_file)
    print(schema)

    print("\n--- Scansione Valori Nulli (Analisi a blocchi) ---")
    pfile = ParquetFile(parquet_file)
    null_series = pd.Series(0, index=schema.names)

    for batch in pfile.iter_batches(batch_size=1_000_000):
        chunk_df = batch.to_pandas()
        null_series = null_series.add(chunk_df.isnull().sum())

    if null_series.sum() == 0:
        print("Ottimo: Non ci sono valori nulli nel dataset.")
    else:
        print("Attenzione! Trovati valori nulli nelle seguenti colonne:")
        print(null_series[null_series > 0])

    print("\n--- Anteprima Dati (Caricamento parziale) ---")
    pfile = ParquetFile(parquet_file)
    first_rows = next(pfile.iter_batches(batch_size=10)).to_pandas()
    print(first_rows)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Controlla un file Parquet.")
    parser.add_argument("parquet_file", help="Path al file Parquet (es. ton_v2.parquet)")
    args = parser.parse_args()

    path = Path(args.parquet_file)
    if not path.exists():
        print(f"Errore: il file '{path}' non esiste.")
    elif path.suffix.lower() != ".parquet":
        print(f"Attenzione: '{path}' non sembra un file .parquet.")
    else:
        check_parquet(str(path))