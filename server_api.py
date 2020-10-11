from flask import Flask, request, Response, render_template
from flask import send_file
from maya_widget import get_data
import pathlib
import io


app = Flask(__name__)
current_path = pathlib.Path().absolute()


@app.route('/api/post', methods=['POST'])
def post_api():
    data = request.json
    user_weight = int(data.get('weight', None))
    if 'weight' in data.keys():
        if 49 < user_weight < 148:
            weight_scale = (user_weight / 48)
        elif 48 > user_weight > 16:
            weight_scale = (user_weight / 48)
        elif user_weight == 48:
            pass
        elif user_weight > 148:
            weight_scale = 3
        elif user_weight < 14:
            weight_scale = -3
        else:
            return None
        if weight_scale:
            get_data('weight', weight_scale)
        maya_location = f'{current_path}/result.obj'
    with open(maya_location, 'rb') as bites:
        return send_file(
                     io.BytesIO(bites.read()),
                     attachment_filename='result.obj')


app.run(host="0.0.0.0", port=5000)
