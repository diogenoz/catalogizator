import os

import db_app
from pathlib import Path
import hashlib
import xml.etree.cElementTree as et
import re


class App:
    def __init__(self, db: db_app.DBApp):
        self.db = db

    def get_file_hash_sha512(self, file_path):
        buf_size = 65536
        sha512 = hashlib.sha512()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                sha512.update(data)
        return sha512.hexdigest()

    def add_tag_to_file(self, file_path, category_id):
        if not os.path.isfile(file_path):
            print("Don't exist file with this path")
            raise
        path = Path(file_path)
        size = path.stat().st_size
        name = path.name
        hash_sum = self.get_file_hash_sha512(file_path)
        file_id = self.db.find_same_file(size, hash_sum)
        print("fileId =" + str(file_id))

        if not file_id:
            file_id = self.db.add_file(name, file_path, size, hash_sum)
            print("fileId =" + str(file_id))

        link_id = self.db.get_tag(file_id, category_id)
        print("link_id=" + str(link_id))
        if not link_id:
            print("addTag: fileId=" + str(file_id) + " categoryId=" + str(category_id))
            self.db.add_tag(file_id, category_id)
        self.retagging_file(file_id, file_path)

    def retagging_file(self, file_id, file_path):
        if not os.path.isfile(file_path):
            print("Don't exist file with this path")
            raise
        path = Path(file_path)
        file_name = path.name

        # 1. clear file_name from tags
        tag_template = '\[\[(.+)\]\]'
        regex = re.compile(tag_template)
        clear_file_name = regex.sub('', file_name)

        # 2. add new tags to file name
        categories = self.db.get_tags_by_file(file_id)
        prefix = '['
        for category in categories:
            prefix += '[' + category[1] + ']'
        prefix += ']'
        new_file_name = prefix + clear_file_name

        # 3. rename file
        path.rename(Path(path.parent, new_file_name))

        # 4. upd file_info in db
        self.db.upd_file_path(file_id, str(Path(path.parent, new_file_name)), new_file_name)

    @staticmethod
    def create_playlist(playlist_file_path, file_paths):
        root = et.Element("playlist")
        root.set("xmlns", "http://xspf.org/ns/0/")
        root.set("xmlns:vlc", "http://www.videolan.org/vlc/playlist/ns/0/")
        root.set("version", "1")

        track_list = et.Element("trackList")
        root.append(track_list)

        title = et.Element("title")
        title.text = str(playlist_file_path)
        root.append(title)

        extension = et.Element("extension")
        extension.set("application", "http://www.videolan.org/vlc/playlist/0")
        root.append(extension)

        index = 0
        for file_path in file_paths:
            # check that the file exists
            if not os.path.isfile(file_path):
                continue

            track = et.Element("track")

            location_elem = et.SubElement(track, 'location')
            location_elem.text = "file://" + str(file_path)

            extension_elem = et.SubElement(track, 'extension')
            extension_elem.set('application', 'http://www.videolan.org/vlc/playlist/0')

            id_elem = et.SubElement(extension_elem, 'vlc:id')
            id_elem.text = str(index)
            track_list.append(track)

            new_vlc_elem = et.Element('vlc:item')
            new_vlc_elem.set('tid', str(index))
            extension.append(new_vlc_elem)

            index += 1

        et.dump(root)
        tree = et.ElementTree(root)
        with open(playlist_file_path, 'wb') as f:
            tree.write(f)

    def export_to_playlist(self, category_id, playlist_file_path):
        file_paths = self.db.get_files_with_tag(category_id)
        self.create_playlist(playlist_file_path, file_paths)

    def add_category(self, name):
        return self.db.add_category(name)

    def disable_category(self, category_id):
        self.db.disable_category(category_id)

    def get_categories(self):
        return self.db.get_categories()

    def delete_tag(self, path, category_id):
        if not os.path.isfile(path):
            print("Don't exist file with this path")
            raise
        the_path = Path(path)
        size = the_path.stat().st_size
        hash_sum = self.get_file_hash_sha512(path)
        file_id = self.db.find_file_by_path(size, hash_sum, path)
        print("fileId =" + str(file_id))

        link_id = self.db.get_tag(file_id, category_id)
        print("link_id=" + str(link_id))
        if link_id:
            self.db.delete_tag(file_id, category_id)

        self.retagging_file(file_id, path)
