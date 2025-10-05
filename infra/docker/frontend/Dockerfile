FROM node:22.15.1-alpine

ENV WORKDIR=/home/cosmobras48/frontend

# Installing image dependencies
RUN apk update && apk add --no-cache \
    libc6-compat

# Enabling and preparing pnpm. This method avoids needing to install pnpm via npm
RUN corepack enable \
    && corepack prepare pnpm@latest --activate

WORKDIR ${WORKDIR}

# Copying deps list and lock file
COPY ./frontend/package.json ./package.json
COPY ./frontend/pnpm-lock.yaml ./pnpm-lock.yaml

# Installing packages and caching the result
RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --frozen-lockfile
 
COPY ./frontend/src ./src
COPY ./frontend/public ./public
COPY ./frontend/tsconfig.json ./tsconfig.json

EXPOSE 3000
 
ENTRYPOINT ["pnpm"]
