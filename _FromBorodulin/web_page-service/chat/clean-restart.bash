#!/bin/bash
sudo rm ./*.pyc ./disqusdb/*.pyc ./templates/*.pyc ./disqusapi/*.pyc
sudo service apache2 restart