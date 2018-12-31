#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 31 19:06:15 2018

@author: marekmasiak
"""




import http.server
import json

try:
    import mysql.connector
except:
    from pip._internal import main
    package = 'mysql-connector'
    main(['install', package, '--quiet'])
    import mysql.connector
from mysql.connector import errorcode


class CustomRequestHandler(http.server.BaseHTTPRequestHandler):

    
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(b'<html><head><title>success</title></head><body>please use POST requests for now</body></html>')

    def do_POST(self):
        
        data_dict = {}
        
        
        #change to own credentials
        config = {
            'user': 'user',
            'password': 'password',
            'host': 'localhost',
            'database': 'base'
}
        
        def fail(self,message):
            self.send_response(400)
            self.send_header('Content-type','text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(str.encode(message))
        
        def succeed(self):
            self.send_response(200)
            self.send_header('Content-type','text/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(str.encode(str(data_dict)))
        
        data = self.rfile.read(int(self.headers['Content-Length']))
        is_it_json = 1
        is_it_urlencoded = 1
        skip = 0
        data = data.decode()
        print (data)
        try:
            data_dict = json.loads(data)
            print(data_dict)
        except:
            is_it_json = 0
        if '=' not in data and '&' not in data:
            is_it_urlencoded = 0
        else:
            for data_cell in data.split('&'):
                data_dict[data_cell.split('=')[0]] = data_cell.split('=')[1]
        if is_it_json != 0 or is_it_urlencoded != 0:
            if 'type' in data_dict and 'query' in data_dict:
                try:
                    connection = mysql.connector.connect(user=config['user'], password=config['password'],
                              host=config['host'],
                              database=config['database'])
                    connection.close()
                except mysql.connector.Error as err:
                    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                        fail(self,"<html><head><title>failure</title></head><body>Something is wrong with your user name or password</body></html>")
                        skip = 1
                    elif err.errno == errorcode.ER_BAD_DB_ERROR:
                        fail(self,"<html><head><title>failure</title></head><body>Database does not exist</body></html>")
                        skip = 1
                    else:
                        fail(self,'<html><head><title>failure</title></head><body>'+str(err)+'</body></html>')
                        skip = 1
                if skip == 0:
                   succeed(self)
                skip = 0
            else:
                fail(self,'<html><head><title>failure</title></head><body>missing data</body></html>')
        else:
            fail(self,'<html><head><title>failure</title></head><body>unrecognised data type</body></html>')
        

def run():
    hostaddress = '127.0.0.1'
    port = 8000
    server_address = (hostaddress, port)
    httpd = http.server.HTTPServer(server_address, CustomRequestHandler)
    httpd.serve_forever()

run()