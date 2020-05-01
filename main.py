from flask import Flask
from flask_restful import Resource, Api
import sys

app = Flask(__name__)
api = Api(app)

USAGE = 'Usage: python main.py [ROOT] [PORT]'

root = 8000
port = '.'

class Directory(Resource):
  def get(self):
    return {'hello': 'world'}

api.add_resource(Directory, '/')

if __name__ == '__main__':
  try:
    root = str(sys.argv[1])
  except Exception:
    print(USAGE)
    print 'Using default root %s' % root

  try:
    port = int(sys.argv[2])
  except Exception, e:
    print 'Using default port %d' % port

  app.run(debug=True, host='0.0.0.0', port=port)