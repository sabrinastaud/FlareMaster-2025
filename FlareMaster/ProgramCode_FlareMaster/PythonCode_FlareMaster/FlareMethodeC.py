#FlareMaster Programm - Methode A File

'''Hier befindet sich der Code für die Auswertung von Image Flare nach Methode C
Das Hauptprogramm heißt FlareAppMain.py'''

#Importieren von Bibliotheken
import streamlit as st #Web-App-Oberfläche
import cv2 #OpenCV
import numpy as np #NumPy (numerische Operationen & Array-Verarbeitung)
import matplotlib.pyplot as plt #Matplotlib


#Bildverarbeitung
def image_processing(image_bytes):

    #Inhalt der Bilddatei in einen Byte-Array
    #https://docs.streamlit.io/develop/api-reference/media/st.image
    file_bytes = np.asarray(bytearray(image_bytes.read()), dtype=np.uint8)
    #Byte-Daten in ein farbiges Bild decodieren
    img_color = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    #Error Meldung
    if img_color is None:
        st.error("Fehler beim Laden des Bildes! Bitte überprüfen Sie ihre Datei")
        return None

    #Konvertiere das Bild von BGR (OpenCV) in RGB
    img_rgb = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
    #Graustufen-Version für Canny Detektion
    gray_img = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    
    #Canny-Algorithmus: https://docs.opencv.org/4.x/da/d22/tutorial_py_canny.html
    #Schwellwerte: Was ist definitiv eine Kante und was ist nur im "Hintergrund"
    edges = cv2.Canny(gray_img, 50, 150)
    
    #5x5 Kernel aus Einsen für morphologische Operation
    #Kleine Lücken in den Kanten schließen
    kernel = np.ones((5, 5), np.uint8)
    morph = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    #cv2.RETR_EXTERNAL sucht nur äußersten Konturen
    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #Error Meldung
    if not contours:
        st.error("Leider kein dunkles Feld gefunden! Bitte überprüfen Sie ihre Datei")
        return None
    #Wähle größte Kontur basierend auf Fläche 
    biggest_cont = max(contours, key=cv2.contourArea)

    #Leere/schwarze Maske in der Größe des Graustufenbildes
    dark_mask = np.zeros_like(gray_img)
    #Zeichne größte Kontur in Maske und fülle sie aus (thickness=-1)
    cv2.drawContours(dark_mask, [biggest_cont], -1, 255, thickness=-1)
    
    #Berechne die Diagonale des Bildes (auch für adaptiven Erosionsradius (margin))
    img_h, img_w = gray_img.shape
    D = np.sqrt(img_w**2 + img_h**2)
    margin = max(int(D / 70), 1)
    #Erstelle Kernel für Erosion
    erosion_kernel = np.ones((2 * margin + 1, 2 * margin + 1), np.uint8)
    mask_eroded = cv2.erode(dark_mask, erosion_kernel, iterations=1)
    
    #Wandle erodierte Maske in booleschen Array (True = Pixel im dunklen Feld)
    eroded_dark_bool = mask_eroded.astype(bool)
    pixel_dark = img_rgb[eroded_dark_bool]
    #Berechne Durchschnittswert Pixel (pro Farbkanal) -> Falls keine Pixel vorhanden - setze auf [0, 0, 0]
    avg_dark = np.mean(pixel_dark, axis=0) if pixel_dark.size > 0 else [0, 0, 0]

    #Finde erneut Konturen - diesmal im erodierten dunklen Feld
    contours_eroded, _ = cv2.findContours(mask_eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours_eroded:
        #Wähle größte Kontur
        biggest_erod = max(contours_eroded, key=cv2.contourArea)
        #Ermittle Rechteck dieser Kontur
        x_dark, y_dark, w_dark, h_dark = cv2.boundingRect(biggest_erod)
        #Berechne Abstand 
        gap = int(2 * (D / 70))
        #Bestimme Position (jetzt weißes Feld)
        white_x = min(x_dark + w_dark + gap, img_rgb.shape[1] - w_dark)
        white_y = y_dark
        white_field = img_rgb[white_y:white_y+h_dark, white_x:white_x+w_dark].copy()
        #Berechne Durchschnittswert der Pixel
        avg_white = np.mean(white_field.reshape(-1, 3), axis=0) if white_field.size > 0 else [0, 0, 0]
    else:
        st.error("Leider kein erodiertes dunkles Feld gefunden! Bitte überprüfen Sie Ihre Datei")
        return None

    YLuma_d = 0.299 * avg_dark[0] + 0.587 * avg_dark[1] + 0.114 * avg_dark[2]
    YLuma_w = 0.299 * avg_white[0] + 0.587 * avg_white[1] + 0.114 * avg_white[2]
    #Kein durch 0 möglich
    flare = (YLuma_d / YLuma_w) * 100 if YLuma_w != 0 else 0

    output = img_color.copy()
    #Umriss dunkles Feld
    cv2.drawContours(output, [biggest_cont], -1, (0, 255, 0), 1)
    #Messfeld schwarz Umriss
    cv2.drawContours(output, contours_eroded, -1, (0, 0, 255), 1)
    #Messfeld weiß Umriss
    cv2.rectangle(output, (white_x, white_y), (white_x + w_dark, white_y + h_dark), (255, 0, 0), 2)
    #Konvertiere in RGB wegen OpenCV BGR
    output_rgb = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)

    #Plot der Verarbeitung
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes[0, 0].imshow(img_rgb)
    axes[0, 0].set_title("Hochegladenes Bild")
    axes[0, 0].axis("off")
    
    axes[0, 1].imshow(edges, cmap="gray")
    axes[0, 1].set_title("Erkannte Kanten")
    axes[0, 1].axis("off")
    
    axes[1, 0].imshow(morph, cmap="gray")
    axes[1, 0].set_title("Morph Operator (Schließen der Lücken)")
    axes[1, 0].axis("off")
    
    axes[1, 1].imshow(output_rgb)
    axes[1, 1].set_title("Erkannte Messfelder")
    axes[1, 1].axis("off")
    plt.tight_layout()

    #Dictionary
    return {
        "avg_dark": avg_dark,         
        "avg_white": avg_white,       
        "YLuma_d": YLuma_d,     
        "YLuma_w": YLuma_w,   
        "flare": flare,               
        "plot_fig": fig,              
        "output_rgb": output_rgb,     
    }


def run_method_c_auto():
    if "measurements_C" not in st.session_state:
        st.session_state["measurements_C"] = []

    st.header("Methode C: Automatische Bildmessung")
    st.write("Laden Sie hier ganz einfach ein zuvor aufgenommenes Kamerabild hoch! ")
    st.write("Nach dem Hochladen der gewünschten Aufnahme über den Button 'Browse Files' öffnet sich automatisch der Tab 'Ergebnisse'. "
    " In diesem Tab können weitere Informationen zur Messung angegeben werden. Um die Messung zu speichern, ist ein Klick auf den Button "
    "'Messung speichern' erforderlich.")
    st.write("Im Expander werden die Ergebnisse in Kurzform bereits angezeigt. Genaue Angaben befinden "
    "sich im Navigationsabschnitt 'Messverlauf'."
    " Neben dem Tab 'Ergebnisse' befindet sich auch die Möglichkeit 'Visualisierung' auszuwählen. "
    " Dies ermöglicht im Zweifelsfall eine Überprüfung der korrekten Bildverarbeitung und Positionierung der Messrahmen.")
    uploaded_file = st.file_uploader("Bild hochladen", type=["jpg", "jpeg", "png", "bmp", "tiff"], key="c1")
    
    if uploaded_file:
        results = image_processing(uploaded_file)
        if results is None:
            st.error("Fehler bei der Bildverarbeitung. Bitte überprüfen Sie Ihre Datei!")
            return
        
        tabs = st.tabs(["Ergebnisse", "Visualisierung"])
        with tabs[0]:
            #Eingabe User
            st.write("Speichern weiterer Informationen zur Messung. Sie werden ebenfalls später in der Messtabelle abgespeichert und angezeigt!")
            with st.form(key="c_measurement_info_form"):
                name = st.text_input("Name der Messung:")
                exposure_time = st.number_input("Exposure Time (s):", value=1.0, step=0.1)  
                gain = st.number_input("Gain:", value=1.0, step=0.1)  
                f_wert = st.number_input("f-Wert:", value=1.0, step=0.5)  
                other_info = st.text_area("Anmerkungen:")
                save_button = st.form_submit_button("Messung speichern")
            
            #Speichern (nur in der aktiven Session)
            if save_button:
                measurement = {
                    "Name": name,
                    "Belichtungszeit (s)": exposure_time,
                    "Gain": gain,
                    "f-Wert": f_wert,
                    "Flare": results["flare"],
                    "Dunkles RGB": results["avg_dark"],
                    "Dunkles YLuma": results["YLuma_d"],
                    "Weißes RGB": results["avg_white"],
                    "Weißes YLuma": results["YLuma_w"],
                    "Anmerkungen": other_info,
                    "Modus": "Automatisch"
                }
                st.session_state["measurements_C"].append(measurement)
                st.success("Messung wurde gespeichert!")
                st.success(f"Flare-Wert: {results['flare']:.2f} %")
            
            #Expander für Ergebnisse
            with st.expander("### Ergebnisse"):
                st.write("Eine detaillierte Beschreibung der Messergebnisse befindet sich im Navigationsabschnitt 'Messverlauf'")
                st.write(f"Name: {name}")
                st.write(f"Flare: {results['flare']:.2f} %")

        
        with tabs[1]:
            st.write("Hier wird die automatisch ausgeführte Bildverarbeitung dargestellt, "
            "wodurch eine Überprüfung der korrekten Positionierung der Messrahmen ermöglicht wird.")
            st.pyplot(results["plot_fig"])
            st.image(results["output_rgb"], caption="Messbild", use_container_width=True)
    
    else:
        st.info("Bitte laden Sie ein Bild hoch!")

#Methode C Manuell
def run_method_c_manual():
    if "measurements_C" not in st.session_state:
        st.session_state["measurements_C"] = []

    st.header("Methode C: Manuelle Bildmessung")
    st.write("Achten Sie unbedingt darauf, dass Sie sich an die Messanforderungen der ISO 18844 halten und die beiden Messfelder richtig auswählen! "
    "Um die Auswertung vollständig auszuführen, klicken Sie sich durch alle drei Tabs und füllen Sie die angeforderten Felder aus. "
    "Im letzten Tab können Sie die Auswertung speichern und ausführen.")

    # Create tabs for "Helles Messfeld", "Dunkles Messfeld", and "Parameter"
    tabs = st.tabs(["Helles Messfeld", "Dunkles Messfeld", "Weitere Parameter & Speichern"])

    with tabs[0]:
        st.write("Geben Sie zum Start bitte den Namen der Messung an!")
        name = st.text_input("Name der Messung:")
        st.write("Hier werden die RGB-Werte für das **helle Messfeld** eingegeben. "
        "Die Werte für das helle (weiße) Messfeld sollten bei etwa 225 +/- 8 liegen!")
        # RGB Eingabe für helles Feld
        white_r = st.number_input("Weißes Messfeld - R:", value=0.0, min_value=0.0, max_value=255.0)
        white_g = st.number_input("Weißes Messfeld - G:", value=0.0, min_value=0.0, max_value=255.0)
        white_b = st.number_input("Weißes Messfeld - B:", value=0.0, min_value=0.0, max_value=255.0)

    with tabs[1]:
        st.write("Hier werden die RGB-Werte für das **dunkle Messfeld** eingegeben:")
        # RGB Eingabe für dunkles Feld
        dark_r = st.number_input("Dunkles Messfeld - R:", value=0.0, min_value=0.0, max_value=255.0)
        dark_g = st.number_input("Dunkles Messfeld - G:", value=0.0, min_value=0.0, max_value=255.0)
        dark_b = st.number_input("Dunkles Messfeld - B:", value=0.0, min_value=0.0, max_value=255.0)

    with tabs[2]:
        st.write("Geben Sie zum Schluss noch die ausgewählten **Messparameter** an:")
        # Eingabe zusätzliche Parameter
        exposure_time = st.number_input("Exposure Time (s):", value=1.0, step=0.1)
        gain = st.number_input("Gain:", value=1.0, step=0.1)
        f_wert = st.number_input("f-Wert:", value=1.0, step=0.1)

        # Eingabe Messungsinformationen
        other_info = st.text_area("Anmerkungen:")

        # Button zum Speichern und Berechnen
        save_button = st.button("Messung berechnen und speichern")

        if save_button:
            # Berechnungen durchführen
            avg_dark = [dark_r, dark_g, dark_b]
            avg_white = [white_r, white_g, white_b]
            YLuma_d = 0.299 * avg_dark[0] + 0.587 * avg_dark[1] + 0.114 * avg_dark[2]
            YLuma_w = 0.299 * avg_white[0] + 0.587 * avg_white[1] + 0.114 * avg_white[2]

            if YLuma_w == 0:
                st.error("Fehler: YLuma des weißen Messfeldes darf nicht 0 sein! Bitte geben Sie Werte ein die bei etwa 225 +/- 8 liegen!")
                return

            flare = (YLuma_d / YLuma_w) * 100

            # Messung speichern
            measurement = {
                "Name": name,
                "Belichtungszeit (s)": exposure_time,
                "Gain": gain,
                "f-Wert": f_wert,
                "Dunkles RGB": avg_dark,
                "Dunkles YLuma": YLuma_d,
                "Weißes RGB": avg_white,
                "Weißes YLuma": YLuma_w,
                "Flare": flare,
                "Anmerkungen": other_info,
                "Modus": "Manuell"
            }

            st.session_state["measurements_C"].append(measurement)
            st.success("Messung gespeichert!")
            st.success(f"Flare: {flare:.2f} %")

            # Ergebnisse anzeigen
            with st.expander("### Ergebnisse"):
                st.write("Eine detaillierte Beschreibung der Messergebnisse befindet sich im Navigationsabschnitt 'Messverlauf'")
                st.write(f'Name: {name}')
                st.write(f"Flare: {flare:.2f} %")



#Start Hauptprogramm
if __name__ == "__main__":
    run_method_c_auto()
