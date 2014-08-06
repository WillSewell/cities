from HTMLParser import HTMLParser
import urllib

class CountryListParser(HTMLParser):

    in_cities_table = False
    column_count = 0
    data_count = 0
    cur_val = ""

    def handle_starttag(self, tag, attrs):
        if tag == 'td' and self.in_cities_table and self.column_count < 6:
            self.column_count += 1
            self.data_count = 1

    def handle_endtag(self, tag):

        if tag == 'td' and self.in_cities_table:
            print self.cur_val
            if self.column_count == 6:
                self.column_count = 0
                print '-----------'

    def handle_data(self, data):
        if data == 'Local Name': self.in_cities_table = True
        if self.in_cities_table:
            if self.data_count == 1:
                self.cur_val = data
            else:
                self.cur_val += data
                self.data_count += 1

parser = CountryListParser()
sock = urllib.urlopen('http://en.wikipedia.org/wiki/List_of_agglomerations_by_population')
parser.feed(sock.read())
sock.close()