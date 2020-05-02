import os
from pwd import getpwuid
import sys

from flask import Flask, jsonify


app = Flask(__name__)

ROOT = '.'
PORT = 8000


class InvalidPathError(Exception):
  '''Simple class for representing path errors.

  Attributes:
    message: The error message to include with the 400 call
  '''
  status_code = 400

  def __init__(self, message):
    '''Initializes an error with a given error message.'''
    Exception.__init__(self)
    self.message = message

  def to_dict(self):
    '''Converts Exception object to a dictionary.'''
    response = {
      'message': self.message,
    }
    return response


def concat_paths(root, path):
  '''Concats two path variables with a / connecting char.

  Args:
    root: First part of the path.
    path: Part of path that should be appended.

  Returns:
    The combined path string.
  '''
  return '%s/%s' % (root, path)


def list_files(path):
  '''Lists all files for a given path.

  Args:
    path: The path to look up.

  Returns:
    A list of file descriptions, formatted as a JSON object.

  Raises:
    InvalidPathError: An error occurred when listing files for the path.
  '''
  try:
    files = os.listdir(path)
  except Exception:
    raise InvalidPathError('Could not list files for path %s' % path)
  out = []
  for file in files:
    out.append(describe_file(path, file))
  return {
    'files': out,
  }


def describe_file(path, filename):
  '''Looks up an individual file and reports on some select columns.

  Args:
    path: The root path containing the file.
    filename: The name of the file to look up.

  Returns:
    A dict containing the filename, size (in Bytes), owner, and permissions
    for the requested file.
  '''
  status = os.stat(concat_paths(path, filename))
  return {
    'filename': filename,
    'sizeBytes': status.st_size,
    'owner': getpwuid(status.st_uid).pw_name,
    'permissions': oct(status.st_mode),
  }


def read_file(path):
  '''Reads in an individual file.

  Args:
    path: The full path of the file to read in.

  Returns:
    The contents of the file (jsonified).
  '''
  with open(path, 'r') as f:
    contents = f.read()
  return {
    'file': contents,
  }


# Handle all GETs with the same method, regardless of path.
@app.route('/', defaults={'path': ''}, methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def get_file(path):
  '''Gets files associated with a route.

  If a route refers to an individual file, returns the contents of that
  file instead.

  Args:
    path: The full path for the request. This will correspond to the path
        whose files are to be looked up.

  Returns:
    Http response with status code 200 and either a list of file information
    for the requested directory, or the file contents if path was for a file.

  Raises:
    InvalidPathError: Path refers to a special file type, ie neither a file
    nor a directory.
  '''
  path = concat_paths(ROOT, path)
  response = {}
  if os.path.isdir(path):  
    response = jsonify(list_files(path))
  elif os.path.isfile(path):
    response = jsonify(read_file(path))
  else:
    raise InvalidPathError('Path is neither file nor directory')

  response.status_code = 200
  return response


@app.errorhandler(InvalidPathError)
def handle_invalid_path(error):
  '''Error handler for thrown InvalidPathErrors.

  Args:
    error: InvalidPathError to be returned with an error status code (400).
  '''
  response = jsonify(error.to_dict())
  response.status_code = error.status_code
  return response


if __name__ == '__main__':
  try:
    ROOT = str(sys.argv[1])
  except Exception:
    print 'Usage: python main.py [ROOT] [PORT]'
    print 'Using default root %s' % ROOT

  try:
    PORT = int(sys.argv[2])
  except Exception, e:
    print 'Using default port %d' % PORT

  app.run(host='0.0.0.0', port=PORT)