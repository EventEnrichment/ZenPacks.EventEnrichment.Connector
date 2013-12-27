How to setup a zenpack development environment on ubuntu precise:

As root do:

apt-get install python-dev libxml2-dev libxslt1-dev
curl https://raw.github.com/pypa/pip/master/contrib/get-pip.py -o get-pip.py
python get-pip.py
ln -s /usr/local/bin/pip /usr/bin
pip install --upgrade setuptools
pip install virtualenv
ln -s /usr/local/bin/virtualenv /usr/bin

As yourself do:
virtualenv --system-site-packages zpd
source zpd/bin/activate # this is like rvm use - sets up your env in a sandbox
pip install lxml
pip install pytz

Now you can dev the zenpack and build with:

python setup.py bdist_egg

To deploy to zenoss server, use the Capfile in the pupal repo like:

HOSTS=zenoss.host cap zpd:deploy_zenpack

When it prompts you for the egg file, give the full path to the egg file in the dist dir.

NOTE, you need to add your ssh pub key to the zenoss authorized_keys file on the zenoss host.  The cap task joyent:dist_pub_key will do that for you.













