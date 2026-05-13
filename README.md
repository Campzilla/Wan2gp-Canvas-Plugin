# Wan2GP Canvas Plugin

Un potente plugin per **Wan2GP** che aggiunge un **Canvas Editor** integrato direttamente nell'interfaccia UI. Ti permette di disegnare, spostare, ridimensionare e modificare le immagini, inviandole in un click al nodo "Reference Image".

## 🚀 Funzionalità principali

- **Immagini su Canvas:** Importa le tue immagini o incollale dagli appunti.
- **Strumenti di Precisione:** Sposta (nudge), ridimensiona, ruota, specchia e gestisci l'opacità con controlli avanzati.
- **Supporto multi-livello:** Disegna a mano libera in modo non distruttivo usando pennelli di dimensioni e colori personalizzabili.
- **Integrazione One-Click:** Un solo pulsante invia il risultato finale *direttamente* nel campo di input di Wan2GP (Reference Image).
- **Esportazione:** Salva il tuo lavoro sul computer in formato `.png` o `.jpg`.
- **Completamente Locale e Sicuro:** Essendo un plugin nativo e interamente lato client (React/Gradio), non ci sono connettori cloud né telemetrie nascoste. I tuoi dati restano sul dispositivo!

## 📦 Installazione

Installare questo plugin è semplice, ti basta copiare la cartella direttamente in Wan2GP:

1. Scarica e/o estrai lo zip contenente la cartella `wan2gp_canvas_plugin` in modo da avere dentro il suo contenuto (`__init__.py`, `plugin.py`, la directory `dist`, ecc.).
2. Sposta l'intera cartella `wan2gp_canvas_plugin` nella sotto-directory `plugins/` della tua installazione di Wan2GP (risultato `wan2gp/plugins/wan2gp_canvas_plugin`).
3. Avvia (o riavvia) l'ambiente Wan2GP.
4. Troverai la nuova scheda **"Canvas Editor"** pronta all'uso!

## 🛠 Costruito Con
* **Python** & **Gradio** per il bridge con l'app madre (Wan2GP)
* **React** e **Konva** (Vite in single-file-mode) per creare il canvas

## 📝 Licenza

Rilasciato sotto licenza **MIT**. Sentiti libero di utilizzare, modificare e condividere liberamente questo plugin!
