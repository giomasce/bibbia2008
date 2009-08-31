#!/usr/bin/python
# bibbia.py - Searches or shows Bible quotes
# Copyright (C) 2009  Giovanni Mascellani <mascellani@poisson.phc.unipi.it>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, re
from pysqlite2 import dbapi2 as sqlite

def connectDB(dbFilename = "bibbia.sqlite"):
	dbConn = sqlite.connect(dbFilename)
	dbCur = dbConn.cursor()
	return dbCur

def ricerca(argv):
	query = "select * from formattata where"
	first = True
	for i in argv:
		andText = ""
		if not first:
			andText = " and"
		query += "%s testo like '%%%s%%'" % (andText, i)
		first = False
	cursor = connectDB()
	cursor.execute(query)
	number = 0
	for row in cursor:
		print ("%s %s, %s%s: %s") % row
		number += 1
	print "Trovati %d risultati" % (number)

def mostra(argv):
	citazione = " ".join(argv)
	regex = re.compile(" *([^ ]+) *(?:([0-9]+)(?: *, *([0-9]+))?)? *")
	match = regex.match(citazione)
	if match == None:
		print """Non riesco a riconoscere la citazione che mi hai dato.
Se sei convinto che sia giusta, per favore segnala un bug."""
		sys.exit(1)
	else:
		if match.group(2) == None:
			# Citazione solo libro
			query = "select * from formattata where libro = '%s'" % (match.group(1))
		elif match.group(3) == None:
			# Citazione libro e capitolo
			query = "select * from formattata where libro = '%s' and capitolo = %s" % (match.group(1), match.group(2))
		else:
			# Citazione completa
			query = "select * from formattata where libro = '%s' and capitolo = %s and versetto = %s" % (match.group(1), match.group(2), match.group(3))
	cursor = connectDB()
	cursor.execute(query)
	# Qui bisognerebbe ordinare correttamente i dati, sia per gestire
	# i casi eccezionali, sia per non fidarsi dell'ordine resituito dal DB
	number = 0
	for row in cursor:
		print ("%s %s, %s%s: %s") % row
		number += 1
	print "Trovati %d risultati" % (number)

def main(argv = None):
	if argv == None:
		argv = sys.argv

	if len(argv) < 2:
		print "Per favore, dimmi cosa fare"
		sys.exit(1)
	command = argv[1]
	if (command == "search"):
		ricerca(argv[2:])
	elif (command == "show"):
		mostra(argv[2:])
	else:
		print "Comand %s sconosciuto" % (command)
		sys.exit(1)

if (__name__ == "__main__"):
	main()

