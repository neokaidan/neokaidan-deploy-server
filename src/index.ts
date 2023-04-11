import express, { Express, Request, Response } from "express";
import dotenv from "dotenv";
import { getActiveContainers } from "./docker";

const AUTHORIZATION_HEADER = "Authorization";

dotenv.config();


const app: Express = express();
const port = process.env.PORT;
const githubSecret = process.env.GITHUB_SECRET;

if (port == null) {
    throw new Error("PORT is undefined. Check the .env file")
}

// JSON middleware
app.use(express.json());

app.get("/", (req: Request, res: Response) => {
    res.send("Neokaidan deployment server");
});

app.get("/containers", async (req: Request, res: Response) => {
    const containersList = await getActiveContainers();

    console.log('ALL: ' + containersList.length);
    res.send(containersList.length.toString());
});

app.post("deploy", async (req: Request, res: Response) => {
    const token = req.header(AUTHORIZATION_HEADER);

    if (token != githubSecret) {
        console.error("Invalid GitHub Secret");
        res.status(401).send("Invalid GitHub Secret");
        return;
    }

    console.log("Received data: ", req.body)
});

app.listen(port, () => {
    console.log(`Deployment server is running at http://localhost:${port}`);
});
