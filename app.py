#!/usr/bin/env python3
"""
Simple Flask app for testing a Docker container.
"""

from flask import Flask, jsonify
import os
import platform
import datetime

app = Flask(__name__)


@app.route('/')
def home():
    """Home endpoint with container information."""
    return jsonify({
        'message': 'Application is running successfully in a Docker container!',
        'timestamp': datetime.datetime.now().isoformat(),
        'python_version': platform.python_version(),
        'platform': platform.platform(),
        'container_id': os.environ.get('HOSTNAME', 'unknown'),
        'environment': dict(os.environ)
    })


@app.route('/health')
def health():
    """Healthcheck endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.datetime.now().isoformat()
    })


@app.route('/info')
def info():
    """System information endpoint."""
    return jsonify({
        'python_version': platform.python_version(),
        'platform': platform.platform(),
        'architecture': platform.architecture(),
        'processor': platform.processor(),
        'hostname': os.environ.get('HOSTNAME', 'unknown'),
        'working_directory': os.getcwd(),
        'user': os.environ.get('USER', 'unknown')
    })


@app.route('/multiply/<int:a>/<int:b>')
def multiply(a, b):
    return jsonify({'result': a * b})


@app.route('/divide/<int:a>/<int:b>')
def divide(a, b):
    if b == 0:
        return jsonify({'error': 'Division by zero'}), 400
    return jsonify({'result': a / b})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
