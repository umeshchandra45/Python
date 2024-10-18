print("hello world")

#variables are containers to store data
#in python variable name should start with a letter or _(underScore)
x=100
y=200

print(x+y)

a,b,c=1,5,'hello'
print(a,b,c,sep="")#nospace
print(a,b,c,sep='\n')#nextline
print(a,b,c,sep='\t')#tabspace


#swapping,python supports multi assingnment which supports assigning multiple values to multiple variables at same time
x=10
y=20

x,y=y,x
print(x)


#operators are symbols which performs operations between multiple variables
# Arethematic operators
x=5
y=2

print(x+y)
print(x/y)#2.5
print(x//y)#2
print(x%y)#1
print(x*y)#10
print(x**y)#25 5 square

#relational operators always returns boolean values > < <= >= != ==
print(x>y)
print(x>=y)
print(x<=y)
print(x!=y)
print(x==y)

#logical operators always returns a boolean values (and or not)
a=True
b=False

print(a and b)#false
print(a or b)#true

print(not b)#true

#concatination which will combine two values of same data types except bolean int and float

print(True+5)#6 python will consider true as 1)
print(False+5)#5 python will consider true as 0
#print("hi"+6)#it will give error

#formating the output

a=10
b="age"
c=500.3

print(a,b,c)
print("a is",a,"b is",b,"c is",c)
print("a is %d b is %s c is %g"%(a,b,c));print("a is {} b is {} c is {}".format(a,b,c))
print("a is {} b is {} c is {}".format(a,b,c))

#type casting

m=2
k=3.14
l="hi"
p=m*l
print(p)
n=int(k)
o=str(m)

print(type(n))
print(type(m))
print(type(o))


#taking input from user and by default python will consider every console as string

number=input("enter number")

number2=input("enter number2")
print(number+number2)

#to change user input values for required data types we should mention datatype before input keyword

number3=int(input("enter number"))
number4=int(input("enter number"))
number4=int(input("enter number"))
print(number3+number4)
#or
number=input("enter number")

number2=input("enter number2")

print(int(number)+float(number2))






