# Discovery Config Validator

Web service for validating Bento discovery configuration files.


## Deploying

An all-in-one image with the server and client is available as 
[`ghcr.io/bento-platform/discovery_config_validator:edge`](https://ghcr.io/bento-platform/discovery_config_validator).

### Configuration

* To enable JSON logs (presumably for production), set the environment variable `USE_JSON_LOGS=True`.
* To prevent the server from trying to serve client files, set `SERVE_CLIENT=False`.
* To change where the server tries to serve client files from, set `CLIENT_PATH` to another path. 


## Developing

### Server

1. Install `uv` (see https://github.com/astral-sh/uv?tab=readme-ov-file#installation)
2. Clone the repository: `git clone git@github.com:bento-platform/discovery_config_validator.git`
3. Install dependencies: `uv install`
4. Run the server with auto-reloading: `uv run uvicorn run --reload dcv_server.main:app`. This will by default run the
   server and serve client files built using the instructions below.

### Client

1. Install NodeJS 22.x and NPM.
2. Go to the client directory: `cd dcv_client`
3. Install dependencies: `npm install`
4. Run the Webpack watch script to build the client and automatically rebuild it upon changes: `npm run watch`
