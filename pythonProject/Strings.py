#string is a collection of charectors, you cannot change charector in string by index
a='umesh'
print(len(a))
print(a[2])
b='chandra'
c=a+' '+b
print(c)
for i in c:
    print(i,end=' ')
print('a' in c)
print('u' not in c)
print('umesh \nreddy')
