from flask import Flask, request
from escpos.printer import Usb

app = Flask(__name__)

@app.route('/print', methods=['POST'])
def print_text():
    data = request.json
    text = data.get("text", "")

    printer = Usb(0x0416, 0x5011)  # Modelə görə dəyiş
    printer.text(text)
    printer.cut()
    return "OK", 200

app.run(host='0.0.0.0', port=5000)
