from flask import Flask, request, render_template, redirect
from pyrad.client import Client
from pyrad.dictionary import Dictionary
import os, subprocess, uuid

app = Flask(__name__)
DICT_PATH = "/home/jonathan/portal-cautivo/portal/dict/dictionary"
RADIUS_SECRET = os.environ.get("RADIUS_SECRET", "naruto2026").encode('utf-8')

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def login(path):
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        client_ip = request.remote_addr

        try:
            srv = Client(server="127.0.0.1", secret=RADIUS_SECRET, dict=Dictionary(DICT_PATH))
            req = srv.CreateAuthPacket(code=1, User_Name=username)
            req["User-Password"] = req.PwCrypt(password)
            reply = srv.SendPacket(req)
            
            if reply.code == 2:  # Access-Accept
                role = reply.get("Reply-Message", ["invitado"])[0]
                timeout = reply.get("Session-Timeout", [1800])[0]
                
                try:
                    acct_req = srv.CreateAcctPacket(User_Name=username)
                    acct_req["Acct-Status-Type"] = "Start"
                    acct_req["Acct-Session-Id"] = str(uuid.uuid4())
                    acct_req["Framed-IP-Address"] = client_ip
                    srv.SendPacket(acct_req)
                except Exception as acct_e:
                    print(f"Error en Accounting Start: {acct_e}")

                subprocess.run(["sudo", "nft", "add", "element", "ip", "portal_nat", "allowed_ip", f"{{ {client_ip} timeout {timeout}s }}"], check=True)
                return render_template(f'landing_{role}.html', username=username, timeout=timeout)
            else:
                error = "Credenciales incorrectas."
        except Exception as e:
            error = f"Error conectando con RADIUS: {e}"
            
    return render_template('login.html', error=error)

@app.route('/logout', methods=['POST'])
def logout():
    username = request.form.get('username')
    client_ip = request.remote_addr
    try:
        srv = Client(server="127.0.0.1", secret=RADIUS_SECRET, dict=Dictionary(DICT_PATH))
        acct_req = srv.CreateAcctPacket(User_Name=username)
        acct_req["Acct-Status-Type"] = "Stop"
        acct_req["Acct-Session-Id"] = str(uuid.uuid4())
        acct_req["Framed-IP-Address"] = client_ip
        srv.SendPacket(acct_req)
        
        subprocess.run(["sudo", "nft", "delete", "element", "ip", "portal_nat", "allowed_ip", f"{{ {client_ip} }}"], check=True)
    except Exception as e:
        print(f"Error en Accounting-Stop: {e}")
        
    return redirect("http://10.10.0.1")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
