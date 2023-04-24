# Deployment server for Neokaidan web site

### scripts
- `./install.sh` — install 'gacd_server' as daemon
- `./uninstall.sh` — uninstall daemon and symlink
- `pip install -r requirements.txt` — install Python packages for development
- `pip install .` — install 'gacd_server' server with symlink

### configuration
`.env` file for setting ENV variables:
- PORT — TCP port for server
- GITHUB_SECRET — secret generated with `openssl rand -hex 20` and stored in GitHub secrets

### API
```json
{
  "owner": "Registry Login",
  "repository": "Docker repository",
  "tag": "v0.0.1",
  "ports": {"8080": 8080, “443”: 443}
}
```

- `tag` — git tag to deploy
- `ports` — port mappings between docker container and server
