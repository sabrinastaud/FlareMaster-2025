# FlareMaster-2025
FlareMaster ist ein interaktives Webtool zur Messung und Analyse von Bildstreulicht (Image Flare) optischer Kamerasysteme. 
Die Applikation basiert auf Python und Streamlit und implementiert normbasierte Methoden aus der ISO 18844 für eine einfache Auswertung und Analyse.
FlareMaster wurde für die Bachelorarbeit "Bewertung des Einflusses von Streulichtartefakten auf die Bildqualität im RoboticScope" entwickelt. 
Das Programm ist dadurch speziell auf das während der Arbeit konstruierte Messsetup abgestimmt.

**Version:** 1.0  
**Autor:** Sabrina Staud

**Technologie-Stack:** Python, Streamlit, Pandas

---

## Projektübersicht

FlareMaster ist eine Streamlit-Webanwendung zur Analyse von optischen Streulichtmessungen nach **ISO 18844**. Die Anwendung bietet zwei Hauptmethoden zur Auswertung von Messdaten (Methode A und Methode C) und erlaubt die visuelle Darstellung sowie tabellarische Auswertung der Ergebnisse.

### Features

- 🔬 Messmethoden nach ISO 18844: Methode A und Methode C (manuell & automatisch)
- 📈 Visuelle Datenanalyse mittels interaktiver Diagramme
- 📊 Tabellenbasierte Eingabe und Auswertung von Messwerten
- 🧭 Klar strukturierte Benutzeroberfläche mit Menüführung zur intuitiven Verwendung 
- 🛠 Einfacher Start über `.bat`-Datei

---

## Startanleitung
Damit die Anwendung auf dem Rechner ausgeführt werden kann, ist es zuerst notwendig, den gesamten "FlareMaster"-Ordner herunterzuladen. Im Ordner befindet sich schlussendlich eine weitere Textdatei mit der Bezeichnung "README_AnleitungZumStart.txt". Darin erfolgt eine detaillierte Erläuterung der Schritte wie die Applikation gestartet werden kann.

### Ordnerstruktur
FlareMaster/
├── README_AnleitungZumStart.txt
├── ProgramCode_FlareMaster/
│   ├── BatchStart_FlareMaster.bat
│   └── PythonCode_FlareMaster/
│       ├── FlareAppMain.py         #Startseite
│       ├── FlareMethodeA.py        #Methode A
│       ├── FlareMethodeC.py        #Methode C 
│       ├── MeasurementChart.py     #Messverlauf
│       └── __pycache__/
└── FlareMaster.lnk                 #FlareMaster Applikation (Verknüpfung der Batch-Datei "BatchStart_FlareMaster.bat"

## Datenquellen
- ISO-Norm 18844 für Flare-Messungen
- Vorlesung "Programmierübung 2 – SS 2023" am Management Center Innsbruck 
- Komponenten von Streamlit.io

