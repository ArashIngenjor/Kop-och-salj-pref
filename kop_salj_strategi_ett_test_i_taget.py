import pandas as pd
from matplotlib import pyplot as plt

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
	
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
    
#Dessa kurser väljs för att testa strategi

kurs_kop = 290
kurs_salj = 380

# Filen som innehåller kurserna
filnamn_import = 'CORE-PREF.ST.csv'

#-----------------------------------------

data_aktie = pd.read_csv(filnamn_import)

price_date = pd.to_datetime(data_aktie['Date'])
price_close_pref = data_aktie['Close']

start_kapital = 10000
antal_aktier = 0
varde_strategi = start_kapital
antal_transaktioner = 0
har_aktier = False
likvider = start_kapital

utveckling_strategi_kr = [start_kapital]*len(price_close_pref)

# Punkter för köp och sälj
kurser_kop = []
datum_kop = []

kurser_salj = []
datum_salj = []

for i in range(len(price_date)):
    Kurs_close = price_close_pref[i]

    # Köp
    if Kurs_close<kurs_kop and har_aktier==False:
        kop(Kurs_close)
        print(price_date[i])
        print("Kurs: " + str(Kurs_close))
        print("antal_aktier: " + str(antal_aktier))
        print("likvider: " + str(likvider))
        print("antal_transaktioner: " + str(antal_transaktioner))
        print("Värde portfölj: " + str(Kurs_close*antal_aktier + likvider))
        print("\n")
        kurser_kop.append(Kurs_close)
        datum_kop.append(price_date[i])

    # Sälj    
    elif Kurs_close>kurs_salj and har_aktier==True:
        salj(Kurs_close)
        print(price_date[i])
        print("Kurs: " + str(Kurs_close))
        print("antal_aktier: " + str(antal_aktier))
        print("likvider: " + str(likvider))
        print("antal_transaktioner: " + str(antal_transaktioner))
        print("Värde portfölj: " + str(Kurs_close*antal_aktier + likvider))
        print("\n")
        kurser_salj.append(Kurs_close)
        datum_salj.append(price_date[i])
        
    # Beräknar värdet på portföljen (ex utdelning)
    utveckling_strategi_kr[i] = Kurs_close*antal_aktier + likvider
    


Varde_sista_dag_strategi = utveckling_strategi_kr[len(utveckling_strategi_kr)-1]
print("Sista dagen på körningen: ")
print(price_date[len(price_date)-1])
print("Värde på portföljen sista dagen: ")
print(Varde_sista_dag_strategi)

plot1 = plt.subplot2grid((2,1), (0,0), rowspan=1, colspan=1)
plot2 = plt.subplot2grid((2,1), (1,0), rowspan=1, colspan=1)

# Plottar kurva för priset på aktien och kurva för utvecklingen på strategi
plot1.plot(price_date, price_close_pref)
plot2.plot(price_date, utveckling_strategi_kr)

# Plottar gröna punkter vid köp och röda vid sälj
plot1.scatter(datum_kop, kurser_kop, color='g', label='Köp')
plot1.scatter(datum_salj, kurser_salj, color='r', label='Sälj')

plot1.set_title(filnamn_import)
plot1.set(ylabel='Kurs')
plot2.set(ylabel='Utveckling på 10 000kr')

plot1.legend()
plt.show()
