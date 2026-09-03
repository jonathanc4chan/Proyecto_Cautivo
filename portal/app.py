from flask import Flask, render_template, request, redirect, url_for
from pyrad.client import Client
from pyrad.dictionary import Dictionary
import pyrad.packet
import traceback

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return redirect(url_for('index'))
    
    try:
        srv = Client(server="127.0.0.1", secret=b"testing123", dict=Dictionary("radius_dict_minimo.conf"))
        srv.timeout = 5
        
        req = srv.CreateAuthPacket(code=pyrad.packet.AccessRequest)
        req["User-Name"] = username
        req["User-Password"] = req.PwCrypt(password)
        
        reply = srv.SendPacket(req)
        
        if reply.code == pyrad.packet.AccessAccept:
            reply_msg = reply.get("Reply-Message", ["Bienvenido"])[0]
            if isinstance(reply_msg, bytes):
                reply_msg = reply_msg.decode('utf-8')
            return f"¡Autenticación exitosa! {reply_msg}. Ya tienes acceso a la red."
        else:
            return "Credenciales incorrectas. Acceso denegado.", 401

    except Exception as e:
        print("--- ERROR EXCEPCIÓN RADIUS ---")
        traceback.print_exc()
        return f"Error interno: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
EOF
