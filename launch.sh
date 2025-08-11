#!/usr/bin/env bash

if [[ "$1" == "" ]] ; then echo "Multi-user mode enabled." ; else cd "$1" ; fi

echo "Launch Dockerized UC-PACT Tool"
echo "Available profiles: default, dev, tests, pytest, integration-tests"
echo -n "Select a profile: "

read -r profile

if [[ "$profile" == "tests" || "$profile" == "pytest" ]] ; then
    echo -n "Filename (*.txt) for exporting stdout/stderr (leave blank to disable): "
    read -r logfile
    (cd logfiles && touch "$logfile") || (docker compose --profile $profile build && docker compose --profile $profile up)
    (cd logfiles && touch "$logfile") && \
        docker compose --profile "$profile" build && \
        docker compose --profile "$profile" up &> "./logfiles/$logfile" && \
        echo "Open ./logfiles/$logfile for shell output."
    echo "Bringing $profile profile down..."
    docker compose --profile "$profile" down
else
    docker compose --profile "$profile" build && docker compose --profile "$profile" up
    echo "Bringing $profile profile down..."
    docker compose --profile "$profile" down
fi
