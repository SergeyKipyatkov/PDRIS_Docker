from flask import Flask
import MySQLdb
import os

app = Flask(__name__)

def connect_db():
  try:
    DB_HOST = os.environ['MYSQL_HOST']
    DB_PASS = os.environ['MYSQL_ROOT_PASSWORD']
    DB_NAME = os.environ['MYSQL_DATABASE']
    DB_USER = os.environ['MYSQL_USER']
    return MySQLdb.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
    
  except MySQLdb.OperationalError as ex:
    if ex.args[0] == 2002:
      print("Database has not started yet. Restarting...")
    else:
      print("Unexpected database error: ", ex.args[1])
    exit(-1)

conn = connect_db()


@app.route("/")
def index_page():
  conn.query("SELECT id, name, age FROM `users`")
  r = conn.store_result()
  return { 'users': r.fetch_row(maxrows=10, how=1) }
  
@app.route("/users")
def users_list():
  conn.query("SELECT id, name, age FROM `users`")
  r = conn.store_result()
  return { 'users': r.fetch_row(maxrows=10000, how=1) }

@app.route("/users/<id>")
def single_user(id):
  conn.query(f"SELECT id, name, age FROM `users` WHERE id={id}")
  res = conn.store_result().fetch_row(how=1)
  return res[0] if len(res) > 0 else ("User not found", 404)
    

@app.route("/health")
def health():
  return { 'status': 'ok' }

@app.route('/<path:path>')
def catch_all(path):
  return ('Error 404 - Not found', 404)

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8000)