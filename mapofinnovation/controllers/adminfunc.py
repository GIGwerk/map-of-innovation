import logging
import redis 
import csv
import os 
import re 

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from datetime import datetime
from mapofinnovation.lib.base import BaseController, render
from pylons.decorators import jsonify
log = logging.getLogger(__name__)

class AdminfuncController(BaseController):

    # @jsonify
    def addfromcsv(self):
        if os.environ.get("REDIS_URL") :
            redis_url = os.environ.get("REDIS_URL")
        else:
            redis_url = "localhost"        
        r_server = redis.Redis(redis_url)
        with open('mapofinnovation/public/updated_spaces_ready_for_merge.csv', 'rb') as csv_file:
                dialect = csv.Sniffer().sniff(csv_file.read(), delimiters=',')
                csv_file.seek(0)
                csv_reader = csv.DictReader(csv_file, dialect=dialect)
                for row in csv_reader:
                    tempkey = (str(row['name']+str(datetime.now())))
                    key = ''.join(e for e in tempkey if e.isalnum())
                    #TODO : shift this code to another function
                    row.update({'wiki':('/uifunc/wikipage/'+key)})
                    row.update({'archived':False})
                    row.update({'verified':True})
                    r_server.hmset(re.sub(' ','',key),row) 
        return {'success':'true'}

if __name__ == "__main__":
    instance = AdminfuncController()
    AdminfuncController.addfromcsv(instance)
