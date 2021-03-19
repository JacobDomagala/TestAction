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

if [ -z "${INPUT_COMMIT_MESSAGE:-}" ]; then
    echo "INPUT_COMMIT_MESSAGE not set, using default"
    INPUT_COMMIT_MESSAGE='Push build time graph'
fi

GIT_REPOSITORY_URL="https://${INPUT_GITHUB_PERSONAL_TOKEN}@github.com/$GITHUB_REPOSITORY.wiki.git"

docker build -t test_name:latest .

containerId=$(docker create test_name:latest)
docker cp "$containerId":/script.sh .
docker rm "$containerId"


# tmp_dir=$(mktemp -d -t ci-XXXXXXXXXX)
# (
#     cd "$tmp_dir" || exit 1
#     git init
#     git config user.name "$GITHUB_ACTOR"
#     git config user.email "$GITHUB_ACTOR@users.noreply.github.com"
#     git pull "$GIT_REPOSITORY_URL"

#     # Generate graph
#     python3 /generate_graph.py -o $tmp_dir/"${INPUT_FILENAME}"

#     git add .
#     git commit -m "$INPUT_COMMIT_MESSAGE"
#     git push --set-upstream "$GIT_REPOSITORY_URL" master
# ) || exit 1
# rm -rf "$tmp_dir"

cat script.sh
echo 10 20 > temp.txt
