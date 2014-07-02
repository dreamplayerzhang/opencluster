"""
Definition of the various exceptions that are used in opencluster.
opencluster - Python Distibuted Computing API.
Copyright by www.cnlab.net
"""
import logging

import psutil

import configuration as conf
from Pyro4.errors import CommunicationError

logger = logging.getLogger(__name__)

class ServiceError(Exception):
    """Generic service errors."""
    pass

class CommunicateError(CommunicationError) :
    pass

class ClosetoOverError(Exception):
    """the errors related to memory used"""
    @classmethod
    def checkMemCapacity(cls):
        phymem = psutil.phymem_usage()
        safeMemoryPer = conf.Conf.getSafeMemoryPerNode()
        if phymem.percent > safeMemoryPer :
            e = ClosetoOverError("The capacity close to out of memory, please clear out some data!  used {0}% > {1}%".format(phymem.percent,safeMemoryPer))
            e.tm = float(phymem.total)
            e.fm = float(phymem.free)
            raise e
        return True
    def errorPrint(self) :
        return "total memory:%.2fM,free :%.2fM" % (self.tm/1000000l,self.fm/1000000l)

class RecallError(Exception):
    """
    A call could not be completed successfully,then a recall will be done again.
    """
    def __init__(self):
        super(RecallError, self).__init__("The call has not been returned yet, you cant repeat call!")
        self.recall = False
    def setRecall(self,recall):
        self.recall = recall

    def checkRecall(self):
        if self.recall :
            raise self
        return self.recall

    def tryRecall(self,inHouse):
        try :
            if self.checkRecall() :
                self.setRecall(True)
        except RecallError , e :
            logger.error("tryRecall",e)
            return -1
        return 0

class LeaderError(Exception):
    """
    the error of election of a leader in a park.
    """
    def __init__(self):
        super(LeaderError, self).__init__()
    def setServer(self, thisServer, leaderServer):
        self.thisServer = thisServer
        self.leaderServer = leaderServer;
    def getLeaderServer(self):
        return self.leaderServer


class FttpError(Exception):
    """ fttp operation related errors."""
    pass


