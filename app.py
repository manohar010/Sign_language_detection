from signLanguage.logger import logging
from signLanguage.exception import signException
import sys

try:
  ans = 2+3
  logging.info(ans)
  print(ans)

except Exception as e:
  logging.info(signException(e, sys))
  raise signException(e, sys)
