rm -f `find . -name "*~"`
rm -rf build dist ZenPacks.EventEnrichment.Connector.egg-info
python setup.py bdist_egg
