
# connect to database here

import MySQLdb
import csv
import os

try:
  DB_HOST = os.environ['MYSQL_HOST']
  DB_PASS = os.environ['MYSQL_ROOT_PASSWORD']
  DB_NAME = os.environ['MYSQL_DATABASE']
  DB_USER = os.environ['MYSQL_USER']
  conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, password=DB_PASS, database=DB_NAME)
  
except MySQLdb.OperationalError as ex:
  if ex.args[0] == 2002:
    print("Database has not started yet. Restarting...")
  else:
    print("Unexpected migration error: ", ex.args[1])
  exit(-1)

conn.query("""
CREATE TABLE if not exists users (
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  name CHAR(255) NOT NULL,
  age INT NOT NULL,
  PRIMARY KEY (id) 
);
""")

conn.query("TRUNCATE TABLE users")

csvfile = open('data.csv', newline='')
reader = csv.reader(csvfile, delimiter=',')
header = next(reader) # skip header

try:
  row_count = 0
  for row in reader:
    name, age = row
    print(name, age)
    row_count += 1
    conn.query(f"INSERT INTO users (name, age) VALUES ('{name}', {age})")
  conn.commit()
  print(f"Database migration completed! Inserted {row_count} records")
  
  conn.query(f"SELECT * FROM `users`")
  r = conn.store_result()
  for row in r.fetch_row(maxrows=10000, how=0):
    print(row)
  
except MySQLdb.OperationalError as ex:
  print("Unexpected migration error: ", ex.args[1])
