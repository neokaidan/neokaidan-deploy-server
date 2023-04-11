export type SysError = {
    errno: string,
    message: string,
    stacktrace: string
}

export type DockerContainerInfo = {
    shortId: string,
    containerName: string,
    image: string,
    created: number,
    containerStatus: string,
    ports: Array<DockerContainerPortInfo>
}

export type DockerContainerPortInfo = {
    ip: string;
    privatePort: number;
    publicPort: number;
    portType: string;
}
