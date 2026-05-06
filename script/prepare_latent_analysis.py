import pyarrow.parquet as pq
import pandas as pd
import pathlib

DATA_DIR = pathlib.Path("data")
INPUT_FILE = DATA_DIR / "ton_v2.parquet"
OUTPUT_FILE = DATA_DIR / "benign_samples_100k_random.parquet"

def extract_random_benign_low_ram():
    print(f"Inizio scansione globale su {INPUT_FILE}...")
    
    parquet_file = pq.ParquetFile(INPUT_FILE)
    benign_chunks = []
    
    # Iteriamo su tutti i row groups del file Parquet
    for i in range(parquet_file.num_row_groups):
        try:
            # Leggiamo il gruppo di righe
            table_chunk = parquet_file.read_row_group(i)
            df_chunk = table_chunk.to_pandas()
            
            # Filtriamo usando 'Label' con la L maiuscola
            filtered = df_chunk[df_chunk['Label'] == 0]
            
            if not filtered.empty:
                # Prendiamo un piccolo campione casuale da ogni blocco (max 2000 righe)
                # Questo garantisce varietà senza saturare la RAM
                n_to_sample = min(len(filtered), 3000)
                benign_chunks.append(filtered.sample(n=n_to_sample, random_state=42))
            
            if i % 20 == 0:
                print(f"Avanzamento: Processato gruppo {i}/{parquet_file.num_row_groups}...")
                
        except Exception as e:
            print(f"Errore nel gruppo {i}: {e}")
            continue

    if not benign_chunks:
        print("Errore critico: Nessun dato trovato con Label == 0. Ricontrolla i nomi delle colonne.")
        return

    # Uniamo i campioni raccolti da tutto il file
    print("Unione dei campioni e finalizzazione...")
    final_df = pd.concat(benign_chunks)
    
    # Se abbiamo raccolto più di 100k, riduciamo a 100k esatti in modo casuale
    if len(final_df) > 100000:
        final_df = final_df.sample(n=100000, random_state=42)
    
    # Identifichiamo le feature per l'analisi (numeriche e sensate)
    exclude = ['Label', 'type', 'ts', 'src_port', 'dst_port', 'src_ip', 'dst_ip']
    numeric_cols = final_df.select_dtypes(include=['number']).columns
    perturbable = [c for c in numeric_cols if c in final_df.columns and c not in exclude]
    
    print("\n--- STATISTICHE PER LA PERTURBAZIONE ---")
    print(final_df[perturbable].describe().loc[['min', 'max', 'std']].transpose())
    
    # Salvataggio finale
    final_df.to_parquet(OUTPUT_FILE)
    print(f"\n✅ Dataset salvato con successo: {OUTPUT_FILE}")
    print(f"Totale campioni benigni raccolti: {len(final_df)}")

if __name__ == "__main__":
    extract_random_benign_low_ram()