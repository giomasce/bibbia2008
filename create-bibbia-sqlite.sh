#!/bin/bash

echo "create table bibbia (indice integer primary key autoincrement, libro text, capitolo numeric, versetto numeric, lettera text, testo text);"
echo "begin;"
sed -e "s/^\([^:]*\):\([^:]*\):\([^:]*\):\([^:]*\):\(.*\)$/insert into bibbia(libro, capitolo, versetto, lettera, testo) values \(\"\1\", \"\2\", \"\3\", \"\4\", \"\5\");/"
echo "create unique index bibbia_idx on bibbia(libro, capitolo, versetto, lettera);"
echo "commit;"
