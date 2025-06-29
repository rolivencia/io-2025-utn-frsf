import pandas as pd

def parsear_seccion_variables(lineas):
    datos = []
    for linea in lineas:
        if linea.strip() == "" or "Variable" in linea and "Value" in linea and "Reduced Cost" in linea:
            continue
        partes = linea.split()
        if len(partes) < 3:
            continue
        # Los últimos dos elementos son siempre valor y costo reducido
        valor = partes[-2]
        reduced_cost = partes[-1]
        # Todo lo anterior es el nombre de la variable
        nombre = " ".join(partes[:-2])
        try:
            datos.append([nombre, float(valor), float(reduced_cost)])
        except ValueError:
            # Si no se puede convertir a float, skip esta línea
            continue
    return pd.DataFrame(datos, columns=["Variable", "Valor", "Costo Reducido"])

def parsear_seccion_restricciones(lineas):
    datos = []
    for linea in lineas:
        if linea.strip() == "" or ("Row" in linea and "Slack or Surplus" in linea and "Dual Price" in linea):
            continue
        partes = linea.split()
        if len(partes) < 3:
            continue
        # Los últimos dos elementos son siempre slack/surplus y dual price
        slack = partes[-2]
        dual = partes[-1]
        # Todo lo anterior es el nombre de la restricción
        nombre = " ".join(partes[:-2])
        try:
            datos.append([nombre, float(slack), float(dual)])
        except ValueError:
            # Si no se puede convertir a float, skip esta línea
            continue
    return pd.DataFrame(datos, columns=["Restricción", "Slack o Excedente", "Precio Dual"])

def procesar_archivo_lingo(ruta_archivo):
    with open(ruta_archivo, encoding="utf-8") as f:
        lineas = f.readlines()

    corte_idx = None
    for i, linea in enumerate(lineas):
        if "Row" in linea and "Slack or Surplus" in linea and "Dual Price" in linea:
            corte_idx = i
            break

    if corte_idx is None:
        raise ValueError("No se encontró el encabezado de la sección de restricciones")

    seccion_variables = lineas[:corte_idx]
    seccion_restricciones = lineas[corte_idx+1:]

    df_vars = parsear_seccion_variables(seccion_variables)
    df_restr = parsear_seccion_restricciones(seccion_restricciones)

    df_vars.to_csv("variables.csv", index=False)
    df_restr.to_csv("restricciones.csv", index=False)

    with pd.ExcelWriter("lingo_output.xlsx") as writer:
        df_vars.to_excel(writer, sheet_name="Variables", index=False)
        df_restr.to_excel(writer, sheet_name="Restricciones", index=False)

    print("Archivos generados: variables.csv, restricciones.csv, lingo_output.xlsx")

if __name__ == "__main__":
    procesar_archivo_lingo("reporte-solucion-optima.txt")
