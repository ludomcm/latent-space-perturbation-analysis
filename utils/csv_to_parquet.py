import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import time
import argparse
from pathlib import Path

def convert_csv_to_parquet(csv_file: str):
    # Ricava automaticamente il nome del file parquet dal csv
    parquet_file = str(Path(csv_file).with_suffix(".parquet"))
    chunk_size = 500000

    print(f"Starting conversion: {csv_file} -> {parquet_file}")
    start_time = time.time()

    try:
        reader = pd.read_csv(csv_file, chunksize=chunk_size, low_memory=False)
        writer = None

        for i, chunk in enumerate(reader):
            table = pa.Table.from_pandas(chunk)

            if writer is None:
                writer = pq.ParquetWriter(parquet_file, table.schema)

            writer.write_table(table)
            print(f"Processed chunk {i+1} (approx. {(i+1)*chunk_size:,} rows)...")

        if writer:
            writer.close()

        elapsed = (time.time() - start_time) / 60
        print(f"\nSuccess! Conversion completed in {elapsed:.2f} minutes.")
        print(f"Output saved to: {parquet_file}")

    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a CSV file to Parquet format.")
    parser.add_argument("csv_file", help="Path to the input CSV file (e.g. ton_v2.csv)")
    args = parser.parse_args()

    convert_csv_to_parquet(args.csv_file)