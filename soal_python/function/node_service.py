import MySQLdb
from datetime import datetime
import random
import string


class NodeService:

    DB_HOST = "localhost"
    DB_USER = "admin"
    DB_PASSWORD = "admin"
    DB_NAME = "ProjectDB"
    TABLE_NAME = "nodeDB"


    def __init__(self):
        self.createDatabase()
        self.createTable()


    def getConnection(self, use_database=True):
        if use_database:
            return MySQLdb.connect(
                host=self.DB_HOST,
                user=self.DB_USER,
                passwd=self.DB_PASSWORD,
                db=self.DB_NAME
            )

        return MySQLdb.connect(
            host=self.DB_HOST,
            user=self.DB_USER,
            passwd=self.DB_PASSWORD
        )


    def createDatabase(self):
        connection = self.getConnection(use_database=False)
        cursor = connection.cursor()

        query = "CREATE DATABASE IF NOT EXISTS {}".format(self.DB_NAME)
        cursor.execute(query)

        connection.commit()
        cursor.close()
        connection.close()


    def createTable(self):
        connection = self.getConnection()
        cursor = connection.cursor()

        query = """
        CREATE TABLE IF NOT EXISTS {} (
            id VARCHAR(10) PRIMARY KEY,
            name VARCHAR(100),
            updated_at DATETIME
        )
        """.format(self.TABLE_NAME)

        cursor.execute(query)

        connection.commit()
        cursor.close()
        connection.close()


    def generateNodeId(self):
        huruf_angka = string.ascii_letters + string.digits
        random_part = ""
        for i in range(5):
            random_part += random.choice(huruf_angka)

        node_id = "NODE-{}".format(random_part)
        print("node_id baru : " + node_id)

        return node_id
    

    def readNode(self):
        connection = self.getConnection()
        cursor = connection.cursor(MySQLdb.cursors.DictCursor)

        query = "SELECT id, name, updated_at FROM {}".format(self.TABLE_NAME)
        cursor.execute(query)

        rows = cursor.fetchall()

        cursor.close()
        connection.close()

        return rows


    def createNode(self, name):
        if not name:
            raise ValueError("Nama node tidak boleh kosong")

        connection = self.getConnection()
        cursor = connection.cursor()

        node_id = self.generateNodeId()
        updated_at = datetime.now()

        query = """
        INSERT INTO {} (id, name, updated_at)
        VALUES (%s, %s, %s)
        """.format(self.TABLE_NAME)

        cursor.execute(query, (node_id, name, updated_at))
        connection.commit()

        cursor.close()
        connection.close()

        print("Sukses create data di database")
        return {
            "id": node_id,
            "name": name,
            "updated_at": updated_at
        }
    

    def updateNode(self, node_id, name):
        if not node_id:
            raise ValueError("Node ID tidak boleh kosong")

        if not name:
            raise ValueError("Nama node tidak boleh kosong")

        connection = self.getConnection()
        cursor = connection.cursor()

        check_query = "SELECT id FROM {} WHERE id = %s".format(self.TABLE_NAME)
        cursor.execute(check_query, (node_id,))
        result = cursor.fetchone()

        if not result:
            cursor.close()
            connection.close()
            raise ValueError("Node tidak ditemukan")

        updated_at = datetime.now()

        update_query = """
        UPDATE {}
        SET name = %s, updated_at = %s
        WHERE id = %s
        """.format(self.TABLE_NAME)

        cursor.execute(update_query, (name, updated_at, node_id))
        connection.commit()

        cursor.close()
        connection.close()

        print("Sukses update data di database")
        return True
    

    def deleteNode(self, node_id):
        if not node_id:
            raise ValueError("Node ID tidak boleh kosong")

        connection = self.getConnection()
        cursor = connection.cursor()

        check_query = "SELECT id FROM {} WHERE id = %s".format(self.TABLE_NAME)
        cursor.execute(check_query, (node_id,))
        result = cursor.fetchone()

        if not result:
            cursor.close()
            connection.close()
            raise ValueError("Node tidak ditemukan")

        delete_query = "DELETE FROM {} WHERE id = %s".format(self.TABLE_NAME)
        cursor.execute(delete_query, (node_id,))
        connection.commit()

        cursor.close()
        connection.close()

        print("Sukses delete data di database")
        return True
    

if __name__ == "__main__":

    print("Tes class node_service")

    node_service = NodeService()

    # generate id
    # node_service.generateNodeId()

    # read
    # nodes = node_service.readNode()
    # print("Data : ", nodes)

    # create
    # tes_result = node_service.createNode("tes123")
    # print(tes_result)

    # update
    # tes_result = node_service.updateNode("NODE-6Wuqu", "update 1")
    # print(tes_result)

    # delete
    # tes_result = node_service.deleteNode("NODE-kmSBn")
    # print(tes_result)

    nodes = node_service.readNode()
    print("Data akhir : ", nodes)

    print("Selesai")