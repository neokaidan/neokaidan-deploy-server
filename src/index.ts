import express, { Express, Request, Response } from "express";
import dotenv from "dotenv";

import { ContainerInfo } from "dockerode";

import { getActiveContainers } from "./docker";

dotenv.config();

const app: Express = express();
const port = process.env.PORT;

if (port == null) {
    throw new Error("PORT is undefined. Check the .env file")
}

app.get("/", (req: Request, res: Response) => {
    res.send("Neokaidan deployment server");
});

app.get("/containers", async (req: Request, res: Response) => {
    const containersList = await getActiveContainers();

    console.log('ALL: ' + containersList.length);
    res.send(containersList.length.toString());
});

app.listen(port, () => {
    console.log(`Deployment server is running at http://localhost:${port}`);
});
