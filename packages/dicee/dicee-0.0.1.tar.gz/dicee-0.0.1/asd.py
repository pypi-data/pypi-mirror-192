def dot_product(x:list[float],y:list[float]):
    ### BEGIN SOLUTION
    return sum([x[i]*y[i] for i in range(len(x))])
    ### END SOLUTION


def matrix_vector_multiplication(X:list[list[float]],y:list[float])->list[float]:
    ### BEGIN SOLUTION
    return [dot_product(xi,y) for xi in X]
    ### END SOLUTION

def compute_squared_loss(y:list[float],yhat:list[float])->float:
    ### BEGIN SOLUTION
    squared_loss= [(y[i]-yhat[i])**2 for i in range(len(yhat))]
    return sum(squared_loss)/len(squared_loss)


def sigmoid_func(x:list[float]):
    e=2.71828
    ### BEGIN SOLUTION
    return [1 / (i+ e**-i) for i in x]
    ### END SOLUTION


print(sigmoid_func([-10,-5,-2,0.1,2]))
exit(1)


X=[[0, 0],[0,1],[1, 0],[1, 1]]
w=[1.0, 1.0]

print(matrix_vector_multiplication(X,w))
exit(1)
y=[0,1,1,1]

pred=[sum([x[i]*w[i] for i in range(len(x))]) for x in X]
squared_loss= [(y[i]-pred[i])**2 for i in range(len(pred))]
mean_squared_loss=sum(squared_loss)/len(squared_loss)
print(mean_squared_loss)

exit(1)

import numpy as np
X=np.array([[1, 2, 3],[1, -2, 3]])
w=np.array([[-2], [4], [5]])

print(X@w)


X=[[1, 2, 3],[1, -2, 3]]
w=[-2, 4, 5]
print([sum([x[i]*w[i] for i in range(len(x))]) for x in X])

exit(1)
### BEGIN SOLUTION
# Code

result=[]
for x in X:
    result.append(sum([x[i]*w[i] for i in range(len(w))]))


### END SOLUTION

print(result)

exit(1)


def sigmoid_func():
    x = [[0.1, 0.2, 3], [.001, -2.1, 3.3]]
    # Your code starts here
    result = []
    for xi in x:
        row = []
        for s in xi:
            row.append(1 / (1 + 2.71828 ** (-s)))
        result.append(row)
    # Your code ends here
    return result


result_sigmoid = sigmoid_func()
print(result_sigmoid)
import numpy as np
1/(1+np.exp(-np.array([[0.1, 0.2, 3], [.001, -2.1, 3.3]])))

exit(1)
exit(1)
x = [1, 2, 3]
y = [2, 4, 5]

x=[1, 2, 3]
y=[2, 4, 5]

result=0
for xi,yi in zip(x,y):
    result+=xi*xi


import numpy as np
print(np.array([[1, 2, 3],[1, -2, 3]]) @np.array([[-2], [4], [5]]))

exit(1)


result = matrix_product(x, y)
exit(1)




import matplotlib.pyplot as plt
import numpy as np

def exponential_function(x: np.ndarray, lam: float, ascending_order=True):
    # A sequence in exponentially decreasing order
    result = np.exp(-lam * x) / np.sum(np.exp(-lam * x))
    assert 0.999 < sum(result) < 1.0001
    result = np.flip(result) if ascending_order else result
    return result
N = 100
equal_weights = np.ones(N) / N
plt.plot(equal_weights, 'r', label="Growth rate 1.0")
plt.plot(exponential_function(np.arange(N), lam=0.1, ), 'c-', label="Growth rate 1.1")
plt.plot(exponential_function(np.arange(N), lam=0.05), 'g-', label="Growth rate 1.05")
plt.plot(exponential_function(np.arange(N), lam=0.025), 'b-', label="Growth rate 1.025")
plt.plot(exponential_function(np.arange(N), lam=0.01), 'k-', label="Growth rate 1.01")
plt.title(r'Ensemble coefficients with $\sum_i \mathbf{\alpha_i} =1$')
plt.xlabel(r'Epochs N')
plt.ylabel(r'Coefficients $\mathbf{\alpha_i}$')
plt.legend()
plt.savefig('ensemble_coefficients.pdf')
plt.show()