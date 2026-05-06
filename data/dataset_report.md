# Report Analisi Dataset: ToN_IoT (v2)

## Informazioni Generali
*   **Data Analisi:** 2026-05-06
*   **Formato File:** Parquet (convertito da CSV)
*   **Integrità:** 16.940.496 righe (Corrispondenza 100% con i record del file sorgente).
*   **Valori Nulli:** 0 (Dataset verificato come "clean").

## Distribuzione delle Classi (Macro)
| Etichetta | Descrizione | Conteggio | Percentuale |
| :--- | :--- | :--- | :--- |
| **0** | Benign (Traffico Normale) | 6.099.469 | 36.00% |
| **1** | Attack (Traffico Malevolo) | 10.841.027 | 64.00% |

## Dettaglio Tipologie di Attacco
| Tipo di Attacco | Conteggio | Percentuale sul Totale |
| :--- | :--- | :--- |
| **Benign** | 6.099.469 | 36.005 % |
| **Scanning** | 3.781.419 | 22.322 % |
| **XSS** | 2.455.020 | 14.492 % |
| **DDoS** | 2.026.234 | 11.961 % |
| **Password** | 1.153.323 | 6.808 % |
| **DoS** | 712.609 | 4.207 % |
| **Injection** | 684.465 | 4.040 % |
| **Backdoor** | 16.809 | 0.099 % |
| **MITM** | 7.723 | 0.046 % |
| **Ransomware** | 3.425 | 0.020 % |

## Osservazioni Tecniche per la Tesi
1. **Sbilanciamento Estremo:** Le classi *Backdoor*, *MITM* e *Ransomware* sono sotto-rappresentate (complessivamente < 0.2%). Sarà necessario valutare tecniche di bilanciamento (SMOTE o Weighted Loss) in fase di addestramento.
2. **Dominanza Scanning:** Oltre il 22% del traffico è costituito da scansioni, indicando una forte presenza di attività di ricognizione nel dataset.