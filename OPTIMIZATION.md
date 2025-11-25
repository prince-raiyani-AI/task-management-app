# Optimization Techniques

This document outlines optimization strategies for Python scripts and database queries, specifically within the context of a Flask-SQLAlchemy application.

## 1. Script Optimization

### List Comprehensions vs. Loops
List comprehensions are generally faster and more readable (Pythonic) than traditional for-loops for creating lists.

**Unoptimized (Loop):**
```python
squared_numbers = []
for n in range(1000000):
    squared_numbers.append(n * n)
```

**Optimized (List Comprehension):**
```python
squared_numbers = [n * n for n in range(1000000)]
```
*Reasoning*: List comprehensions are optimized at the C level in CPython, avoiding the overhead of repeated `append` method calls.

## 2. Query Optimization

### The N+1 Problem
The N+1 problem occurs when the application executes one initial query to fetch a list of records (N) and then executes an additional query for each record to fetch related data.

**Unoptimized (Lazy Loading):**
```python
users = User.query.all()  # 1 Query
for user in users:
    print(user.tasks)     # N Queries (one per user)
```
*Total Queries*: 1 + N

**Optimized (Eager Loading):**
```python
from sqlalchemy.orm import joinedload

users = User.query.options(joinedload(User.tasks)).all() # 1 Query with JOIN
for user in users:
    print(user.tasks)     # 0 extra queries
```
*Total Queries*: 1

*Reasoning*: Using `joinedload` performs a SQL JOIN, fetching all necessary data in a single round-trip to the database, significantly reducing latency.
