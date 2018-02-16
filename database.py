# Import dependencies
import sqlite3

def main():
	dbName = 'podcasts.db'
	connection = connect(dbName)
	createTables(connection)
	connection.close()

def connect(path):
	connection = sqlite3.connect(path)

	return connection

def createTables(connection):
	sqlShow = (
		'CREATE TABLE IF NOT EXISTS show (' +
			'name text NOT NULL, ' +
			'link text NOT NULL, ' + 
			'description text NOT NULL, ' +
			'overcastURL text NOT NULL UNIQUE ON CONFLICT IGNORE' +
			');'
		)

	sqlEpisode = (
		'CREATE TABLE IF NOT EXISTS episode (' +
			'show integer, ' +
			'name text NOT NULL, ' +
			'description text NOT NULL, ' +
			'publishDate text NOT NULL, '
			'overcastURL text NOT NULL UNIQUE ON CONFLICT IGNORE, ' +
			'remoteFile text NOT NULL, ' +
			'fileType text NOT NULL, ' +
			'localFile text, ' +
			'FOREIGN KEY (show) REFERENCES show(rowid)'
			');'
		)

	cursor = connection.cursor()
	cursor.execute(sqlShow)
	cursor.execute(sqlEpisode)
	connection.commit()

def addRecord(connection, table, dictionary):
	keys = []
	values = []

	for key, value in dictionary.items():
		keys.append(key)
		values.append(value)

	sql = 'INSERT INTO {0} ({1}) VALUES ({2});'.format(
		table, 
		', '.join(keys), 
		', '.join(['?'] * len(keys))
		)

	cursor = connection.cursor()
	cursor.execute(sql, values)
	connection.commit()

if __name__ == '__main__':
	main()