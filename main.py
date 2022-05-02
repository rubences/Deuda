
# Trabajo de Python: Deuda
# El objetivo de este trabajo es hacer un análisis del endeudamiento público por países.

import pandas as pd
import matplotlib.pyplot as plt

# Ejercicio 1
# Crear una función que reciba un país y un tipo de deuda y devuelva un diccionario con todos los periodos y la cantidad de deuda en esos periodos de ese país y tipo de deuda.

# Abrimos el fichero
try:
    f = open('deuda.csv')
except FileNotFoundError:
    print('El fichero no existe.')
else:
    # Creamos una lista con las líneas del fichero.
    lineas = f.readlines()
    f.close()
    # Dividimos la primera línea del fichero que contiene los nombres de las columnas y creamos una lista con los nombres de las columnas.
    columnas = lineas[0].split(',')

    # Creamos un diccionario vacío para ir añadiendo las series de deuda de cada país.
    deudas = {}
    # Recorremos las lineas del fichero desde la 1 hasta el final
    for linea in lineas[1:]:
        # Creamos el diccionario que contendrá la información de una serie país-tipo deuda.
        serie = {}
        # Creamos una lista con los campos partiendo la línea por el carácter ,.
        campos = linea.split(',')
        # Recorremos los campos de la línea
        for i in range(4, len(columnas)):
            # Para cada campo añadimos al diccionario el par con clave el nombre de la columna y valor el campo de la posición i.
            serie[columnas[i][:6]] = campos[i]
        # Añadimos el diccionario a la lista de alojamientos.
        deudas[(campos[1], campos[3])] = serie

    print(deudas)

def deuda_pais(deudas, pais, tipo):
    ''' Función que recibe un diccionario con las deudas de cada país y devuelve la serie de deuda de un tipo y un país dado.

    Parámetros:
        - deudas: Es un diccionario de diccionarios donde las claves del diccionario principal son tuplas (país, tipo de deuda) y los valores son diccionarios con las deudas de cada trimestre.
        - pais: Es una cadena con el nombre del país.
        - tipo: Es una cadena con el tipo de deuda.

    Devuelve: Un diccionario con las deudas trimestrales del tipo y el país dados.
    '''
    return deudas[(pais, tipo)]


# Ejemplo
print(deuda_pais(deudas, 'AUS', 'DP.DOD.DLTC.CR.M1.PS.CD'))

# Ejercicio 2
# Crear una función que reciba un país y un tipo de deuda y devuelva un diccionario con el mínimo y el máximo de deuda de ese tipo para ese país.


def rango_deuda(deudas, pais, tipo):
    ''' Función que devuelve el mínino y el máximo de deuda de un tipo y un país dado.

    Parámetros:
        - deudas: Es un diccionario de diccionarios donde las claves del diccionario principal son tuplas (país, tipo de deuda) y los valores son diccionarios con las deudas de cada trimestre.
        - pais: Es una cadena con el nombre del país.
        - tipo: Es una cadena con el tipo de deuda.

    Devuelve: Un diccionario con el mínimo y el máximo de la deuda trimestral del tipo y el país dados.
    '''

    deuda = deudas[(pais, tipo)]
    return {'Mínimo': min(deuda.values()), 'Máximo': max(deuda.values())}


# Ejemplo
print(rango_deuda(deudas, 'AUS', 'DP.DOD.DLTC.CR.M1.PS.CD'))

# Ejercicio 3
# Crear una función que reciba un país y un año, y devuelva un diccionario con la deuda interna y la deuda externa de ese país en ese año.


def deuda_interna_externa(deudas, pais, año):
    ''' Función que devuelve la deuda interna y externa de un trimestre y un país dado.

    Parámetros:
        - deudas: Es un diccionario de diccionarios donde las claves del diccionario principal son tuplas (país, tipo de deuda) y los valores son diccionarios con las deudas de cada trimestre.
        - pais: Es una cadena con el nombre del país.
        - año: Es una cadena con el año y el trimestre.

    Devuelve: Un diccionario con la deuda interna y externa del trimestre y el país dados.
    '''

    deuda_interna = deudas[(pais, 'DP.DOD.DECD.CR.PS.CD')]
    deuda_externa = deudas[(pais, 'DP.DOD.DECX.CR.PS.CD')]
    return {'Deuda interna': deuda_interna[año], 'Deuda externa': deuda_externa[año]}


# Ejemplo
print(deuda_interna_externa(deudas, 'AUS', '2015Q1'))

# Ejercicio 4
# Crear una función que reciba un país y un año, y devuelva un diccionario con la deuda en moneda local y la deuda en moneda extranjera de ese país en ese año.


def deuda_moneda_local_extranjera(deudas, pais, año):
    ''' Función que devuelve la deuda en moneda local y extranjera de un trimestre y un país dado.

    Parámetros:
        - deudas: Es un diccionario de diccionarios donde las claves del diccionario principal son tuplas (país, tipo de deuda) y los valores son diccionarios con las deudas de cada trimestre.
        - pais: Es una cadena con el nombre del país.
        - año: Es una cadena con el año y el trimestre.

    Devuelve: Un diccionario con la deuda en moneda local y extranjera del trimestre y el país dados.
    '''

    deuda_moneda_local = deudas[(pais, 'DP.DOD.DECN.CR.PS.CD')]
    deuda_moneda_extranjera = deudas[(pais, 'DP.DOD.DECF.CR.PS.CD')]
    return {'Deuda en moneda local': deuda_moneda_local[año], 'Deuda en moneda extranjera': deuda_moneda_extranjera[año]}


# Ejemplo
print(deuda_moneda_local_extranjera(deudas, 'AUS', '2015Q1'))

# Ejercicio 5
# Preprocesar el fichero de deuda pública para obtener un data frame con el país, el tipo de deuda, la fecha y la cantidad de deuda.
deuda = pd.read_csv('deuda.csv')
deuda = deuda.melt(id_vars=['Country Name', 'Country Code', 'Series Name',
                            'Series Code'], var_name='Fecha', value_name='Cantidad')
# Renombramos los nombres de las columnas que queremos
deuda.rename(columns={'Country Name': 'Pais', 'Country Code': 'PaisId',
                      'Series Name': 'Tipo', 'Series Code': 'TipoId'}, inplace=True)
# Extraemos los 6 primeros caracteres de la columna Fecha
deuda['Fecha'] = deuda.Fecha.str[0:6]
# Renombramos los tipos de deuda
tipos = {'DP.DOD.DECD.CR.PS.CD': 'Deuda interna', 'DP.DOD.DECN.CR.PS.CD': 'Deuda en moneda local', 'DP.DOD.DECX.CR.PS.CD': 'Deuda externa',
         'DP.DOD.DECF.CR.PS.CD': 'Deuda en moneda extranjera', 'DP.DOD.DLTC.CR.M1.PS.CD': 'Deuda a lago plazo', 'DP.DOD.DSTC.CR.PS.CD': 'Deuda a corto plazo'}
deuda['TipoId'] = deuda.TipoId.apply(
    lambda x: tipos[x] if x in tipos.keys() else x)

print(deuda)

# Ejercicio 6
# Crear una función que reciba un país y una fecha y devuelva una serie con la deuda total interna, externa, en moneda local, en moneda extranjera, a corto plazo y a largo plazo, de ese país en esa fecha.


def resumen_deuda(deuda, pais, fecha):
    ''' Función que devuelve la deuda total interna, externa, en moneda local, en moneda extranjera, a corto plazo y a largo plazo, de un país y una fecha dados.
    
    Parámetros:
        - deuda: Es un DataFrame con las deudas de los países.
        - pais: Es una cadena con el nombre del país.
        - fecha: Es una cadena con el año y el trimestre.

    Devuelve: Una serie con la deuda total interna, externa, en moneda local, en moneda extranjera, a corto plazo y a largo plazo, del país y la fecha dados.
    '''

    # Filtramos el país, la fecha y los tipos de deuda
    deuda_filtro = deuda[(deuda.PaisId == pais) & (deuda.Fecha == fecha) & deuda.TipoId.isin(
        ['Deuda interna', 'Deuda en moneda local', 'Deuda externa', 'Deuda en moneda extranjera', 'Deuda a lago plazo', 'Deuda a corto plazo'])]
    # Devolvemos la serie de la columna Cantidad tomando como índice la columna del tipo de deuda.
    return pd.Series(list(deuda_filtro.Cantidad), index=deuda_filtro.TipoId)


# Ejemplo
print(resumen_deuda(deuda, 'AUS', '2015Q1'))

# Ejercicio 7
# Crear una función que reciba un tipo de deuda y una fecha, y devuelva una serie con la deuda de ese tipo de todos los países en esa fecha.

def resumen_deuda(deuda, tipo, fecha):
    ''' Función que devuelve la deuda de todos los países de un tipo y en una fecha dados.
    
    Parámetros:
        - deuda: Es un DataFrame con las deudas de los países.
        - tipo: Es una cadena con el tipo de deuda.
        - fecha: Es una cadena con el año y el trimestre.

    Devuelve: Una serie con la deuda de todos los países del tipo y la fecha dados.
    '''

    # Filtramos el tipo de deuda y la fecha
    deuda_filtro = deuda[(deuda.TipoId == tipo) & (deuda.Fecha == fecha)]
    # Devolvemos la serie de la columna Cantidad tomando como índice la columna del país.
    return pd.Series(list(deuda_filtro.Cantidad), index=deuda_filtro.Pais)


# Ejemplo
print(resumen_deuda(deuda, 'Deuda externa', '2015Q1'))

# Ejercicio 8
# Crear una función que reciba un país y una fecha y dibuje un diagrama de sectores con la deuda interna y la deuda externa de ese país en esa fecha.


def sectores_deuda_externa_interna(deudas, pais, fecha):
    ''' Función que dibuja un diagrama de sectores con la deuda interna y externa de un país y una fecha dados.
    
    Parámetros:
        - deuda: Es un DataFrame con las deudas de los países.
        - tipo: Es una cadena con el tipo de deuda.
        - fecha: Es una cadena con el año y el trimestre.
    '''

    # Filtramos el país, la fecha y los tipos de deuda
    deuda_filtro = deuda[(deuda.PaisId == pais) & (
        deuda.Fecha == fecha) & deuda.TipoId.isin(['Deuda interna', 'Deuda externa'])]
    # Creamos una serie de la columna Cantidad tomando como índice la columna del tipo de deuda.
    serie = pd.Series(list(deuda_filtro.Cantidad), index=deuda_filtro.TipoId)
    # Creamos la figura y los ejes
    fig, ax = plt.subplots()
    # Dibujamos el diagrama de sectores
    serie.plot(kind='pie', autopct='%1.0f%%', ax=ax)
    # Añadimos el título
    ax.set_title('Deuda externa vs interna de ' + pais + ' en ' + fecha, loc="center",
                 fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
    # Eliminamos la etiqueta del eje y
    ax.set_ylabel('')
    # Guardamos el gráfico.
    plt.savefig('img/sectores-deuda-externa-interna-' + pais +
                '-' + fecha + '.png', bbox_inches='tight')
    return


# Ejemplo
print(sectores_deuda_externa_interna(deuda, 'AUS', '2015Q1'))

# Ejercicio 9
# Crear una función que reciba un país y una fecha, y dibuje un diagrama de barras con las cantidades de los distintos tipos de deudas de ese país en esa fecha.

def barras_tipos_deuda(deuda, pais, fecha):
    ''' Función que dibuja un diagrama de barras con las cantidades de los distintos tipos de deudas de un país y una fecha dados.
    
    Parámetros:
        - deuda: Es un DataFrame con las deudas de los países.
        - pais: Es una cadena con el nombre del país.
        - fecha: Es una cadena con el año y el trimestre.
    '''

    # Filtramos el país, la fecha y los tipos de deuda
    deuda_filtro = deuda[(deuda.PaisId == pais) & (deuda.Fecha == fecha)]
    # Creamos la figura y los ejes
    fig, ax = plt.subplots()
    # Dibujamos el diagrama de barras
    deuda_filtro.plot(kind='bar', x='Tipo', y='Cantidad', ax=ax)
    # Añadimos el título
    ax.set_title('Deuda por tipología de ' + pais + ' en ' + fecha, loc="center",
                 fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
    # Eliminamos la leyenda
    ax.legend().remove()
    # Guardamos el gráfico.
    plt.savefig('img/barras-tipos-deuda-' + pais + '-' +
                fecha + '.png', bbox_inches='tight')
    return


# Ejemplo
print(barras_tipos_deuda(deuda, 'AUS', '2015Q1'))

# Ejercicio 10
# Crear una función que reciba una lista de países y un tipo de deuda y dibuje un diagrama de líneas con la evolución de ese tipo de deuda de esos países (una línea por país).

def evolucion_tipo_deuda(deuda, paises, tipo):
    ''' Función que dibuja un diagrama de líneas con la evolución de un tipo de deuda y una lista de países dados.
    
    Parámetros:
        - deuda: Es un DataFrame con las deudas de los países.
        - paises: Es una lista de cadenas con los nombres de los países.
        - tipo: Es una cadena con el tipo de deuda.
    '''

    # Filtramos los países y el tipo de deuda
    deuda_filtro = deuda[(deuda.PaisId.isin(paises)) & (deuda.TipoId == tipo)]
    # Convertimos la fecha en el índice
    deuda_filtro.set_index('Fecha', inplace=True)
    # Creamos la figura y los ejes
    fig, ax = plt.subplots()
    # Dibujamos el diagrama de barras
    deuda_filtro.groupby('PaisId').Cantidad.plot(legend=True, ax=ax)
    # Añadimos el título
    ax.set_title('Evolución de ' + tipo, loc="center",
                 fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
    # Guardamos el gráfico.
    plt.savefig('img/evolucion-tipo-deuda-' +
                tipo + '.png', bbox_inches='tight')
    return

# Ejemplo
evolucion_tipo_deuda(deuda, ['GEO', 'SLV', 'MDA'], 'Deuda interna')

# Ejercicio 11
# Crear una función que reciba un país y una lista de tipos de deuda y dibuje un diagrama de líneas con la evolución de esos tipos de deuda de ese país (una línea por tipo de deuda).

def evolucion_deuda_pais(deuda, pais, tipos):
    ''' Función que dibuja un diagrama de líneas con la evolución de unos tipos de deuda y un país dado.

    Parámetros:
        - deuda: Es un DataFrame con las deudas de los países.
        - pais: Es un cadena con el nombre del país.
        - tipos: Es una lista de cadenas con los tipo de deuda.
    '''

    # Filtramos el país y los tipos de deuda
    deuda_filtro = deuda[(deuda.PaisId == pais) & (deuda.TipoId.isin(tipos))]
    # Convertimos la fecha en el índice
    deuda_filtro.set_index('Fecha', inplace=True)
    # Creamos la figura y los ejes
    fig, ax = plt.subplots()
    # Dibujamos el diagrama de barras
    deuda_filtro.groupby('TipoId').Cantidad.plot(legend=True, ax=ax)
    # Añadimos el título
    ax.set_title('Evolución de los tipos de deuda de ' + pais, loc="center",
                 fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
    # Guardamos el gráfico.
    plt.savefig('img/evolucion-deuda-' + pais + '.png', bbox_inches='tight')
    return


# Ejemplo
evolucion_deuda_pais(deuda, 'SLV', ['Deuda interna', 'Deuda externa'])

# Ejercicio 12
# Crear una función que reciba una lista de países y una lista de tipos de deuda, y dibuje un diagrama de cajas con las deudas de esos tipos de esos países (una caja por país y tipo de deuda).

def cajas_deuda(deuda, paises, tipos):
    ''' Función que dibuja un diagrama de cajas con las deudas de unos tipos y unos países dados.

    Parámetros:
        - deuda: Es un DataFrame con las deudas de los países.
        - paises: Es una lista de cadenas con los nombres de los países.
        - tipos: Es una lista de cadenas con los tipo de deuda.
    '''

    # Filtramos el país y los tipos de deuda
    deuda_filtro = deuda[(deuda.PaisId.isin(paises)) &
                         (deuda.TipoId.isin(tipos))]
    # Creamos la figura y los ejes
    fig, ax = plt.subplots()
    # Dibujamos el diagrama de cajas
    deuda_filtro.boxplot(column='Cantidad', by=['PaisId', 'TipoId'], ax=ax)
    # Añadimos el título
    ax.set_title('Deuda de ' + ', '.join(paises) + '\n(' + ', '.join(tipos) + ')',
                 loc="center", fontdict={'fontsize': 14, 'fontweight': 'bold', 'color': 'tab:blue'})
    plt.suptitle('')
    # Rotamos las etiquetas del eje x
    plt.xticks(rotation=90)
    # Guardamos el gráfico.
    plt.savefig('img/cajas-deuda-' + '-'.join(paises) + '-' +
                '-'.join(tipos) + '.png', bbox_inches='tight')
    return


# Ejemplo
cajas_deuda(deuda, ['BOL', 'MDA', 'SLV'], ['Deuda interna', 'Deuda externa'])
