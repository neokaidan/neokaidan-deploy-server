# Deployment server for Neokaidan web site

### stack
- Node.JS 16+
- TypeScript 5+
- Express 4+

### scripts
- `npm run build` — compile typescript to `dist/` directory
- `npm start` — compile server and start on `localhost:${PORT}` where PORT declares in ENV

### configuration
`.env` file for setting ENV variables:
- PORT — TCP port for server
- GITHUB_SECRET — secret generated with `openssl rand -hex 20` and stored in GitHub secrets

### API
```json
{
  "owner": "логин докер аккаунта",
  "repository": "имя докер репозитория",
  "tag": "v0.0.1",  //тэг который надо задеплоить
  "ports": {"8080": 8080, “443”: 443} // мапинг портов между хостом и контейнером
}
```
