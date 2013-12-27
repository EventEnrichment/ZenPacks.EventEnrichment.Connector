rm `find . -name "*~"`
rm -rf build dist ZenPacks.EE.Connector.egg-info
python setup.py bdist_egg
