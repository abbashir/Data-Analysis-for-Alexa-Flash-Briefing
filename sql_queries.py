import pandas as pd
import pyodbc as db

connection = db.connect('DRIVER={SQL Server};'
                        'SERVER=137.116.139.217;'
                        'DATABASE=ARCHIVESKF;'
                        'UID=sa;PWD=erp@123')

connection1 = db.connect('DRIVER={SQL Server};'
                        'SERVER=10.168.2.247;'
                        'DATABASE=DCR_MREPORTING;'
                        'UID=sa;PWD=erp')

# YTargetQuery = """DECLARE @day int
#                     set @day=right(convert(varchar(8),DATEADD(D,0,GETDATE()-1),112),2)
#                     select sum(target)/@day as YesterdayTarget from TDCL_BranchTarget
#                     where YEARMONTH= CONVERT(varchar(6), getdate(), 112) """
#
# YSalesQuery = """select  Sum(EXTINVMISC) as  YesterdaySales from OESalesDetails
#                     where TRANSDATE = convert(varchar(8),DATEADD(D,0,GETDATE()-1),112)
#                      """
# YesterdayTarget = pd.read_sql_query(YTargetQuery, connection)
# YesterdayTarget = str(int(YesterdayTarget.YesterdayTarget))
#
# YSales = pd.read_sql_query(YSalesQuery, connection)
# YSales = str(int(YSales.YesterdaySales))
# Achievement = str(round((int(YSales)/int(YesterdayTarget))*100, 2))
#
# # print('Yesterday Target =', YesterdayTarget)
# # print('Yesterday Sales =', YSales)
# # print('Achievements = ', Achievement)
#
# # # ------------------ Todays Sales Trend -----------------
# trendq = """ DECLARE @DATE AS SMALLDATETIME = GETDATE()
# DECLARE @FIRSTDATEOFMONTH AS SMALLDATETIME = CONVERT(SMALLDATETIME, CONVERT(CHAR(4),YEAR(@DATE)) + '-' + CONVERT(CHAR(2),MONTH(@DATE)) + '-01')
# DECLARE @YESTERDAY AS SMALLDATETIME = DATEADD(d,-1,@DATE)
# DECLARE @This_month as CHAR(6)= CONVERT(VARCHAR(6), GETDATE(), 112)
# DECLARE @FIRSTDATEOFMONTH_STR AS CHAR(8)=CONVERT(VARCHAR(10), @FIRSTDATEOFMONTH , 112)
# DECLARE @YESTERDAY_STR AS CHAR(8)=CONVERT(VARCHAR(10), @YESTERDAY , 112)
#
# DECLARE @TotalDaysInMonth as Integer=(SELECT DATEDIFF(DAY, getdate(), DATEADD(MONTH, 1, getdate())))
# DECLARE @totalDaysGone as integer =(SELECT DATEPART(DD, getdate())-1)
#
# Select
#     SUM(ISNULL(DAY_END_SALE.NET_SALE,0))/@totalDaysGone as Trend FROM
# (
# SELECT
# SUM(CASE WHEN TRANSTYPE=1 THEN EXTINVMISC ELSE 0 END) AS GROSS_SALE,
# SUM(CASE  WHEN TRANSTYPE=2 OR TRANSTYPE=4 THEN EXTINVMISC ELSE 0 END) AS NET_RETURN,
# SUM(EXTINVMISC) AS NET_SALE
# FROM OESALESDETAILS
# WHERE TRANSDATE BETWEEN  @FIRSTDATEOFMONTH_STR AND @YESTERDAY_STR GROUP BY MSOTR
# ) AS DAY_END_SALE
#                      """
# trend_df = pd.read_sql_query(trendq, connection)
# trend = str(int(trend_df['Trend']))
# print(trend)



# # Doctor call -------------------

doctorcall = """ declare @lstdate varchar(8) = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112)
            declare @fstdate varchar(8) = CONVERT(varchar(8), dateadd(mm, -1,dateadd(dd, +1, eomonth(getdate()))),112)

            select
            count (distinct case when CONVERT(varchar(8), DATEADD(day,0,visit_date),112)=@lstdate then doc_id end) as lastdaycount,
            count (distinct case when CONVERT(varchar(8), DATEADD(day,0,visit_date),112) between @fstdate and @lstdate
            then doc_id end) as thismonthcount
            from sm_doctor_visit
            """
import datetime
current_day = datetime.datetime.now()
current_day = current_day.strftime("%d")

doctorcalldf = pd.read_sql_query(doctorcall, connection1)
lastday_d_count = int(doctorcalldf.lastdaycount)
thismonth_d_count = int(doctorcalldf.thismonthcount)
averaged_call = round(thismonth_d_count/int(current_day)-1)

print('lastday_d_count',  lastday_d_count)
print('thismonth_d_count', thismonth_d_count)
print('averaged_call', averaged_call)

## NSM wise sales, target and achievements
# nsm = """
#         declare @totaldays varchar(8) =  DateDiff(Day,getdate(),DateAdd(month,1,getdate()))
#         select nsmname, SUM(daywisetarget) as daywisetarget, sum(lstdaysales) as lastdaysales,
#         --(sum(lstdaysales)*100)/SUM(daywisetarget) as per
#         case when SUM(daywisetarget) = 0 then 0 else (sum(lstdaysales)*100)/SUM(daywisetarget) end as PercentVal
#         from
#         (select nsmname, msotr, SUM(target)/@totaldays as daywisetarget from RFieldForce
#         where yearmonth= CONVERT(varchar(6), DATEADD(day,0,getdate()),112)
#         group by NSMNAME, msotr) as nsm
#         left join
#         (select MSOTR, SUM(EXTINVMISC) as lstdaysales from oesalesdetails
#         where transdate = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112) and transtype=1
#         group by MSOTR) as sales
#         on nsm.msotr=sales.msotr
#         group by nsmname
#         order by  PercentVal desc
#                 """
#
# nsmdf = pd.read_sql_query(nsm, connection)
# nsm_name = nsmdf.nsmname.tolist()
# nsm_ld_target = nsmdf.daywisetarget.tolist()
# nsm_ld_sales = nsmdf.lastdaysales.tolist()
# nsm_ld_achiv = nsmdf.PercentVal.tolist()
#
# print(nsm_name)
# print(nsm_ld_target)
# print(nsm_ld_sales)
# print(nsm_ld_achiv)

# # Chemist coverage
# overall_chemist = """ declare @lstdate varchar(8) = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112)
#         select SUM(totalcust) as totalchemist, SUM(covercust) as coverchemist,
#         (SUM(covercust)*100)/SUM(totalcust) as [percentage]
#         from
#         (select audtorg,count(distinct idcust) as totalcust  from CustomerInformation
#         where --audtorg='pbnskf' and
#         swactv=1
#         group by AUDTORG) as totalcust
#         left join
#         (select audtorg, count(distinct customer) as covercust from OESalesDetails
#         where transdate= @lstdate --and audtorg='pbnskf'
#         group by AUDTORG) as covcust
#         on totalcust.AUDTORG=covcust.AUDTORG """
#
# overall_chemistdf = pd.read_sql_query(overall_chemist, connection)
#
# total_chemist = int(overall_chemistdf.totalchemist)
# covered_chemist = int(overall_chemistdf.coverchemist)
# chemist_cov_per = int(overall_chemistdf.percentage)
#
# print('Total Chemist = ', total_chemist)
# print('Coverd Chemist =', covered_chemist)
# print('Coverd Percentage=', chemist_cov_per, '%')

# lowest_chemist_coverage = """declare @lstdate varchar(8) = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112)
#         select top 5 branch.branch, SUM(totalcust) as totalcust, SUM(covercust) as covercust,
#         (SUM(covercust)*100)/SUM(totalcust) as per
#         from
#         (select audtorg,count(distinct idcust) as totalcust  from CustomerInformation
#         where --audtorg='pbnskf' and
#         swactv=1
#         group by AUDTORG) as totalcust
#         left join
#         (select audtorg, count(distinct customer) as covercust from OESalesDetails
#         where transdate= @lstdate --and audtorg='pbnskf'
#         group by AUDTORG) as covcust
#         on totalcust.AUDTORG=covcust.AUDTORG
#         left join
#         (select RTRIM(branch) as branch,skf from BRANCHLIST) as branch
#         on totalcust.AUDTORG=branch.skf
#         group by branch.branch
#         order by per asc
#         """
# lowest_chemist_coveragedf = pd.read_sql_query(lowest_chemist_coverage, connection)
# print(lowest_chemist_coveragedf)