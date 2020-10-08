import pandas as pd
import pyodbc as db
import datetime
from calendar import monthrange

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=137.116.139.217;'
                        'DATABASE=ARCHIVESKF;'
                        'UID=sa;PWD=erp@123')


# # --------- Month target -----------------------------------------
target_df = pd.read_sql_query("""
            select sum(target) as MonthTarget from TDCL_BranchTarget
            where YEARMONTH = CONVERT(varchar(6), dateAdd(day,0,getdate()), 112) """, connection)


# # ------------- MTD Target --------------------------------------
date = datetime.datetime.now()
current_day = date.strftime("%d")
days_in_month = max(monthrange(int(date.strftime("%Y")), int(date.strftime("%m"))))




# ------ Trend ------------------------------
day_sales = pd.read_sql_query(""" select right(left(transdate, 10), 2) as date ,  SUM(EXTINVMISC) as sales
            ,SUM(case when convert(varchar,DATETIME, 114) <= convert(varchar, getdate(), 114)  then EXTINVMISC end) as CurrentSales
            from OESalesDetails
            where --convert(varchar,DATETIME, 114) <= convert(varchar, getdate(), 114) and
            left(TRANSDATE,6)=CONVERT(varchar(6), dateAdd(day,0,getdate()), 112)
            group by transdate
            order by right(left(transdate, 10), 2) """, connection)

total_target = int(target_df.MonthTarget)
mtd_target = int( (total_target/int(days_in_month)) * int(current_day))
mtd_sales = int(sum(day_sales.sales))
mtd_achiv = round((mtd_sales/mtd_target) * 100, 2)


from_yesterday_sales = sum(day_sales.sales.iloc[0: len(day_sales.sales) - 1])
from_current_time_sales = sum(day_sales.CurrentSales.iloc[0: len(day_sales.CurrentSales) - 1])
todays_current_sales = int(day_sales.CurrentSales.tail(1))

trend_percent = round((from_current_time_sales / from_yesterday_sales) * 100, 2)

mtd_trend_val  = int((sum(day_sales.sales) * 100) / trend_percent)

# print('Months Target = ', total_target)
# print('MTD target    = ', mtd_target)
# print('MTD sales     = ', mtd_sales)
# print('MTD achiv %   = ', mtd_achiv)
# print('MTD Trend     = ', mtd_trend_val)
# print('Trend Percent = ', trend_percent)

# print('\n -----------------------------------------------------')

#  # ---------- Yesterday Summary -------------------------------
yesterday_target = int(total_target/days_in_month)
yesterday_sales = int(day_sales.sales[day_sales.sales.index[-2]])
yesterday_achiv = round((yesterday_sales/yesterday_target) * 100, 2)
yesterday_current_time_sales = int(day_sales.CurrentSales[day_sales.CurrentSales.index[-2]])
yesterday_trend = int((yesterday_current_time_sales * 100) / trend_percent)

# print('Yesterday Target = ', yesterday_target)
# print('Yesterday Sales  = ', yesterday_sales)
# print('Yesterday Achiv% = ', yesterday_achiv)
# print('This time Yesterday Trend was  = ', yesterday_trend)
#
# print('\n -----------------------------------------------------')

# # ----------- Todays Summary ----------------------------------
todays_target = int(total_target/days_in_month)
todays_sales = int(day_sales.CurrentSales.tail(1))
todays_achiv = round((todays_sales/todays_target)* 100, 2)
todays_trend_val = int((todays_current_sales * 100) / trend_percent)
willbe_todays_achiv = round((todays_trend_val/todays_target)*100, 2)
# print('Todays Target     =', todays_target)
# print('Todays Sales      =', todays_current_sales)
# print('Todays Achivment  =', todays_achiv)
# print('Todays Trends val = ', todays_trend_val)

