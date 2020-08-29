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
# YesterdayTarget = int(YesterdayTarget.YesterdayTarget)
#
# YSales = pd.read_sql_query(YSalesQuery, connection)
# YSales = int(YSales.YesterdaySales)
# Achievement = round((YSales/YesterdayTarget)*100, 2)

# print('Yesterday Target =', YesterdayTarget)
# print('Yesterday Sales =', YSales)
# print('Achievements = ', Achievement)


# # Doctor call
doctorcall = """ declare @lstdate varchar(8) = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112)
            declare @fstdate varchar(8) = CONVERT(varchar(8), dateadd(mm, -1,dateadd(dd, +1, eomonth(getdate()))),112)
            
            select 
            count (distinct case when CONVERT(varchar(8), DATEADD(day,0,visit_date),112)=@lstdate then doc_id end) as lastdaycount,
            count (distinct case when CONVERT(varchar(8), DATEADD(day,0,visit_date),112) between @fstdate and @lstdate 
            then doc_id end) as thismonthcount
            from sm_doctor_visit
            """
doctorcalldf = pd.read_sql_query(doctorcall, connection1)
lastdaycount = int(doctorcalldf.lastdaycount)
thismonthcount = int(doctorcalldf.thismonthcount)


## NSM wise sales, target and achievements
nsm = """declare @totaldays varchar(8) =  DateDiff(Day,getdate(),DateAdd(month,1,getdate()))

        select nsmname, SUM(daywisetarget) as daywisetarget, sum(lstdaysales) as lastdaysales,
        --(sum(lstdaysales)*100)/SUM(daywisetarget) as per
        case when SUM(daywisetarget) = 0 then 0 else (sum(lstdaysales)*100)/SUM(daywisetarget) end as per
         from
        (select nsmname, msotr, SUM(target)/@totaldays as daywisetarget from RFieldForce
        where yearmonth=202008
        group by NSMNAME, msotr) as nsm
        left join
        (select MSOTR, SUM(EXTINVMISC) as lstdaysales from oesalesdetails
        where transdate = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112) and transtype=1
        group by MSOTR) as sales
        on nsm.msotr=sales.msotr
        group by nsmname """

nsmdf = pd.read_sql_query(nsm, connection1)
print(nsmdf)

# # Chemist coverage
overall_chemist = """ declare @lstdate varchar(8) = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112)
        select SUM(totalcust) as totalchemist, SUM(covercust) as coverchemist, 
        (SUM(covercust)*100)/SUM(totalcust) as [percentage]
        from 
        (select audtorg,count(distinct idcust) as totalcust  from CustomerInformation
        where --audtorg='pbnskf' and 
        swactv=1
        group by AUDTORG) as totalcust
        left join
        (select audtorg, count(distinct customer) as covercust from OESalesDetails
        where transdate= @lstdate --and audtorg='pbnskf'
        group by AUDTORG) as covcust
        on totalcust.AUDTORG=covcust.AUDTORG"""

overall_chemistdf = pd.read_sql_query(overall_chemist, connection1)
print(overall_chemistdf)

lowest_chemist_coverage = """declare @lstdate varchar(8) = CONVERT(varchar(8), DATEADD(day,-1,getdate()),112)
        select top 5 branch.branch, SUM(totalcust) as totalcust, SUM(covercust) as covercust, 
        (SUM(covercust)*100)/SUM(totalcust) as per
        from 
        (select audtorg,count(distinct idcust) as totalcust  from CustomerInformation
        where --audtorg='pbnskf' and 
        swactv=1
        group by AUDTORG) as totalcust
        left join
        (select audtorg, count(distinct customer) as covercust from OESalesDetails
        where transdate= @lstdate --and audtorg='pbnskf'
        group by AUDTORG) as covcust
        on totalcust.AUDTORG=covcust.AUDTORG
        left join 
        (select RTRIM(branch) as branch,skf from BRANCHLIST) as branch
        on totalcust.AUDTORG=branch.skf
        group by branch.branch
        order by per asc
        """
lowest_chemist_coveragedf = pd.read_sql_query(lowest_chemist_coverage, connection1)
print(lowest_chemist_coveragedf)