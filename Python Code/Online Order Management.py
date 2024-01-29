import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime


scope = ['https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_name('dry-age-beef-order-management-0a86941f1462.json', scope)
client = gspread.authorize(creds)


doc_id = "1gWPYcCK3SGYaWMqHqM-w1kXTA_Q37q0Mm947IqXn5E0"
sheet = client.open_by_key(doc_id).sheet1
data = sheet.get_all_records()


df = pd.DataFrame(data)


df[df.columns[0]] = df[df.columns[0]].str.replace('上午', 'AM').str.replace('下午', 'PM')
date_format = '%Y/%m/%d %p %I:%M:%S'  
df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], format=date_format, errors='coerce')


start_date = datetime(2024, 1, 1)
end_date = datetime(2024, 12, 31)


df = df[(df[df.columns[0]] >= start_date) & (df[df.columns[0]] <= end_date)]


original_date_format = '%Y/%m/%d %p %I:%M:%S'
df[df.columns[0]] = df[df.columns[0]].dt.strftime(original_date_format).str.replace('AM', '上午').str.replace('PM', '下午')


column_prefixes = {
    4: "Short Ribs ",  
    5: "Short Ribs ",  
    6: "Short Ribs ",  
    7: "Regular ",     
    8: "Regular ",     
    9: "Regular ",     
    10: "Sinew Removed ",  
    11: "Sinew Removed ",  
    12: "Sinew Removed "   
}


for index, prefix in column_prefixes.items():
    df.columns.values[index] = prefix + df.columns.values[index]

df.fillna(0, inplace=True)


excel_filename = 'Order - EN.xlsx'
df.to_excel(excel_filename, index=False, engine='openpyxl')

print(f'The Online Order has been successfully written to the local Excel file：{excel_filename}')
