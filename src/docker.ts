import Docker, {ContainerInfo, Port} from "dockerode";
import {DockerContainerInfo, DockerContainerPortInfo, SysError} from "./dockerTypes";
import fs from "fs";

const dockerSocket = process.env.DOCKER_SOCKET || '/var/run/docker.sock';

if (!fs.statSync(dockerSocket).isSocket()) {
    throw new Error("Are you sure the docker is running?");
}

const localDocker = new Docker({ socketPath: dockerSocket });

export const getActiveContainers = (): Promise<Array<DockerContainerInfo>> => {
    return new Promise((resolve, reject) => {
        const listOptions = {
            all: true
        }

        try {
            localDocker.listContainers(listOptions, function (err: any, containers?: Array<ContainerInfo>) {
                if (err != null) {
                    const errorObj: SysError = {
                        errno: err.errno,
                        message: err.message,
                        stacktrace: err.stack
                    }

                    reject(errorObj);
                }

                const parsedContainersInfo = (containers as Array<ContainerInfo>)
                    .map((item: ContainerInfo): DockerContainerInfo => {
                        return {
                            shortId: item.Id,
                            containerName: item.Names[0],
                            image: item.Image,
                            created: item.Created,
                            containerStatus: item.Status,
                            ports: item.Ports.map((libPort: Port): DockerContainerPortInfo => {
                                return {
                                    ip: libPort.IP,
                                    publicPort: libPort.PublicPort,
                                    privatePort: libPort.PrivatePort,
                                    portType: libPort.Type
                                };
                            })
                        };
                    });

                resolve(parsedContainersInfo);
            });
        } catch (err) {
            reject(err);
        }
    });
}

// export const killOldContainer = (containerName: string): boolean => {
//
//
//     return true;
// }
//
// export const deployNewContainer = ()