#! Gehaltsrechner
#Python 3.13.0 |IDE MS-VS-Code Portable version| 
#True PATH : E:\MS-VS-Code-64bit_zip Portable version\data\Vs-Code scrpite

"""Unsere importierung anderer Module"""
from time import *
from math import *
import pprint
import sys
from datetime import datetime
"""Globale Variablen"""     

Ehe_P_AN = False
T="-|-"

#   Dictionary als Anzeige-Objekt und Speicher-Objekt 

Gehalt_dict= {
    "Bruttolohn-Auswertung | ": ["Brutto-Jahr","Brutto-Monat","Brutto-Tag","Brutto-Stunde","Netto_Jahr","Netto-Monat","Netto-Tag","Netto-Stunde","Einkommensteuer","Sozialabgaben","Grundfreibetrag","Steuerklasse"],
    "Steuerklasse          | ": ["    Sie gilt für Singles ledige, getrennt lebende oder geschiedene Arbeitnehmerinnen und Arbeitnehmer.",
                                 "    Etwas weniger Steuern werden hier fällig und zwar für Alleinerziehende, die Anspruch auf den Entlastungsbetrag (4.008 €, für jedes weitere Kind erhöht sich der Betrag um jeweils 240 € pro Jahr) haben.\n",
                                 "    Für den deutlich besser verdienenden Ehepartner. Der andere Teil des Paars erhält automatisch die Klasse V.",
                                 "    Macht ein Ehepaar nichts, landen beide Eheleute in Steuerklasse IV, die die gleichen Abzüge hat wie Klasse I. Auch zu empfehlen, wenn beide ein ähnliches Einkommen haben.\n",
                                 "    Mit Faktor: Ebenfalls für Ehepaare. Hier wird die monatliche Steuerlast nur etwas „gerechter“ aufgeteilt als in der 3/4-Kombination.\n",
                                 "    Sie stellt das Gegenstück zur Klasse III dar. Kommt beim deutlich schlechter verdienenden Ehepartner zur Anwendung.\n",
                                 "    Die braucht ein Arbeitnehmer, wenn er einen zweiten steuerpflichtigen Job annimmt."],
    "Sozialabgaben         | " :["Rentenversicherung       = 9,3%","Krankenversicherung      = 7,3%","Pflegeversicherung       = 15,25%","Arbeitslosenversicherung = 1,2%"],
    "Einkommen-Ehepartners | " :["Brutto-Jahr","Brutto-Monat","Brutto-Tag","Brutto-Stunde","Netto_Jahr","Netto-Monat","Netto-Tag","Netto-Stunde","Einkommensteuer","Sozialabgaben","Grundfreibetrag","Steuerklasse"],                        
      }

#   Funktionen dieses Moduls

def ändern_indexListe(dict, key, index, Wert):
    if key in dict and index < len(dict[key]):
        dict[key][index] = Wert

""" 
    Ablauf:
    Funktion um Schlüssel(keys)-Wertpaare(values) eines dictionaries Anhand der bereits Vorhandenen Indexe zu sortieren/einzufügen/verändern
    dict_Name = {
        "Schlüssel1":["Wertpaar1","Wertpaar2",],
        "Schlüssel2":["Wertpaar1","Wertpaar2",],
        }  
#   Beispiel-Aufruf der Funktion:
    ändern_indexListe(dict_Name, "Schlüssel1",0,"Neuer Wert")
    
    dict_Name = {
        "Schlüssel1":["Neuer Wert","Wertpaar2",],
        "Schlüssel2":["Wertpaar1","Wertpaar2",],
    }

    Erklärung:
    Anhand des indexes des Schlüssels sowie der Wertpaare(innerhalb der dazugehörigen Liste) des dicts zu ändern,
    ändert also den bestehenden Wert des gewählten indexes,
    wichtig der Index muss bereits vorhanden sein und die dictionary aufteilung muss "Schlüssel":[Wertpaar]sein.!!   

"""
    
    #!   Funktionen

#   Sozialabgaben
def berechne_sozialabgaben(bruttolohn):
    rentenversicherung = bruttolohn * 0.093                                 # Arbeitnehmeranteil
    krankenversicherung = bruttolohn * 0.073                                # Arbeitnehmeranteil (ohne Zusatzbeitrag)
    pflegeversicherung = bruttolohn * 0.01525                               # Arbeitnehmeranteil ohne Kind
    arbeitslosenversicherung = bruttolohn * 0.012                           # Arbeitnehmeranteil
    sozialabgaben = rentenversicherung + krankenversicherung + pflegeversicherung + arbeitslosenversicherung
    
    return sozialabgaben
#   Einkommensteuer
def berechne_einkommensteuer(zve):
    if zve <= 11604:
        return 0
    elif 11605 <= zve <= 17005:
        y = (zve - 11604) / 10000
        est = (922.98 * y + 1400) * y
    elif 17006 <= zve <= 66760:
        z = (zve - 17005) / 10000
        est = (181.19 * z + 2397) * z + 1025.38
    elif 66761 <= zve <= 277825:
        est = 0.42 * zve - 10602.13
    else:
        est = 0.45 * zve - 18936.88
    return round(est)

#   Nettolohn
def berechne_nettolohn(bruttolohn, steuerklasse,kinder,verheiratet):
    sozialabgaben     = berechne_sozialabgaben(bruttolohn)
    
    if kinder > 0:                                                          #   Wenn kinder dann
        steuerklasse > 1
        if  verheiratet == False:
            steuerklasse = 2
            grundfreibetrag = 15624 + 240 * kinder
        elif verheiratet == True:
            steuerklasse = 3
            grundfreibetrag = 27448 + 240 * kinder
        else:
            steuerklasse    = 2
            grundfreibetrag = 15624 + 240 * kinder    
    else:                                                                   #   Wenn keine kinder dann
        if steuerklasse == 2:
            print("Um in der Steuerklasse 2 abrechnen zu können, bedarf es einem Kind.\nDem Steuerzahler steht dann ein Kinderfreibetrag von 4260,00€ zu.")
            steuerklasse = 1  
            grundfreibetrag = 11604
        elif verheiratet == True:
            steuerklasse    = 3 
            grundfreibetrag = 23208
        elif steuerklasse in [1, 4]:
            grundfreibetrag = 11604
        else:
            grundfreibetrag = 0
    
    # Funktionsaufrufe
    zve          = bruttolohn - sozialabgaben - grundfreibetrag
    est          = berechne_einkommensteuer(zve)
    nettolohn    = bruttolohn - sozialabgaben - est
    
    # Berechnungen für Brutto- und Nettolohn
    Brutto_Jahr   = bruttolohn
    Brutto_Monat  = bruttolohn   / 12
    Brutto_Tag    = Brutto_Monat / 21.65
    Brutto_Stunde = Brutto_Tag   / 8

    Netto_Jahr    = nettolohn
    Netto_Monat   = nettolohn   / 12
    Netto_Tag     = Netto_Monat / 21.65
    Netto_Stunde  = Netto_Tag   / 8

    return round(nettolohn),round(est),round(sozialabgaben),round(grundfreibetrag),kinder,steuerklasse,verheiratet,round(Brutto_Jahr),round(Brutto_Monat, 2),round(Brutto_Tag, 2),round(Brutto_Stunde,2),round(Netto_Jahr,2),round(Netto_Monat,2),round(Netto_Tag,2),round(Netto_Stunde,2)

#   Funktionen für 2.Auswertung, in diesem Fall für Ehepartner 

#   Sozialabgaben  
def berechne_Ehe_sozialabgaben(Ehe_bruttolohn):    
    Ehe_rentenversicherung = Ehe_bruttolohn * 0.093                                 # Arbeitnehmeranteil
    Ehe_krankenversicherung = Ehe_bruttolohn * 0.073                                # Arbeitnehmeranteil (ohne Zusatzbeitrag)
    Ehe_pflegeversicherung = Ehe_bruttolohn * 0.01525                               # Arbeitnehmeranteil ohne Kind
    Ehe_arbeitslosenversicherung = Ehe_bruttolohn * 0.012                           # Arbeitnehmeranteil
    Ehe_sozialabgaben = Ehe_rentenversicherung + Ehe_krankenversicherung + Ehe_pflegeversicherung + Ehe_arbeitslosenversicherung
    
    return Ehe_sozialabgaben
#   Einkommensteuer    
def berechne_Ehe_einkommensteuer(Ehe_zve):        
    if Ehe_zve <= 11604:
        return 0
    elif 11605 <= Ehe_zve <= 17005:
        y = (Ehe_zve - 11604) / 10000
        Ehe_est = (922.98 * y + 1400) * y
    elif 17006 <= Ehe_zve <= 66760:
        z = (Ehe_zve - 17005) / 10000
        Ehe_est = (181.19 * z + 2397) * z + 1025.38
    elif 66761 <= Ehe_zve <= 277825:
        Ehe_est = 0.42 * Ehe_zve - 10602.13
    else:
        Ehe_est = 0.45 * Ehe_zve - 18936.88
    
    return round(Ehe_est)
#   Nettolohn    
def berechne_Ehe_nettolohn(Ehe_bruttolohn,Ehe_SK,Ehe_grundfreibetrag):
    Ehe_sozialabgaben = berechne_Ehe_sozialabgaben(Ehe_bruttolohn)
    
    match Ehe_SK:
        case "4":
            Ehe_grundfreibetrag = 11604 
        case "5":
            Ehe_grundfreibetrag = 0
        case _:
            print("Steuerklasse des Ehepartners kann  nur 4 oder 5 sein und in Summe 8."
                    "\nAchtung: Für Ihren Partner lohnt sich nur noch ein Minijob mit 538 Mtl.")
            Ehe_grundfreibetrag = 0
            Ehe_grundfreibetrag = 0
    # Funktionsaufrufe
    Ehe_zve      = Ehe_bruttolohn - Ehe_sozialabgaben - Ehe_grundfreibetrag
    Ehe_est      = berechne_Ehe_einkommensteuer(Ehe_zve)
    Ehe_nettolohn= Ehe_bruttolohn - Ehe_sozialabgaben - Ehe_est
    
    # Berechnungen für Brutto-/Nettolohn Ehe_P_AN
    Ehe_JB        = Ehe_bruttolohn
    Ehe_MB        = Ehe_JB / 12
    Ehe_TB        = Ehe_MB / 21.65
    Ehe_SB        = Ehe_TB / 8

    Ehe_JN        = Ehe_nettolohn
    Ehe_MN        = Ehe_JN / 12
    Ehe_TN        = Ehe_MN / 21.65
    Ehe_SN        = Ehe_TN / 8
    
    return round(Ehe_nettolohn,2),round(Ehe_bruttolohn,2),round(Ehe_zve, 2),round(Ehe_est, 2),Ehe_SK,round(Ehe_sozialabgaben, 2),round(Ehe_grundfreibetrag, 2),round(Ehe_JB, 2),round(Ehe_MB, 2),round(Ehe_TB, 2) ,round(Ehe_SB, 2) ,round(Ehe_JN, 2) ,round(Ehe_MN, 2) ,round(Ehe_TN, 2) ,round(Ehe_SN, 2)

""" # Beispielaufruf
    Diese Funktion berechnet die Sozialabgaben, die Einkommensteuer und den Nettolohn basierend auf den aktuellen Formeln für 2024
    zve=Zu versteuerndes Einkommen= Bruttolohn
    est= Einkommensteuer
"""
#   Anzeige bei Start 
datum = datetime.now().strftime("- %d-%m-%Y  -|- %H:%M:%S |")
print(f"{T:<10}Wilkommen in Ihrem Gehaltsrechner{T:>10}"
    "\nWie viel Lohnsteuer zu zahlen ist, hängt immer entscheidend davon ab, welche Freibeträge einem zur Verfügung stehen.\n"
    "Dieser Gehaltsrechner verfügt über die aktuellen Zahlen der Freibeträge des Jahres 2024.\n"
    f"Es ist der {datum}")

#   Hauptschleife der Ausführung/Programmes

while True:
    Optionen=input(f"Möchten sie :\n1| Anzeigen{T:>25}  \n2| Einkommen berechen {T:>14}\n3| Oder das Programm verlassen. {T:>4} ").strip().lower() 
    if Optionen=="1":
        Optionen="anzeigen"
        print(f"Ihre Auswahl :{Optionen:^8} | \n")
        """|Aufzählungsschleife mit enumerate Funktion um die Listen in unserem Gehalt_dict zu numerieren,  |
           |start=1 gibt unsere startzahl an sonst 0.|"""
        print("Einkommens-Auswertung  |")   
        for i,values in enumerate(Gehalt_dict["Bruttolohn-Auswertung | "],start=1):
            print(f"                       |  - {i:^10} -|-{values:^10}")
        if Ehe_P_AN == True:
            print("\nEhepartner-Auswertung  |")
            for i,values in enumerate(Gehalt_dict["Einkommen-Ehepartners | "],start=12):
                print(f"                       |  - {i:^10} -|-{values:^10}")
        else:
            info = int(input("Wünschen sie Informationen zu den Steuerklassen? 1|Ja 2|Nein "))
            if info == 1:
                for i,values in enumerate(Gehalt_dict["Steuerklasse          | "],start=1):
                    print(f"Steuerklasse           |  - {i:^10} -|-{values}")
            elif info == 2:
                continue
            elif info !=1 or 2:
                print("Ungültige Eingabe: ") 
            else:
                continue
            pprint.pprint(Gehalt_dict["Sozialabgaben         | "])
    elif Optionen == "2":
        #Lokale Variablen - dienen dazu um der Funktion Werte zu übermitteln
        bruttolohn   = float(input("Geben sie Ihren Bruttolohn ein :"))  
        steuerklasse = int(input("Geben sie Ihre Steuerklasse ein: |-1-|-2-|-3-|-4-|-5-|-6-|"))
        kinder       = int(input("Wie viele Kinder leben in Ihrem Haushalt?"))
        verheiratet  = False
        verheiratet  = input("Haben sie einen Ehepartner?")=="ja"
        
        nettolohn,est,sozialabgaben,grundfreibetrag,kinder,steuerklasse,Brutto_Jahr,Brutto_Monat,Brutto_Tag,Brutto_Stunde,Netto_Jahr,Netto_Monat,Netto_Tag,Netto_Stunde,verheiratet,=berechne_nettolohn(bruttolohn,steuerklasse,kinder,verheiratet)
        ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",0,f"Brutto-Jahr            |{bruttolohn:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",1,f"Brutto-Monat           |{Brutto_Monat:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",2,f"Brutto-Tag             |{Brutto_Tag:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",3,f"Brutto-Stunde          |{Brutto_Stunde:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",4,f"Netto-Jahr             |{Netto_Jahr:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",5,f"Netto-Monat            |{Netto_Monat:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",6,f"Netto-Tag              |{Netto_Tag:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",7,f"Netto-Stunde           |{Netto_Stunde:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",8,f"Einkommenssteuer       |{est:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",9,f"Sozialabgaben          |{sozialabgaben:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",10,f"Grundfreibetrag        |{grundfreibetrag:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",11,f"Steuerklasse           |{steuerklasse:^10} |")
        
        print(f"Bruttolohn     : {bruttolohn}€")
        print(f"Nettolohn      : {nettolohn}€")
        print(f"Einkommensteuer: {est}€")
        print(f"Steuerklasse   : {steuerklasse}")
        print(f"Kinder         : {kinder}")
        print(f"Verheiratet    : {verheiratet}")
        print(f"Sozialabgaben  : {sozialabgaben}€")
        print(f"Grundfreibetrag: {grundfreibetrag}€")
        if verheiratet == True:
            Ehe_P_AN=input("Ist dieser Arbeitnehmer :")=="ja"
            while Ehe_P_AN == True:
                if steuerklasse >= 3:
                    print("\nIhre Steuerklasse muss gemeinsam 8 ergeben wenn sie also 3 haben, hat Ihr Partner 5.\nAb hier lohnt sich für Ihren Partner nur ein Minijob mit einem Verdienst von 538€ mtl. ")
                    Ehe_bruttolohn  = float(input("Geben sie bitte das Jahres  Brutto Ihres Partenrs ein."))
                    Ehe_Sk          = input("Geben sie die Steuerklasse Ihres Partners ein.") == "5"
                    Ehe_zve,Ehe_est,Ehe_sozialabgaben,Ehe_grundfreibetrag,Ehe_SK,Ehe_JB,Ehe_MB,Ehe_TB,Ehe_SB,Ehe_JN,Ehe_MN,Ehe_TN,Ehe_SN=berechne_Ehe_nettolohn(Ehe_bruttolohn,Ehe_grundfreibetrag,Ehe_SK)
                    # Funktionsaufruf von def ändern_indexListe 
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",0,f"Brutto-Jahr            |{Ehe_JB:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",1,f"Brutto-Monat           |{Ehe_MB:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",2,f"Brutto-Tag             |{Ehe_TB:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",3,f"Brutto-Stunde          |{Ehe_SB:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",4,f"Netto-Jahr             |{Ehe_JN:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",5,f"Netto-Monat            |{Ehe_MN:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",6,f"Netto-Tag              |{Ehe_TN:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",7,f"Netto-Stunde           |{Ehe_SN:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",8,f"Einkommenssteuer       |{Ehe_est:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",9,f"Sozialabgaben          |{Ehe_sozialabgaben:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",10,f"Grundfreibetrag        |{Ehe_grundfreibetrag:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",11,f"Steuerklasse           |{Ehe_Sk:^10} |")
                elif steuerklasse >= 4:
                    Ehe_bruttolohn  = float(input("Geben sie bitte das Jahres  Brutto Ihres Partenrs ein."))
                    Ehe_Sk          = input("Geben sie die Steuerklasse Ihres Partners ein.") == "4"
                    Ehe_zve,Ehe_est,Ehe_sozialabgaben,Ehe_grundfreibetrag,Ehe_SK,Ehe_JB,Ehe_MB,Ehe_TB,Ehe_SB,Ehe_JN,Ehe_MN,Ehe_TN,Ehe_SN=berechne_Ehe_nettolohn(Ehe_bruttolohn,Ehe_grundfreibetrag,Ehe_SK)
                    # Funktionsaufruf von def ändern_indexListe 
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",0,f"Brutto-Jahr            |{Ehe_JB:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",1,f"Brutto-Monat           |{Ehe_MB:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",2,f"Brutto-Tag             |{Ehe_TB:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",3,f"Brutto-Stunde          |{Ehe_SB:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",4,f"Netto-Jahr             |{Ehe_JN:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",5,f"Netto-Monat            |{Ehe_MN:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",6,f"Netto-Tag              |{Ehe_TN:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",7,f"Netto-Stunde           |{Ehe_SN:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",8,f"Einkommenssteuer       |{Ehe_est:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",9,f"Sozialabgaben          |{Ehe_sozialabgaben:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",10,f"Grundfreibetrag        |{Ehe_grundfreibetrag:^10.2f}€|")
                    ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",11,f"Steuerklasse           |{Ehe_Sk:^10} |")
                else:
                    continue
            else:
                continue             
        else:
           continue   
    elif Optionen== "3":                         # Bedingung zum beenden
        sys.exit("Programm wird beendet")
    else:
        print("Ungültige Eingabe") 
    
       
    #   Funktionsaufruf ändern_indexListe """ändern_indexListe(dict,"Name des Key"-Key,index-"vom Wertpaar",Wert)"""
"""    ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",0,f"Brutto-Jahr            |{bruttolohn:^10.2f}€|")
    ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",1,f"Brutto-Monat           |{Brutto_Monat:^10.2f}€|")
    ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",2,f"Brutto-Tag             |{Brutto_Tag:^10.2f}€|")
    ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",3,f"Brutto-Stunde          |{Brutto_Stunde:^10.2f}€|")
    ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",4,f"Netto-Jahr             |{Netto_Jahr:^10.2f}€|")
    ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",5,f"Netto-Monat            |{Netto_Monat:^10.2f}€|")
    ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",6,f"Netto-Tag              |{Netto_Tag:^10.2f}€|")
    ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",7,f"Netto-Stunde           |{Netto_Stunde:^10.2f}€|")
    ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",8,f"Einkommenssteuer       |{est:^10.2f}€|")
    ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",9,f"Sozialabgaben          |{sozialabgaben:^10.2f}€|")
    ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",10,f"Grundfreibetrag        |{grundfreibetrag:^10.2f}€|")
    ändern_indexListe(Gehalt_dict,"Bruttolohn-Auswertung | ",11,f"Steuerklasse           |{steuerklasse:^10} |")
    if Ehe_P_AN == True:
        ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",0,f"Brutto-Jahr            |{Ehe_JB:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",1,f"Brutto-Monat           |{Ehe_MB:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",2,f"Brutto-Tag             |{Ehe_TB:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",3,f"Brutto-Stunde          |{Ehe_SB:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",4,f"Netto-Jahr             |{Ehe_JN:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",5,f"Netto-Monat            |{Ehe_MN:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",6,f"Netto-Tag              |{Ehe_TN:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",7,f"Netto-Stunde           |{Ehe_SN:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",8,f"Einkommenssteuer       |{Ehe_est:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",9,f"Sozialabgaben          |{Ehe_sozialabgaben:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",10,f"Grundfreibetrag        |{Ehe_grundfreibetrag:^10.2f}€|")
        ändern_indexListe(Gehalt_dict,"Einkommen-Ehepartners | ",11,f"Steuerklasse           |{Ehe_Sk:^10} |")
        continue 
        """
   
