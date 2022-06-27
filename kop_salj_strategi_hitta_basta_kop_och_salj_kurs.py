import pandas as pd
import xlsxwriter

# Funktion för köp av aktien
def kop(kurs_nu):
    global antal_aktier
    global likvider
    global har_aktier
    global antal_transaktioner

    likvider_innan_kop = likvider
    antal_aktier = likvider//kurs_nu
    likvider = likvider_innan_kop%kurs_nu

    har_aktier = True
    antal_transaktioner = antal_transaktioner + 1

# Funktion för sälj av aktien     
def salj(kurs_nu):
    global antal_aktier
    global likvider
    global har_aktier
    global antal_transaktioner
    
    likvider = likvider + antal_aktier*kurs_nu
    
    antal_aktier = 0
    har_aktier = False
    antal_transaktioner = antal_transaktioner + 1
    


data_aktie = pd.read_csv('CORE-PREF.ST.csv')

price_date = pd.to_datetime(data_aktie['Date'])
price_close_pref = data_aktie['Close']

# Initierar parametrar
kurs_kop = 1
kurs_salj = 1

lagsta_kurs = int(round(price_close_pref.min()))
hogsta_kurs = int(round(price_close_pref.max()))

# Skriv rubruker till excel-fil
filename = "Resultat.xlsx"

workbook = xlsxwriter.Workbook(filename)
worksheet = workbook.add_worksheet()

worksheet.write(0, 0, "Kurs köp")
worksheet.write(0, 1, "Kurs sälj")
worksheet.write(0, 2, "Antal transaktioner")
worksheet.write(0, 3, "Utveckling 10 000 kr")

aktuell_rad_excel = 1

for s in range(hogsta_kurs, lagsta_kurs-1, -1):
    kurs_salj = s
    
    for k in range(lagsta_kurs, hogsta_kurs+1):
        kurs_kop = k

        if kurs_kop<kurs_salj:
            #--------------------------- Ett test
            start_kapital = 10000
            antal_aktier = 0
            varde_strategi = start_kapital
            antal_transaktioner = 0
            har_aktier = False
            likvider = start_kapital

            utveckling_strategi_kr = [start_kapital]*len(price_close_pref)

            for i in range(len(price_date)):
                Kurs_close = price_close_pref[i]

                #print(price_date[i])
                if Kurs_close<kurs_kop and har_aktier==False:
                    kop(Kurs_close)

                elif Kurs_close>kurs_salj and har_aktier==True:
                    salj(Kurs_close)
                    
                # Beräknar värdet på portföljen (ex utdelning)
                utveckling_strategi_kr[i] = Kurs_close*antal_aktier + likvider
                

            Varde_sista_dag_strategi = utveckling_strategi_kr[len(utveckling_strategi_kr)-1]

            # Skriver resultat till excel
            worksheet.write(aktuell_rad_excel, 0, kurs_kop)
            worksheet.write(aktuell_rad_excel, 1, kurs_salj)
            worksheet.write(aktuell_rad_excel, 2, antal_transaktioner)
            worksheet.write(aktuell_rad_excel, 3, Varde_sista_dag_strategi)

            # Går till nästa rad
            aktuell_rad_excel = aktuell_rad_excel + 1

            #---------------------------
workbook.close()

