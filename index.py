#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
usuarios = json.load(open('usuarios.json'))
parqueados = json.load(open('parqueados.json'))
pisos = json.load(open('tiposParqueaderos.json'))
estadisticas = open('estadisticas.txt', 'w')

def registro_vehiculo():
    nombre = input('Ingrese nombre y apellidos: ')
    identificacion = input('Ingrese su identificación (número entero): ')
    tipo_usuario = input('Ingrese tipo de usuario [Estudiante|Profesor|Personal Administrativo]: ')
    placa = input('Ingrese placa del vehículo: ')
    tipo_vehiculo = input('Ingrese tipo de vehículo [Automóvil|Automóvil Eléctrico|Motocicleta|Discapacitado]: ')
    plan_pago = input('Ingrese plan de pago [Mensualidad|Diario]: ')
    if validar('identificacion', int(identificacion)):
        print('Registro exitoso')
        usuarios['usuarios'].append([nombre, identificacion, tipo_usuario, placa, tipo_vehiculo, plan_pago])
        json.dump(usuarios, open('usuarios.json', 'w'))
    else:
        print('Este usuario ya se encuentra registrado')

def validar(tipo, elem):
    if tipo == 'identificacion':
        ident_actuales = []
        for usr in usuarios['usuarios']:
            ident_actuales.append(usr[1])
        return not elem in ident_actuales
    elif tipo == 'placa':
        placas_actuales = []
        for usr in usuarios['usuarios']:
            placas_actuales.append(usr[3])
        return not elem in placas_actuales
    elif tipo == 'parqueados':
        placas_actuales = []
        for piso in parqueados:
            for vehiculo in parqueados[piso]:
                placas_actuales.append(vehiculo[0])
        return not elem in placas_actuales

def ingreso_vehiculo():
    placa = input('Ingrese su placa: ')

    #Verificar si la placa ya se encuentra en el parqueadero
    while not validar('parqueados', placa):
        print('Esta placa ya se encuentra en el parqueadero')
        placa = input('Ingrese su placa: ')

    #Asigna tipo de vehiculo y la categoria_usuario verificando si ya se encuentra en el archivo usuarios.json
    categoria_usuario = ''
    if validar('placa', placa):
        tipo_vehiculo = input('Ingrese tipo de vehículo [Automóvil|Automóvil Eléctrico|Motocicleta|Discapacitado]: ')
        categoria_usuario = 'Visitante'
    else:
        tipo_vehiculo = ''
        for usr in usuarios['usuarios']:
            if placa == usr[3]:
                tipo_vehiculo = usr[4]
        categoria_usuario = 'Regular'

    #Genera la vista de los puestos disponibles segun el tipo de vehiculo y los puestos libres
    matrix = [
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"]
	]
    disponibles = {'Automóvil': [1], 'Automóvil Eléctrico': [1,2], 'Motocicleta': [3], 'Discapacitado': [1, 4]}
    for piso in parqueados:
        if piso == 'Piso6':
            del matrix[4:9]
        #Marca con X las posiciones que estan ocupadas
        for registro in parqueados[piso]:
            x, y = (registro[1:3])
            matrix[x][y] = 'X'
        #Marca con X las posiciones que no correspoden al tipo de vehiculo del usuario
        x = 0
        for fila in pisos[piso]:
            y = 0
            for celda in fila:
                if celda not in disponibles[tipo_vehiculo]:
                    matrix[x][y] = 'X'
                y += 1
            x += 1
        print(piso)
        print('  1   2   3   4   5   6   7   8   9   10')
        print('  ──────────────────────────────────────')
        cont = 1
        for line in matrix:
            print(cont, ' | '.join((line)))
            print('  ──────────────────────────────────────')
            cont += 1
        matrix = [
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"],
		["0","0","0","0","0","0","0","0","0","0"]
	]
    print('Estos son los parqueados disponibles (\'X\' significa no disponible)')

    #Pregunta por la posicion en la que el usuario quiere ingresar y verifica si sí es una posicion valida
    valido = False
    piso_parqueo = ''
    posicion = ''
    while not valido:
        piso_parqueo = input('Ingrese el piso en el que quiere parquear [Piso1|Piso2...]: ')
        posicion = eval(input('Ingrese la posición separado por coma (fila, columna): '))
        celda_disponible = True
        celda_tipo = False
        for registro in parqueados[piso_parqueo]:
            if (registro[1], registro[2]) == (posicion[0] - 1, posicion[1] - 1):
                celda_disponible = False
        if pisos[piso_parqueo][posicion[0]-1][posicion[1]-1] in disponibles[tipo_vehiculo]:
            celda_tipo = True
        valido = celda_disponible and celda_tipo
        if valido == False:
            print('La posición no es válida, intente otra vez')

    #Registra el vehiculo en el archivo de parqueados.json
    vehiculo = [placa, int(posicion[0])-1, int(posicion[1])-1, categoria_usuario, tipo_vehiculo]
    if valido:
        print('Ingreso exitoso')
        parqueados[piso_parqueo].append(vehiculo)
        json.dump(parqueados, open('parqueados.json', 'w'))

def retirar_vehiculo():
    placa = input('Ingrese su placa: ')
    horas = input('Ingrese el número de horas en el parqueadero (número entero): ')
    usuario = ''
    costos = {'Estudiante': 1000, 'Profesor': 2000, 'Personal Administrativo': 1500, 'Visitante': 3000}

    #verifica que el vehiculo está en el parqueadero
    if (not validar('parqueados', placa)):
        #Busca en qué piso y que posicion del registro se encuentra el vehiculo
        piso_actual = ''
        indice_parqueo = ''
        for piso in parqueados:
            for usr in parqueados[piso]:
                if usr[0] == placa:
                    usuario = usr
                    piso_actual = piso
                    indice_parqueo = parqueados[piso].index(usr)
                    break
        tipo_usuario = ''

        #Verifica el tipo de plan que tiene cada usuario si es Regular o Visitante y genera el costo
        if usuario[3] == 'Regular':
            plan_pago = ''
            for usr in usuarios['usuarios']:
                if placa == usr[3]:
                    plan_pago, tipo_usuario = usr[5], usr[2]

            if plan_pago == 'Mensualidad':
                print('El usuario tiene mensualidad, retiro exitoso')
            elif plan_pago == 'Diario':
                total = (costos[tipo_usuario]*int(horas))
                print(f'El costo es de {total}, retiro exitoso')

        elif usuario[3] == 'Visitante':
            tipo_usuario = 'Visitante'
            total = (costos[tipo_usuario]*int(horas))
            print(f'El costo es de {total}, retiro exitoso')

        #Borra el registro de ese usuario en el archivo parqueados.json
        del parqueados[piso_actual][indice_parqueo]
        json.dump(parqueados, open('parqueados.json', 'w'))
    else:
        print('Este vehículo no se encuentra en el parqueadero')

def generar_reportes():
    #Genera las estadisticas de Cantidad de usuarios por tipo de usuarios
    tipos_usuarios = {'Estudiante': 0, 'Profesor': 0, 'Personal Administrativo': 0, 'Visitante': 0}
    for usr in usuarios['usuarios']:
        tipos_usuarios[usr[2]] += 1
    for piso in parqueados:
        for usr in parqueados[piso]:
            if usr[3] == 'Visitante':
                tipos_usuarios['Visitante'] += 1
    estadisticas.write('Cantidad de vehículos por tipo de usuario:\n')

    #Genera las estadisticas de Cantidad de vehiculos por tipo de vehiculos
    for elem in tipos_usuarios:
        estadisticas.write(f'{elem}: {tipos_usuarios[elem]} vehiculos\n')
    tipo_vehiculos = {'Automóvil': 0, 'Automóvil Eléctrico': 0, 'Motocicleta': 0, 'Discapacitado': 0}
    for piso in parqueados:
        for usr in parqueados[piso]:
            tipo_vehiculos[usr[4]] += 1
    estadisticas.write('Cantidad de vehículos por tipo de vehículo:\n')

    #Calcula total de vehiculos y cantidad de vehiculo por piso
    for elem in tipo_vehiculos:
        estadisticas.write(f'{elem}: {tipo_vehiculos[elem]}\n')
    total_vehiculos = 0
    total_por_pisos = {}

    #Genera porcentajes por total de vehiculos y cantidad de vehiculo por piso
    for piso in parqueados:
        total_vehiculos += len(parqueados[piso])
        total_por_pisos[piso] = len(parqueados[piso])
    estadisticas.write(f'Porcentaje global: {round((total_vehiculos/550)*100, 2)}%\n')
    for elem in total_por_pisos:
        total_espacios = len(pisos[elem])
        estadisticas.write(f'{elem}: {round((total_por_pisos[elem]/(total_espacios*10))*100, 2)}%\n')
    print('Reportes generados exitosamente, ver archivo estadisticas.txt')

#Menu de ingreso
if __name__ == "__main__":
    opciones = {'1': registro_vehiculo, '2': ingreso_vehiculo, '3': retirar_vehiculo, '4': generar_reportes}
    print('Bienvenido Usuario(a)\n\n1.Registro Vehiculo\t2.Ingresar Vehiculo\n\n3.Retirar Vehiculo\t4.Generar Reportes\n')
    accion = input('Ingrese la acción que quiere realizar (número): ')
    opciones[accion]()
