from random import randrange
X=[0 for i in range(10)]
Y=[0 for i in range(10)]
for t in range(10):
	X[t]=randrange(10)
	Y[t]=randrange(10)
print(X)
print(Y)

def summation(X):
	sum=0
	for x in X:
		sum=sum+x
	return sum
	
def mean(X):
	mean=summation(X)/len(X)
	return mean

def square(X):
	D =[x**2 for x in X]  
	return D
	
def mul(X,Y):
	d=[X[i]*Y[i] for i in range(len(X)))]
	return d

def correlation(X,Y):
	n=len(X)
	r=0
	r= (n*summation(mul(X,Y)) - summation(X)*summation(Y))/((n*summation(square(X))-(summation(X))**2)*(n*summation(square(Y))-(summation(Y))**2))**(0.5)
	print(r)
	
correlation(X,Y)