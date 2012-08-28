import MySQLdb as mdb
import edd

# connect to mysql database

try:
    db=mdb.connect("localhost",user="distance",passwd="CosmicFlu2",db="EDDsDB")
except:
    print "There was an error in connecting to the database"
    exit(1)

print "EDD: generation of Leda related files"

answer=edd.query_yes_no("Would you like to query the database in Lion to regenerate Leda from scratch?",default="no")

if (answer=="yes"):
    answer=edd.query_yes_no("Are you sure you want to continue (it will take about 1 hour to finish) ?", default="no")
    if (answer=="yes"):
        edd.drop_leda_table(db)
        #edd.define_leda_columns(db)
        edd.create_leda_table(db)
        # Retrieve the list of pgc numbers
        print "Retrieving pgc list from database..."
        cur=db.cursor()
        cur.execute('SELECT pgc from pgc;')
        results=cur.fetchall()
        #print results
        pgcs = [x[0] for x in results]
        #print pgcs
        cur.close()
        edd.generate_kleda_orig_from_lyon(db,pgcs)
        edd.copy_leda_orig_int_leda(db)
        
answer=edd.query_yes_no("Would you like to generate a new leda bar file from the current kleda in the database?",default="no")
if (answer=="yes"):
    edd.generate_leda_bar_file(db)





