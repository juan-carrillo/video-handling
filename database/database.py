import mysql.connector

from mysql.connector import Error
from mysql.connector import DatabaseError

class MySql(object):
	"""docstring for MySql"""
	def __init__(self):
		super(MySql, self).__init__()


		self.connection = mysql.connector.connect(
			host="localhost",
			user="root",
			password="password",
			port=42333
		)

		self.cursor = self.connection.cursor()

	def change_database(self, db_name):
		self.close_connection()

		self.connection = mysql.connector.connect(
			host="localhost",
			user="root",
			password="password",
			database=db_name,
			port=42333
		)

		self.cursor = self.connection.cursor()

	def execute_query(self, query_string):
		return self.cursor.execute(query_string)

	def create_database(self, db_name):
		return self.execute_query(f'CREATE DATABASE IF NOT EXISTS {db_name}')

	def is_connected(self):
		return self.connection.is_connected()

	def commit(self):
		self.connection.commit()

	def close_connection(self):
		if self.connection.is_connected():
			self.cursor.close()
			self.connection.close()
			print("MySQL connection is closed")

	def insert_rows(self, table_name, columns, values):
		statement = f"""
		INSERT INTO 
			{table_name} ({columns})
		VALUES 
		{values}
		"""
		print(statement)
		self.execute_query(statement)
		
		return self.commit()



def main():
	sql_handler = MySql()

	try:
		sql_handler.create_database('test')

		if sql_handler.connection.is_connected():
			db_Info = sql_handler.connection.get_server_info()
			print("Connected to MySQL Server version ", db_Info)

			sql_handler.cursor.execute("select database();")
			record = sql_handler.cursor.fetchone()
			print("You're connected to database: ", record)
	except Error as e:
		print("Error while connecting to MySQL", e)
	else:
		if sql_handler.connection.is_connected():
			sql_handler.cursor.close()
			sql_handler.connection.close()
			print("MySQL connection is closed")
	print('END OF MAIN PROCESS')


if __name__ == '__main__':
	main()