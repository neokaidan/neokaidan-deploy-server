import os
import sys

from flask import Flask, g
from flask import request, jsonify

import config as cfg
import logger as log
import docker_service as ds
import __version__


app = Flask(__name__)


def need_auth_token(func):
    def wrapper_func(*args, **kwargs):
        if request.headers.get("Authorization") != g.config.auth_secret:
            return jsonify({"message": "Bad token"}), 401
        return func(*args, **kwargs)
    return wrapper_func


@app.route("/", methods=["GET"])
def index():
    return "Neokaidan deployment server. Version: %s" % __version__, 200


# Получение списка всех активных контейнеров
@need_auth_token
@app.route("/get_active", methods=["GET"])
def get_active():
    return jsonify(g.docker_service.get_active_containers()), 200


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
def get_active():
    g.log.debug(f"Received {request.data}")
    image_name, container_name = g.docker_service.get_container_name(request.json)
    ports = request.json.get("ports") if request.json.get("ports") else None
    status, errmsg = g.docker_service.deploy_new_container(image_name, container_name, ports)

    if status:
        return jsonify({
            "status": status
        }), 200
    else:
        return jsonify({
            "status": status,
            "error": errmsg
        }), 400


def main():
    configuration = cfg.Configuration()
    logger = log.get_logger()

    g.config = configuration
    g.log = logger
    g.docker_service = ds.DockerService(configuration, logger)
    app.run(host="0.0.0.0", port=configuration.PORT_ENV)


if __name__ == "__main__":
    main()
