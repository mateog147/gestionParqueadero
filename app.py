from flask import Flask, render_template, redirect, session, flash, request,url_for
from flask.templating import render_template
from bd import cargardato, resgistrardato
from datetime import datetime
import math
import os

server = Flask('__name__')

@server.route('/')
@server.route('/home/')
@server.route('/index/')
def index():
    return render_template('index.html')

@server.route('/ingreso')
@server.route('/ingreso/',methods=['GET', 'POST'])
def ingresar():
    if request.method=='GET':
        return render_template('ingreso.html')
    else:
        placa = request.form['placa']
        ingreso = datetime.now()

        print(f'voy a registrar {placa}')
        #intento conectarme
        try:
            dat = None
            if placa==None:
                msg = 'ERROR: SE DEBE INGRESAR UNA PLACA'
            else:
                # Valido los datos 
                sql = f"SELECT * FROM disponible"
                dat = cargardato(sql)
                dis = dat[0][0]
                if dis <=0:
                    return render_template('error.html',mensaje='ERROR  NO HAY CUPOS DISPONIBLES')

                sql = f"INSERT INTO registros (placa, ingreso) VALUES ('{placa}', '{ingreso}')"
                #print('arme a consulta')
                res = resgistrardato(sql)
                if res==0:
                    msg ='ERROR AL CARGAR LA INFORMACIÓN'
                else:
                    msg = 'Ok'

                sql = f"SELECT * FROM disponible"
                dat = cargardato(sql)
                dis = dat[0][0]
                dis -= 1
                sql = f"UPDATE disponible SET actual = {dis}"
                res = resgistrardato(sql)
                if res==0:
                    return render_template('error.html',mensaje='ERROR AL RESTAR LOS CUPOS')
                else:
                    msg = 'Ok'
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)

        if msg=="Ok":
            return redirect('/home/')
        else:
            return render_template('error.html',mensaje=msg)

@server.route('/egreso')
@server.route('/egreso/',methods=['GET', 'POST'])
def retirar():
    if request.method=='GET':
        return render_template('egreso.html')
    else:
        placa = request.form['placa']
        salida = datetime.now()
        #print(f'me pidieron buscar {placa}')
        #intento conectarme
        try:
            dat = None
            if placa==None:
                msg = 'ERROR: SE DEBE INGRESAR UNA PLACA'

            else:
                # Valido los datos 
                sql = f"SELECT ingreso FROM registros WHERE placa='{placa}' AND estado='A'"
                #print('arme a consulta')
                dat = cargardato(sql)
                if len(dat)==0:
                    msg ='ERROR:: PLACA SIN REGISTRO ACTIVO'
                else:
                    msg = 'Ok'
                    ingreso = datetime.fromisoformat(dat[0][0])
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)
            dat = None

        if msg=="Ok":
            #print('INFO ENCONTRAda')
            resta = math.ceil((salida - ingreso).total_seconds()/60.0)
            saldo = resta*100
            #print(resta)
            session['placa'] = placa
            session['saldo'] = saldo
            session['ingreso'] = ingreso
            session['salida'] = salida
            return redirect(url_for('pagar'))
        else:
            return render_template('error.html',mensaje=msg)

@server.route('/pago')
@server.route('/pago/',methods=['GET', 'POST'])
def pagar():
    if request.method=='GET':
        return render_template('pago.html',plc=session['placa'],pago=session['saldo'],horaEntrada=session['ingreso'],horaSalida=session['salida'])
    else:

        #intento conectarme
        try:
            dat = None
            if session['placa']==None:
                msg = 'ERROR'
            else:
                # Valido los datos 
                sql = f"UPDATE registros SET estado = 'C', pago = '{session['saldo']}', salida = '{session['salida']}' WHERE placa='{session['placa']}' AND estado='A'"
                #print('arme a consulta')
                res = resgistrardato(sql)
                if res==0:
                    msg ='ERROR AL CARGAR LA INFORMACIÓN'
                else:
                    msg = 'Ok'

                sql = f"SELECT * FROM disponible"
                dat = cargardato(sql)
                dis = dat[0][0]
                dis += 1
                sql = f"UPDATE disponible SET actual = {dis}"
                res = resgistrardato(sql)
                if res==0:
                    return render_template('error.html',mensaje='ERROR AL ACTUALIZAR LOS CUPOS')
                else:
                    msg = 'Ok'
                    
        except Exception:
            msg = 'ERROR: Por favor intente luego'
            print(Exception)

        if msg=="Ok":
            return redirect('/home/')
        else:
            return render_template('error.html',mensaje=msg)
@server.route('/estado')
@server.route('/estado/')
def estado():
    try:
        # Valido los datos 
        sql = f"SELECT * FROM disponible"
        #print('arme a consulta')
        dat = cargardato(sql)
        if len(dat)==0:
            msg ='ERROR'
        else:
            msg = 'Ok'
            dis = dat[0][0]
                    
    except Exception:
        msg = 'ERROR: Por favor intente luego'
        print(Exception)
        dat = None
    if msg == 'Ok':
        return render_template('estado.html',disponible=dis)
    else:
        return render_template('error.html')
@server.route('/error')
@server.route('/error/')
def error():
    return render_template('error.html',mensaje='ERROR')

if __name__=='__main__':
    server.secret_key=os.urandom(12)
    server.run(debug=True,port=8080)