import re

matric_number = "fuo/17/phy/6633"

x = matric_number.split('/')

for c in x[2:3]:
    if c != 'csi':
        print("It's not found")
    else:
        print("It's found")
# x = re.findall("[csi]", matric_number)
# if x in "fuo/17/phy/6645":
#     print("csi is not in the matric number")
# else:
#     print("csi is in the matric number")