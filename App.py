import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Datei zum Speichern der Daten
DB_FILE = "nachtigallenhof_log.csv"

# Falls die Datei noch nicht existiert, erstellen wir sie mit Spalten
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Zeitstempel", "Name"])
    df.to_csv(DB_FILE, index=False)

st.set_page_config(page_title="Nachtigallenhof Check-in", page_icon="🐴", layout="centered")

# Titel der App
st.title("🐴 Nachtigallenhof")
st.subheader("Anlagen-Nutzung registrieren")

# --- REITER-BEREICH ---
st.info("Bitte trage deinen Namen ein, bevor du auf den Hof fährst.")

# Eingabefeld für den Namen
reiter_name = st.text_input("Dein Vor- und Nachname:", placeholder="z. B. Anna Müller")

if st.button("Jetzt einchecken & Tor nutzen", type="primary"):
    if reiter_name.strip() == "":
        st.error("Bitte gib zuerst deinen Namen ein!")
    else:
        # Neuen Eintrag erstellen
        jetzt = datetime.now().strftime("%d.%m.%Y %H:%M")
        neuer_eintrag = pd.DataFrame([{"Zeitstempel": jetzt, "Name": reiter_name.strip()}])
        
        # In die Datei speichern
        neuer_eintrag.to_csv(DB_FILE, mode='a', header=False, index=False)
        
        st.success(f"Danke {reiter_name}! Dein Check-in wurde um {jetzt} registriert. Gute Fahrt!")

# --- ADMIN-BEREICH (Für dich zur Abrechnung) ---
st.markdown("---")
with st.expander("🔐 Admin-Bereich (Abrechnung & Zähler)"):
    # Einfacher Passwortschutz (Ersetze 'hof2026' durch dein Wunschpasswort)
    passwort = st.text_input("Admin-Passwort eingeben:", type="password")
    
    if passwort == "hof2026":
        st.write("### Aktuelle Statistik (Halbjahr)")
        
        # Daten laden
        df_log = pd.read_csv(DB_FILE)
        
        if df_log.empty:
            st.info("Es gibt noch keine registrierten Nutzungen.")
        else:
            # Zählen, wie oft jeder Name vorkommt
            nutzungs_anzahl = df_log["Name"].value_counts().reset_index()
            nutzungs_anzahl.columns = ["Reiter", "Anzahl Nutzungen"]
            
            # Tabelle anzeigen
            st.dataframe(nutzungs_anzahl, use_container_width=True)
            
            # Zähler zurücksetzen
            st.write("### Zähler zurücksetzen")
            st.warning("Achtung: Das Zurücksetzen löscht alle bisherigen Einträge für das neue Halbjahr!")
            
            if st.button("Zähler jetzt auf Null setzen"):
                # Datei leeren (nur die Kopfzeile bleibt)
                df_empty = pd.DataFrame(columns=["Zeitstempel", "Name"])
                df_empty.to_csv(DB_FILE, index=False)
                st.success("Zähler erfolgreich auf Null gesetzt! Die Seite lädt gleich neu.")
                st.rerun()
