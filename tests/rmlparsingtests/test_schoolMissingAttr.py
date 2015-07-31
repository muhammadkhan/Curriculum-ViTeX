import sys
from os.path import pardir, sep
sys.path.append(pardir + sep + pardir + sep)
from src.resumeParser import RMLParser as rmlp
from src.cvitexexceptions import InvalidRMLFileException as badrml
if __name__ == "__main__":
  try:
    parsed = rmlp("schoolMissingAttr.rml")
    print("test success!")
  except badrml:
    e = sys.exc_info()[0]
    print("exception caught: " + str(e))
