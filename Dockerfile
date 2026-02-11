FROM python:3.13-trixie AS server-build

RUN pip install uv

WORKDIR /app

COPY pyproject.toml .
COPY uv.lock .
COPY README.md .
COPY LICENSE .
COPY dcv_server dcv_server

RUN uv sync --frozen

FROM node:24-bookworm AS client-build

WORKDIR /app/dcv_client
COPY dcv_client/src src
COPY dcv_client/package.json .
COPY dcv_client/package-lock.json .
COPY dcv_client/tsconfig.json .
COPY dcv_client/webpack.config.js .

RUN npm ci && npm run build

FROM server-build

# Only keep build artifacts from client rather than whole node_modules+src directories:
COPY --from=client-build /app/dcv_client/dist /app/dcv_client/dist

ENV SERVE_CLIENT=True
ENV CLIENT_PATH=/app/dcv_client/dist

CMD ["uv", "run", "uvicorn", "dcv_server.main:app", "--host", "0.0.0.0", "--port", "8000"]
