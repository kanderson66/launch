try:
    file = open('myfile.txt', 'r')
except FileNotFoundError:
    print('hi')

text1 = file.readline()
file.close()
text1 += file.readline()
print(text1)