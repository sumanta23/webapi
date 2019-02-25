from flask import Flask, abort, request, jsonify, render_template 
import json
from cors import crossdomain
import uuid
app = Flask(__name__, template_folder='.')

from slurmpy import Slurm

origins = "192.168.33.3:8081, 192.168.33.33:8888"


@app.route('/')
def main_handler():
   return render_template('index.html')

@app.route('/submitjob', methods=["POST"])
@crossdomain(origin=origins, methods=['POST'],
             headers=['Accept', 'Content-Type', 'X-Requested-With'])
def submitJob():
    if not request.json:
        abort(400)
    body = request.json
    code = body["code"]
    body.pop('code', None)  # remove key
    account = body["account"]
    if not account:
        abort(400)
    kargs= {"partition" : "debug"}
    for key, value in body.items():
        kargs[key] = value

    print(kargs)
    s = Slurm(str(uuid.uuid4()), kargs)
    code = "MYDATA=/data"+account+"\n"+code
    x = s.run(code);
    print("result",x)
    return jsonify(x)

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8888, debug=False)







