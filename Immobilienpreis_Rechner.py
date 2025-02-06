
import pandas as pd

def berechne_immobilienpreis(df):
    # Annahme: Basispreis pro m² Wohnfläche (abhängig von der Stadt/Land Lage)
    basispreis_stadt = 3000  # €/m²
    basispreis_land = 2000   # €/m²
    
    preise = []
    
    for _, row in df.iterrows():
        wohnflaeche = row['Wohnfläche (m²)']
        grundstueck = row['Grundstück (m²)']
        architektenhaus = row['Architektenhaus']
        makler = row['Makler']
        denkmalschutz = row['Denkmalschutz']
        baujahr = row['Baujahr']
        lage = row['Lage']
        ausstattung = row['Ausstattung']
        hausart = row['Hausart']
        bundesland = row['Bundesland']
        
        # Basispreis bestimmen
        basispreis = basispreis_stadt if lage == "Stadt" else basispreis_land
        
        # Altersabschlag
        altersabschlag = max(0, (2025 - baujahr) * 0.5)
        
        # Zuschläge und Abschläge
        zuschlag_architekt = 1.2 if architektenhaus else 1.0
        abschlag_makler = 0.95 if makler else 1.0
        zuschlag_denkmalschutz = 1.1 if denkmalschutz else 1.0
        
        # Ausstattungsfaktor (1 = einfach, 1.2 = gehoben, 1.5 = luxuriös)
        ausstattungsfaktor = 1.0 if ausstattung == "einfach" else 1.2 if ausstattung == "gehoben" else 1.5
        
        # Berechnung des Preises
        preis = wohnflaeche * basispreis
        preis *= zuschlag_architekt * abschlag_makler * zuschlag_denkmalschutz * ausstattungsfaktor
        preis -= altersabschlag * 1000  # Abschlag basierend auf Alter
        
        # Grundstückswert (pauschal 300 €/m²)
        preis += grundstueck * 300
        
        preise.append(preis)
    
    df['Geschätzter Preis (€)'] = preise
    return df

# Beispiel-Daten laden
daten = {
    'Wohnfläche (m²)': [120, 150],
    'Grundstück (m²)': [500, 800],
    'Architektenhaus': [True, False],
    'Makler': [False, True],
    'Denkmalschutz': [False, True],
    'Baujahr': [2000, 1950],
    'Lage': ["Stadt", "Land"],
    'Ausstattung': ["gehoben", "einfach"],
    'Hausart': ["Einfamilienhaus", "Villa"],
    'Bundesland': ["Bayern", "NRW"]
}

df = pd.DataFrame(daten)
df = berechne_immobilienpreis(df)

# Anzeige der berechneten Werte
import ace_tools as tools

tools.display_dataframe_to_user(name="Immobilienpreis Berechnung", dataframe=df)