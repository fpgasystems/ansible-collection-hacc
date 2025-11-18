#!/bin/bash

cd /usr/share/nginx/html/deb-repo

dpkg-scanpackages . /dev/null | gzip -9c > Packages.gz
dpkg-scanpackages . /dev/null > Packages
apt-ftparchive release . > Release

#gpg --batch --passphrase '' --quick-generate-key "deb_repo_key" default default 0
#
#gpg --default-key deb_repo_key --output Release.gpg --detach-sign Release
#gpg --default-key deb_repo_key --output InRelease --clearsign Release
#gpg --export --armor deb_repo_key > repo-key.asc

exec nginx -g "daemon off;"

