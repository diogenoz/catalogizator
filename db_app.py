import sqlite3


class DBApp:

    def __init__(self, dbName):
        self.connection = sqlite3.connect(dbName)
        print("connection test ok")

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def getTag(self, file_id, category_id):
        cursor = self.connection.cursor()
        link_id = None
        query_params = {"file_id": file_id,  "category_id": category_id}
        query_string = """ SELECT l.link_id  
                            FROM `File_link_category` l 
                            WHERE l.file_id = :file_id 
                              AND l.category_id = :category_id; """
        try:
            cursor.execute(query_string, query_params)
            result = cursor.fetchone()
            if result:
                link_id = result[0]
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("insert ok")
        finally:
            cursor.close()

        return link_id

    def addTag(self, fileId: int, categoryId: int):
        cursor = self.connection.cursor()

        query_params = {"category_id": categoryId, "file_id": fileId}
        query_string = """\
        INSERT INTO `File_link_category`(`category_id`,`file_id`) VALUES (:category_id, :file_id);
        """
        try:
            cursor.execute(query_string, query_params)
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("insert ok")
        finally:
            cursor.close()

    def deleteTag(self, file_id, category_id):
        cursor = self.connection.cursor()

        query_params = {"file_id": file_id, "category_id": category_id}
        query_string = """\
                DELETE FROM `File_link_category` WHERE file_id = :file_id AND category_id = :category_id;
                """
        try:
            cursor.execute(query_string, query_params)
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("delete ok")
        finally:
            cursor.close()


    def getFilesWithTag(self, categoryId):
        cursor = self.connection.cursor()
        paths = []
        query_params = {"categoryId": categoryId}
        query_string = """ SELECT DISTINCT f.path  FROM `File_link_category` l JOIN 'File' f 
        ON f.file_id = l.file_id   WHERE l.category_id = :categoryId; """
        try:
            cursor.execute(query_string, query_params)

            for row in cursor:
                paths.append(row[0])


        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("insert ok")
        finally:
            cursor.close()

        return paths

    def addCategory(self, name, is_enable=1):
        categoryId = None
        cursor = self.connection.cursor()


        query_params = {"name": name, "is_enable": is_enable}
        query_string = """\
                INSERT INTO `Category`(`name`,`is_enable`) VALUES (:name, :is_enable);
                """
        try:
            cursor.execute(query_string, query_params)

            categoryId = cursor.lastrowid
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("insert ok")
        finally:
            cursor.close()
        return categoryId

    def disableCategory(self, category_id):
        cursor = self.connection.cursor()

        query_params = {"category_id": category_id, "is_enable": 0}
        query_string = """\
                UPDATE `Category` SET is_enable = :is_enable WHERE category_id = :category_id;
                """
        try:
            cursor.execute(query_string, query_params)
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("insert ok")
        finally:
            cursor.close()

    def getCategories(self):
        cursor = self.connection.cursor()
        categories = []
        query_string = """ SELECT c.name  FROM `Category` c"""
        try:
            cursor.execute(query_string)

            for row in cursor:
                categories.append(row[0])

        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("insert ok")
        finally:
            cursor.close()

        return categories

    def addFile(self, name, path, size, hash):
        fileId = None
        cursor = self.connection.cursor()

        query_params = {"name": name, "path": path, "size": size, "hash": hash}
        query_string = """\
                INSERT INTO `File`(`name`,`path`,`size`,`hash`) VALUES (:name, :path, :size, :hash);
                """
        try:
            cursor.execute(query_string, query_params)

            fileId = int(cursor.lastrowid)
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("insert ok")
        finally:
            cursor.close()
        return fileId

    def delFile(self, file_id):
        cursor = self.connection.cursor()

        query_params = {"file_id": file_id}
        query_string = """\
                DELETE FROM `File` WHERE file_id = :file_id;
                """
        try:
            cursor.execute(query_string, query_params)
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("insert ok")
        finally:
            cursor.close()

    def findSameFile(self, size, hash):
        cursor = self.connection.cursor()
        file_id = None

        query_params = {"size": size, "hash": hash}
        query_string = """\
        SELECT file_id FROM `File` WHERE size = :size and hash = :hash;
        """
        try:
            cursor.execute(query_string, query_params)
            result = cursor.fetchone()
            if result != None:
                file_id = int(result[0])
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("find it")
        finally:
            cursor.close()
        return file_id

    def findFileByPath(self, size, hash, path):
        cursor = self.connection.cursor()
        file_id = None

        query_params = {"size": size, "hash": hash, "path": path}
        query_string = """\
        SELECT file_id FROM `File` f WHERE f.size = :size and f.hash = :hash and f.path = :path;
        """
        try:
            cursor.execute(query_string, query_params)
            result = cursor.fetchone()
            if result != None:
                file_id = int(result[0])
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("find it")
        finally:
            cursor.close()
        return file_id