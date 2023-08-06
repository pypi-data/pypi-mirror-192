#from .txt import (txt,numbers_in_txt)
from .version import get_version

if get_version()=='1.0.1':
    pass
else:
    print("Please improve this model in to 1.0.1.")
    pass

__all__=['txt','plot']
