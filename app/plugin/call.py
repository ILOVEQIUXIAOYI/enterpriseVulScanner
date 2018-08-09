"""
    Created by zltningx on 18-4-30.
"""

import os
from importlib import import_module

res_tmp = import_module('.plugin.plugins.crack_mssql', 'app')
res_tmp.run(1, 1)