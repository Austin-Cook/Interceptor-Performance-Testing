from flask import Flask, request

app = Flask(__name__)

out_file = None

@app.route('/report', methods=[ 'POST' ])
def report():
    body = request.json
    
    if 'identifier' not in body or 'time' not in body:
        return '', 400
    
    if 'sec' not in body['time'] or 'usec' not in body['time']:
        return '', 400

    if out_file:
        print(f'{body["identifier"]} {body["time"]["sec"]}:{body["time"]["usec"]}', file=out_file)

    return '', 200

if __name__ == '__main__':
    out_file = open('report_log.txt', 'w')
    app.run('127.0.0.1', 4560)
    out_file.close()