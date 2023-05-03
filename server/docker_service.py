import docker
from docker.errors import DockerException

from .config import Configuration
from logging import Logger


class DockerService:
    def __init__(self, config: Configuration, logger: Logger):
        self.config = config
        self.log = logger
        try:
            self.client = docker.DockerClient(base_url=self.config.docker_socket)
        except DockerException as e:
            err_msg = str(e)
            if err_msg.find("PermissionError") >= 0:
                raise PermissionError(f"Socket '{self.config.docker_socket}' requires sudo rights. Run the server with sudo rights, or change socket permission")
            elif err_msg.find("FileNotFoundError") >= 0:
                raise FileExistsError(f"Socket '{self.config.docker_socket}' not found. Updated env file or socket")
            else:
                raise e

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

        registry = item.get("registry")
        repository = item.get("repository")
        tag = item.get("tag", "latest")

        if registry and repository and tag:
            return f"{registry}/{repository}:{tag}", repository

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
