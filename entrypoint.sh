#!/bin/bash

set -euo pipefail

function debug() {
    echo "::debug file=${BASH_SOURCE[0]},line=${BASH_LINENO[0]}::$1"
}

function warning() {
    echo "::warning file=${BASH_SOURCE[0]},line=${BASH_LINENO[0]}::$1"
}

function error() {
    echo "::error file=${BASH_SOURCE[0]},line=${BASH_LINENO[0]}::$1"
}

function add_mask() {
    echo "::add-mask::$1"
}

if [ -z "$GITHUB_ACTOR" ]; then
    error "GITHUB_ACTOR environment variable is not set"
    exit 1
fi

if [ -z "$GITHUB_REPOSITORY" ]; then
    error "GITHUB_REPOSITORY environment variable is not set"
    exit 1
fi

if [ -z "${INPUT_GITHUB-PERSONAL-TOKEN}" ]; then
    error "github-personal-token environment variable is not set"
    exit 1
fi

add_mask "${INPUT_GITHUB-PERSONAL-TOKEN}"

if [ -z "${WIKI_COMMIT_MESSAGE:-}" ]; then
    debug "WIKI_COMMIT_MESSAGE not set, using default"
    WIKI_COMMIT_MESSAGE='Push build time graph'
fi

GIT_REPOSITORY_URL="https://${INPUT_GITHUB-PERSONAL-TOKEN}@github.com/$GITHUB_REPOSITORY.wiki.git"

debug "Checking out wiki repository"
tmp_dir=$(mktemp -d -t ci-XXXXXXXXXX)
(
    cd "$tmp_dir" || exit 1
    git init
    git config user.name "$GITHUB_ACTOR"
    git config user.email "$GITHUB_ACTOR@users.noreply.github.com"
    git pull "$GIT_REPOSITORY_URL"
) || exit 1

# Generate graph
python3 /generate_graph.py -o $tmp_dir/graph.jpg

debug "Committing and pushing changes"
(
    cd "$tmp_dir" || exit 1

    git add .
    git commit -m "$WIKI_COMMIT_MESSAGE"
    git push --set-upstream "$GIT_REPOSITORY_URL" master
) || exit 1

rm -rf "$tmp_dir"

exit 0
