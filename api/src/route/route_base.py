from flask import jsonify


def success_status():
    return jsonify({"status": 'success'})