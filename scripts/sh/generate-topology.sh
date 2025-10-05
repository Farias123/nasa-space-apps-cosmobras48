#!/bin/bash

function topology() {
    DOCKER_COMPOSE_DIAGRAM_LOCATION="resources/docs/images"

    echo "Generating topology diagram..."

    OUTPUT_FILE="docker-topology.png"
    DOCKER_COMPOSE_FILE_PATH="infra/docker/compose.yml"

    chmod 777 "./$DOCKER_COMPOSE_DIAGRAM_LOCATION"

    echo "Docker Compose YAML to be used:   $DOCKER_COMPOSE_FILE_PATH"
    echo "Topology diagram PNG saved in:    $DOCKER_COMPOSE_DIAGRAM_LOCATION/$OUTPUT_FILE"

    docker run \
		--rm \
		-it \
		--name dcv \
        -v "$(pwd):/input:rw" \
        -v "$(pwd)/$DOCKER_COMPOSE_DIAGRAM_LOCATION:/output:rw" \
		pmsipilot/docker-compose-viz \
		render \
			-m \
			image \
			--force \
            --horizontal \
			--output-file /output/$OUTPUT_FILE \
            $DOCKER_COMPOSE_FILE_PATH
}

$@
