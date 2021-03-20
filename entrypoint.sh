#!/bin/bash

set -x

cd "$GITHUB_WORKSPACE"

ls

if [ -z "$GITHUB_ACTOR" ]; then
    echo "GITHUB_ACTOR environment variable is not set"
    exit 1
fi

if [ -z "$GITHUB_REPOSITORY" ]; then
    echo "GITHUB_REPOSITORY environment variable is not set"
    exit 1
fi

if [ -z "${INPUT_GITHUB_PERSONAL_TOKEN}" ]; then
    echo "github-personal-token environment variable is not set"
    exit 1
fi

if [ -z "${INPUT_DOCKER_USERNAME}" ]; then
    echo "Docker username is missing!"
    exit 1
fi

if [ -z "${INPUT_DOCKER_PASSWORD}" ]; then
    echo "Docker password is missing!"
    exit 1
fi

if [ -z "${INPUT_COMMIT_MESSAGE:-}" ]; then
    echo "INPUT_COMMIT_MESSAGE not set, using default"
    INPUT_COMMIT_MESSAGE='Push build time graph'
fi

GIT_REPOSITORY_URL="https://${INPUT_GITHUB_PERSONAL_TOKEN}@github.com/$GITHUB_REPOSITORY.wiki.git"

docker build -t ${INPUT_DOCKER_REPOSITORY}:latest . | tee output.txt

containerId=$(docker create ${INPUT_DOCKER_REPOSITORY}:latest)
docker cp "$containerId":/time.txt .
docker rm "$containerId"

echo "${INPUT_DOCKER_PASSWORD}" | docker login -u ${INPUT_DOCKER_USERNAME} --password-stdin docker.io

#docker push ${INPUT_DOCKER_REPOSITORY}:latest

tmp_dir=$(mktemp -d -t ci-XXXXXXXXXX)
(
    cd "$tmp_dir" || exit 1
    git init
    git config user.name "$GITHUB_ACTOR"
    git config user.email "$GITHUB_ACTOR@users.noreply.github.com"
    git pull "$GIT_REPOSITORY_URL"

    cat "$GITHUB_WORKSPACE"/time.txt
    cat "$GITHUB_WORKSPACE"output.txt

    # Generate graph
    # python3 /generate_graph.py -i $tmp_dir/"${INPUT_FILENAME}" -o $tmp_dir/"${INPUT_FILENAME}"

    # git add .
    # git commit -m "$INPUT_COMMIT_MESSAGE"
    # git push --set-upstream "$GIT_REPOSITORY_URL" master
) || exit 1

rm -rf "$tmp_dir"
