import os

print(os.popen("vcgencmd measure_temp").read())