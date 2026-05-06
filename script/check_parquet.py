import pandas as pd
import pyarrow.parquet as pq
from pyarrow.parquet import ParquetFile

parquet_file = "data/ton_v2.parquet"

print("--- Controllo Metadati (Zero consumo RAM) ---")
# Leggiamo solo i metadati per vedere il numero di righe
metadata = pq.read_metadata(parquet_file)
print(f"Numero totale di righe: {metadata.num_rows}")
print(f"Numero di colonne: {metadata.num_columns}")

print("\n--- Struttura Colonne ---")
# Leggiamo solo lo schema (nomi e tipi)
schema = pq.read_schema(parquet_file)
print(schema)

# --- NUOVA SEZIONE: CHECK VALORI NULLI ---
print("\n--- Scansione Valori Nulli (Analisi a blocchi) ---")
pfile = ParquetFile(parquet_file)
null_series = pd.Series(0, index=schema.names)

# Leggiamo il file a blocchi di 1 milione di righe per non saturare la RAM
for batch in pfile.iter_batches(batch_size=1_000_000):
    chunk_df = batch.to_pandas()
    null_series = null_series.add(chunk_df.isnull().sum())

if null_series.sum() == 0:
    print("Ottimo: Non ci sono valori nulli nel dataset.")
else:
    print("Attenzione! Trovati valori nulli nelle seguenti colonne:")
    print(null_series[null_series > 0])

print("\n--- Anteprima Dati (Caricamento parziale) ---")
# Usiamo PyArrow per leggere solo le prime 5 righe senza caricare 2.5GB
from pyarrow.parquet import ParquetFile
pfile = ParquetFile(parquet_file)
first_rows = next(pfile.iter_batches(batch_size=10)).to_pandas()
print(first_rows)