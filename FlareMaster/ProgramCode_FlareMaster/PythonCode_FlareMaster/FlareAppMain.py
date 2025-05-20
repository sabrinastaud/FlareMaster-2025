#FlareMaster Programm - Main File 

'''
Hier befindet sich das Main File der FlareMaster Oberfläche.
Um die Oberfläche im Terminal zu Öffnen einfach "python -m streamlit run FlareAppMain.py" eingeben

Informationen wurde hauptsächlich aus https://streamlit.io/components und der Vorlesung SS 2023 Programmierübung 2. 
Bei Auschnitten in denen andere Quellen verwendet wurden, ist dies im Code vermerkt!
Berechnungen und andere Mess- und Auswertungsangaben wurden aus der ISO 18844 entommen.
'''

#Zu importierende Bibliotheken
import streamlit as st #Erstellung der Webanwendung
import pandas as pd  

from streamlit_option_menu import option_menu #Menü für Navigation
from FlareMethodeA import run_method_a  #Methode A 
from FlareMethodeC import run_method_c_auto, run_method_c_manual  #Methode C 
from MeasurementChart import measurement_table  #Darstellung von Messdaten

#Main Menü
def main():
    #Streamlit Seite konfigurieren
    st.set_page_config(page_title="FlareMaster 2025 ", layout="wide")

    #CSS, um das Design der Tabs zu ändern: Tabs dunkel und Text weiß
    #Die Akzentfarbe wird aus der Konfiguration (config.toml) übernommen
    st.markdown(
        """
        <style>
        /* Hintergrundfarbe & Textfarbe der Tabs */
        div[role="tablist"] button {
            background-color: #0f1117 !important;
            color: white !important;
            border: none !important;
            outline: none !important;
        }
        div[role="tablist"] button[aria-selected="true"] {
            border-bottom: 3px solid var(--primary-color) !important; /* = #4CAF50 aus config.toml */
        }
        /* Radio-Buttons: Label in weißer Schrift */
        .stRadio label {
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    #Session-State Variablen: Speichert zwischen den Seitenzuständen
    if "method_A" not in st.session_state:
        st.session_state["method_A"] = []  #Falls keine Daten da sind
    if "method_C" not in st.session_state:
        st.session_state["method_C"] = [] 

    #Seitenleisten Navigation: Fügt eine Navigation auf der linken Seite hinzu
    with st.sidebar:
        selected = option_menu(
            "Navigation",  
            ["Auswertung", "Messverlauf", "Hilfe"],  
            icons=["clipboard-data", "clock-history", "question-circle"], 
            menu_icon="none",  
            default_index=0,  
            styles={ 
                "container": {"padding": "5!important", "background-color": "#262730"},
                "nav-title": {"color": "black", "background-color": "#1b2631"},
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "margin": "0px",
                    "color": "black",
                    "--hover-color": "#eee",
                    "background-color": "white",
                    "opacity": "0.8"
                },
                "nav-link-selected": {  
                    "background-color": "#B0C4DE",
                    "font-size": "14px",
                    "font-weight": "bold",
                    "color": "black"
                },
                "icon": {"font-size": "16px", "color": "black"}
            }
        )

    #Menüpunkt "Auswertung"
    if selected == "Auswertung":
        st.header("Image Flare Auswertung durchführen")
        st.write("Mit FlareMaster können aufgenommene Kamerabilder gemäß ISO 18844 ausgewertet werden."
        " Bitte beachten Sie, dass Sie beim Aufnehmen der Bilder die Anforderungen der ISO 18844 einhalten! ")
        st.write("Zu Beginn ist die gewünschte Methode auszuwählen. "
        "Beachten Sie, dass die Methode C mit dem für die Messung konstruierten Messaufbau als primäre Methode anzuwenden ist.")
        
        #Tabs für Methode C und Methode A
        method_decision = st.tabs(["Methode C", "Methode A"])
        
        #Methode C - Automatisch oder Manuell
        with method_decision[0]:
            st.subheader("Auswertung nach ISO 18844 Methode C")
            st.warning("Stellen Sie sicher, dass Sie einen Kontrast von mindestens 3000:1 mit Ihrem Testchart erreichen (wie es bei dem während der Bachelorarbeit 2025 erstellten Aufbau gegeben ist). "
            "Andernfalls können Ergebnisse verfälscht werden.")
            st.write("Bitte wählen Sie zunächst aus, ob Sie bereits eine Aufnahme gespeichert haben und hochladen möchten (Automatischer Modus) oder ob Sie die aufgenommenen Parameter manuell eingeben möchten (Manueller Modus).")
            
            mode_c = st.radio("Bitte Modus auswählen:", ["Automatisch", "Manuell"], horizontal=True, key="mode_c")
            
            if mode_c == "Automatisch":
                run_method_c_auto()
            else:
                run_method_c_manual()

        #Methode A - Manuell
        with method_decision[1]:
            st.subheader("Auswertung nach Methode A")
            st.warning("Bitte stellen Sie sicher, dass Sie einen Kontrast von mindestens 40:1 mit Ihrem Testchart erreichen. "
            "Andernfalls können Ergebnisse verfälscht werden. Sollten Sie sich nicht sicher sein, wie Sie die Bildaufnahme machen müssen "
            "und wie die Werte ausgelesen werden, schauen Sie vorher in die ISO 18844!")
            run_method_a()
    
    #Menüpunkt "Messverlauf"
    elif selected == "Messverlauf":
        st.header("Messverlauf")
        st.write("In diesem Abschnitt erfolgt die Darstellung der vorher gespeicherten Ergebnisse in Tabellenform oder die Visualisierung in Form von Grafiken. "
        "Die Tabellen und Grafiken können am Ende ganz einfach heruntergeladen werden.")
        measurement_table()  
    
    #Menüpunkt "Hilfe"
    elif selected == "Hilfe":
        st.title("Anleitung & FAQ")
    
        st.subheader("Einführung")
        st.write("Diese Benutzeroberfläche dient zur Berechnung von **Image Flare** in aufgenommenen Bildern "
        "Die Berechnungen basieren auf Messwerten, die gemäß **ISO 18844** aufgenommen wurden.")
        
        st.subheader("Bildaufnahme nach ISO 18844")
        st.write("Bitte beachten Sie, dass die Bilder nach den Anforderungen der ISO 18844 aufgenommen werden müssen! Nur dann liefter FlareMaster auch richtige Ergebnisse."
        "Verwenden Sie außerdem den für diese Messung konstruierten Messaufbau der im Rahmen der Bachelorarbeit 'Bewertung des Einflusses von Streulichtartefakten auf die Bildqualität im RoboticScope'"
        "angefertigt wurde. Beachten Sie außerdem, dass Methode C als primäre Methode verwendet werden sollte!")
        
        st.subheader("Nutzung der Software")
        st.subheader("Auswahl der Methode und Ausführung der Auswertung")
        st.write("Um eine Auswertung zu starten klicken Sie bitte zuerst links in der Navigation auf den Reiter 'Auswertung'. Hier können Sie sich dann für eine der beiden Methoden (A oder C) entscheiden."
        "Verwenden Sie das für die Auswertung konstruierte Messsetup, dann nutzen Sie bitte Methode C als Auswertungsmethode! Sollten Sie nicht das dafür konzipierte Setup verwenden so beachten Sie bitte die Anforderungen aus der ISO 18844")
        
        st.write("**Methode C**")
        st.write("Sobald Sie sich für die Methode C entschieden haben befinden Sie sich in der Oberfläche für die automatische Auswertung. Hier können Sie"
        "ganz einfach ein Bild dass sie vorher aufgenommen haben einlesen. Klicken Sie dazu einfach auf den 'Browse File' Button. Dann öffnet sich ein Ordner Ihres Rechners und Sie können das gespeicherte Bild auswählen."
        "Das Programm erkennt dann mittels Bildverarbeitung die beiden Felder und zeichnet die passenden Messrahmen in denen dann die RGB Werte gemessen werden."
        "Im nächsten Schritt können Sie weitere Infos wie den Namen der Messung, Gain, f-Wert und Belichtungszeiten eingeben damit diese Informationen später auch in der Messtabelle gespeichert werden können."
        "Um die Auswertung dann zu speichern klicken Sie einfach unten auf den Button 'Messung speichern'. Die Ergebnisse befinden sich nun im Reiter ''Messverlauf'' oder aber auch (in Kurzform) im Expander unter dem 'Messung speichern' Button. Klicken Sie diesen ganz einfach an uns sehen Sie schnell die Ergebnisse der Messung ein.")
        
        st.write("Wenn Sie keine Aufnahme einlesen wollen, klicken Sie auf den Tab Manuell. "
        " Hier geben Sie einfach die RGB-Werte und sonstigen Parameter per Hand ein. "
        " Klicken Sie sich durch die drei Tabs und füllen Sie alle geforderten Felder aus. Im letzten Tab speichern Sie die Messung. "
        " Auch hier werden alle Mesungen im Reiter 'Mesverlauf' oder im Expander 'Ergebnisse' gespeichert.")
        
        st.write("**Methode A**")
        st.write("Wenn Sie nicht das vorgeschriebene Setup verwenden und es deshalb laut ISO 18844 Methode A anwenden müssen, "
        "wählen Sie einfach den Tab Methode A. Hier müssen Sie lediglich alle Werte manuell eingeben. Das Programm berechnet dann den daraus "
        "resultierenden Flare-Wert."
        " Achten Sie hier besonders auf die Anforderungen der ISO! Außerdem benötigen Sie ein weiteres Messchart (Chart 2)."
        "Im Anschluss können Sie auch hier in den drei Tabs die angeforderten Werte eingeben und anschließend speichern. "
        "Die Messergebnisse finden Sie entweder (in Kurzform) im 'Expander' darunter oder im Naviagtionsreiter 'Messverlauf' ausführlich angeführt.")
        
        st.subheader("Messverlauf")
        st.write("In diesem Reiter finden Sie alle Messungen, die in dieser Session gespeichert wurden. "
        "Vergleichen Sie hier beide Methoden in Tabellen und Grafiken. Mit einem Klick auf den Download-Button in der rechten oberen "
        "Ecke der Tabelle oder Grafik laden Sie diese einfach herunter. Wählen Sie dazu im ersten Schritt das gewünschte Dateiformat aus. Bei den Grafiken können Sie auch zwischen den Typen Balkendiagramm und Punktdiagramm (mit der Möglichkeit die Punkte zu verbinden) wählen.")

        st.header("FAQ – Häufig gestellte Fragen")
        
        with st.expander("Warum bekomme ich die Fehlermeldung 'Division durch Null ist nicht möglich! Überprüfen Sie bitte Ihre Eingabewerte.' oder 'Fehler: YLuma des weißen Messfeldes darf nicht 0 sein!'?"):
            st.write("Die Berechnung von Image Flare basiert unter anderem auf einer Division der Flächen. Sobald die Eingabe bedeuten würde, dass der Nenner 0 ist (was bdeuten würde, dass die **helle* Fläche komplett schwarz ist) wird Ihnen eine Fehlermeldung angezeigt."
            "Überprüfen Sie, ob die hellen RGB-Werte, Belichtungszeit oder f-Wert **keine Nullwerte** haben.")
        
        with st.expander("Kann ich die gespeicherten Messwerte exportieren?"):
            st.write("Ja! Die gespeicherten Messungen können als **CSV-Datei** (Tabelle) oder **PNG/SVG-Datei** (Diagrammgrafik) exportiert werden.")
        
        
        with st.expander("Welche Kameraeinstellungen sollte ich verwenden?"):
            st.write("Vor allem: Fester Gain, kein Auto-Exposure, kein Auto-Whitebalance. Um sicher zu gehen, dass die Aufnahmen korrekt sind sollten Sie jedoch die ISo 18844 genau durchlesen!")
        
        with st.expander("Bleiben meine Daten erhalten, wenn ich den Tab verlasse aber offen lasse?"):
            st.write("Ja, die Messwerte bleiben in der Sitzung gespeichert, gehen aber nach einem Neustart (oder bei zu langer Nictaktivität) verloren.")

        st.write("Sollten Sie Probleme oder weitere Fragen haben wenden Sie sich bitte an den zuständigen Entwickler (siehe Verfasser der Bachelorarbeit 2025)")
        st.write("Ihr FlareMaster 2025")

# Wenn das Skript direkt ausgeführt wird, wird die main-Funktion aufgerufen
if __name__ == "__main__":
    main()
