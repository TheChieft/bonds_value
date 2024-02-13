from datetime import datetime

def si_vendo(fc, fv, te, ta, vb):
    years_to_maturity = (fc - fv).days / 365.0  # Calculamos los años hasta el vencimiento
    r = te *((((1+ta)**years_to_maturity) -1) / ((1 + ta) ** years_to_maturity) * ta) + (100/((1+ta)**years_to_maturity))
    return r

vb = 5000000  # Valor nominal del bono
te = 12  # Tasa del cupón (%)
ta = 14  # Tasa actual (%)
fc = datetime(2022, 2, 13)  # Fecha del último pago de cupón
fv = datetime(2023, 2, 13)  # Fecha de venta del bono

print(si_vendo(fc, fv, te, ta, vb))