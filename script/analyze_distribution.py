import pandas as pd

# Carichiamo il file (abbiamo visto che la RAM regge se non facciamo operazioni folli)
df = pd.read_parquet("data/ton_v2.parquet", columns=['Attack', 'Label'])

print("--- Distribuzione Classi (Label) ---")
# 0 = Benign, 1 = Attack
print(df['Label'].value_counts(normalize=True) * 100)

print("\n--- Conteggio Specifico Attacchi ---")
print(df['Attack'].value_counts())

print("\n--- Percentuale per ogni tipo di traffico ---")
print(df['Attack'].value_counts(normalize=True) * 100)