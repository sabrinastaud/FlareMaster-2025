#FlareMaster Programm - Tabelle und visuelle Darstellung

'''Hier werden Messungen die in der aktiven Session gespeichert wurden in einer Tabelle gespeichert. 
Zudem kann man sich die Ergebnisse auch grafisch darstellen lassen um sie besser miteinander vergleichen zu können.'''

#Zu importierende Bibliotheken
import streamlit as st #Erstellung der Web-App
import pandas as pd #Erstellung/Bearbeitung von DataFrames
import altair as alt #Erzeugung interaktiver Diagramme

def measurement_table():
    #Warnung
    st.warning(
        "Achtung: Messungen werden nur in der aktiven Session gespeichert! "
        "Sobald Sie die Oberfläche neu laden oder einige Zeit vergeht, werden die Messungen gelöscht. "
        "Stellen Sie sicher, dass Sie nach einer Messreihe die .csv Datei herunterladen, um sie final zu speichern."
    )
    
    #Initialisiere zwei Listen 
    all_data_A = []  #Methode A
    all_data_C = []  #Methode C
    
    #Methode A
    if "measurements_A" in st.session_state:
        #Iteriere über alle gespeicherten Messungen
        for m in st.session_state["measurements_A"]:
            #Erstelle Dictionary mit relevanten Messdaten (Werte formatiert)
            measurement = {
                "Name": m.get("Name", ""),  
                "Flare": round(m.get("Flare", 0), 1),  
                "Methode": "A",  
                "Belichtungszeit (s)": round(m.get("Belichtungszeit (s)", 0), 1), 
                "f-Wert": round(m.get("f-Wert", 0), 1),  
                "Gain": round(m.get("Gain", 0), 1),  
                "Anmerkungen": m.get("Anmerkungen", ""),  
                "Aufnahme 1": ', '.join(map(str, [round(x, 1) for x in m.get("Aufnahme 1", [0, 0, 0])])),
                "Aufnahme 2": ', '.join(map(str, [round(x, 1) for x in m.get("Aufnahme 2", [0, 0, 0])])),
                "Aufnahme 3": ', '.join(map(str, [round(x, 1) for x in m.get("Aufnahme 3", [0, 0, 0])])),

                
            }
            all_data_A.append(measurement)
    
    #Methode C
    if "measurements_C" in st.session_state:
        #Iteriere über alle Messungen
        for m in st.session_state["measurements_C"]:
            measurement = {
                "Name": m.get("Name", ""),
                "Flare": round(m.get("Flare", 0), 1),
                "Methode": "C",  
                #Modus ob Automatisch oder Manuell
                "Modus": "Manuell" if m.get("Modus") == "Manuell" else "Automatisch",
                #Parameter die Optional sind (sonst 0)
                "Belichtungszeit (s)": round(m.get("Belichtungszeit (s)", 0), 1),
                "f-Wert": round(m.get("f-Wert", 0), 1),
                "Gain": round(m.get("Gain", 0), 1),
                "Anmerkungen": m.get("Anmerkungen", ""),
                "RGB-Werte (dunkel)": ', '.join(map(str, [round(x, 1) for x in m.get("Dunkles RGB", [0, 0, 0])])),
                "RGB-Werte (hell)": ', '.join(map(str, [round(x, 1) for x in m.get("Weißes RGB", [0, 0, 0])]))
            }
            all_data_C.append(measurement)
    
    #Liegen Messungen vor?
    if not all_data_A and not all_data_C:
        st.info("Es sind leider noch keine Messungen vorhanden!")
        return

    #Erstelle DataFrame
    df_A = pd.DataFrame(all_data_A) if all_data_A else pd.DataFrame()
    df_C = pd.DataFrame(all_data_C) if all_data_C else pd.DataFrame()
    #Verbinde beide DataFrames
    df = pd.concat([df_A, df_C], ignore_index=True)

    tabs = st.tabs(["Methode C - Tabelle & Visualisierung", "Methode A - Tabelle & Visualisierung"])
    
    with tabs[0]:  # Methode C
        st.markdown("### Übersicht der Messungen nach Methode C")
        if not df_C.empty:
            st.write(
                df_C.style.format({
                    "Flare": "{:.1f}",
                    "Belichtungszeit (s)": "{:.1f}",
                    "f-Wert": "{:.1f}",
                    "Gain": "{:.1f}",
                }).set_table_styles([
                    {"selector": "th", "props": "font-size:16px; font-weight:bold; text-align:center;"},
                    {"selector": "td", "props": "font-size:14px; text-align:center;"}
                ])
            )
        
        if not df_C.empty:
            measurement_options_C = df_C["Name"].unique().tolist()
            selected_measurements_C = st.multiselect(
                "Wählen Sie die gewünschten Messungen für Methode C aus:",
                options=measurement_options_C,
                default=measurement_options_C  # Standardmäßig alle ausgewählt
            )

            filtered_df_C = df[df["Name"].isin(selected_measurements_C) & (df["Methode"] == "C")]
            
            # Diagrammtyp für Methode C auswählen
            chart_type_C = st.radio("Wählen Sie einen Diagrammtyp für Methode C:", options=["Punkt/Linien", "Balken"], index=0)

            # Diagramm erstellen für Methode C
            if chart_type_C == "Balken":
                chart_C = alt.Chart(filtered_df_C).mark_bar().encode(
                    x=alt.X("Name:N", sort=list(filtered_df_C["Name"]), title="Messung"),
                    y=alt.Y("Flare:Q", title="Flare-Wert"),
                    color="Methode:N",
                    tooltip=["Name", "Flare", "Methode", "Belichtungszeit (s)", "f-Wert", "Gain", "Anmerkungen", "RGB-Werte (dunkel)", "RGB-Werte (hell)"]
                ).properties(
                    title="Flare-Werte von Methode C (Balkendiagramm)",
                    width=600
                )
            else:
                connect_points_C = st.checkbox("Punkte verbinden (Liniendiagramm)", value=False)
                if connect_points_C:
                    chart_C = alt.Chart(filtered_df_C).mark_line(point=True).encode(
                        x=alt.X("Name:N", sort=list(filtered_df_C["Name"]), title="Messung"),
                        y=alt.Y("Flare:Q", title="Flare-Wert"),
                        color="Methode:N",
                        tooltip=["Name", "Flare", "Methode", "RGB-Werte (dunkel)", "RGB-Werte (hell)", "Belichtungszeit (s)", "f-Wert", "Gain", "Anmerkungen"]
                    ).properties(
                        title="Flare-Werte von Methode C (Liniendiagramm)",
                        width=600
                    )
                else:
                    chart_C = alt.Chart(filtered_df_C).mark_point().encode(
                        x=alt.X("Name:N", sort=list(filtered_df_C["Name"]), title="Messung"),
                        y=alt.Y("Flare:Q", title="Flare-Wert"),
                        color="Methode:N",
                        tooltip=["Name", "Flare", "Methode", "RGB-Werte (dunkel)", "RGB-Werte (hell)", "Belichtungszeit (s)", "f-Wert", "Gain", "Anmerkungen"]
                    ).properties(
                        title="Flare-Werte von Methode C (Punktdiagramm)",
                        width=600
                    )
            st.altair_chart(chart_C, use_container_width=True)

    with tabs[1]:  # Methode A
        st.markdown("### Übersicht der Messungen nach Methode A")
        if not df_A.empty:
            st.write(
                df_A.style.format({
                    "Flare": "{:.1f}",
                    "Belichtungszeit (s)": "{:.1f}",
                    "YLuma 1": "{:.1f}",
                    "YLuma 2": "{:.1f}",
                    "H1": "{:.1f}",
                    "H2": "{:.1f}",
                    "f-Wert": "{:.1f}",
                    "Gain": "{:.1f}",
                    "aufnahme1": "{:.1f}",
                    "aufnahme2": "{:.1f}",
                    "aufnahme3": "{:.1f}"
                }).set_table_styles([
                    {"selector": "th", "props": "font-size:16px; font-weight:bold; text-align:center;"},
                    {"selector": "td", "props": "font-size:14px; text-align:center;"}
                ])
            )
        
        if not df_A.empty:
            measurement_options_A = df_A["Name"].unique().tolist()
            selected_measurements_A = st.multiselect(
                "Wählen Sie die gewünschten Messungen für Methode A aus:",
                options=measurement_options_A,
                default=measurement_options_A  # Standardmäßig alle ausgewählt
            )

            filtered_df_A = df[df["Name"].isin(selected_measurements_A) & (df["Methode"] == "A")]
            
            # Diagrammtyp für Methode A auswählen
            chart_type_A = st.radio("Wählen Sie einen Diagrammtyp für Methode A:", options=["Punkt/Linien", "Balken"], index=0)

            # Diagramm erstellen für Methode A
            if chart_type_A == "Balken":
                chart_A = alt.Chart(filtered_df_A).mark_bar().encode(
                    x=alt.X("Name:N", sort=list(filtered_df_A["Name"]), title="Messung"),
                    y=alt.Y("Flare:Q", title="Flare-Wert"),
                    color="Methode:N",
                    tooltip=["Name", "Flare", "Methode", "Aufnahme 1", "Aufnahme 2", "Belichtungszeit (s)", "f-Wert", "Gain", "Anmerkungen"]
                ).properties(
                    title="Flare-Werte von Methode A (Balkendiagramm)",
                    width=600
                )
            else:
                connect_points_A = st.checkbox("Punkte verbinden", value=False)
                if connect_points_A:
                    chart_A = alt.Chart(filtered_df_A).mark_line(point=True).encode(
                        x=alt.X("Name:N", sort=list(filtered_df_A["Name"]), title="Messung"),
                        y=alt.Y("Flare:Q", title="Flare-Wert"),
                        color="Methode:N",
                        tooltip=["Name", "Flare", "Methode", "Aufnahme 1", "Aufnahme 2", "Belichtungszeit (s)", "f-Wert", "Gain", "Anmerkungen"]
                    ).properties(
                        title="Flare-Werte von Methode A (Liniendiagramm)",
                        width=600
                    )
                else:
                    chart_A = alt.Chart(filtered_df_A).mark_point().encode(
                        x=alt.X("Name:N", sort=list(filtered_df_A["Name"]), title="Messung"),
                        y=alt.Y("Flare:Q", title="Flare-Wert"),
                        color="Methode:N",
                        tooltip=["Name", "Flare", "Methode", "Aufnahme 1", "Aufnahme 2", "Belichtungszeit (s)", "f-Wert", "Gain", "Anmerkungen"]
                    ).properties(
                        title="Flare-Werte von Methode A (Punktdiagramm)",
                        width=600
                    )
            st.altair_chart(chart_A, use_container_width=True)
