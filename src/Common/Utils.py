__author__ = 'zmiller'



def chunk(aList, iChunkSize):
    """
    Divides a list into smaller chunked lists
    :param aList: the list to chunk
    :param iChunkSize: the size of a chunk
    :return: a list of lists representing chunks of the original list
    """

    aChunks = []
    iBeginChunk = 0
    iLenList = len(aList)
    while iBeginChunk < iLenList:
        iEndChunk = iBeginChunk + min(iChunkSize, iLenList)
        aChunks.append(aList[iBeginChunk:iEndChunk])
        iBeginChunk = iEndChunk

    return aChunks