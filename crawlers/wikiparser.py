from HTMLParser import HTMLParser
import urllib
import psycopg2
from ConfigParser import *

c = ConfigParser()
c.read('db.ini')

conn = psycopg2.connect(
    database=c.get('db', 'database'),
    user=c.get('db', 'user'),
    password=c.get('db', 'password'))
cur = conn.cursor()


class CountryListParser(HTMLParser):

    in_cities_table = False
    column_count = 0
    data_count = 0
    cur_val = ""
    cur_local_name = ""
    cur_eng_name = ""
    cur_country = ""
    cur_agglom_pop = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'td' and self.in_cities_table and self.column_count < 6:
            self.column_count += 1
            self.data_count = 1

    def handle_endtag(self, tag):
        if tag == 'td' and self.in_cities_table:
            print self.cur_val
            if self.column_count == 2:
                self.cur_local_name = self.cur_val
            if self.column_count == 3:
                self.cur_eng_name = self.cur_val
            if self.column_count == 4:
                self.cur_country = self.cur_val
            if self.column_count == 5:
                self.cur_agglom_pop = self.cur_val
            if self.column_count == 6:
                self.column_count = 0
                qry = """
INSERT INTO cities
    (local_name, eng_name, country, agglom_population)
VALUES (%s, %s, %s, %s)
"""
                args = (self.cur_local_name, self.cur_eng_name,
                        self.cur_country,
                        self.cur_agglom_pop.replace(',', ''))
                cur.execute(qry, args)
                conn.commit()

    def handle_data(self, data):
        if data == 'Local Name':
            self.in_cities_table = True
        if self.in_cities_table:
            if self.data_count == 1:
                self.cur_val = data
            else:
                self.cur_val += data
                self.data_count += 1

parser = CountryListParser()
sock = urllib.urlopen(
    'http://en.wikipedia.org/wiki/List_of_agglomerations_by_population')
parser.feed(sock.read())
sock.close()

cur.close()
conn.close()
