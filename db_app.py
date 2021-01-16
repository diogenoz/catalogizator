import sqlite3


class DBApp:

    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        print("connection test ok")

    def __del__(self):
        self.connection.commit()
        self.connection.close()

    def get_tag(self, file_id, category_id):
        cursor = self.connection.cursor()
        link_id = None
        query_params = {"file_id": file_id, "category_id": category_id}
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

    def get_tags_by_file(self, file_id):
        cursor = self.connection.cursor()
        result = None
        query_params = {"file_id": file_id}
        query_string = """ SELECT l.category_id
                                 ,c.name  
                            FROM `File_link_category` l, `Category` c 
                            WHERE l.file_id = :file_id
                              AND c.is_enable = 1
                              AND l.category_id = c.category_id
                            ORDER BY c.category_id; """
        try:
            cursor.execute(query_string, query_params)
            result = cursor.fetchall()
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("insert ok")
        finally:
            cursor.close()

        return result

    def add_tag(self, file_id: int, category_id: int):
        cursor = self.connection.cursor()

        query_params = {"category_id": category_id, "file_id": file_id}
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
            self.connection.commit()
            cursor.close()

    def delete_tag(self, file_id, category_id):
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
            self.connection.commit()
            cursor.close()

    def get_files_with_tag(self, category_id):
        cursor = self.connection.cursor()
        paths = []
        query_params = {"categoryId": category_id}
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

    def add_category(self, name, is_enable=1):
        category_id = None
        cursor = self.connection.cursor()

        query_params = {"name": name, "is_enable": is_enable}
        query_string = """\
                INSERT INTO `Category`(`name`,`is_enable`) VALUES (:name, :is_enable);
                """
        try:
            cursor.execute(query_string, query_params)

            category_id = cursor.lastrowid
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("insert ok")
        finally:
            self.connection.commit()
            cursor.close()
        return category_id

    def disable_category(self, category_id):
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
            self.connection.commit()
            cursor.close()

    def get_categories(self):
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

    def add_file(self, name, path, size, hash_sum):
        file_id = None
        cursor = self.connection.cursor()

        query_params = {"name": name, "path": path, "size": size, "hash": hash_sum}
        query_string = """\
                INSERT INTO `File`(`name`,`path`,`size`,`hash`) VALUES (:name, :path, :size, :hash);
                """
        try:
            cursor.execute(query_string, query_params)

            file_id = int(cursor.lastrowid)
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("insert ok")
        finally:
            self.connection.commit()
            cursor.close()
        return file_id

    def del_file(self, file_id):
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
            self.connection.commit()
            cursor.close()

    def find_same_file(self, size, hash_sum):
        cursor = self.connection.cursor()
        file_id = None

        query_params = {"size": size, "hash": hash_sum}
        query_string = """\
        SELECT file_id FROM `File` WHERE size = :size and hash = :hash;
        """
        try:
            cursor.execute(query_string, query_params)
            result = cursor.fetchone()
            if result is not None:
                file_id = int(result[0])
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("find it")
        finally:
            cursor.close()
        return file_id

    def find_file_by_path(self, size, hash_sum, path):
        cursor = self.connection.cursor()
        file_id = None

        query_params = {"size": size, "hash": hash_sum, "path": path}
        query_string = """\
        SELECT file_id FROM `File` f
        WHERE f.size = :size 
          AND f.hash = :hash 
          AND f.path = :path;
        """
        try:
            cursor.execute(query_string, query_params)
            result = cursor.fetchone()
            if result is not None:
                file_id = int(result[0])
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("find it")
        finally:
            cursor.close()
        return file_id

    def get_file_by_id(self, file_id):
        cursor = self.connection.cursor()
        result = None

        query_params = {"file_id": file_id}
        query_string = """\
                SELECT f.file_id
                      ,f.path
                      ,f.name
                      ,f.size
                      ,f.hash
                FROM `File` f
                WHERE f.file_id = :file_id;
                """
        try:
            cursor.execute(query_string, query_params)
            result = cursor.fetchone()
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("find it")
        finally:
            cursor.close()
        return result

    def upd_file_path(self, file_id, path, name):
        cursor = self.connection.cursor()

        query_params = {"file_id": file_id, "path": path, "name": name}
        query_string = """\
                UPDATE `File`
                SET path = :path
                   ,name = :name
                WHERE file_id = :file_id;
                """
        try:
            cursor.execute(query_string, query_params)
        except sqlite3.DatabaseError as err:
            print("Ошибка:", err)
        else:
            print("upd_file_path it")
        finally:
            self.connection.commit()
            cursor.close()
