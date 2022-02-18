#!/bin/bash
echo "Holy guacamole"
echo
echo "Removing cached files."
find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf

echo
echo "Removing pytest files"
rm -rf htmlcov .pytest_cache coverage.xml

echo
echo "Removing cover files"
find . | grep -E "(\.py,cover$)" | xargs rm -rf