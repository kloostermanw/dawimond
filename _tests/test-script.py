#!/usr/bin/env python3
import sys, os

sys.path.insert(0, os.path.abspath('..'))
from scripts.script import Script

critical = 0
warning = 0
script = 'process'
arguments = 'httpd,php artisan queue:work,/usr/bin/redis-server'

obj = Script.factory(script)
output = obj.run(warning, critical, arguments)

print(output)