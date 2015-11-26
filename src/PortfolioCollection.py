__author__ = 'zmiller'

import imp
import os

from Common import Logger


class PortfolioCollection:
    def __init__(self):

        self.aPortfolios = []

        # recursively iterate over the directory that contains algorithm classes
        for root, dirs, files in os.walk("Algorithms"):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":

                    try:
                        # get an algorithm's file information
                        path = os.path.join(root, file)
                        info = os.stat(path)
                        oPortfolio = {"last_modified": info.st_mtime, "file_path": path, "file_name": file}

                        # TODO: we should also add a user identifier so we know who this algo belongs to

                        # get an algorithm's object instance
                        strAlgorithmClass = file.split(".")[0]
                        oModule = imp.load_source(strAlgorithmClass, path)
                        oAlgorithm = getattr(oModule, strAlgorithmClass)()

                        # store an algorithm's file info and obj instance
                        oPortfolio['algorithm'] = oAlgorithm
                        self.aPortfolios.append(oPortfolio)

                        del path, info, strAlgorithmClass, oModule

                    except Exception as e:
                        Logger.logError("Failed to instantiate {0}: {1}".format(str(file), str(e)))
                        Logger.logError("Failed to instantiate {0}: {1}".format(str(file), str(e)))

    def getCollection(self):
        """
        Returns an array of objects that contain an algorithm and the algorithms properties
        :return: array of objects
        """
        return self.aPortfolios

