import pandas as pd
import matplotlib.pyplot as plt

# wczytaj pliki
liczniki_cieplo = pd.read_excel("LicznikCiepła.xlsx")
pogoda_gdansk_swibno = pd.read_excel("Pogoda_gdańsk_wykonanie.xlsx", sheet_name='Świbno')
pogoda_gdansk_rebiech = pd.read_excel("Pogoda_gdańsk_wykonanie.xlsx", sheet_name='Rębiechowo')
sred_temp = pd.read_excel("Pogoda_gdańsk_wykonanie.xlsx", sheet_name='Godzinowe', header=2).iloc[:, -1]

# ujednolicenie typów dat w jeden typ
liczniki_cieplo['UNIT_DATE'] = pd.to_datetime(liczniki_cieplo['UNIT_DATE'], format='%d.%m.%Y %H')
liczniki_cieplo['UNIT_DATE'] = liczniki_cieplo['UNIT_DATE'].dt.floor('H')
pogoda_gdansk_swibno['Data'] = pd.to_datetime(pogoda_gdansk_swibno['Data'], format='%d.%m.%Y %H')
pogoda_gdansk_rebiech['Data'] = pd.to_datetime(pogoda_gdansk_rebiech['Data'], format='%d.%m.%Y %H')

# ujednolicenie plików
ujednolicone = liczniki_cieplo.merge(pogoda_gdansk_swibno, left_on='UNIT_DATE', right_on='Data', how='left')
ujednolicone = ujednolicone.merge(pogoda_gdansk_rebiech, on='Data', how='left')
ujednolicone = ujednolicone.rename(
    columns={'Temperatura_x': 'temperatura_swibno', 'Temperatura_y': 'temperatura_rebiech'})
ujednolicone['srednia-temp'] = sred_temp

# policz agregacje dla dni osobno
pogrupowane_dniami = ujednolicone.groupby(ujednolicone['UNIT_DATE'].dt.date).mean()
pogrupowane_dniami['dni'] = pogrupowane_dniami.index
pogrupowane_dniami = pogrupowane_dniami.reset_index(drop=True)
ujednolicone = ujednolicone.merge(pogrupowane_dniami, left_on=ujednolicone['UNIT_DATE'].dt.date, right_on='dni',
                                  how='left')


# policz agregacje dla miesięcy osobno
pogrupowane_mcami = ujednolicone.groupby([ujednolicone['UNIT_DATE'].dt.year, ujednolicone['UNIT_DATE'].dt.month])
srednie = pogrupowane_mcami[['ThermalEnergy', 'srednia-temp']].agg(['mean'])
srednie.columns = ['ThermalEnergy_sred_miesiac', 'srednia-temp_sred_miesiac']
ujednolicone = ujednolicone.merge(srednie,
                                  left_on=[ujednolicone['UNIT_DATE'].dt.year, ujednolicone['UNIT_DATE'].dt.month],
                                  right_index=True)
print(ujednolicone)
# ujednolicone.to_excel("output.xlsx")
