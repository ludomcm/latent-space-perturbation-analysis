import argparse
import pathlib
import pandas as pd
import pyarrow.parquet as pq


def extract_random_malicious_low_ram(input_path: pathlib.Path):
    # Genera l'output partendo dall'input: nome_base + _malicious_samples.parquet
    output_name = f"{input_path.stem}_malicious_samples.parquet"
    output_path = input_path.parent / output_name

    print(f"Inizio estrazione ATTACCHI da {input_path}...")
    print(f"Il file di output sarà salvato in: {output_path}")

    parquet_file = pq.ParquetFile(input_path)
    malicious_chunks = []

    # Iteriamo su tutti i row groups del file Parquet
    for i in range(parquet_file.num_row_groups):
        try:
            table_chunk = parquet_file.read_row_group(i)
            df_chunk = table_chunk.to_pandas()

            # --- Label == 1 sono gli attacchi ---
            filtered = df_chunk[df_chunk["Label"] == 1]

            if not filtered.empty:
                # Campioniamo per avere varietà (max 3000 righe)
                n_to_sample = min(len(filtered), 3000)
                malicious_chunks.append(
                    filtered.sample(n=n_to_sample, random_state=42)
                )

            if i % 20 == 0:
                print(
                    f"Processato gruppo {i}/{parquet_file.num_row_groups}..."
                )

        except Exception as e:
            print(f"Errore nel gruppo {i}: {e}")
            continue

    if not malicious_chunks:
        print("Errore: Nessun attacco trovato (Label == 1).")
        return

    print("Finalizzazione dataset malicious...")
    final_df = pd.concat(malicious_chunks)

    # Prendiamo 100k campioni di attacco
    if len(final_df) > 100000:
        final_df = final_df.sample(n=100000, random_state=42)

    # Statistica utile per la tesi: quanti attacchi di ogni tipo abbiamo preso?
    if "type" in final_df.columns:
        print("\n--- DISTRIBUZIONE TIPI DI ATTACCO ESTRATTI ---")
        print(final_df["type"].value_counts())

    # Salvataggio finale
    final_df.to_parquet(output_path)
    print(f"\nDataset attacchi salvato: {output_path}")


if __name__ == "__main__":
    # Configurazione degli argomenti da riga di comando
    parser = argparse.ArgumentParser(
        description="Estrae campioni malevoli (attacchi) da un file Parquet in modo ottimizzato per la RAM."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Percorso del file Parquet di input (es. data/ton_v2.parquet)",
    )

    args = parser.parse_args()

    # Convertiamo la stringa ricevuta in un oggetto Path di pathlib
    path_di_input = pathlib.Path(args.input_file)

    # Controllo di sicurezza sull'esistenza del file
    if not path_di_input.exists():
        print(f"Errore: Il file '{path_di_input}' non esiste.")
    else:
        extract_random_malicious_low_ram(path_di_input)