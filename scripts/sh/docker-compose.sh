#!/bin/bash

function yamlpath() {
    ENVIRONMENT=${1:-"develop"}
    INFRA_ROOT_PATH="infra/docker"
    COMPOSE_YAML_BASENAME="compose"

    case $ENVIRONMENT in
        dev|develop|development|desenvolvimento)
            echo "$INFRA_ROOT_PATH/$COMPOSE_YAML_BASENAME.yml" ;;
        prod|production)
            echo "$INFRA_ROOT_PATH/$COMPOSE_YAML_BASENAME.yml" ;;
        *) 
            echo "Ambiente desconhecido: $ENVIRONMENT" >&2
            exit 1 ;;
    esac 
}

$@
