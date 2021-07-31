#!/bin/bash
# =========================================
# Convenience script for cutting releases:
#   * Commit, tag, and push version change
#   * Deploy to PyPi
# =========================================
if [[ $# -eq 0 ]] ; then
    echo 'Usage: ./release.bash <version> (e.g. 0.2.0)'
    exit 1
fi

version=$1
echo "Modifying version in fcxref/_version.py to $version"
sed -E -i "s/'(.*)'/'$version'/g" ./fcxref/_version.py

set -x
git add .
git commit -m "v$version"
git tag "v$version"
git push
git push --tags
set +x

rm -rf dist/
python setup.py sdist

# https://github.com/plyint/encpass.sh
. encpass.sh

export TWINE_PASSWORD=$(get_secret pypi password)

# exit when any command fails
set -e

# print commands before executing
set -x
twine upload --username gbroques dist/*
