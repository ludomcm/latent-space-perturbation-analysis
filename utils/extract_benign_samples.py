import argparse
import pathlib
import pandas as pd
import pyarrow.parquet as pq


def extract_random_benign_low_ram(input_path: pathlib.Path):
    # Genera l'output partendo dall'input: nome_base + _benign_samples.parquet
    output_name = f"{input_path.stem}_benign_samples.parquet"
    output_path = input_path.parent / output_name

    print(f"Inizio scansione globale su {input_path}...")
    print(f"Il file di output sarà salvato in: {output_path}")

    parquet_file = pq.ParquetFile(input_path)
    benign_chunks = []

    # Iteriamo su tutti i row groups del file Parquet
    for i in range(parquet_file.num_row_groups):
        try:
            # Leggiamo il gruppo di righe
            table_chunk = parquet_file.read_row_group(i)
            df_chunk = table_chunk.to_pandas()

            # Filtriamo usando 'Label' con la L maiuscola
            filtered = df_chunk[df_chunk["Label"] == 0]

            if not filtered.empty:
                # Prendiamo un piccolo campione casuale da ogni blocco (max 3000 righe)
                n_to_sample = min(len(filtered), 3000)
                benign_chunks.append(
                    filtered.sample(n=n_to_sample, random_state=42)
                )

            if i % 20 == 0:
                print(
                    f"Avanzamento: Processato gruppo {i}/{parquet_file.num_row_groups}..."
                )

        except Exception as e:
            print(f"Errore nel gruppo {i}: {e}")
            continue

    if not benign_chunks:
        print(
            "Errore critico: Nessun dato trovato con Label == 0. Ricontrolla i nomi delle colonne."
        )
        return

    # Uniamo i campioni raccolti da tutto il file
    print("Unione dei campioni e finalizzazione...")
    final_df = pd.concat(benign_chunks)

    # Se abbiamo raccolto più di 100k, riduciamo a 100k esatti in modo casuale
    if len(final_df) > 100000:
        final_df = final_df.sample(n=100000, random_state=42)

    # Identifichiamo le feature per l'analisi (numeriche e sensate)
    exclude = [
        "Label",
        "type",
        "ts",
        "src_port",
        "dst_port",
        "src_ip",
        "dst_ip",
    ]
    numeric_cols = final_df.select_dtypes(include=["number"]).columns
    perturbable = [
        c for c in numeric_cols if c in final_df.columns and c not in exclude
    ]

    print("\n--- STATISTICHE PER LA PERTURBAZIONE ---")
    print(
        final_df[perturbable]
        .describe()
        .loc[["min", "max", "std"]]
        .transpose()
    )

    # Salvataggio finale
    final_df.to_parquet(output_path)
    print(f"\nDataset salvato con successo: {output_path}")
    print(f"Totale campioni benigni raccolti: {len(final_df)}")


if __name__ == "__main__":
    # Configurazione degli argomenti da riga di comando
    parser = argparse.ArgumentParser(
        description="Estrae campioni benigni da un file Parquet in modo ottimizzato per la RAM."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Percorso del file Parquet di input (es. data/ton_v2.parquet)",
    )

    args = parser.parse_args()

    # Convertiamo la stringa ricevuta in un oggetto Path di pathlib
    path_di_input = pathlib.Path(args.input_file)

    # Controllo di sicurezza: il file esiste davvero?
    if not path_di_input.exists():
        print(f"Errore: Il file '{path_di_input}' non esiste.")
    else:
        extract_random_benign_low_ram(path_di_input)