import pandas as pd
import pyodbc as db

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=137.116.139.217;'
                        'DATABASE=ARCHIVESKF;'
                        'UID=sa;PWD=erp@123')

YTargetQuery = """DECLARE @day int 
                    set @day=right(convert(varchar(8),DATEADD(D,0,GETDATE()-1),112),2)
                    select sum(target)/@day as YesterdayTarget from TDCL_BranchTarget
                    where YEARMONTH= CONVERT(varchar(6), getdate(), 112) """

YSalesQuery = """select  Sum(EXTINVMISC) as  YesterdaySales from OESalesDetails
                    where TRANSDATE = convert(varchar(8),DATEADD(D,0,GETDATE()-1),112)
                     """

YesterdayTarget = pd.read_sql_query(YTargetQuery, connection)
YesterdayTarget = int(YesterdayTarget.YesterdayTarget)

YSales = pd.read_sql_query(YSalesQuery, connection)
YSales = int(YSales.YesterdaySales)
Achievement = str(round((YSales/YesterdayTarget)*100, 2)) + "%"

print('Yesterday Target =', YesterdayTarget)
print('Yesterday Sales =', YSales)
print('Achievements = ', Achievement)
