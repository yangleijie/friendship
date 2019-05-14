from flask import Flask, render_template, request
import sqlite3 as sql
import sqlite3
import time
import datetime
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/enternew/')
def new_student():
    return render_template('staff.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
    if request.method == 'POST':
       try:
          name = request.form['nm']
          age = request.form['age']
          telNum = request.form['telNum']
          salary = request.form['salary']

          with sql.connect("database.db") as con:
             cur = con.cursor()

             cur.execute("INSERT INTO StaffInfo (name,age,telNum,salary) VALUES (?,?,?,?)",(name,age,telNum,salary))

             con.commit()
             msg = "Record successfully added"
       except:
          con.rollback()
          msg = "error in insert operation"

       finally:
          return render_template("result.html",msg = msg)
          con.close()
@app.route('/attendance/')
def attendance():
    CurrDate = time.strftime('%Y.%m.%d',time.localtime(time.time()))
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select name from StaffInfo")    
    rows = cur.fetchall()
 
    return render_template("StaffAttendance.html",CurrDate=CurrDate,rows = rows)
    con.close()
@app.route('/addAttendance',methods = ['POST', 'GET'])
def addAttendance():
    CurrDate = time.strftime('%Y.%m.%d',time.localtime(time.time()))
    if request.method == 'POST':
       try:
        
          check_boxlist = request.form.getlist('nm')
          with sql.connect("database.db") as con:
             cur = con.cursor()
             for  i in check_boxlist:

               cur.execute("INSERT INTO attendance (name,time,date) VALUES ('%s','%s','%s')"%(i,1,CurrDate))
       
               con.commit()
               message = "Record successfully added"
       except:
          con.rollback()
          message = "error in insert operation"

       finally:
          return render_template("RES.html",message=message)
          con.close()
     
@app.route('/list/')
def list():
    con = sql.connect("database.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from StaffInfo")

    rows = cur.fetchall()
    return render_template("list.html",rows = rows)
@app.route('/search/')
def search():
    FirstDay = datetime.date(datetime.date.today().year,datetime.date.today().month,1)
    CurrDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
   
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select name from StaffInfo")    
    rows = cur.fetchall()
 
    return render_template("SalarySearch.html",CurrDate=CurrDate,rows = rows,FirstDay=FirstDay)
    con.close()

@app.route('/SearchResult',methods = ['POST'])
def SearchResult():
    
    Staffname = request.form['staff']
   
    CurrDate = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    from_date = request.form['from']
    to_date = request.form['to']
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
   
  
    #X = cur.execute("select name, (c.time*c.salary)as amount from (select a.name, a.time,b.salary from (select name,sum (time) as time ,date from attendance where date between 'from_date' and 'to_date' group by name )  as a,(select name,salary from StaffInfo) as b where a.name = b.name) as c where name = 'Staffname' ")
    #X = cur.execute("select name,sum(time) from attendance group by name")
    #X=cur.execute("select name, salary*time from (select a.name,a.salary,b.time from  StaffInfo as a,(select name,sum(time)as time from attendance where date between '"+from_date+"' and ' "+to_date+" ' group by name)as b where a.name=b.name)where name=' "+Staffname+" ' ")
    #X=cur.execute("select name, salary*time as money from (select a.name,a.salary,b.time from  StaffInfo as a,(select name,sum(time)as time from attendance where date between '%s' and '%s' group by name)as b where a.name=b.name)where name='%s' "%(from_date,to_date,Staffname))
    X=cur.execute("select name, salary*time as money from (select a.name,a.salary,b.time from  StaffInfo as a,(select name,sum(time)as time from attendance where date between '%s' and '%s' group by name)as b where a.name=b.name)where name='%s' "%('2019.04.01','2019.04.30','张三'))
    amount = X.fetchone()
    print(amount)
  
    AA = amount[1]


    return render_template("SearchResult.html", AA=AA, Staffname=Staffname,from_date=from_date, to_date= to_date)
    con.commit()
    con.close()




@app.route('/init')
def init():
    conn = sqlite3.connect('database.db')
    print ("Opened database successfully")

    conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
    print ("Table created successfully")
    conn.close()
    return None
if __name__ == '__main__':
 
    app.run(debug = True)
