import os
import sys
import urllib2
import angles
import EDD_config

def create_tables(db):
  cur=db.cursor()
  cur.execute("CREATE TABLE ktables ( \
   dbtable varchar(255) primary key not null, \
   category varchar(255) , \
   bibcode varchar(19) , \
   catalog varchar(255) , \
   abbreviation varchar(255) , \
   description varchar(400) , \
   md5sum varchar(32) , \
   file varchar(255));")
  db.commit()
   
  cur.execute("CREATE TABLE kcolumns (\
   `dbtable` character varying(255) not null, \
   `tabcolumn` character varying(255) not null, \
   `units` character varying(255) , \
   `description` character varying(300) , \
   `ucd` character varying(255) , \
   `justification` character(2) , \
   `format` character varying(255)  );")
  db.commit()

  cur.execute("CREATE TABLE pgc (\
   `pgc` integer not null);")
  db.commit()


def define_leda_columns(db):

  leda_columns=[]
  leda_columns.append((" kleda","al1950             ","hour            ","RA 1950 (hours decimal value)   ","\N                              ","r            ","%10.5f"))
  leda_columns.append((" kleda","de1950             ","deg             ","DEC 1950 (degrees decimal value)     ","\N                              ","r            ","%10.5f"))
  leda_columns.append((" kleda","al2000             ","hour            ","RA 2000 (hours decimal value)  ","\N                              ","r            ","%10.5f"))
  leda_columns.append((" kleda","de2000             ","deg             ","DEC 2000 (degrees decimal value)  ","\N                              ","r            ","%10.5f"))
  leda_columns.append((" kleda","l2                 ","deg             ","Galactic longitude    ","\N                              ","r            ","%10.5f"))
  leda_columns.append((" kleda","b2                 ","deg             ","Galactic latitude    ","\N                              ","r            ","%10.5f"))
  leda_columns.append((" kleda","sgl                ","deg             ","Galactic longitude      ","\N                              ","r            ","%10.5f"))
  leda_columns.append((" kleda","sgb                ","deg             ","Galactic latitude        ","\N                              ","r            ","%10.5f"))
  leda_columns.append((" kleda","t                  ","\N              ","Morphological type code      ","\N                              ","r            ","%5.1f"))
  leda_columns.append((" kleda","e_t                ","\N              ","Actual error on t            ","\N                              ","r            ","%5.1f"))
  leda_columns.append((" kleda","logr25             ","\N              ","log of axis ratio (major axis/minor axis)      ","\N                              ","r            ","%8.2f"))
  leda_columns.append((" kleda","e_logr25           ","\N              ","log of axis ratio (major axis/minor axis)    ","\N                              ","r            ","%8.2f"))
  leda_columns.append((" kleda","mg2                ","mag             ","Central Lick Mg2 index     ","\N                              ","r            ","%6.4f"))
  leda_columns.append((" kleda","incl               ","deg             ","Inclination between line of sight and polar axis    ","\N                              ","r            ","%6.1f"))
  leda_columns.append((" kleda","lambda             ","\N              ","Luminosity index       ","\N                              ","r            ","%6.2f"))  
  leda_columns.append((" kleda","bri25              ","mag/arcsec2     ","Mean surface brightness within isophote 25    ","\N                              ","r            ","%6.2f"))
  leda_columns.append((" kleda","vrot               ","km/s            ","Maximum rotation velocity corrected for inclination      ","\N                              ","r            ","%6.1f"))
  leda_columns.append((" kleda","e_vrot             ","km/s            ","Actual error on vrot       ","\N                              ","r            ","%6.1f"))
  leda_columns.append((" kleda","hic                ","mag             ","21-cm index bt-m21c in magnitude     ","\N                              ","r            ","%6.2f"))
  leda_columns.append((" kleda","lc                 ","\N              ","Luminosity class code      ","src.class.luminosity            ","r            ","%5.1f"))
  leda_columns.append((" kleda","e_lc               ","\N              ","Actual error on lc       ","stat.error;src.class.luminosity ","r            ","%5.1f"))
  leda_columns.append((" kleda","logd25             ","log(0.1 arcmin) ","log of apparent diameter (d25 in 0.1 arcmin)    ","phys.angSize.smajAxis           ","r            ","%8.2f"))
  leda_columns.append((" kleda","e_logd25           ","log(0.1 arcmin) ","Actual error on logd25     ","stat.error;phys.angSize.smajAxis","r            ","%8.2f"))
  leda_columns.append((" kleda","pa                 ","deg             ","Major axis position angle (North Eastwards)     ","pos.posAng                      ","r            ","%6.1f"))
  leda_columns.append((" kleda","brief              ","mag/arcsec2     ","Mean effective surface brightness       ","phot.mag.sb;stat.mean           ","r            ","%6.2f"))
  leda_columns.append((" kleda","e_brief            ","mag/arcsec2     ","Actual error on brief                ","stat.error;phot.mag.sb;stat.mean","r            ","%6.2f"))
  leda_columns.append((" kleda","bt                 ","mag             ","Total B-magnitude         ","phot.mag;em.opt.B               ","r            ","%6.2f"))
  leda_columns.append((" kleda","e_bt               ","mag             ","Actual error on bt       ","stat.error;phot.mag;em.opt.B    ","r            ","%6.2f"))
  leda_columns.append((" kleda","it                 ","mag             ","Total I-magnitude           ","phot.mag;em.opt.I               ","r            ","%6.2f"))
  leda_columns.append((" kleda","e_it               ","mag             ","Actual error on it        ","stat.error;phot.mag;em.opt.I    ","r            ","%6.2f"))
  leda_columns.append((" kleda","ubt                ","mag             ","Total U-B color             ","phot.color;em.opt.U;em.opt.B    ","r            ","%6.2f"))
  leda_columns.append((" kleda","bvt                ","mag             ","Total B-V color         ","phot.color;em.opt.B;em.opt.V    ","r            ","%6.2f"))
  leda_columns.append((" kleda","ube                ","mag             ","Effective U-B color         ","phot.color;em.opt.U;em.opt.B    ","r            ","%6.2f"))
  leda_columns.append((" kleda","bve                ","mag             ","Effective B-V color      ","phot.color;em.opt.B;em.opt.V    ","r            ","%6.2f"))
  leda_columns.append((" kleda","vmaxg              ","km/s            ","Apparent maximum rotation velocity of gas   ","src.veloc.rotat;stat.max        ","r            ","%6.1f"))
  leda_columns.append((" kleda","e_vmaxg            ","km/s            ","Actual error on vmaxg      ","stat.error;src.veloc.dispersion ","r            ","%6.1f"))
  leda_columns.append((" kleda","vmaxs              ","km/s            ","Apparent maximum rotation velocity of stars   ","src.veloc.rotat;stat.max        ","r            ","%6.1f"))
  leda_columns.append((" kleda","e_vmaxs            ","km/s            ","Actual error on vmaxs    ","stat.error;src.veloc.dispersion ","r            ","%6.1f"))
  leda_columns.append((" kleda","vdis               ","km/s            ","Central velocity dispersion       ","src.veloc.dispersion            ","r            ","%6.1f"))
  leda_columns.append((" kleda","e_vdis             ","km/s            ","Actual error on vdis     ","stat.error;src.veloc.dispersion ","r            ","%6.1f"))
  leda_columns.append((" kleda","e_mg2              ","mag             ","Actual error on mg2      ","stat.error                      ","r            ","%6.4f"))
  leda_columns.append((" kleda","m21                ","mag             ","21-cm line flux in magnitude     ","phot.mag;em.line.HI             ","r            ","%6.2f"))
  leda_columns.append((" kleda","e_m21              ","mag             ","Actual error on m21      ","stat.error;phot.mag;em.line.HI  ","r            ","%6.2f"))
  leda_columns.append((" kleda","mfir               ","mag             ","Far infrared magnitude     ","phot.mag;em.IR                  ","r            ","%6.2f"))
  leda_columns.append((" kleda","vrad               ","km/s            ","Heliocentric radial velocity (cz) from radio measurement     ","src.veloc;em.radio              ","r            ","%8.0f"))
  leda_columns.append((" kleda","e_vrad             ","km/s            ","Actual error on vrad      ","stat.error;src.veloc;em.radio   ","r            ","%8.0f"))
  leda_columns.append((" kleda","vopt               ","km/s            ","Heliocentric radial velocity (cz) from optical measurement        ","src.veloc;em.opt                ","r            ","%8.0f"))
  leda_columns.append((" kleda","e_vopt             ","km/s            ","Actual error on vopt        ","stat.error;src.veloc;em.opt     ","r            ","%8.0f"))
  leda_columns.append((" kleda","v                  ","km/s            ","Mean Heliocentric radial velocity (cz)     ","src.veloc                       ","r            ","%8.0f"))
  leda_columns.append((" kleda","e_v                ","km/s            ","Actual error on v      ","stat.error;src.veloc            ","r            ","%8.0f"))
  leda_columns.append((" kleda","ag                 ","mag             ","Galactic extinction in B-band    ","phys.absorption.gal;em.opt.B    ","r            ","%6.2f"))
  leda_columns.append((" kleda","ai                 ","mag             ","Internal extinction due to inclination in B-band   ","phys.absorption;em.opt.B        ","r            ","%6.2f"))
  leda_columns.append((" kleda","a21                ","mag             ","21-cm self absorption       ","phys.absorption;em.line.HI      ","r            ","%6.2f"))
  leda_columns.append((" kleda","logdc              ","log(0.1 arcmin) ","log of apparent corrected diameter (dc in 0.1 arcmin)          ","phys.angSize.smajAxis           ","r            ","%8.2f"))
  leda_columns.append((" kleda","btc                ","mag             ","Total apparent corrected B-magnitude      ","phot.mag;em.opt.B               ","r            ","%6.2f"))
  leda_columns.append((" kleda","itc                ","mag             ","Total apparent corrected I-magnitude         ","phot.mag;em.opt.I               ","r            ","%6.2f"))
  leda_columns.append((" kleda","ubtc               ","mag             ","Total apparent corrected U-B color     ","phot.color;em.opt.U;em.opt.B    ","r            ","%6.2f"))
  leda_columns.append((" kleda","bvtc               ","mag             ","Total apparent corrected B-V color       ","phot.color;em.opt.B;em.opt.V    ","r            ","%6.2f"))
  leda_columns.append((" kleda","m21c               ","mag             ","Corrected 21-cm line flux in magnitude     ","phot.mag;em.line.HI             ","r            ","%6.2f"))
  leda_columns.append((" kleda","vlg                ","km/s            ","Radial velocity (cz) with respect to the Local Group      ","src.veloc                       ","r            ","%8.0f"))
  leda_columns.append((" kleda","vgsr               ","km/s            ","Radial velocity (cz) with respect to the GSR    ","src.veloc                       ","r            ","%8.0f"))
  leda_columns.append((" kleda","vvir               ","km/s            ","Radial velocity (cz) corrected for LG infall onto Virgo       ","src.veloc                       ","r            ","%8.0f"))
  leda_columns.append((" kleda","v3k                ","km/s            ","Radial velocity (cz) with respect to the CMB radiation         ","src.veloc                       ","r            ","%8.0f"))
  leda_columns.append((" kleda","modz               ","\N             ","\N   ","\N            ","r            ","%6.2f"))
  leda_columns.append((" kleda","mod0               ","\N             ","\N    ","\N            ","r            ","%6.2f"))
  leda_columns.append((" kleda","mabs               ","mag             ","Absolute B-band magnitude    ","phys.magAbs;em.opt.B            ","r            ","%6.2f"))                                    
  leda_columns.append((" kleda","objname            ","\N              ","Principal name ","\N                              ","r            ","%30s"))
  leda_columns.append((" kleda","objtype            ","\N              ","Type of object (G=galaxy; S=Star ...)   ","\N                              ","r            ","%7s"))
  leda_columns.append((" kleda","type               ","\N              ","Morphological type      ","src.morph.type                  ","r            ","%5s"))
  leda_columns.append((" kleda","bar                ","\N              ","Barred galaxy (B)   ","\N                              ","r            ","%4s"))
  leda_columns.append((" kleda","ring               ","\N              ","Galaxy with ring (R)     ","\N                              ","r            ","%5s"))
  leda_columns.append((" kleda","multiple           ","\N              ","Multiple galaxy (M)     ","meta.code.multip                ","r            ","%9s"))
  leda_columns.append((" kleda","compactness        ","\N              ","Compact (C) or diffuse (D)      ","\N                              ","r            ","%14s"))
  leda_columns.append((" kleda","angclass           ","\N              ","ANGCLASS      ","\N                              ","r            ","%14s"))
  leda_columns.append((" kleda","pgc                ","\N              ","PGC number   ","\N                              ","r            ","%06d"))

  # we are missing mucin mup and lgg
  
  cur=db.cursor()
  cur.executemany("INSERT INTO kcolumns VALUES (%s,%s,%s,%s,%s,%s,%s)",  leda_columns)
  db.commit()

def create_leda_table(db):
    cur=db.cursor()
    cur.execute("CREATE TABLE kleda_orig (\
   `pgc` integer not null,\
   `objname` varchar(30),\
   `objtype` varchar(15),\
   `al1950` decimal(10,7),\
   `de1950` decimal(10,7),\
   `al2000` decimal(10,7),\
   `de2000` decimal(10,7),\
   `l2` decimal(10,7),\
   `b2` decimal(10,7),\
   `sgl` decimal(10,7) ,\
   `sgb` decimal(10,7),\
   `f_` integer,\
   `type` varchar(15),\
   `bar` varchar(10),\
   `ring` varchar(10),\
   `multiple` varchar(10),\
   `compactness` varchar(10),\
   `angclass` varchar(10),\
   `t` decimal(6,1),\
   `e_t` decimal(6,1),\
   `lc` decimal(6,1),\
   `e_lc` decimal(6,1),\
   `logd25` decimal(8,2),\
   `e_logd25` decimal(8,2),\
   `logr25` decimal(8,2),\
   `e_logr25` decimal(8,2),\
   `pa` decimal(6,2),\
   `brief` decimal(6,2),\
   `e_brief` decimal(6,2),\
   `bt` decimal(6,2),\
   `e_bt` decimal(6,2) ,\
   `it` decimal(6,2),\
   `e_it` decimal(6,2),\
   `ubt` decimal(6,2),\
   `bvt` decimal(6,2),\
   `ube` decimal(6,2),\
   `bve` decimal(6,2),\
   `vmaxg` decimal(6,2),\
   `e_vmaxg` decimal(6,2),\
   `vmaxs` decimal(6,2),\
   `e_vmaxs` decimal(6,2),\
   `vdis` decimal(6,2),\
   `e_vdis` decimal(6,2),\
   `mg2` decimal(6,2),\
   `e_mg2` decimal(6,2),\
   `m21` decimal(6,2),\
   `e_m21` decimal(6,2),\
   `mfir` decimal(6,2),\
   `vrad` integer,\
   `e_vrad` integer,\
   `vopt` integer,\
   `e_vopt` integer,\
   `v` integer,\
   `e_v` integer,\
   `ag` decimal(6,2),\
   `ai` decimal(6,2) ,\
   `incl` decimal(6,2),\
   `a21` decimal(6,2),\
   `lambda` decimal(6,2),\
   `logdc` decimal(6,2),\
   `btc` decimal(6,2),\
   `itc` decimal(6,2),\
   `ubtc` decimal(6,2),\
   `bvtc` decimal(6,2),\
   `bri25` decimal(6,2) ,\
   `vrot` decimal(6,2),\
   `e_vrot` decimal(6,2),\
   `m21c` decimal(6,2),\
   `hic` decimal(6,2),\
   `vlg` integer,\
   `vgsr` integer,\
   `vvir` integer,\
   `v3k` integer,\
   `modz` decimal(6,2),\
   `mod0` decimal(6,2),\
   `mabs` decimal(6,2),\
    PRIMARY KEY (`PGC`) );")
    db.commit()
    cur.close()


def copy_leda_orig_into_leda(db):
  # add the column definition for kleda to kcolumns
  define_leda_columns(db)
  # retrive the list of columns just added using a query
  cursor=db.cursor()
  cursor.execute('select tabcolumn from kcolumns where dbtable like "%kleda";')
  results=cursor.fetchall()
  # turn into array
  columns=[x[0].lstrip().rstrip() for x in results]
  # turn into a string separated by comma
  columns=",".join(columns)
  print "Creating a new kleda from kleda_orig using columns: "+columns
  cursor.execute("Create table kleda select "+columns+" from kleda_orig;")
  db.commit()
  # add primary key
  cursor.execute("alter table kleda add primary key (pgc);")
  db.commit()
  # make sure we don't display kleda_orig
  cursor.execute('delete from kcolumns where dbtable like "%kleda_orig%";')
  db.commit()
  cursor.execute('delete from ktables where dbtable like "%kleda_orig%";')
  db.commit()
  # make sure we display kleda
  cursor.execute('INSERT into ktables values\
    ("kleda","Redshift Catalogs","NULL","LEDA","LEDA","LEDA database","NULL","NULL");')
  db.commit()
  # calculate RA and DEC from al2000 de2000
  print "reading ra and dec..."
  cursor.execute("Select al2000,de2000 from kleda;")
  results=cursor.fetchall()
  cursor.close()
  cursor=db.cursor()
  print "transforming into new format..."
  ra=["" if x[0] is None else str(angles.AlphaAngle(h=float(str(x[0])))).replace("HH","").replace("MM","").replace("SS","").replace(" ","") for x in results]
  dec=["" if x[1] is None else str(angles.DeltaAngle(d=float(str(x[1])))).replace("DD","").replace("MM","").replace("SS","").replace(" ","")  for x in results]

  print "reading kleda ..."
  cursor.execute("select * from kleda;")
  results=cursor.fetchall()
  results=[list(x) for x in results]
  # add the RA2000 and DEC2000 columns
  cursor.execute("ALTER TABLE kleda ADD COLUMN RA2000 varchar(20);")
  db.commit()
  cursor.execute("ALTER TABLE kleda ADD COLUMN DEC2000 varchar(20);")
  db.commit()
  cursor.execute("INSERT INTO kcolumns(dbtable,tabcolumn,units,description,ucd,justification,format) VALUES ('kleda','RA2000','h','Right Ascension (J2000)','','r','%12s');")
  db.commit()
  cursor.execute("INSERT INTO kcolumns(dbtable,tabcolumn,units,description,ucd,justification,format) VALUES ('kleda','DEC2000','deg','Declination (J2000)','','r','%12s');")
  db.commit()

  print "adding RA and DEC..."
  for k in range(len(results)):
    results[k].append(ra[k])
    results[k].append(dec[k])
  cursor.execute("Delete from kleda;")
  db.commit()
  cursor.close()
  cursor=db.cursor()
  format = "%s,"*len(results[0])
  format = format[:-1]
  print "lines to add to leda: "+str(len(results))
  print "now inserting into kleda with new coordinates..."
  print results[0]
  for data in results:
      try:
        cursor.execute("Insert into kleda values("+format+");",data)
      except:
        print "Error: cannot add the data:"
        print data
      
  db.commit()
  cursor.close()

def generate_kleda_orig_from_lyon(db,elements):

  pgcs=elements
  #if (len(elements)==0):
  #  # Retrieve the list of pgc numbers
  #  print "Retrieving pgc list from database..."
  #  cur=db.cursor()
  #  cur.execute('SELECT * from pgc')
  #  pgcs=cur.fetchall()
  #  cur.close()
  #if (len(elements)):
  #  print "Retrieving leda information for selected elements"
  #  pgcs=elements

  leda=[]
  # cycle through pgc numbers to build the query string
  query=""
  print "Querying leda..."
  #print (pgcs)
  for ind in range(len(pgcs)):
     query=query+"%20or%20pgc%3D"+str(pgcs[ind])
     if (ind % 200 == 0 or ind>=len(pgcs)-1):
         print "Query results ... "+str(ind)+"/"+str(len(pgcs)-1)
         query=query[5:]
         url='http://leda.univ-lyon1.fr/leda/fullsqlmean.cgi?Query=select%20*%20where'+query
         result=urllib2.urlopen(url)
         for myline in result:
             if "<" in myline:
                 continue
             if myline=="":
                 continue
             elements=myline.replace("-","").replace(" ","").split("|")
             elements=[x if x else None for x in elements]
             if ("pgc" in elements[0]):
                 continue
             if (len(elements)<2):
                 continue
             elements.pop()
             if (elements):
               print elements[:3]
               leda.append((elements))
         query=""
  if (leda):
   num=len(leda[1])
   print "number of elements is "+str(num)
   print leda[0]
   print leda[1]
   format = "%s,"*num
   format = format[:-1]

   #insert data into database
   print "inserting data into database..."
   cur=db.cursor()
   cur.executemany("INSERT INTO kleda_orig VALUES ("+format+")",leda) 
   db.commit()
   print "New data has been downloaded from Lyon. You should create an updated leda_bar file."
   answer=edd.query_yes_no("Would you like to update the leda_bar file now ?",default="yes")
   if (answer=="yes"):
     generate_leda_bar_file(db)

   print "--------------------------------------------------------------------------------------------------------------------------------------------------------------------------"
  else:
   print "No results returned from leda"

def drop_leda_table(db):
  cur=db.cursor()
  cur.execute('DROP table if exists kleda_orig;')
  db.commit()
  #cur.execute('DELETE from ktables where dbtable like "%kleda%";')
  #db.commit()
  cur.close()

def generate_leda_bar_file(db):
  cur=db.cursor()
  #columns_to_select="pgc,objname,objtype,al1950,de1950,al2000,dec2000,l2,b2,sgl,sgb,f_,type,bar,ring,multiple,compactness,angclass,t,e_t,lc,e_lc,logd25,e_logd25,logr25,e_logr25,pa,brief,e_brief,bt,e_bt,it,e_it,ubt,bvt,ube,bve,vmaxg,e_vmaxg,vmaxs,e_vmaxs,vdis,e_vdis,mg2,e_mg2,m21,e_m21,mfir,vrad,e_vrad,vopt,e_vopt,v,e_v,ag,ai,incl,a21,lambda,logdc,btc,itc,ubtc,bvtc,bri25,vrot,e_vrot,m21c,hic,vlg,vgsr,vvir,v3k,modz,mod0,mabs"
  #cur.execute("Select "+columns_to_select+" from kleda_orig;")
  cur.execute("Select * from kleda_orig;")
  leda=cur.fetchall()
  if (os.path.exists(EDD_config.bar_files+'leda_bar')):
      os.unlink(EDD_config.bar_files+'leda_bar')
  f=open(EDD_config.bar_files+"leda_bar","wb")
  for line in leda:
      #print line
      line=["" if x is None else str(x) for x in line]
      outputline='|'.join(line)+"\n"
      #print outputline
      f.write(outputline)
  f.close()


#def add_ra_dec_to_leda(db):
#  cur=db.cursor()
  


def query_yes_no(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.
    
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")



def determine_format(format):
    format=format.lower()
    if format=="":
        format="%s"
        return format
    if format=="real":
        format="%10.3f"
        return format
    if format=="int":
        format="%d"
        return format
    # determine first type
    format0=format.split("(")
    if format0[0]=="varchar":
      try:        
        format1=format0[1].replace(')','')
        return "%"+format1+"s"
      except:
        print "Error in converting format: "
        print format0
        exit()
    if format0[0]=="numeric":
        format1=format0[1].split(',')
        format1[1]=format1[1].replace(')','')
        return "%"+format1[0]+"."+format1[1]+"f"
    print "Format "+format+" cannot be converted... exiting."
    exit

def calculate_el_de(table, positions,remove):
  output_table=[]
  for line in table:
    RAh=line[int(positions[0][1]):int(positions[0][2])].lstrip().rstrip()
    if RAh=="":
      RAh=0
    RAm=line[int(positions[1][1]):int(positions[1][2])].lstrip().rstrip()
    if RAm=="":
      RAm=0
    RAs=line[int(positions[2][1]):int(positions[2][2])].lstrip().rstrip()
    if RAs=="":
      RAs=0
    DEsign=line[int(positions[3][1]):int(positions[3][2])].lstrip().rstrip()
    if DEsign=="":
      DEsign="+"
    DEd=line[int(positions[4][1]):int(positions[4][2])].lstrip().rstrip()
    if DEd=="":
      DEd=0
    DEm=line[int(positions[5][1]):int(positions[5][2])].lstrip().rstrip()
    if DEm=="":
      Dem=0
    DEs=line[int(positions[6][1]):int(positions[6][2])].lstrip().rstrip()
    if DEs=="":
      DEs=0

    if remove:
      # remove the part of the line containing coordinates and the next |
      counter=positions[6][2]
      while line[int(counter)] != "|":
        counter=counter+1
      #print "line before:"+line
      line=line[:int(positions[0][1])]+line[counter+1:]
      #print "line after:"+line
    #print RAh, RAm, RAs
    #print DEsign, DEd, DEm, DEs
    el = float(RAh)+float(RAm)/60+float(RAs)/3600
    de = float(DEd)+float(DEm)/60+float(DEs)/3600

    if DEsign=="-":
      de=-de
    # add the coordinates at the end of the line
    line=line+"|"+str(el)+"|"+str(de)
    output_table.append(line)
  print table[0]
  print output_table[0]
  return output_table  

