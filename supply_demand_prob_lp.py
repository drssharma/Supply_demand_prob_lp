#!/usr/bin/env python
# coding: utf-8

# ### Supply and Demand Linear Programming Problem

# #### Objective:

# The main objective of this project is to explain Supply and demanad in Linear programming problem in Python using Pulp library.  

# ### what is Optimization?

# “Optimization” comes from the same root as “optimal”, which means best. When you optimize something, you are “making it best”. But “best” can vary. If you’re a football player,you might want to maximize your running yards, and also minimize your fumbles. Both maximizing and minimizing are types of optimization problems. 
# Mathematically, an optimization problem consists of maximizing or minimizing a real function by systematically choosing input values from within an allowed set and computing the value of the function.

# ### The demand and supply problem:

# You want to minimize the cost of shipping goods from 2 different warehouses to 4 different customers. Each warehouse has a limited supply and each customer has a certain demand. We need to fulfil the demand of the customers by shipping products from given warehouses such that the overall cost of shipping is minimum and we are also able to satisfy the customer demands using limited supply available with each warehouse.

# ### Data
# Let's say it is a sports company which supplies its goods to its customers here distributors. 
# 1. The cost of shipping matrix for Warehouse i to Customer j is as follows. Each value can also be represented as Cij suggesting Cost C to ship from Warehouse i to Customer j.

#  ##### Cost of shipping($per product)
#              
# |           |custormer1|customer2|customer3|customer4|
# |:---------:| :--------:|  :-------:| :--------:|:-------:|
# |Warehouse1 |    1     |   3     |    0.5  |    0.4  |
# |Warehouse2 |   2.5    |   5     |    1.5  |    2.5  |

# 2. The customer demands and the warehouse availability is as follows.
# 
# #### Customer demands
# |customer1|35000|
# | :---:   | :--:|
# |customer2|22000|
# |customer3|18000|
# |customer4|30000|
# 
# #### Warehouses capacity
# |Warehouse1|60000|
# |:---:  |:---:|
# |Warehouse2|80000|

# #### Formulating the Problem:
# 1) Decision Variables
# 
# |      |customer1|customer2|customer3|customer4|
# |:---: |:---:    |:---:    |:---:    |:---:    |
# |Warehouse1|X11|X12|X13|X14|
# |Warehouse2|X21|X22|X23|X24|

# 2) Objective Function
# 
# Our objective function is defined as the overall cost of shipping these products and we need to minimize this overall cost. 
# 
# 
# ![image.png](attachment:image.png)
# 
# 3) Constraints
# 
# we will have 2 major types of constraints:
# 
# 3.1) Warehouse Constraints or Supply Constraints: These constraints basically say that the overall supply that will be done by each warehouse across all the 4 customers is less than or equal to the maximum availability/capacity of that warehouse.
# 
# ![image-2.png](attachment:image-2.png)

# 3.2) Customer Constraints or Demand Constraints:
# 
# ![image.png](attachment:image.png)

# how we can code this problem in Python and finding the minimum cost of supplying the goods. We will also get the optimal answer which will suggest how many goods should be supplied by which warehouse and to which customers.

# ### Importing libraries:

# In[1]:


from pulp import *
import pandas as pd
import numpy as np


# In[2]:


n_warehouses = 2
n_customers = 4

# Cost Matrix
cost_matrix = np.array([[1, 3, 0.5, 4],
                       [2.5, 5, 1.5, 2.5]])
# Demand Matrix
cust_demands = np.array([35000, 22000, 18000, 30000])

# Supply Matrix
warehouse_supply = np.array([60000, 80000])


# #### Model Initialization:

# In[4]:


model = LpProblem("Supply-Demand-Problem", LpMinimize)


# #### Defining Decision Variables:

# In[5]:


variable_names = [str(i)+str(j) for j in range(1, n_customers+1) for i in range(1, n_warehouses+1)]
variable_names.sort()
print("Variable Indices:", variable_names)


# In[6]:


DV_variables = LpVariable.matrix("X", variable_names, cat = "Integer", lowBound= 0 )
allocation = np.array(DV_variables).reshape(2,4)
print("Decision Variable/Allocation Matrix: ")
print(allocation)


# #### Objective Function:

# In[7]:


obj_func = lpSum(allocation*cost_matrix)
print(obj_func)
model +=  obj_func
print(model)


# Constraints:

# In[8]:


#Supply Constraints
for i in range(n_warehouses):
    print(lpSum(allocation[i][j] for j in range(n_customers)) <= warehouse_supply[i])
    model += lpSum(allocation[i][j] for j in range(n_customers)) <= warehouse_supply[i] , "Supply Constraints " + str(i)


# In[9]:


# Demand Constraints
for j in range(n_customers):
    print(lpSum(allocation[i][j] for i in range(n_warehouses)) >= cust_demands[j])
    model += lpSum(allocation[i][j] for i in range(n_warehouses)) >= cust_demands[j] , "Demand Constraints " + str(j)


# In[10]:


#Checking the model:
print(model)


# #### Run the model and check status:

# In[11]:


#model.solve()
model.solve(PULP_CBC_CMD())

status =  LpStatus[model.status]

print(status)


# #### Output the Objective Function Value and Decision Variables Value

# In[12]:


print("Total Cost:", model.objective.value())

# Decision Variables

for v in model.variables():
    try:
        print(v.name,"=", v.value())
    except:
        print("error couldnt find value")


# In[13]:


#Further, we can check how many products need to be supplied from each warehouse and hence how much capacity will be needed at each warehouse.
# Warehouse 1 and Warehouse 2 required capacity

for i in range(n_warehouses):
    print("Warehouse ", str(i+1))
    print(lpSum(allocation[i][j].value() for j in range(n_customers)))


# In[ ]:




