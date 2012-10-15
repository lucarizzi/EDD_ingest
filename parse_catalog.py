# open the catalogs.pl file and reads it
import commands

f=open("catalogs.pl","r")

# cycle through the lines

keywords = ["category","catalog","abbreviation","dbtable","bibcode","description","filename"]

lines = f.readlines()

for k in range(0,len(lines)):
    
    myline=lines[k].lstrip().strip()
    columns=myline.split("=>")
    #print ">>"+columns[0]+"<<"
    #if columns[0] in ["","sub catalogs {",'my $dir = "../data/";','my @catalogs = ();',"},","};","sql"]:
    #print "skipping..."   
    #    continue
    if columns[0]=="};":
        print "end"
        continue
    if columns[0] in ["sql "]:
        special_sql_code=columns[1].replace("[","").replace("]","").lstrip(" '").rstrip("',").replace('"','').replace("\\","")
        print "special_code=>"+special_sql_code
        i=1
        while True:
            next_line=lines[k+i].lstrip().rstrip()
            special_sql_code=next_line.lstrip().rstrip().replace(" ]","").replace("]","").lstrip(" '").rstrip("',").replace('"','').replace("\\","")
            if (next_line=="};"):
                break
            if (next_line=="]"):
                break
            print "special_code=>"+special_sql_code
            i=i+1
        continue

    if columns[0].count("#") > 0:
        stra=columns[0]
        if stra[0]=="#":
          continue
    if columns[0]=="$catalogs[++$#catalogs] = {":
        print "begin"
        continue
    first_argument = columns[0].lstrip().rstrip()
    if len(columns)>1:
        second_argument = columns[1].lstrip().rstrip()
        if myline.count("[")==0:
            second_argument=second_argument.replace(",","").replace('"','')
    if first_argument=="filename":
        second_argument=second_argument.replace("$dir.","")
        md5=commands.getoutput("md5 "+second_argument)
        md5=md5.split("=")
        #try:
        #    print "md5=>"+md5[1].lstrip()
        #except:
        #    #print "Error trying to compute md5 on "+second_argument

    if first_argument in keywords:
        print first_argument+"=>"+second_argument
        exit

    if myline.count("[")>0:
        variable_description=second_argument.split('"')
        if len(variable_description)>5:
            #print variable_description
            type=variable_description[1]
            unit=variable_description[3]
            description=variable_description[5]
            positions = variable_description[0].replace('[','').split(',')
            if type=="int":
                size=int(positions[1])-int(positions[0])+1
                type="int("+str(size)+")"

            if first_argument.replace('"','') in ['RAh','RAm','RAs','DE-','DEd','DEm','DEs']:
                print "coordinate=>"+first_argument+"|"+positions[0]+"|"+positions[1]+"|"+type+"|"+unit+"|"+description                
            else:
                first_argument=first_argument.replace('"','')
                print "column=>"+first_argument+"|"+type+"|"+unit+"|"+description

                
