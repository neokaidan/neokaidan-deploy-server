import Docker, { ContainerInfo } from "dockerode";
import fs from "fs";

const dockerSocket = process.env.DOCKER_SOCKET || '/var/run/docker.sock';

if (!fs.statSync(dockerSocket).isSocket()) {
    throw new Error("Are you sure the docker is running?");
}

const localDocker = new Docker({ socketPath: dockerSocket });

export const getActiveContainers = (): Promise<Array<ContainerInfo>> => {
    return new Promise((resolve, reject) => {
        const listOptions = {
            all: true
        }

        localDocker.listContainers(listOptions, function(err: any, containers?: Array<ContainerInfo>) {
            if (err != null) {
                reject(err);
            }

            resolve(containers as Array<ContainerInfo>);
        });
    });
}
