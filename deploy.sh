rm -rf dist
rm -rf build
rm -rf *.egg-info
cp version.py cstl/
python setup.py sdist bdist_wheel
twine upload dist/*