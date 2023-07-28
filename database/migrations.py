from database import MySql


def delete_table(mysql_connector, table_name):
	mysql_connector.execute_query(f'DROP TABLE IF EXISTS {table_name}')


def create_video_data_table(mysql_connector, table_name):
	delete_table(mysql_connector, table_name)

	statement = """CREATE TABLE {} (
	    id int NOT NULL AUTO_INCREMENT,
	    clip_name varchar(255),
	    clip_file_extension varchar(10),
	    clip_duration int,
	    clip_location longtext,
	    created_at timestamp null default null,
	    updated_at timestamp null default null,
	    PRIMARY KEY (id)
	)
	""".format(table_name)
	return mysql_connector.execute_query(statement)


def main():
	sql_handler = MySql()

	sql_handler.create_database('test')
	sql_handler.change_database('test')

	if sql_handler.is_connected():
		db_Info = sql_handler.connection.get_server_info()
		print("Connected to MySQL Server version ", db_Info)

		sql_handler.cursor.execute("select database();")
		record = sql_handler.cursor.fetchone()
		print("You're connected to database: ", record)

		create_video_data_table(sql_handler, 'video_data')

	sql_handler.close_connection()
	print('END OF MAIN PROCESS')


if __name__ == '__main__':
	main()