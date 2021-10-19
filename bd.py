import sqlite3
URL_DB = 'parqueadero.db'

def resgistrardato(sql) -> int:
    #Ejecuta consultas de acción : INSERT, DELETE,UPDATE
    try:
        #primera acción conectarme a la base de datos
        with sqlite3.connect(URL_DB) as conec:  #se hace con un manejador de contexto para cerrar la conección una vez culminado el proceso
            #creo un area intermedia para gestion de los contenidos(tambien llamado cursor)
            cur = conec.cursor()
            #procedo con la consulta
            res = cur.execute(sql).rowcount
            if res !=0: #VERIFICO SI HAY ALGUN CAMBIO
                conec.commit() #ASEGURO QUE SER GUARDE EL CAMBIO
    except:
        res = 0
    return res

def cargardato(sql) ->list:
    """"voy a hacer una consulta a la base de datos"""
    try:
        with sqlite3.connect(URL_DB) as conec:
            cur = conec.cursor()
            res = cur.execute(sql).fetchall()
    except Exception:
        res = None
    return res
