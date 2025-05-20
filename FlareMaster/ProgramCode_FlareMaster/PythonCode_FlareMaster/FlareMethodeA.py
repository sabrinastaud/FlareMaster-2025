#FlareMaster Programm - Methode A File

'''Hier befindet sich der Code für die Auswertung von Image Flare nach Methode A
Das Hauptprogramm heißt FlareAppMain.py'''

#Zu importierende Bibliotheken
import streamlit as st
import pandas as pd

#Berechnung von H = Gain*ExposureTime*(1/(f-Wert^2))
def calc_h(gain, exp_time, f_val):
    return gain*exp_time * (1/(f_val**2))

#Berechnung Luma 
#Gewichtung nach menschlicher Farbwahrnehmung!!!
def calc_luma(r, g, b):
    return 0.299*r + 0.587*g + 0.114*b

#Berechnung Flare Wert
def calc_flare(y1, h1, y3, h2, y2):
    try:
        flare = (((y2 / h2) - (y3 / h2)) / (y1 / h1)) * 100 #Prozentangabe vom Image Flare
        return flare
    except ZeroDivisionError:
        #Division durch Null
        st.error("Division durch Null ist nicht möglich! Überprüfen Sie bitte Ihre Eingabewerte.")
        return None

#Speichern der Messung (NUR IN DER SESSION)
def save_button(name, y1, y2, h1, y3, h2, flare_value, gain_A1, f_val_A1, exp_time_A1, aufnahme1, aufnahme2, aufnahme3):
    new_entry = {
        "Name": name,
        "YLuma 1": y1,
        "YLuma 2": y2,
        "H1": h1,
        "YLuma 3": y3,
        "H2": h2,
        "Flare": flare_value,
        "Gain": gain_A1,
        "f-Wert": f_val_A1,
        "Belichtungszeit (s)": exp_time_A1,
        "Aufnahme 1": aufnahme1,
        "Aufnahme 2": aufnahme2,
        "Aufnahme 3": aufnahme3
    }
    if "measurements_A" not in st.session_state:
        st.session_state["measurements_A"] = []
    st.session_state["measurements_A"].append(new_entry)
    st.success("Messung wurde gespeichert!")

#Hauptfunktion Berechnung
def run_method_a():
    st.header("Flare-Berechnung - Methode A")

    tabs = st.tabs(["Aufnahme 1 (Chart 1)", "Aufnahme 2 (Chart 1)", "Aufnahme 3 (Chart 2)"])

    #Aufnahme 1
    with tabs[0]:
        st.subheader("Aufnahme 1 - Testchart 1")
        st.write("Geben Sie zum Start bitte den Namen der Messung an!")
        name = st.text_input("Name der Messung")
        st.write("Hier werden die Parameter aus der Messung mit Testchart 1 (hell) eingetragen. "
        "Die hellen (weißen) RGB Werte sollen dabei bei 225 +/- 8 liegen.")
        gain_A1 = st.number_input("Gain", min_value=0.0, step=0.5, value=1.0)
        exp_time_A1 = st.number_input("Belichtungszeit (s)", min_value=0.0, step=0.1)
        f_val_A1 = st.number_input("f-Wert", min_value=0.0, step=0.5, value=1.0)
        r1 = st.number_input("R-Wert (Aufnahme 1)", min_value=0, max_value=255) #Limitieren, das Wert nicht mehr als 255 sein kann (8-Bit Farbtiefe)
        g1 = st.number_input("G-Wert (Aufnahme 1)", min_value=0, max_value=255)
        b1 = st.number_input("B-Wert (Aufnahme 1)", min_value=0, max_value=255)
        aufnahme1 = [r1,g1,b1]
        y_luma1 = calc_luma(r1, g1, b1)
        h1 = calc_h(gain_A1, exp_time_A1, f_val_A1) #Exposure Value H
        st.write(f"YLuma 1 ist {y_luma1:.2f}")
        st.write(f"H1 ist {h1:.4f}")

    #Aufnahme 2
    with tabs[1]:
        st.subheader("Aufnahme 2 - Testchart 1")
        st.write("Hier wurde die Belichtungszeit aus Aufnahme 1 8x so hoch eingestellt. "
        "Der Gain und der f-Wert bleiben dabei die selben und müssen nicht nochmal angegeben werden.")
        r2 = st.number_input("R-Wert (Aufnahme 2)", min_value=0, max_value=255)
        g2 = st.number_input("G-Wert (Aufnahme 2)", min_value=0, max_value=255)
        b2 = st.number_input("B-Wert (Aufnahme 2)", min_value=0, max_value=255)
        aufnahme2 = [r2,g2,b2]
        y_luma2 = calc_luma(r2, g2, b2)
        h2 = h1 * 8  #H2 wird aus H1 berechnet
        st.write(f"YLuma 2 ist {y_luma2:.2f}")
        st.write(f"H2 ist {h2:.4f}")

    #Aufnahme 3
    with tabs[2]:
        st.subheader("Aufnahme 3 - Testchart 2")
        st.write("Hier werden die Werte von Testchart 2 (dunkel) angegeben. Die Einstellungen bleiben dabei die selben wie in Aufnahme 2.")
        r3 = st.number_input("R-Wert (Aufnahme 3)", min_value=0, max_value=255)
        g3 = st.number_input("G-Wert (Aufnahme 3)", min_value=0, max_value=255)
        b3 = st.number_input("B-Wert (Aufnahme 3)", min_value=0, max_value=255)
        aufnahme3 = [r3,g3,b3]
        y_luma3 = calc_luma(r3, g3, b3)
        st.write(f"YLuma 3 ist {y_luma3:.2f}")

        #Berechnung und Speicherung
        if st.button("Flare berechnen und speichern"):
            flare_value = calc_flare(y_luma1, h1, y_luma3, h2,y_luma2)
            if flare_value is not None:
                save_button(name, y_luma1,y_luma2, h1, y_luma3, h2, flare_value, gain_A1, f_val_A1, exp_time_A1, aufnahme1, aufnahme2, aufnahme3)
                st.success(f"Flare-Wert: {flare_value:.2f} %")
                with st.expander("Ergebnis und Details"):
                    st.write("Eine detaillierte Beschreibung der Messergebnisse befindet sich im Navigationsabschnitt 'Messverlauf'")
                    st.write(f"Name: {name}")
                    st.write(f"Flare-Wert: {flare_value:.2f} %")

#Anzeige der gespeicherten Messungen 
def display_measurements_a():
    st.header("Messverlauf für Methode A")
    st.write("Hier werden die aufgenommenen Messungen aus Methode A dargestellt. "
    "Sie können ganz einfach als Tabelle (.csv) oder als Grafik heruntergeladen und gespeichert werden.")
    if "measurements_A" in st.session_state and st.session_state["measurements_A"]:
        df = pd.DataFrame(st.session_state["measurements_A"])
        st.dataframe(df)
    else:
        st.info("Es sind leider noch keine Messungen vorhanden!")
