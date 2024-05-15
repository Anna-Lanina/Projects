import pandas
import math
import sklearn.ensemble
#import numpy

def green(string): return '\033[92m' + string + '\033[00m'
BEGIN_INFO = '\x1b[5;30;42m'
END_INFO = '\x1b[0m'

data_path = './data_sample.xlsx'
claims_data = pandas.read_excel(data_path, index_col = 0).sample(frac = 1)
print(green('Claims data:'))
print(claims_data)
print()

train_percent, test_percent = 0.6, 0.3
full_size = len(claims_data.index)
train_size, test_size = math.ceil(full_size * train_percent), math.ceil(full_size * test_percent)
val_size = full_size - train_size - test_size
print(BEGIN_INFO + 'Full size: ', full_size, 'Train size :', train_size, 'Test size :', test_size, 'Validation size :', val_size,  END_INFO)
print()
assert val_size > 0, 'WRONG SIZES SPLIT'
train_data = claims_data.iloc[0:train_size, :]
test_data = claims_data.iloc[train_size:train_size + test_size, :]
val_data = claims_data.iloc[train_size + test_size:, :]
print(green('Train data:'))
print(train_data)
print()
print(green('Test data:'))
print(test_data)
print()
print(green('Validation data:'))
print(val_data)
print()

train_data.dropna(inplace = True)
train_X, train_Y = train_data.iloc[:, :-1], train_data.iloc[:,-1]
train_X = train_X[['Mileage', 'VehickeKind']]
print(green('Train X:'))
print(train_X)
print(green('Train Y:'))
print(train_Y)

rfr_model = sklearn.ensemble.RandomForestRegressor()
rfr_model.fit(train_X.to_numpy().reshape(-1,1), train_Y.to_numpy())
