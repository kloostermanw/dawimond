import shutil

from scripts.script import Script

class DiskUse(Script):

    def run(self, warning, critical, partition):
        total, used, free = shutil.disk_usage(partition)
        fltValue = round((used/total*100), 5)

        if (fltValue > float(critical)):
            intCode = self.STATUS_CRITICAL
        elif (fltValue > float(warning)):
            intCode = self.STATUS_WARNING
        else:
            intCode = self.STATUS_OK
        
        strMessage = "disk usage is " + str(round(fltValue, 2)) + "%"
        data = {"value": fltValue}

        return {"code": intCode, "data": data, "message": strMessage}
