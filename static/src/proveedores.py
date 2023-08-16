from flask import request, render_template, Blueprint
from static.src.googleAPI import service, config, access_token
import requests, json

proveedores_bp = Blueprint('/static/src/proveedores', __name__)

# Ruta para "Ver Proveedores"
@proveedores_bp.route('/VerProveedor', methods=['GET'])
def ver_proveedor():
    # Obtener datos de la hoja de cálculo
    url = 'https://sheets.googleapis.com/v4/spreadsheets/160T7u6nxNElz5BX6oCbqNX_aRDR8WrEh2bOYAQCFNdQ/values/Proveedores'
    headers = {'Authorization': 'Bearer ' + access_token}
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)['values']

    return render_template('/proveedores/proveedorVer.html', data=data)


# Ruta para ver "Agregar proveedores"
@proveedores_bp.route('/Ver/AgregarProveedor', methods=['GET'])
def VerAgregarProveedor():
    return render_template('/proveedores/proveedorAgregar.html')


# Ruta para "Agregar proveedores"
@proveedores_bp.route('/agregarProveedor', methods=['POST'])
def agregar_proveedor():
    # Obtener los datos enviados en la solicitud POST
    RAZON_SOCIAL = request.form['RAZON_SOCIAL']
    RIF = request.form['RIF']
    DIRECCION = request.form['DIRECCION']
    TELEFONO = request.form['TELEFONO']
    PORCENTAJE = request.form['PORCENTAJE']

    # Obtener datos de la hoja de cálculo
    sheet_id = config.get('GOOGLE_SPREADSHEET_ID')
    range_name = config.get('GOOGLE_CELL_RANGE')
    result = service.spreadsheets().values().get(
    spreadsheetId=sheet_id, range=range_name).execute()
    rows = result.get('values', [])
    
    # Verificar si existe el proveedor
    for i in range(len(rows)):
        for x in range(len(rows[i])):
            if rows[i][x] == RIF:
                mensaje= "Este proveedor ya existe."
                return render_template('/proveedores/proveedorMensaje.html',mensaje=mensaje)

    # Define los parámetros para agregar una nueva fila
    spreadsheet_id = config.get('GOOGLE_SPREADSHEET_ID')
    value_input_option = 'USER_ENTERED'
    insert_data_option = 'INSERT_ROWS'
    value_range_body = {
        'values': [[RIF, RAZON_SOCIAL, DIRECCION, TELEFONO, PORCENTAJE]]
    }
    # Agrega los datos a la hoja de cálculo
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=range_name,
        valueInputOption=value_input_option,
        insertDataOption=insert_data_option,
        body=value_range_body
    ).execute()

    mensaje = "Proveedor creado con éxito."
    return render_template('/proveedores/proveedorMensaje.html', mensaje=mensaje)


# Ruta para ver"Editar Proveedores"
@proveedores_bp.route('/Ver/EditarProveedor', methods=['GET'])
def VerEditarProveedor():
    return render_template('/proveedores/proveedorEditar.html')


# Ruta para "Editar Proveedores"
@proveedores_bp.route('/EditarProveedor', methods=['POST'])
def editar_proveedor():
    # Obtener los datos enviados en la solicitud POST
    RIFB = request.form['RIF']

    # Obtener datos de la hoja de cálculo
    sheet_id = config.get('GOOGLE_SPREADSHEET_ID')
    range_name = config.get('GOOGLE_CELL_RANGE')
    result = service.spreadsheets().values().get(
    spreadsheetId=sheet_id, range=range_name).execute()
    rows = result.get('values', [])
    
    # Compara los datos de la primera fila con los datos solicitados a través del formulario
    for i in range(len(rows)):
        for x in range(len(rows[i])):
            if rows[i][x] == RIFB:
                CONSULTA = rows[i]
                return render_template('/proveedores/proveedorEditarOK.html', CONSULTA=CONSULTA, RIFB=RIFB)
            
    # Si no encuentra, muestra mensaje de error
    mensaje = "Proveedor no encontrado."
    return render_template('/proveedores/proveedorMensaje.html', mensaje=mensaje)


# Ruta para "Editar ProveedoresOK"
@proveedores_bp.route('/EditarProveedorOK', methods=['POST'])
def editar_proveedorOK():
    # Obtener los datos enviados en la solicitud POST
    RAZON_SOCIAL = request.form['RAZON_SOCIAL']
    RIF = request.form['RIF']
    DIRECCION = request.form['DIRECCION']
    TELEFONO = request.form['TELEFONO']
    PORCENTAJE = request.form['PORCENTAJE']
    RIFB = request.form['RIFB']

    sheet_id = config.get('GOOGLE_SPREADSHEET_ID')
    range_name = 'A:A'
    result = service.spreadsheets().values().get(
    spreadsheetId=sheet_id, range=range_name).execute()
    rows = result.get('values', [])

    # Busca la coincidencia en la columna A
    search_value = RIFB
    cell_index = -1
    for i, row in enumerate(rows):
        if row and row[0] == search_value:
            cell_index = i
            break
    if cell_index >= 0:
        cell_letter = 'A'
        cell_range_letter = cell_letter + str(cell_index + 1)
    
    # Define los parámetros para editar una fila
    update_range = cell_range_letter
    update_body = {
        'range': update_range,
        'values': [[RIF, RAZON_SOCIAL, DIRECCION, TELEFONO, PORCENTAJE]],
        'majorDimension': 'ROWS'
    }
    # Define los parámetros para editar
    service.spreadsheets().values().update(
    spreadsheetId=config.get('GOOGLE_SPREADSHEET_ID'),
    range=update_range,
    valueInputOption='USER_ENTERED',
    body=update_body).execute()

    mensaje = "Proveedor editado con éxito."
    return render_template('/proveedores/proveedorMensaje.html',mensaje=mensaje)


# Ruta para ver "Eliminar Proveedores"
@proveedores_bp.route('/Ver/EliminarProveedor', methods=['GET'])
def VerEliminarProveedor():
    return render_template('/proveedores/proveedorEliminar.html')


# Ruta para "Eliminar Proveedores"
@proveedores_bp.route('/EliminarProveedor', methods=['POST'])
def eliminar_proveedor():
    # Obtener los datos enviados en la solicitud POST
    RIFB = request.form['RIF']
    
    # Obtener datos de la hoja de cálculo
    sheet_id = config.get('GOOGLE_SPREADSHEET_ID')
    range_name = config.get('GOOGLE_CELL_RANGE')
    result = service.spreadsheets().values().get(
    spreadsheetId=sheet_id, range=range_name).execute()
    rows = result.get('values', [])

    # Compara los datos de la primera fila con los datos solicitados a través del formulario
    for i in range(len(rows)):
        for x in range(len(rows[i])):
            if rows[i][x] == RIFB:
    
                # Busca la coincidencia en la columna A
                search_value = RIFB
                cell_index = -1
                for i, row in enumerate(rows):
                    if row and row[0] == search_value:
                        cell_index = i
                        break
                if cell_index >= 0:
                    cell_letter1 = 'A'
                    cell_letter2 = ':E'
                    cell_range_letter = cell_letter1 + str(cell_index + 1) + cell_letter2 + str(cell_index + 1)

                # Define el rango de filas que deseas eliminar
                range_name = cell_range_letter

                # Elimina los datos del rango de filas especificado
                clear_values_request_body = {}
                service.spreadsheets().values().clear(
                spreadsheetId=sheet_id, range=range_name, body=clear_values_request_body).execute()

                mensaje = "Proveedor eliminado con éxito."
                return render_template('/proveedores/proveedorMensaje.html', mensaje=mensaje)
    
    # Si no encuentra, muestra mensaje de error
    mensaje = "Proveedor no encontrado."
    return render_template('/proveedores/proveedorMensaje.html', mensaje=mensaje)

            

    
    