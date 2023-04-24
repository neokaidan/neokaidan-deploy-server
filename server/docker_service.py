import docker

import config as cfg
import logger as log
from logging import Logger


class DockerService:
    def __init__(self, config: cfg.Configuration, logger: Logger):
        self.config = config
        self.log = logger
        self.client = docker.DockerClient(base_url=self.config.docker_socket)

    def get_active_containers(self):
        containers = self.client.containers.list()
        result = []

        for container in containers:
            result.append({
                "short_id": container.short_id,
                "container_name": container.name,
                "image_name": container.image.tags,
                "created": container.attrs["Created"],
                "status": container.status,
                "ports": container.ports,
            })

        return result

    @staticmethod
    def get_container_name(item: dict) -> [str, str]:
        if not isinstance(item, dict):
            return ""

        owner = item.get("owner")
        repository = item.get("repository")
        tag = item.get("tag", "latest").replace("v", "")

        if owner and repository and tag:
            return f"{owner}/{repository}:{tag}", repository

        if repository and tag:
            return f"{repository}:{tag}", repository

        return "", ""

    def kill_old_container(self, container_name: str) -> bool:
        try:
            container = self.client.containers.get(container_name)
            container.kill()
        except Exception as e:
            self.log.warning(f"Error while delete container {container_name}, {e}")
            return False
        finally:
            # Удаление остановленых контейнеров, чтобы избежать конфликта имен
            self.log.debug(self.client.containers.prune())

        self.log.info(f"Container deleted. container_name = {container_name}")

        return True

    def deploy_new_container(self, image_name: str, container_name: str, ports: dict = None):
        try:
            # Пул последнего image из docker hub"a
            self.log.info(f"pull {image_name}, name={container_name}")
            self.client.images.pull(image_name)
            self.log.debug("Success")
            self.kill_old_container(container_name)
            self.log.debug("Old killed")
            # Запуск нового контейнера
            self.client.containers.run(image=image_name, name=container_name, detach=True, ports=ports)

        except Exception as e:
            self.log.error(f"Error while deploy container {container_name}, \n{e}")
            return False, str(e)

        self.log.info(f"Container deployed. container_name = {container_name}")

        return True, ""
