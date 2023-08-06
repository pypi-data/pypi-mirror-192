from openpyxl import Workbook, load_workbook
import pandas as pd
import os
import report

AMOUNT_IN_VND_HEADER = "amount in vnd"
TRANSACTION_DATE_HEADER = "Ngày giao dịch"
CUSTOMER_ACCOUNT_NUMBER_HEADER = "Số tài khoản khách hàng"
TRANSACTION_NO_HEADER = "Lần giao dịch"
TRANSACTION_TYPE_HEADER = "Loại giao dịch"
AMOUNT_HEADER = "Tổng số tiền"
CURRENCY_HEADER = "Loại tiền"
REMARK_HEADER = "Ghi chú"
SOURCE_ACCOUNT_HEADER = "Tài khoản nguồn"
SOURCE_CUSTOMER_HEADER = "Tên chủ tài khoản nguồn"
DESTINATION_ACCOUNT_HEADER = "Tài khoản đích"
DESTINATION_CUSTOMER_HEADER = "Tên chủ tài khoản đích"
USD_TO_VND = 23500
CURRENCY_USD = "USD"
CURRENCY_VND = "VND"
TOTAL_INCOME = "(A)Doanh thu số tiền về"
INCOME_FROM_DIRECT_DEPOSIT = "+ Trực tiếp từ HĐKD, nộp tiền mặt (B)"
INCOME_FROM_CAPITAL_TRANSFER = "+ Điều vốn (C)"

def run():
    file_path = os.path.join(report.INPUT_FOLDER, "sao kê vnd.xlsx")
    dtf = pd.read_excel(file_path)
    dtf = dtf.iloc[:-1]
    file_path = os.path.join(report.INPUT_FOLDER, "sao kê usd.xlsx")
    dtf2 = pd.read_excel(file_path)
    dtf2 = dtf2.iloc[:-1]
    print(dtf)
    print(dtf2)
    dtf_total = pd.concat([dtf, dtf2])
    print(dtf_total)

    

    dtf_total[AMOUNT_IN_VND_HEADER] = dtf_total.apply(lambda row: round(float(row[AMOUNT_HEADER])*(USD_TO_VND if row[CURRENCY_HEADER] == CURRENCY_USD else 1)/1000000,3), axis=1)
    print(dtf_total[AMOUNT_IN_VND_HEADER])
    totalIncome = dtf_total[AMOUNT_IN_VND_HEADER].sum()
    print(f'Total income: {totalIncome}')

    customerName = dtf_total[SOURCE_CUSTOMER_HEADER][0:1][0]
    keywords = customerName.split(" ")
    keywords = keywords[-2:]
    keywords = " ".join(keywords)
    print(keywords)

    dtf_pricipal_movement = dtf_total[dtf_total[DESTINATION_CUSTOMER_HEADER].str.contains(keywords,na=False)]
    print(dtf_pricipal_movement)

    incomeFromCapitalTransfer = dtf_pricipal_movement[AMOUNT_IN_VND_HEADER].sum()
    incomeFromDirectDeposit = totalIncome - incomeFromCapitalTransfer
    print(f'Total income: {totalIncome}')
    print(f'B: {incomeFromDirectDeposit}')
    print(f'C: {incomeFromCapitalTransfer}')

    OUTPUT_ITEM_LABEL = "Chỉ tiêu (trđ)"

    outputDict = {
        OUTPUT_ITEM_LABEL: [TOTAL_INCOME, INCOME_FROM_DIRECT_DEPOSIT, INCOME_FROM_CAPITAL_TRANSFER],
        "2022": [totalIncome, incomeFromDirectDeposit, incomeFromCapitalTransfer]
    }

    outputDf = pd.DataFrame.from_dict(outputDict)

    output_file_path = os.path.join(report.OUTPUT_FOLDER,"output.xlsx")
    with pd.ExcelWriter(output_file_path) as excel_writer:
        dtf_total.to_excel(excel_writer,"Sheet1")
        outputDf.to_excel(excel_writer, "Sheet2")