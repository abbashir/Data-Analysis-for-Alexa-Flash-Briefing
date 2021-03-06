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

YTargetQuery = """ DECLARE @day int
                    set @day=right(convert(varchar(8),DATEADD(D,0,GETDATE()-1),112),2)
                    select sum(target)/@day as YesterdayTarget from TDCL_BranchTarget
                    where YEARMONTH= CONVERT(varchar(6), getdate(), 112) """

# YSalesQuery = """select  Sum(EXTINVMISC) as  YesterdaySales from OESalesDetails
#                     where TRANSDATE = convert(varchar(8),DATEADD(D,0,GETDATE()-1),112)
#                      """
# YesterdayTarget = pd.read_sql_query(YTargetQuery, connection)
# YesterdayTarget = str(int(YesterdayTarget.YesterdayTarget))
#
# YSales = pd.read_sql_query(YSalesQuery, connection)
# YSales = str(int(YSales.YesterdaySales))
# Achievement = str(round((int(YSales)/int(YesterdayTarget))*100, 2))

# print('Yesterday Target =', YesterdayTarget)
# print('Yesterday Sales =', YSales)
# print('Achievements = ', Achievement)

# # # ------------------ Todays Sales Trend -----------------
# # trendq = """ DECLARE @DATE AS SMALLDATETIME = GETDATE()
# #             DECLARE @FIRSTDATEOFMONTH AS SMALLDATETIME = CONVERT(SMALLDATETIME, CONVERT(CHAR(4),YEAR(@DATE)) + '-' + CONVERT(CHAR(2),MONTH(@DATE)) + '-01')
# #             DECLARE @YESTERDAY AS SMALLDATETIME = DATEADD(d,-1,@DATE)
# #             DECLARE @This_month as CHAR(6)= CONVERT(VARCHAR(6), GETDATE(), 112)
# #             DECLARE @FIRSTDATEOFMONTH_STR AS CHAR(8)=CONVERT(VARCHAR(10), @FIRSTDATEOFMONTH , 112)
# #             DECLARE @YESTERDAY_STR AS CHAR(8)=CONVERT(VARCHAR(10), @YESTERDAY , 112)
# #
# #             DECLARE @TotalDaysInMonth as Integer=(SELECT DATEDIFF(DAY, getdate(), DATEADD(MONTH, 1, getdate())))
# #             DECLARE @totalDaysGone as integer =(SELECT DATEPART(DD, getdate())-1)
# #
# #             Select
# #                 SUM(ISNULL(DAY_END_SALE.NET_SALE,0))/@totalDaysGone as Trend FROM
# #             (
# #             SELECT
# #             SUM(CASE WHEN TRANSTYPE=1 THEN EXTINVMISC ELSE 0 END) AS GROSS_SALE,
# #             SUM(CASE  WHEN TRANSTYPE=2 OR TRANSTYPE=4 THEN EXTINVMISC ELSE 0 END) AS NET_RETURN,
# #             SUM(EXTINVMISC) AS NET_SALE
# #             FROM OESALESDETAILS
# #             WHERE TRANSDATE BETWEEN  @FIRSTDATEOFMONTH_STR AND @YESTERDAY_STR GROUP BY MSOTR
# #             ) AS DAY_END_SALE
# #         """
# #
# # trend_df = pd.read_sql_query(trendq, connection)
# # trend = str(int(trend_df['Trend']))
# # print(trend)
# #
# #
# #
# # # Doctor call -------------------
# #
# # doctorcall = """ declare @lstdate varchar(8) = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112)
# #             declare @fstdate varchar(8) = CONVERT(varchar(8), dateadd(mm, -1,dateadd(dd, +1, eomonth(getdate()))),112)
# #
# #             select
# #             count (distinct case when CONVERT(varchar(8), DATEADD(day,0,visit_date),112)=@lstdate then doc_id end) as lastdaycount,
# #             count (distinct case when CONVERT(varchar(8), DATEADD(day,0,visit_date),112) between @fstdate and @lstdate
# #             then doc_id end) as thismonthcount
# #             from sm_doctor_visit
# #             """
# #
# # import datetime
# # current_day = datetime.datetime.now()
# # current_day = current_day.strftime("%d")
# #
# # doctorcalldf = pd.read_sql_query(doctorcall, connection1)
# # lastday_d_count = int(doctorcalldf.lastdaycount)
# # thismonth_d_count = int(doctorcalldf.thismonthcount)
# # averaged_call = round(thismonth_d_count/int(current_day)-1)
# #
# # print('lastday_d_count',  lastday_d_count)
# # print('thismonth_d_count', thismonth_d_count)
# # print('averaged_call', averaged_call)
# #
# #
# #
# # # Chemist coverage
# # overall_chemist = """ declare @lstdate varchar(8) = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112)
# #         select SUM(totalcust) as totalchemist, SUM(covercust) as coverchemist,
# #         (SUM(covercust)*100)/SUM(totalcust) as [percentage]
# #         from
# #         (select audtorg,count(distinct idcust) as totalcust  from CustomerInformation
# #         where --audtorg='pbnskf' and
# #         swactv=1
# #         group by AUDTORG) as totalcust
# #         left join
# #         (select audtorg, count(distinct customer) as covercust from OESalesDetails
# #         where transdate= @lstdate --and audtorg='pbnskf'
# #         group by AUDTORG) as covcust
# #         on totalcust.AUDTORG=covcust.AUDTORG """
# #
# # overall_chemistdf = pd.read_sql_query(overall_chemist, connection)
# #
# # total_chemist = int(overall_chemistdf.totalchemist)
# # covered_chemist = int(overall_chemistdf.coverchemist)
# # chemist_cov_per = int(overall_chemistdf.percentage)
# #
# # print('Total Chemist = ', total_chemist)
# # print('Coverd Chemist =', covered_chemist)
# # print('Coverd Percentage =', chemist_cov_per, '%')
# #
# # #
# # lowest_chemist_coverage = """declare @lstdate varchar(8) = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112)
# #         select top 5 branch.branch, SUM(totalcust) as totalcust, SUM(covercust) as covercust,
# #         (SUM(covercust)*100)/SUM(totalcust) as per
# #         from
# #         (select audtorg,count(distinct idcust) as totalcust  from CustomerInformation
# #         where --audtorg='pbnskf' and
# #         swactv=1
# #         group by AUDTORG) as totalcust
# #         left join
# #         (select audtorg, count(distinct customer) as covercust from OESalesDetails
# #         where transdate= @lstdate --and audtorg='pbnskf'
# #         group by AUDTORG) as covcust
# #         on totalcust.AUDTORG=covcust.AUDTORG
# #         left join
# #         (select RTRIM(branch) as branch,skf from BRANCHLIST) as branch
# #         on totalcust.AUDTORG=branch.skf
# #         group by branch.branch
# #         order by per asc
# #         """
# # lowest_chemist_coveragedf = pd.read_sql_query(lowest_chemist_coverage, connection)
# # lowest_chemist_branch = lowest_chemist_coveragedf['branch'].tolist()
# # print(lowest_chemist_branch)
# # #
# # #
# # # # NSM wise sales, target and achievements
# # nsm = """
# #         declare @totaldays varchar(8) = DateDiff(Day,getdate(),DateAdd(month,1,getdate()))
# #         select nsmname, SUM(daywisetarget) as daywisetarget, sum(lstdaysales) as ldsales,
# #         case when SUM(daywisetarget) = 0 then 0 else (sum(lstdaysales)*100)/SUM(daywisetarget) end as PercentVal,
# #         case when SUM(lstdaysales) = 0 then 0 else (sum(salesReturn.ReturnVal)*-1*100)/SUM(lstdaysales) end as ReturnPercentVal
# #
# #         from
# #         (select nsmname, msotr, SUM(target)/@totaldays as daywisetarget from RFieldForce
# #         where yearmonth= CONVERT(varchar(6), DATEADD(day,0,getdate()),112)
# #         group by NSMNAME, msotr) as nsm
# #
# #         left join
# #         (select MSOTR, SUM(EXTINVMISC) as lstdaysales from oesalesdetails
# #         where transdate = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112) and transtype=1
# #         group by MSOTR) as sales
# #         on nsm.msotr=sales.msotr
# #
# #         left join
# #         (select MSOTR, SUM(EXTINVMISC) as ReturnVal from oesalesdetails
# #         where transdate = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112) and transtype=2
# #         group by MSOTR) as salesReturn
# #         on nsm.msotr=salesReturn.msotr
# #         group by nsmname
# #         order by  PercentVal desc, ReturnPercentVal desc
# #                 """
# #
# # nsmdf = pd.read_sql_query(nsm, connection)
# #
# # actual_nsm = nsmdf[nsmdf.daywisetarget > 1]
# # active_nsm = actual_nsm.daywisetarget.count()
# #
# # full_success_sales = actual_nsm[actual_nsm.PercentVal >= 100]
# # full_success_sales = full_success_sales.nsmname.tolist()
# # print('Hundred percent success = ', full_success_sales)
# #
# # less_than95p_sales = actual_nsm[actual_nsm.PercentVal < 95]
# # less_than95p_sales = less_than95p_sales.nsmname.tolist()
# # print('Less than 95% sales = ', less_than95p_sales)
# #
# # less_than95p_sales_with_low_return = actual_nsm[(actual_nsm['PercentVal'] <= 95) & (actual_nsm['ReturnPercentVal'] < 1)]
# # less_than95p_sales_with_low_return = less_than95p_sales_with_low_return.nsmname.tolist()
# # print('Less than 95% sales with les 1% return = ', less_than95p_sales_with_low_return)
# #
# # target_failed_1p_return = actual_nsm[(actual_nsm['PercentVal'] <= 95) & (actual_nsm['ReturnPercentVal'] >= 1)]
# # target_failed_1p_return = target_failed_1p_return.nsmname.tolist()
# # print('Make more than 1 % returns = ', target_failed_1p_return)
#
#
#
# # # ---------------------- Todays Query -----------------------------
#
# TTargetQuery = """DECLARE @day int
#                 set @day=right(convert(varchar(8),DATEADD(D,0,GETDATE()),112),2)
#                 select sum(target)/@day as TodayTarget from TDCL_BranchTarget
#                 where YEARMONTH= CONVERT(varchar(6), getdate(), 112) """
#
# TSalesQuery = """select  Sum(EXTINVMISC) as  TodaySales from OESalesDetails
#                     where TRANSDATE = convert(varchar(8),DATEADD(D,0,GETDATE()),112)
#                      """
# TodayTarget = pd.read_sql_query(TTargetQuery, connection)
# TodayTarget = str(int(TodayTarget.TodayTarget))
#
# TSales = pd.read_sql_query(TSalesQuery, connection)
# TSales = str(int(TSales.TodaySales))
# Achievement = str(round((int(TSales)/int(TodayTarget))*100, 2))
#
# print('Yesterday Target =', TodayTarget)
# print('Yesterday Sales =', TSales)
# print('Achievements = ', Achievement)
#
# # ------------------ Todays Sales Trend -----------------
# trendq = """ DECLARE @DATE AS SMALLDATETIME = GETDATE()
#             DECLARE @FIRSTDATEOFMONTH AS SMALLDATETIME = CONVERT(SMALLDATETIME, CONVERT(CHAR(4),YEAR(@DATE)) + '-' + CONVERT(CHAR(2),MONTH(@DATE)) + '-01')
#             DECLARE @YESTERDAY AS SMALLDATETIME = DATEADD(d,-1,@DATE)
#             DECLARE @This_month as CHAR(6)= CONVERT(VARCHAR(6), GETDATE(), 112)
#             DECLARE @FIRSTDATEOFMONTH_STR AS CHAR(8)=CONVERT(VARCHAR(10), @FIRSTDATEOFMONTH , 112)
#             DECLARE @YESTERDAY_STR AS CHAR(8)=CONVERT(VARCHAR(10), @YESTERDAY , 112)
#
#             DECLARE @TotalDaysInMonth as Integer=(SELECT DATEDIFF(DAY, getdate(), DATEADD(MONTH, 1, getdate())))
#             DECLARE @totalDaysGone as integer =(SELECT DATEPART(DD, getdate())-1)
#
#             Select
#                 SUM(ISNULL(DAY_END_SALE.NET_SALE,0))/@totalDaysGone as Trend FROM
#             (
#             SELECT
#             SUM(CASE WHEN TRANSTYPE=1 THEN EXTINVMISC ELSE 0 END) AS GROSS_SALE,
#             SUM(CASE  WHEN TRANSTYPE=2 OR TRANSTYPE=4 THEN EXTINVMISC ELSE 0 END) AS NET_RETURN,
#             SUM(EXTINVMISC) AS NET_SALE
#             FROM OESALESDETAILS
#             WHERE TRANSDATE BETWEEN  @FIRSTDATEOFMONTH_STR AND @YESTERDAY_STR GROUP BY MSOTR
#             ) AS DAY_END_SALE
#         """
#
# trend_df = pd.read_sql_query(trendq, connection)
# trend = str(int(trend_df['Trend']))
# print(trend)
#
#
#
# # Doctor call -------------------
#
# # doctorcall = """ declare @lstdate varchar(8) = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112)
# #             declare @fstdate varchar(8) = CONVERT(varchar(8), dateadd(mm, -1,dateadd(dd, +1, eomonth(getdate()))),112)
# #
# #             select
# #             count (distinct case when CONVERT(varchar(8), DATEADD(day,0,visit_date),112)=@lstdate then doc_id end) as lastdaycount,
# #             count (distinct case when CONVERT(varchar(8), DATEADD(day,0,visit_date),112) between @fstdate and @lstdate
# #             then doc_id end) as thismonthcount
# #             from sm_doctor_visit
# #             """
# #
# # import datetime
# # current_day = datetime.datetime.now()
# # current_day = current_day.strftime("%d")
# #
# # doctorcalldf = pd.read_sql_query(doctorcall, connection1)
# # lastday_d_count = int(doctorcalldf.lastdaycount)
# # thismonth_d_count = int(doctorcalldf.thismonthcount)
# # averaged_call = round(thismonth_d_count/int(current_day)-1)
# #
# # print('lastday_d_count',  lastday_d_count)
# # print('thismonth_d_count', thismonth_d_count)
# # print('averaged_call', averaged_call)
#
#
#
# # Chemist coverage
# overall_chemist = """ declare @lstdate varchar(8) = CONVERT(varchar(8), DATEADD(day,0,getdate()),112)
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
# print('Coverd Percentage =', chemist_cov_per, '%')
#
# #
# lowest_chemist_coverage = """
#         declare @lstdate varchar(8) = CONVERT(varchar(8), DATEADD(day,0,getdate()),112)
#         select top 5 branch.branch, SUM(totalcust) as totalcust, isnull(SUM(covercust), 0) as covercust,
#         isnull((SUM(covercust)*100)/SUM(totalcust), 0) as per
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
# lowest_chemist_branch = lowest_chemist_coveragedf['branch'].tolist()
# print(lowest_chemist_branch)
# #
# #
# # # NSM wise sales, target and achievements
# nsm = """
#         declare @totaldays varchar(8) = DateDiff(Day,getdate(),DateAdd(month,1,getdate()))
#
# select nsmname, isnull(SUM(daywisetarget), 0) as daywisetarget, isnull(sum(lstdaysales), 0) as todaysales,
# case when SUM(daywisetarget) = 0 then 0 else (sum(lstdaysales)*100)/isnull(SUM(daywisetarget),0) end as PercentVal,
# case when SUM(lstdaysales) = 0 then 0 else isnull((sum(salesReturn.ReturnVal)*-1*100)/SUM(lstdaysales),0) end as ReturnPercentVal
#
# from
# (select nsmname, msotr, SUM(target)/@totaldays as daywisetarget from RFieldForce
# where yearmonth= CONVERT(varchar(6), DATEADD(day,0,getdate()),112)
# group by NSMNAME, msotr) as nsm
#
# left join
# (select MSOTR, SUM(EXTINVMISC) as lstdaysales from oesalesdetails
# where transdate = CONVERT(varchar(8), DATEADD(day,0,getdate()),112) and transtype=1
# group by MSOTR) as sales
# on nsm.msotr=sales.msotr
#
# left join
# (select MSOTR, SUM(EXTINVMISC) as ReturnVal from oesalesdetails
# where transdate = CONVERT(varchar(8), DATEADD(day,0,getdate()),112) and transtype=2
# group by MSOTR) as salesReturn
# on nsm.msotr=salesReturn.msotr
# group by nsmname
# order by  PercentVal desc, ReturnPercentVal desc
#                 """
#
# nsmdf = pd.read_sql_query(nsm, connection)
#
# actual_nsm = nsmdf[nsmdf.daywisetarget > 1]
# active_nsm = actual_nsm.daywisetarget.count()
#
# full_success_sales = actual_nsm[actual_nsm.PercentVal >= 100]
# full_success_sales = full_success_sales.nsmname.tolist()
# print('Hundred percent success = ', full_success_sales)
#
# less_than95p_sales = actual_nsm[actual_nsm.PercentVal < 95]
# less_than95p_sales = less_than95p_sales.nsmname.tolist()
# print('Less than 95% sales = ', less_than95p_sales)
#
# less_than95p_sales_with_low_return = actual_nsm[(actual_nsm['PercentVal'] <= 95) & (actual_nsm['ReturnPercentVal'] < 1)]
# less_than95p_sales_with_low_return = less_than95p_sales_with_low_return.nsmname.tolist()
# print('Less than 95% sales with les 1% return = ', less_than95p_sales_with_low_return)
#
# target_failed_1p_return = actual_nsm[(actual_nsm['PercentVal'] <= 95) & (actual_nsm['ReturnPercentVal'] >= 1)]
# target_failed_1p_return = target_failed_1p_return.nsmname.tolist()
# print('Make more than 1 % returns = ', target_failed_1p_return)


# # -------- Day wise sales and target -------------------------
trend_df = pd.read_sql_query(""" select right(left(transdate, 10), 2) as date ,  SUM(EXTINVMISC) as sales 
,SUM(case when convert(varchar,DATETIME, 114) <= convert(varchar, getdate(), 114)  then EXTINVMISC end) as CurrentSales
from OESalesDetails 
where --convert(varchar,DATETIME, 114) <= convert(varchar, getdate(), 114) and 
left(TRANSDATE,6)=CONVERT(varchar(6), dateAdd(day,0,getdate()), 112)
group by transdate
order by right(left(transdate, 10), 2) """, connection)

from_yesterday_sales = sum(trend_df.sales.iloc[0: len(trend_df.sales) - 1])
from_current_time_sales = sum(trend_df.CurrentSales.iloc[0: len(trend_df.CurrentSales) - 1])
todays_current_sales = int(trend_df.CurrentSales.tail(1))
print('Todays current sales = ', todays_current_sales)

trend_percent = round((from_current_time_sales / from_yesterday_sales) * 100, 2)
trend_val = round((todays_current_sales * 100) / trend_percent, 2)

print('Trend Percent = ', trend_percent)
print(' Trends = ', trend_val)
