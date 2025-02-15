import pandas as pd

# file = pd.read_csv('Copy of Govaly Withdraw Payment (Responses) - Paid Withdraw.csv')
# print(file.columns)
#
# print(file.tail(10))
#
# file['Vendor'] = file['Vendor'].ffill()
# file['Paid'] = file['Status'].ffill()
# file['Mailed'] = file['Mail'].ffill()
# file['Reduced'] = file['Website'].ffill()
# file['Invoice ID'] = file['Website'].ffill()
# file = file.drop(columns=['Time'])
#
# file.to_csv('filterWithdrawfile.csv', index=True)  # Saves with the index
#
# # print(file.tail(10))
# file2 = pd.read_csv('filterWithdrawfile.csv')
#
# grouped_by = file2.groupby('Vendor')['Earning(BDT)'].sum()
# print(grouped_by)
# print(file2.head(5))
file = pd.read_csv('deliveries_2025-02-12.csv')
print(file.columns)
print(file.head(5))