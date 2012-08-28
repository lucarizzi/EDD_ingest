import MySQLdb as mdb;
import angles;
try:
    db=mdb.connect("localhost",user="distance",passwd="CosmicFlu2",db="EDDsDB")
except:
    print "There was an error in connecting to the database"
    exit(1)

cursor=db.cursor()
cursor.execute("Select pgc,al2000,de2000 from kleda limit 1;")
results=cursor.fetchall()
db.commit()
#ra=["" if x[1] is None else angles.AlphaAngle(h=float(str(x[1]))) for x in results]
#dec=["" if x[2] is None else angles.DeltaAngle(d=float(str(x[2]))) for x in results]
#ra=[angles.AlphaAngle(h=float(str(x[1]))) for x in results]
#print results
#print ra

#cursor.executemany("INSERT into kleda (RA2000,DEC2000) values (%s,%s);",values)
#db.commit()
coords=[]
for x in results:
    #print x[0], x[1]
    ra=0 if x[1] is None else str(angles.AlphaAngle(h=float(str(x[1])))).replace("HH","").replace("MM","").replace("SS","").replace(" ","")
    dec=0 if x[2] is None else angles.AlphaAngle(h=float(str(x[2])))
    coords.append((ra,dec,x[0]))
cursor.execute("select * from kleda limit 1;")
results=cursor.fetchall()
joined=map (lambda x,y: x+y,results,coords)
print joined
#ra=[0.0 if x is None else angles.AlphaAngle(h=float(str(x[0]))) for x in results]
#dec=[0.0 if x is None else angles.DeltaAngle(d=float(str(x[1]))) for x in results]
#values=map (lambda x,y: (x,y), ra,dec)
#cursor.executemany("update kleda set RA2000=%s,DEC2000=%s where pgc='%s';", coords)
#db.commit()
cursor.close()
