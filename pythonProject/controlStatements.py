#conditional Statements if, if else, elif
#in python programming intendation is mandatory which mean we have to maintain code structure properly

age=20
if age>=10:
    print("elegible for vote",end=' ')
    print("elegible for vote")
else:
    print("not eligible for vote")

#example2
if True:print("eligeble")
else:print("not eligeble")

#example3 here in python 1 is considered as true
if 1:print("eligeble")
else:print("not elegible")

#example4 check whether the number is even or odd
num1=11
if num1//2==0:print("number is even")
else:print("number is odd")

#example5 ternary operator

num=11
print("even number") if num//2==0 else print("odd number")

#example6 execute multiple statements in single line

num1=13
{print("hi"),print("java")} if num>=14 else {print("hello"),print("java")}

#example7 for elif statement

weekday=2

if weekday==1:print("sunday")
elif weekday==2:print("monday")
elif weekday==3:print("tuesday")
elif weekday==4:print("wednesday")
elif weekday==5:print("thursday")
elif weekday==6:print("friday")

#assignment 1 check given number is positive or negative

num=0
if num>0:print("positive number")
else :print("negative number")

#assignment 2 check largest of 2 numbers

n1,n2=1,1
if n1>n2:print("n1 is greater number")
elif n2>n1:print("n2 is largest number")
else:print("both are equals")

#assignment 3 check largest of 3 numbers

p1,p2,p3=1,3,0

if p1>p2>p3:print("p1 is greatest number")
elif p2>p3:print("p2 is gretest number")
else:print("p3 is largest number")

#assignment 3 print week number if we provide weekname as input
weekdayname="monday1"
if weekdayname=="monday":
    print("day 2")
elif weekdayname=="tuesday":
    print("day 3")
else:print("invalid week name")

#looping statements
a='hello'
for i in range(5):
    print(a)
b="hi"
count=0
while count<10:
    print(b)
    count=count+1
#continue is a keyword that  will skip remaining steps in the loop for 1 iteration

n=0
while n<5:
    if n==3:
        n=n+1
        print("ab")
        continue
    print(n)#output 0 1 2 ab 4
    n=n+1

#break is a keyword that will use to break entire loop
m=0
while m<5:
    if m==2:
        m=m+1
        print("cd")
        break
    print(m)#output 0 1 cd
    m=m+1
#range
print(list(range(10)))
