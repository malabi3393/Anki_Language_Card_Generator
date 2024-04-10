import re
list = ['...','"bar','foo"']

for n in range(len(list)):
    new_word = re.sub(r"\.|\?|\s|\"", "", list[n])
    print(new_word)
    list[n] = new_word

print(list)

res = [i for i in list if i != '']
print("#------#")
print(res)
