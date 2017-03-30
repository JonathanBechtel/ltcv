import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')

#load customer data from website
d1 = pd.read_csv('C:\Users\Ohio\Documents\GitHub\Lifetime Customer Value\data\w_trans_1.csv')
d2 = pd.read_csv('C:\Users\Ohio\Documents\GitHub\Lifetime Customer Value\data\w_trans_2.csv')
d3 = pd.read_csv('C:\Users\Ohio\Documents\GitHub\Lifetime Customer Value\data\w_trans_3.csv')
d4 = pd.read_csv('C:\Users\Ohio\Documents\GitHub\Lifetime Customer Value\data\w_trans_4.csv')
d5 = pd.read_csv('C:\Users\Ohio\Documents\GitHub\Lifetime Customer Value\data\w_trans_5.csv')

#load transactions from Amazon
df2 = pd.read_csv('C:\Users\Ohio\Documents\GitHub\Lifetime Customer Value\data\Amazon_trans_1.csv')

#a little bit of data munging - clear, concatenate and re-order the data
d1 = d1[d1.columns[0:4]]
df1 = pd.concat([d1, d2, d3, d4, d5])
df1 = df1.rename(index=str, columns={'transaction_date': 'date', 'order_total': 'total', 'customer_first_name': 'first', 'customer_last_name': 'last'})
df1 = df1[['first', 'last', 'total']]
df1 = df1[df1.total != 0]

#slight data munging for 
df2 = df2.rename(index=str, columns={'buyer-name': 'name', 'item-price': 'total', 'sales-channel': 'channel'})
df2 = df2[df2.columns[1:4]]

#create new feature, re-order columns
df1['name'] = df1['first'] + " " + df1['last']
df1 = df1[['name', 'total']]

#combine dataframes
data = pd.concat([df1, df2])

#label channel according to place of origin
def get_channel(channel):
    if channel == "Amazon.com":
        return "Amazon"
    else:
        return "Website"
      
#add new feature  
data['channel'] = data.channel.apply(get_channel)
data = data[['name', 'total', 'channel']]
        
#create group obects
grouped = data['total'].groupby(data['name'])
w_grouped = df1['total'].groupby(df1['name'])
a_grouped = df2['total'].groupby(df2['name'])

#create a plots
plt.hold(True)

plt.figure(0)
x = grouped.count()
y = grouped.sum()
colors = np.random.randn(len(grouped))
area = grouped.count() * 10

plt.scatter(x, y, s=area, c=colors)
plt.title("Order Count and Total Value of E-commerce Customers")
plt.xlabel("Total Orders")
plt.ylabel("Value of All Orders")
plt.show()

plt.figure(1)
x2 = range(len(grouped))
y2 = grouped.sum().sort_values(ascending=False)
plt.bar(x2, y2, color='r')
plt.title("LTCV in Descending Order")
plt.ylabel("LTCV")
plt.show()