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

if [ -z "$GH_PERSONAL_ACCESS_TOKEN" ]; then
    error "GH_PERSONAL_ACCESS_TOKEN environment variable is not set"
    exit 1
fi

echo "Add mask"
add_mask "${GH_PERSONAL_ACCESS_TOKEN}"

if [ -z "${WIKI_COMMIT_MESSAGE:-}" ]; then
    debug "WIKI_COMMIT_MESSAGE not set, using default"
    WIKI_COMMIT_MESSAGE='Automatically publish wiki'
fi

echo "Gitt repo"
GIT_REPOSITORY_URL="https://${GH_PERSONAL_ACCESS_TOKEN}@github.com/$GITHUB_REPOSITORY.wiki.git"

debug "Checking out wiki repository"
tmp_dir=$(mktemp -d -t ci-XXXXXXXXXX)
(
    echo "First dir = $tmp_dir"
    cd "$tmp_dir" || exit 1
    git init
    git config user.name "$GITHUB_ACTOR"
    git config user.email "$GITHUB_ACTOR@users.noreply.github.com"
    git pull "$GIT_REPOSITORY_URL"
) || exit 1


debug "Committing and pushing changes"
(
    echo "Second dir = $tmp_dir"
    cd "$tmp_dir" || exit 1
    echo 'This is a test\
    ![image_description](graph.jpg)' > BuildStatistics.md

    git add .
    git commit -m "$WIKI_COMMIT_MESSAGE"
    git push --set-upstream "$GIT_REPOSITORY_URL" master
) || exit 1

echo "Rm = $tmp_dir"
rm -rf "$tmp_dir"

echo "Inside entrypoint"
exit 0
