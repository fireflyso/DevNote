temp_set = set()
for line in open("1006.log"):
    temp_set.add(line.split('path')[-1][:-14])

for line in open("1007.log"):
    temp_set.add(line.split('path')[-1][:-14])

one_set = set()
for line in open("095.log"):
    one_set.add(line.split('path')[-1][:-14])

print(temp_set-one_set)

