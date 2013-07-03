#!/usr/bin/sh

# get dependencies
sudo apt-get install build-essential libpcre3-dev librasqal3-dev libtool libraptor1-dev libglib2.0-dev ncurses-dev libreadline-dev

# get 4store
wget http://4store.org/download/4store-v1.1.5.tar.gz
tar -zxvf 4store-v1.1.5.tar.gz
cd 4store-v1.1.5/

# compile 4store
export PKG_CONFIG_PATH=/usr/lib64/pkgconfig:/usr/share/pkgconfig:/usr/local/lib64/pkgconfig:/usr/local/share/pkgconfig
./configure
make

# install and test 4store
sudo make install
make test
echo -e '\nSome tests may have failed, but 4store is still good to go.\n'

# set up 4store database
4s-backend-setup xml

# install sparql-query dependencies
cd ..
sudo apt-get install glib-networking libcurl3 libreadline6 libxml2

# get sparql-query
git clone https://github.com/tialaramex/sparql-query.git
cd ./sparql-query

# install sparql-query
make all
sudo make install
