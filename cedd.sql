# This sql script creates the public EDD as views of the secure database
# We are going to delete public EDD and recreate it.
# Assumes that the secure database EDDsDB has been made with create_edds.sql
DROP DATABASE IF EXISTS EDDDB;
CREATE DATABASE EDDDB;
USE EDDDB;

# Create ktables table but leave out secure tables.
# Add any new totally secure table to list here
# If only some columns in the table are secure do not add it here.
CREATE VIEW ktables AS SELECT * FROM EDDsDB.ktables WHERE dbtable NOT IN 
( 'kallceph' 
,'kallcf2' 
,'kallfp' 
,'kallsbf' 
,'kallsn' 
,'kalltfr' 
,'kspittfr3'
,'kcf3sntest'
,'kcomments'
,'kdummy'
,'kefardm' 
,'keneardm'
,'kmisc' 
,'kpnlf' 
,'ktrgb' 
,'ktrgblit' 
,'ksmacdm' 
,'kwisecal'
,'kwisecand'
,'kwissnecal'
,'kcand'
,'k13442' 
,'knamnest'
,'kalf70'
,'karecibocal'
,'kflatgbt'
,'kehsanN'
,'kehsanS'
,'kcf4cand');

# Create kcolumns
CREATE VIEW kcolumns AS SELECT * FROM EDDsDB.kcolumns WHERE tabcolumn != 'P' ;

# Create views of tables with secure columns
CREATE VIEW kcmd AS SELECT * FROM EDDsDB.kcmd WHERE P = 1;
CREATE VIEW kspitphot AS SELECT * FROM EDDsDB.kspitphot WHERE P = 1;

# Create views of all nonsecure tables
# Any table that is not secure needs to be here to show up in public EDD
CREATE VIEW knestnorth AS SELECT * FROM EDDsDB.knestnorth ;
CREATE VIEW knestsouth AS SELECT * FROM EDDsDB.knestsouth ;
CREATE VIEW klucat AS SELECT * FROM EDDsDB.klucat ;
CREATE VIEW krcng AS SELECT * FROM EDDsDB.krcng ;
CREATE VIEW pgc AS SELECT * FROM EDDsDB.pgc ;
CREATE VIEW kbothun AS SELECT * FROM EDDsDB.kbothun ;
CREATE VIEW kcfs AS SELECT * FROM EDDsDB.kcfs ;
CREATE VIEW kcf2 AS SELECT * FROM EDDsDB.kcf2 ;
CREATE VIEW kcf3 AS SELECT * FROM EDDsDB.kcf3 ;
CREATE VIEW kallsn3 AS SELECT * FROM EDDsDB.kallsn3 ;
CREATE VIEW Prfgcvel AS SELECT * FROM EDDsDB.Prfgcvel ;
CREATE VIEW k2m1175 AS SELECT * FROM EDDsDB.k2m1175 ;
CREATE VIEW k2massv AS SELECT * FROM EDDsDB.k2massv ;
CREATE VIEW k2mpp AS SELECT * FROM EDDsDB.k2mpp ;
CREATE VIEW k2mrsaug AS SELECT * FROM EDDsDB.k2mrsaug ;
CREATE VIEW k5sn1a AS SELECT * FROM EDDsDB.k5sn1a ;
CREATE VIEW k8k AS SELECT * FROM EDDsDB.k8k ;
CREATE VIEW kaaronson AS SELECT * FROM EDDsDB.kaaronson ;
CREATE VIEW kangst AS SELECT * FROM EDDsDB.kangst ;
CREATE VIEW karauc AS SELECT * FROM EDDsDB.karauc ;
CREATE VIEW kbern AS SELECT * FROM EDDsDB.kbern ;
CREATE VIEW kblake AS SELECT * FROM EDDsDB.kblake ;
CREATE VIEW kbureau AS SELECT * FROM EDDsDB.kbureau ;
CREATE VIEW kchp AS SELECT * FROM EDDsDB.kchp ;
CREATE VIEW kcng AS SELECT * FROM EDDsDB.kcng ;
CREATE VIEW kcornell AS SELECT * FROM EDDsDB.kcornell ;
CREATE VIEW kcourmath AS SELECT * FROM EDDsDB.kcourmath ;
CREATE VIEW kcourteau AS SELECT * FROM EDDsDB.kcourteau ;
CREATE VIEW kcsn1a AS SELECT * FROM EDDsDB.kcsn1a ;
CREATE VIEW kdale AS SELECT * FROM EDDsDB.kdale ;
CREATE VIEW kdellan AS SELECT * FROM EDDsDB.kdellan ;
CREATE VIEW kedist AS SELECT * FROM EDDsDB.kedist ;
CREATE VIEW kefar AS SELECT * FROM EDDsDB.kefar ;
CREATE VIEW kenearc AS SELECT * FROM EDDsDB.kenearc ;
CREATE VIEW kfisher AS SELECT * FROM EDDsDB.kfisher ;
CREATE VIEW kfsn1a AS SELECT * FROM EDDsDB.kfsn1a ;
CREATE VIEW kgiov AS SELECT * FROM EDDsDB.kgiov ;
CREATE VIEW khancl AS SELECT * FROM EDDsDB.khancl ;
CREATE VIEW khanpp AS SELECT * FROM EDDsDB.khanpp ;
CREATE VIEW khawphot AS SELECT * FROM EDDsDB.khawphot ;
CREATE VIEW khaynes AS SELECT * FROM EDDsDB.khaynes ;
CREATE VIEW kher AS SELECT * FROM EDDsDB.kher ;
CREATE VIEW khipass AS SELECT * FROM EDDsDB.khipass ;
CREATE VIEW khsn1a AS SELECT * FROM EDDsDB.khsn1a ;
CREATE VIEW khstsbf AS SELECT * FROM EDDsDB.khstsbf ;
CREATE VIEW khycensbf AS SELECT * FROM EDDsDB.khycensbf ;
CREATE VIEW kjsn1a AS SELECT * FROM EDDsDB.kjsn1a ;
CREATE VIEW kleda AS SELECT * FROM EDDsDB.kleda ;
CREATE VIEW klga AS SELECT * FROM EDDsDB.klga ;
CREATE VIEW klu AS SELECT * FROM EDDsDB.klu ;
CREATE VIEW kmakvp AS SELECT * FROM EDDsDB.kmakvp ;
CREATE VIEW kmath AS SELECT * FROM EDDsDB.kmath ;
CREATE VIEW kmcc AS SELECT * FROM EDDsDB.kmcc ;
CREATE VIEW kmcdonald AS SELECT * FROM EDDsDB.kmcdonald ;
CREATE VIEW kmkgp AS SELECT * FROM EDDsDB.kmkgp ;
CREATE VIEW kmould AS SELECT * FROM EDDsDB.kmould ;
CREATE VIEW knancay AS SELECT * FROM EDDsDB.knancay ;
CREATE VIEW knewsky AS SELECT * FROM EDDsDB.knewsky ;
CREATE VIEW knwlt AS SELECT * FROM EDDsDB.knwlt ;
CREATE VIEW kolw1cour AS SELECT * FROM EDDsDB.kolw1cour ;
CREATE VIEW kolw2cour AS SELECT * FROM EDDsDB.kolw2cour ;
CREATE VIEW kolw3cour AS SELECT * FROM EDDsDB.kolw3cour ;
CREATE VIEW kolw4cour AS SELECT * FROM EDDsDB.kolw4cour ;
CREATE VIEW koptLW AS SELECT * FROM EDDsDB.koptLW ;
CREATE VIEW kphot AS SELECT * FROM EDDsDB.kphot ;
CREATE VIEW kpiercef AS SELECT * FROM EDDsDB.kpiercef ;
CREATE VIEW kprofiles AS SELECT * FROM EDDsDB.kprofiles ;
CREATE VIEW kpscz AS SELECT * FROM EDDsDB.kpscz ;
CREATE VIEW kpsn1a AS SELECT * FROM EDDsDB.kpsn1a ;
CREATE VIEW kqdist AS SELECT * FROM EDDsDB.kqdist ;
CREATE VIEW krfgc AS SELECT * FROM EDDsDB.krfgc ;
CREATE VIEW krfgc2mass AS SELECT * FROM EDDsDB.krfgc2mass ;
CREATE VIEW krfgcvel AS SELECT * FROM EDDsDB.krfgcvel ;
CREATE VIEW kroth AS SELECT * FROM EDDsDB.kroth ;
CREATE VIEW ks4g AS SELECT * FROM EDDsDB.ks4g ;
CREATE VIEW kschommer AS SELECT * FROM EDDsDB.kschommer ;
CREATE VIEW ksdss AS SELECT * FROM EDDsDB.ksdss ;
CREATE VIEW ksings AS SELECT * FROM EDDsDB.ksings ;
CREATE VIEW ksmac AS SELECT * FROM EDDsDB.ksmac ;
CREATE VIEW ksmac3 AS SELECT * FROM EDDsDB.ksmac3 ;
CREATE VIEW kspringob AS SELECT * FROM EDDsDB.kspringob ;
CREATE VIEW kt07d AS SELECT * FROM EDDsDB.kt07d ;
CREATE VIEW ktfcal AS SELECT * FROM EDDsDB.ktfcal ;
CREATE VIEW ktsbf AS SELECT * FROM EDDsDB.ktsbf ;
CREATE VIEW ktsn1a AS SELECT * FROM EDDsDB.ktsn1a ;
CREATE VIEW kusn1a AS SELECT * FROM EDDsDB.kusn1a ;
CREATE VIEW kv3k AS SELECT * FROM EDDsDB.kv3k ;
CREATE VIEW kvcc AS SELECT * FROM EDDsDB.kvcc ;
CREATE VIEW kverh AS SELECT * FROM EDDsDB.kverh ;
CREATE VIEW kwhisp AS SELECT * FROM EDDsDB.kwhisp ;
CREATE VIEW kwillcl AS SELECT * FROM EDDsDB.kwillcl ;
CREATE VIEW kwillpp AS SELECT * FROM EDDsDB.kwillpp ;
CREATE VIEW k6dfgs AS SELECT * FROM EDDsDB.k6dfgs ;
CREATE VIEW kwisephot AS SELECT * FROM EDDsDB.kwisephot ;
CREATE VIEW kwisepfw AS SELECT * FROM EDDsDB.kwisepfw ;
CREATE VIEW kgplt3500 AS SELECT * FROM EDDsDB.kgplt3500 ;
CREATE VIEW ks4gmulti AS SELECT * FROM EDDsDB.ks4gmulti ;
CREATE VIEW ks4gone AS SELECT * FROM EDDsDB.ks4gone ;
CREATE VIEW kasassn AS SELECT * FROM EDDsDB.kasassn ;
CREATE VIEW klimgroups AS SELECT * FROM EDDsDB.klimgroups ;
CREATE VIEW klvgdb AS SELECT * FROM EDDsDB.klvgdb ;
