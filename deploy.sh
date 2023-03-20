rm -rf dist
rm -rf build
rm -rf *.egg-info
python setup.py sdist bdist_wheel
twine upload dist/*