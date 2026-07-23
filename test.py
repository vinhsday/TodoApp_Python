from datetime import *
str1 = datetime.strptime("2022 11 11", "%Y %m %d")
str2 = datetime.now().strftime("%Y %m %d")
str2 = datetime.strptime(datetime.now(), "%Y %m %d")
day = abs((str1 - str2).days)
print(day)