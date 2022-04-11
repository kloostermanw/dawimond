import os, subprocess

from scripts.script import Script

class Process(Script):

    def run(self, warning, critical, list):
        watch_list = (list.split(','))
        strMessage = ""
        intCode = self.STATUS_OK
        intValue = 0
        
        result = subprocess.run(
            ['/usr/bin/ps', '-eo', 'comm,args:120,pid'],
            stdout=subprocess.PIPE
        )
        
        process_list = result.stdout.decode("utf-8")

        for i in range(len(watch_list)):
            text = watch_list[i]
            found = False

            for line in process_list.split("\n\n"):
                # print(line)
                if text in line:
                    found = True
                    intValue = intValue + 1
            
            if (found == False):
                strMessage += text + " not running "
                intCode = self.STATUS_CRITICAL

        data = {"value": intValue}
        if (intCode == self.STATUS_OK):
            strMessage = "All processes are running."

        return {"code": intCode, "data": data, "message": strMessage}
