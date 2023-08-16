from flask import request, render_template, Blueprint
from static.src.googleAPI import service, config, access_token
import requests, json

compras_bp = Blueprint('/static/src/compras', __name__)

# Ruta para "Ver Compras"
@compras_bp.route('/Ver/VerCompras', methods=['GET'])
def Ver_Compras():
    # Obtener datos de la hoja de cálculo
    url = 'https://sheets.googleapis.com/v4/spreadsheets/160T7u6nxNElz5BX6oCbqNX_aRDR8WrEh2bOYAQCFNdQ/values/Compras'
    headers = {'Authorization': 'Bearer ' + access_token}
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)['values']
    return render_template('/compras/comprasVer.html', data=data)
