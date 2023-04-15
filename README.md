# Deployment server for Neokaidan web site

### scripts
- `pip install -r requirements.txt` — install Python packages for development
- `pip install .` — install daemon server
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
