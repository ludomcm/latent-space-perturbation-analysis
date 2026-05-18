import argparse
import pathlib
import pandas as pd


def analyze_parquet_distribution(input_path: pathlib.Path):
    print(f"Inizio analisi della distribuzione su: {input_path}\n")

    try:
        # Carichiamo solo le colonne necessarie per ottimizzare la RAM
        df = pd.read_parquet(
            input_path, columns=["Attack", "Label"]
        )
    except ValueError as e:
        print(
            f"Errore: Assicurati che il file contenga le colonne 'Attack' e 'Label'. Details: {e}"
        )
        return
    except Exception as e:
        print(f"Errore durante la lettura del file Parquet: {e}")
        return

    print("--- Distribuzione Classi (Label) ---")
    # 0 = Benign, 1 = Attack
    if "Label" in df.columns:
        print(df["Label"].value_counts(normalize=True) * 100)
    else:
        print("Colonna 'Label' non trovata.")

    print("\n--- Conteggio Specifico Attacchi ---")
    if "Attack" in df.columns:
        print(df["Attack"].value_counts())
    else:
        print("Colonna 'Attack' non trovata.")

    print("\n--- Percentuale per ogni tipo di traffico ---")
    if "Attack" in df.columns:
        print(df["Attack"].value_counts(normalize=True) * 100)


if __name__ == "__main__":
    # Configurazione degli argomenti da riga di comando
    parser = argparse.ArgumentParser(
        description="Analizza la distribuzione delle classi e dei tipi di attacco in un file Parquet."
    )
    parser.add_argument(
        "input_file",
        type=str,
        help="Percorso del file Parquet da analizzare (es. data/ton_v2.parquet)",
    )

    args = parser.parse_args()

    # Convertiamo il percorso in un oggetto Path
    path_di_input = pathlib.Path(args.input_file)

    # Controllo di sicurezza
    if not path_di_input.exists():
        print(f"Errore: Il file '{path_di_input}' non esiste.")
    else:
        analyze_parquet_distribution(path_di_input)