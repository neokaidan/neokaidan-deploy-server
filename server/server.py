import os
import sys

from flask import Flask, g
from flask import request, jsonify

from .config import Configuration
from .logger import get_logger
from .docker_service import DockerService
from .__version__ import __version__


app: Flask = Flask("gacd_server")
configuration = Configuration()
logger = get_logger(configuration)
docker_service = DockerService(configuration, logger)


def need_auth_token(func):
    def wrapper_func(*args, **kwargs):
        if request.headers.get("Authorization") != configuration.auth_secret:
            return jsonify({"message": "Bad token"}), 401
        return func(*args, **kwargs)
    return wrapper_func


@app.route("/", methods=["GET"])
def index():
    return "Neokaidan deployment server. Version: %s" % __version__, 200


# Получение списка всех активных контейнеров
@app.route("/get_active", methods=["GET"])
@need_auth_token
def get_active():
    return jsonify(docker_service.get_active_containers()), 200


# Деплой сборки контейнера
# Пример тела запроса:
# {
#   "owner": "gonfff",
#   "repository": "ci_example",
#   "tag": "v0.0.1",
#   "ports": {"8080": 8080}
# }

@need_auth_token
@app.route("/deploy", methods=["POST"])
def deploy():
    logger.debug(f"Received {request.data}")
    image_name, container_name = docker_service.get_container_name(request.json)
    ports = request.json.get("ports") if request.json.get("ports") else None
    status, errmsg = docker_service.deploy_new_container(image_name, container_name, ports)

    if status:
        return jsonify({
            "status": status
        }), 200
    else:
        return jsonify({
            "status": status,
            "error": errmsg
        }), 400


def start_server():
    app.run(host="0.0.0.0", port=configuration.server_port)


if __name__ == "__main__":
    start_server()
