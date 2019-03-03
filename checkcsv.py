#!/usr/bin/env python3

import csv
import re
import sys


COLUMNS = ['Pseudo', 'Nom', 'Promo', 'Mise à jour', 'Latitude', 'Longitude']


def error(msg, line):
    sys.stderr.write(msg)
    sys.stderr.write(" ligne %d\n" % (line + 1))
    sys.exit(1)


_promo = re.compile(r'^(19|20)[0-9][0-9]$')
_date = re.compile(r'^20[0-9][0-9]-[0-9][0-9]-[0-9][0-9]$')
_coord = re.compile(r'^-?[0-9]{1,3}\.[0-9]{1,10}$')


if __name__ == '__main__':
    with open(sys.argv[1]) as fp:
        cols = None
        lines = enumerate(csv.reader(fp))
        line, firstline = next(lines)
        if firstline != COLUMNS:
            error("Header invalide", line)
        for line, row in lines:
            if len(row) != len(COLUMNS):
                error("Nombre de colonnes invalide", line)
            if not _promo.match(row[2]):
                error("Promo invalide %r" % row[2], line)
            if not _date.match(row[3]):
                error("Date de mise a jour invalide %r" % row[3], line)
            if not _coord.match(row[4]):
                error("Latitude invalide %r" % row[4], line)
            if not _coord.match(row[5]):
                error("Longitude invalide %r" % row[5], line)
        print("%d lignes validees" % (line + 1))
