############################################
#       
# - read wrapper 
# - adds line search function
# - adds line count
#
import numpy as np
from FileRead import *
        
class FileRead(object):
    total_linenumber = -1
    
    def __init__(self, filename):
        self.f = open(filename,'r')
        self.filename       = filename
        self.linenumber     = 0
        self.current_line   = ""
    
    def linenumber(self):
        return self.linenumber
    
    def getline(self):
        return self.current_line
    
    def total_linenumber(self):
        if self.total_linenumber == -1:
            while self.readline() != "":
                pass
            self.restart()
        return self.total_linenumber
        
    def find_keyword_line(self,keyword,restart=False):
        if restart:
            self.restart()
        current_linenumber = self.linenumber
        searching = True
        while searching:
            line = self.readline()
            if keyword in line:
                return line
            if line == "":
                self.restart()
            if current_linenumber == self.linenumber:
                return ""
    
    def find_line_starting_with(self,startstr,restart=False):
        if restart:
            self.restart()
        current_linenumber = self.linenumber
        searching = True
        while searching:
            line = self.readline()
            if len(line) >= len(startstr):
                if (startstr == line[:len(startstr)]):
                    return line
            if line == "":
                self.restart()
            if current_linenumber == self.linenumber:
                return ""
    
    def linelist(self,delimiter=" "):
        llist 	= self.current_line.split(delimiter)
        return self.__reducelist(llist)
        
    def __reducelist(self,list_):
        list_ = [value for value in list_ if value != '']
        return list_
        
    def filename(self):
        return self.filename
    def restart(self):
        self.f.close()
        self.f = open(self.filename,'r')
        self.linenumber = 0
    def close(self):
        return self.f.close()
    def readline(self):
        line = self.f.readline()
        self.current_line = line
        if line != '':
            self.linenumber += 1
        else:
            self.total_linenumber = self.linenumber
        return line
    # to allow using in 'with' statements 
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    def read_xyz(self):
        data = list()
        line = self.readline()
        while line!='':
            ll = self.linelist()
            if len(ll)>=4 and ll[0]!='Atoms.':
                snapshot = list()
                while len(ll)>=4:
                    snapshot.append( [float(ft) for ft in ll[1:4]])
                    line = self.readline()
                    ll   = self.linelist()
                data.append(snapshot)
            line = self.readline()
        data = np.array(data)
        return data
