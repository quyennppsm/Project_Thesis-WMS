
da = {
    'carrier': [1, 0.5, 0],
    'age': [0, 0.5, 1],
    'cost': [0, 0.5, 1],
    'price': [1, 0.5, 0],
    'wage': [1, 0.5, 0],
    'day': [1, 0.5, 0]
}
db = {
    'carrier': [1, 0.5, 0],
    'age': [1, 0.5, 0],
    'cost': [0, 0.5, 1],
    'price': [0, 0.5, 1],
    'wage': [0, 0.5, 1],
    'day': [0, 0.5, 1]
}
da = pd.DataFrame(da, index=['high', 'medium', 'low'])
db = pd.DataFrame(db, index=['high', 'medium', 'low'])
print(da.loc['low','carrier'] + da.loc['low','age'] + da.loc['high','cost'] + da.loc['high','price'] + da.loc['high','wage'] + da.loc['high','day'])
print(db.loc['low','carrier'] + db.loc['low','age'] + db.loc['high','cost'] + db.loc['high','price'] + db.loc['high','wage'] + db.loc['high','day'])