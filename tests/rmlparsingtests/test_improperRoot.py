from src.resumeParser import RMLParser as rmlp
from src.cvitexexceptions import InvalidRMLFileException as badrml
import sys
if __name__ == "__main__":
  try:
    parsed = rmlp("improperRoot.rml")
    print("test success!")
  except badrml:
    e = sys.exc_info()[0]
    print("exception caught: " + str(e))
