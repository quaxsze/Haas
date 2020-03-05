import os

from celery.result import AsyncResult
from werkzeug.utils import secure_filename
from flask import render_template, flash, redirect, url_for, request, current_app, jsonify

from app import app
from app.hash_utils import validate_hash, gen_wordlist
from app.tasks import compute_hash, brute_force, dict_attack


@app.route('/hash', methods=['POST'])
def calculate_hash():
    data = request.get_json() or {}
    data_to_hash = data.get("to_hash")
    algorithm = data.get("algorithm")

    if algorithm not in ['md5', 'sha1', 'sha256']:
        resp = jsonify({'message' : 'unsupported algorithm'})
        resp.status_code = 400
        return resp

    if data_to_hash:
        task = compute_hash.delay(data_to_hash, algorithm)
    else:
        resp = jsonify({'message' : 'Malformed request'})
        resp.status_code = 400
        return resp

    resp = jsonify({'task_id' : task.id})
    resp.status_code = 200
    return resp


@app.route('/brute_force_hash', methods=['POST'])
def brute_force_hash():
    data = request.get_json() or {}
    hash_to_crack = data.get("to_hash")
    hash_type = validate_hash(hash_to_crack)
    if not hash_type :
        resp = jsonify({'message' : 'Invalid hash'})
        resp.status_code = 400
        return resp
    else:
        task = brute_force.delay(hash_to_crack, hash_type)
        resp = jsonify({'task_id' : task.id})
        resp.status_code = 200
        return resp


@app.route('/dict_attack_hash', methods=['POST'])
def dict_attack_hash():
    data = request.get_json() or {}
    hash_to_crack = data.get("to_hash")
    hash_type = validate_hash(hash_to_crack)
    if not hash_type :
        resp = jsonify({'message' : 'Invalid hash'})
        resp.status_code = 400
        return resp
    else:
        try:
            wordlist = gen_wordlist()
        except FileNotFoundError:
            resp = jsonify({'message' : 'Wordlist file not found'})
            resp.status_code = 500
            return resp
        task = dict_attack.delay(hash_to_crack, hash_type, wordlist)
        resp = jsonify({'task_id' : task.id})
        resp.status_code = 200
        return resp


@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = AsyncResult(task_id)
    response = {
        'state': task.state
        }

    if task.state == 'FAILURE':
        response['result'] = str(task.result)
    if task.state == 'SUCCES':
        response['result'] = task.result

    resp = jsonify(response)
    resp.status_code = 200
    return resp