import db_app
from pathlib import Path
import hashlib
import xml.etree.cElementTree as ET


class App:
    def __init__(self, db: db_app.DBApp):
        self.db = db

    def getFileHashSHA512(self, filePath):
        BUF_SIZE = 65536
        sha512 = hashlib.sha512()
        with open(filePath, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                sha512.update(data)
        return sha512.hexdigest()

    def addTagToFile(self, filePath, categoryId):
        path = Path(filePath)
        size = path.stat().st_size
        name = path.name
        hash = self.getFileHashSHA512(filePath)
        fileId = self.db.findSameFile(size, hash)
        print("fileId =" + str(fileId))

        if not fileId:
            fileId = self.db.addFile(name, filePath, size, hash)
            print("fileId =" + str(fileId))

        link_id = self.db.getTag(fileId, categoryId)
        print("link_id=" + str(link_id))
        if not link_id:
            print("addTag: fileId=" + str(fileId) + " categorId=" + str(categoryId))
            self.db.addTag(fileId, categoryId)

    def createPlaylist(self, playlistFilePath, filePaths):
        root = ET.Element("playlist")
        root.set("xmlns", "http://xspf.org/ns/0/")
        root.set("xmlns:vlc", "http://www.videolan.org/vlc/playlist/ns/0/")
        root.set("version", "1")

        trackList = ET.Element("trackList")
        root.append(trackList)

        title = ET.Element("title")
        title.text = str(playlistFilePath)
        root.append(title)

        extension = ET.Element("extension")
        extension.set("application", "http://www.videolan.org/vlc/playlist/0")
        root.append(extension)

        index = 0
        for filePath in filePaths:
            track = ET.Element("track")

            locationElem = ET.SubElement(track, 'location')
            locationElem.text = "file://" + str(filePath)

            extensionElem = ET.SubElement(track, 'extension')
            extensionElem.set('application', 'http://www.videolan.org/vlc/playlist/0')

            idElem = ET.SubElement(extensionElem, 'vlc:id')
            idElem.text = str(index)
            trackList.append(track)

            newVlcElem = ET.Element('vlc:item')
            newVlcElem.set('tid', str(index))
            extension.append(newVlcElem)

            index += 1

        ET.dump(root)
        tree = ET.ElementTree(root)
        with open(playlistFilePath, 'wb') as f:
            tree.write(f)

    def exportToPlaylist(self, categoryId, playlistFilePath):
        filePaths = self.db.getFilesWithTag(categoryId)
        self.createPlaylist(playlistFilePath, filePaths)

    def addCategory(self, name):
        return self.db.addCategory(name)

    def disableCategory(self, categoryId):
        self.db.disableCategory(categoryId)

    def getCategories(self):
        return self.db.getCategories()

    def deleteTag(self, path, categoryId):
        the_path = Path(path)
        size = the_path.stat().st_size
        hash = self.getFileHashSHA512(path)
        fileId = self.db.findFileByPath(size, hash, path)
        print("fileId =" + str(fileId))

        link_id = self.db.getTag(fileId, categoryId)
        print("link_id=" + str(link_id))
        if link_id:
            self.db.deleteTag(fileId, categoryId)
