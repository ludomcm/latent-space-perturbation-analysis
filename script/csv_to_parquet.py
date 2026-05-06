import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import time

def convert_csv_to_parquet():
    # Configuration
    csv_file = "data/ton_v2.csv"  
    parquet_file = "data/ton_v2.parquet"
    chunk_size = 500000  # 500k rows per chunk is safe for 16GB RAM
    
    print(f"Starting conversion: {csv_file} -> {parquet_file}")
    start_time = time.time()
    
    try:
        # Initialize the CSV reader in chunks
        # low_memory=False helps with type inference in large datasets
        reader = pd.read_csv(csv_file, chunksize=chunk_size, low_memory=False)
        
        writer = None
        
        for i, chunk in enumerate(reader):
            # Convert pandas DataFrame chunk to PyArrow Table
            table = pa.Table.from_pandas(chunk)
            
            # On first iteration, initialize the ParquetWriter with the schema
            if writer is None:
                writer = pq.ParquetWriter(parquet_file, table.schema)
            
            writer.write_table(table)
            print(f"Processed chunk {i+1} (approx. {(i+1)*chunk_size:,} rows)...")
            
        if writer:
            writer.close()
            
        end_time = time.time()
        elapsed = (end_time - start_time) / 60
        print(f"\n✅ Success! Conversion completed in {elapsed:.2f} minutes.")

    except FileNotFoundError:
        print(f"❌ Error: The file '{csv_file}' was not found.")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    convert_csv_to_parquet()