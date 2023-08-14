from flask import request, render_template, Blueprint
from static.src.googleAPI import service, config, access_token
import requests, json

proveedores_bp = Blueprint('/static/src/proveedores', __name__)

# Ruta para ver "Agregar proveedores"

@proveedores_bp.route('/Ver/AgregarProveedor', methods=['GET'])
def VerAgregarProveedor():
    return render_template('agregarProveedor.html')

# Ruta para "Agregar proveedores"
@proveedores_bp.route('/agregarProveedor', methods=['POST'])
def agregar_proveedor():
    # Obtén los datos enviados en la solicitud POST
    RAZON_SOCIAL = request.form['RAZON_SOCIAL']
    RIF = request.form['RIF']
    DIRECCION = request.form['DIRECCION']
    TELEFONO = request.form['TELEFONO']
    PORCENTAJE = request.form['PORCENTAJE']

    # Define los parámetros para agregar una nueva fila
    spreadsheet_id = config.get('GOOGLE_SPREADSHEET_ID')
    range_name = config.get('GOOGLE_CELL_RANGE')
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

    return render_template('proveedorExito.html')


# Ruta para "Ver Proveedores"
@proveedores_bp.route('/VerProveedor', methods=['GET'])
def ver_proveedor():
    # Obtener datos de la hoja de cálculo
    url = 'https://sheets.googleapis.com/v4/spreadsheets/160T7u6nxNElz5BX6oCbqNX_aRDR8WrEh2bOYAQCFNdQ/values/Proveedores'
    headers = {'Authorization': 'Bearer ' + access_token}
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)['values']

    return render_template('proveedorVer.html', data=data)

# Ruta para "Editar Proveedores"