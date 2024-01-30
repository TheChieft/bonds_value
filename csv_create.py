def create_csv():
    keywords = ["Nemotécnico","Tasa apertura", "Última tasa",
                "Tasa Máxima", "Tasa Mínima", "Cantidad", "Volumen*",
                "Base", "Fecha de emisión","Fecha de vencimiento","Tasa facial","Tipo de tasa*"]
    with open("data/db/info_bonds_public.csv", "w") as file:
        file.write(f"Fecha,{','.join(keywords)}\n")

def write_example_data():
    with open("test.txt", "r") as file:
        for line in file:
            with open("data/db/info_bonds_public.csv", "a") as file:
                file.write(f"{line}")
create_csv()
