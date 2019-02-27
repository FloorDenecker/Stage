# -*- coding: utf-8 -*-
"""
Created on Thu Nov 29 19:17:53 2018

@author: beheerder
"""

import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_excel('D:/Users/beheerder/Documents/Floor/UGent/2018-2019/stage/data/qualtrics/qualtricsoriginal.xlsx')

#gemiddelde geschatte gebruik tijdens week en weekend gevisualiseerd. (maat: minuten/dag)
gebruik = df[['ppn', 'G_WEEK', 'G_WEEKEND']]
#to long format: (1) een kolom ppn , (2)een kolom value en (3) een kolom meaning 
gebruik_long = pd.melt(gebruik, id_vars="ppn", value_vars =['G_WEEK','G_WEEKEND'])
gebruik_long.columns = ["ppn", "moment", "minutesàday"]
sns.lineplot(x="ppn", y="minutesàday", hue="moment", data=gebruik_long)

#kan de ruimte tussen de twee worden opgevuld? 
#orange mean line: mean G_week (over all the participants) 232.7 minutes
#blue mean line: mean G_weekend (over all the participants) 254.1 minutes

sns.lineplot(x="moment", y="minutesàday", data=gebruik_long)
sns.swarmplot(x="moment", y="minutesàday", data=gebruik_long)
sns.factorplot( "moment", "minutesàday", data=gebruik_long, kind="bar", palette="muted", legend=False)

##############
###gerapporteerde piekgebruik
##############

piek = df[['ppn', '5U-9U', '9U-12U', '12U-13U', '13U-18U', '18U-23U', '23U-5U']]
#moet eerst per categorie opgeteld worden
piek_mean = pd.DataFrame({'moment': ['12U-13U', '13U-18U', '18U-23U', '23U-5U','5U-9U', '9U-12U'], 'aantal': [0,0,0,0,0,0], 'proportie': [0,0,0,0,0,0]})
piek_mean['aantal'] = piek.apply(np.sum)

#in long format: (1) ppn, (2) moment, (3) ja/nee
piek_long = pd.melt(piek, id_vars="ppn", value_vars=['5U-9U', '9U-12U', '12U-13U', '13U-18U', '18U-23U', '23U-5U'])
piek_long.columns = ["ppn", "moment", "indicatie"]
piek_long_m = piek_long.groupby("moment")["indicatie"].sum() 
piek_long_m = piek_long_m.to_frame()
piek_long_m.columns = ["aantal"]
piek_long_m["proportie"] = piek_long_m["aantal"]/40
piek_long_m["moment"]= ['12U-13U', '13U-18U', '18U-23U', '23U-5U','5U-9U', '9U-12U']
sns.lineplot(x="moment", y="aantal",data=piek_long_m)

sns.lineplot(x="moment", y="proportie", data=piek_long_m)
sns.factorplot( "moment", "aantal", data=piek_long_m, kind="bar", palette="muted", legend=False)

#############################
###GERAPPORTEERDE APPGEBRUIK
#############################
APP = df[['ppn', 'INTERNET/ZOEK', 'MESSENGERS', 'SNS', 'ENTERTAIN', 'GAMES', 'ANDERE'  ]]
APP_long = pd.melt(APP, id_vars="ppn", value_vars=['INTERNET/ZOEK', 'MESSENGERS', 'SNS', 'ENTERTAIN', 'GAMES', 'ANDERE'])
APP_long.columns = ["ppn", "applicatie", "indicatie"]
APP_long_m = APP_long.groupby("applicatie")["indicatie"].sum() 
APP_long_m = APP_long_m.to_frame()
APP_long_m.columns = ["aantal"]
APP_long_m["proportie"] = APP_long_m["aantal"]/40
APP_long_m["applicatie"]= ['ANDERE', 'ENTERTAIN','GAMES','INTERNET/ZOEK', 'MESSENGERS', 'SNS']
APP_long_m = APP_long_m.reindex(['SNS', 'MESSENGERS', 'INTERNET/ZOEK', 'GAMES', 'ENTERTAIN', 'ANDERE'])

#absoluut aantal mensen die voor die categorie hebben gekozen. 
sns.lineplot(x="applicatie", y="aantal",data=APP_long_m)
sns.pointplot(x="applicatie", y="aantal", data=APP_long_m, markers='o')
plt.xticks(rotation=-90)

sns.factorplot( "applicatie", "aantal", data=APP_long_m, kind="bar", palette="muted", legend=False)
plt.xticks(rotation=-90)
#proportioneel aantal mensen die zeggen dat ze die categorie van applicaties vaak gebruiken (makkelijker vergelijkbaar met MobileDNA data)
sns.lineplot(x="applicatie", y="proportie", data=APP_long_m) #resultaat is hier nog een gespiegelde plot. 
sns.pointplot(x="applicatie", y="proportie", data=APP_long_m, markers='o')
plt.xticks(rotation=-90)

sns.factorplot( "applicatie", "proportie", data=APP_long_m, kind="bar", palette="muted", legend=False)
plt.xticks(rotation=-90)

#dit kan dan vergeleken worden met de proportie van gevonden applicatiegebruik. (probleem: de applicaties komen niet overeen met elkaar. )

#########GERAPPORTEERD SMARTPHONEGEBRUIK
#D/W_AUTO, D/W_ETEN & D/W_SCHOOL onder elkaar zetten (long format). 
#kolom ppn, kolom type en kolom D/W (min 0 - max 7)
D_W = df[['ppn', 'D/W_AUTO', 'D/W_ETEN', 'D/W_SCHOOL']]
D_W_long = pd.melt(D_W, id_vars = "ppn", value_vars=["D/W_AUTO", "D/W_ETEN", "D/W_SCHOOL"])
D_W_long.columns = ["ppn", "type", "D/W"]

D_W_count_long = D_W_long.groupby(["type", "D/W"]).count()
D_W_count_long["type"] = ["D/W_AUTO","D/W_AUTO", "D/W_AUTO", "D/W_AUTO", "D/W_AUTO", "D/W_AUTO", "D/W_AUTO", 
                          "D/W_ETEN","D/W_ETEN","D/W_ETEN","D/W_ETEN","D/W_ETEN","D/W_ETEN","D/W_ETEN","D/W_ETEN",
                          "D/W_SCHOOL","D/W_SCHOOL","D/W_SCHOOL","D/W_SCHOOL","D/W_SCHOOL","D/W_SCHOOL","D/W_SCHOOL"]
D_W_count_long["D/W"] = ["0","1","2","3","4","5","7",
                          "0","1","2","3","4","5","6","7",
                          "0","1","2","3","4","5","7",]
D_W_count_long.columns = ["aantal", "D/W", "type"]
D_W_count_long.to_excel("D_W_count_long.xlsx")
#ontbrekende waarde toevoegen
D_W_count_long_adjust = pd.read_excel('C:/Users/beheerder/D_W_count_long.xlsx')
D_W_count_long_adjust = D_W_count_long_adjust[["D/W", "type.1", "aantal"]]
D_W_count_long_adjust["proportie"] = D_W_count_long_adjust["aantal"]/40

#line + point
sns.pointplot(x="D/W", y="aantal", hue="type.1", data=D_W_count_long_adjust, markers='o')
sns.pointplot(x="D/W", y="proportie", hue="type.1", data=D_W_count_long_adjust, markers='o')

#bar factor plot
sns.factorplot( x="D/W", y="proportie", hue="type.1", data=D_W_count_long_adjust, kind="bar", palette="muted", legend=True)
sns.factorplot(x = "D/W", y="proportie", col = "type.1", data=D_W_count_long_adjust, kind="bar", palette="muted", legend=True)

#voilinplots
sns.violinplot(x="D/W", y="aantal", hue="type.1", data=D_W_count_long_adjust)
plt.show()

###########SMARTPHONEGEBRUIK voor slaap
###########SMARTPHONEGEBRUIK na slaap 

SLAAP = df[["ppn", "MIN_VR_SLAAP", "MIN_NA_WKKR"]]
#waarde die hier staat is het  aantal minuten 
#lineaire regressie
#regressie wordt hier bepaald door een outlier. 
sns.regplot (x = "MIN_VR_SLAAP", y = "MIN_NA_WKKR", data = SLAAP)

#berekeningen met het wide format
#visualisaties met long format
SLAAP_long = pd.melt(SLAAP, id_vars = "ppn", value_vars=["MIN_VR_SLAAP", "MIN_NA_WKKR"])
#in categorieën verdelen? 

SLAAP_MT = df[["ppn", "MIN_VR_SLAAP", "MIN_NA_WKKR", "MT"]]

sns.regplot(x = "MIN_VR_SLAAP", y="MT", data=SLAAP_MT)
sns.regplot(x = "MIN_NA_WKKR", y="MT", data=SLAAP_MT)

###BEDTIJD
bed_wek = df[["ppn", "BEDTIJD", "WEKTIJD"]]
#dit in long format krijgen kolom 1 = ppn, kolom 2 = moment (bed of wek), kolom 3= tijd. 
bed_wek_long = pd.melt(bed_wek, id_vars="ppn", value_vars=["BEDTIJD", "WEKTIJD"])
bed_wek_long_count = bed_wek_long.groupby(["variable", "value"]).count()
bed_wek_long_count.index
#tellen hoeveel mensen op welk moment gaan slapen.
bed_wek_long_count['soort'] = ['BEDTIJD','BEDTIJD','BEDTIJD','BEDTIJD','BEDTIJD',
                                  'BEDTIJD','BEDTIJD','BEDTIJD','BEDTIJD','BEDTIJD',
                                  'BEDTIJD','BEDTIJD','BEDTIJD','BEDTIJD',
                                  'WEKTIJD','WEKTIJD','WEKTIJD','WEKTIJD','WEKTIJD','WEKTIJD',
                                  'WEKTIJD','WEKTIJD','WEKTIJD','WEKTIJD','WEKTIJD','WEKTIJD',
                                  'WEKTIJD','WEKTIJD','WEKTIJD','WEKTIJD','WEKTIJD','WEKTIJD']
bed_wek_long_count['tijd'] = ['00U00', '00U30', '01U00', '01U30', '02U00', '02U30','21U30', '22U00', '22U30', '22U50', '23U00', '23U15', '23U30', '23U45',
                              '05U00', '06U00', '06U30', '06U40', '07U00', '07U20', '07U25', '07U30', '07U40', '07U45', '08U00', '08U30', '09U00', '09U30', 
                              '10U00', '10U30', '11U00', '12U00']
bed_wek_long_count.columns = ["aantal", "tijd", "soort"]
bed_wek_long_count['proportie'] = bed_wek_long_count['aantal']/40


sns.pointplot(x="aantal", y="tijd", hue="soort", data=bed_wek_long_count, markers='o')
sns.pointplot(x="tijd", y="aantal", hue="soort", data=bed_wek_long_count, markers='o')
plt.xticks(rotation=-90)

###vanaf 21U30 - 2u30: slaaptijd -> daarna 5u - 12u
bed_wek_long_count = bed_wek_long_count[['21U30', '22U00', '22U30', '22U50', '23U00', '23U15', '23U30', '23U45','00U00', '00U30', '01U00', '01U30', '02U00', '02U30',
                                         '05U00', '06U00', '06U30', '06U40', '07U00', '07U20', '07U25', '07U30', '07U40', '07U45', '08U00', '08U30', '09U00', '09U30', 
                                         '10U00', '10U30', '11U00', '12U00']]
bed_wek_long_count = bed_wek_long_count.sort_values(by=["tijd"])
sns.pointplot(x="tijd", y="aantal", hue="soort", data=bed_wek_long_count, markers='o')
plt.xticks(rotation=-90)
sns.pointplot(x="tijd", y="proportie", hue="soort", data=bed_wek_long_count, markers='o')
plt.xticks(rotation=-90)
 
#dit kan ook in gelijke categorieën verdeeld worden (en de onbrekende waarden kunnen ook toegevoegd worden)

#############################################
#MT staat in SLAAP_MT. 
#dataset die puur kijkt naar die kolom
SLAAP_MT_select = SLAAP_MT[["MT"]]
#continue verdeling van MT 
sns.set();
sns.kdeplot(SLAAP_MT_select["MT"])
sns.distplot(SLAAP_MT_select["MT"])

#eventueel ook MT in categorieën verdelen: Hoeveel participanten in welke categorie? 
#via een functie toekennen aan een categorie? Handiger is om pd.cut te gebruiken; waarbij de nieuwe column = categorical. 

#(1) need to define boundaries
###welke boundaries nodig? wat zijn de min en max waarden van die kolom. 
SLAAP_MT.describe() #min = 24, #max = 74
bins = [0, 20, 30, 40, 50, 60, 70, 80, 90, 103]

#(2) need to define category names 
names = ['<20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90 - 103']
#(3) apply pd.cut to the desired numeric column 
#obv categorische waarden verdeling gaan bekijken. 
SLAAP_MT_select['MT_categ'] = pd.cut(SLAAP_MT_select['MT'], bins, labels=names)

#nu dus het aantal mensen die die categorie onderschrijven tellen. 
SLAAP_MT_select_count = SLAAP_MT_select.groupby(["MT_categ"]).count()
SLAAP_MT_select_count["categorie"] = ['<20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90 - 103']
SLAAP_MT_select_count["proportie"] = SLAAP_MT_select_count["MT"]/40
SLAAP_MT_select_count.columns = ['aantal', 'categorie', 'proportie']
SLAAP_MT_select_count = SLAAP_MT_select_count[['categorie', 'aantal', 'proportie']]

#verdeling van de multitasking scores (hogere scoring = meer geneigd te multitasken)
sns.pointplot(x="categorie", y="aantal", data=SLAAP_MT_select_count, markers='o')
plt.xticks(rotation=-90)
sns.pointplot(x="categorie", y="proportie", data=SLAAP_MT_select_count, markers='o')
plt.xticks(rotation=-90)
sns.factorplot( x="categorie", y="aantal",  data=SLAAP_MT_select_count, kind="bar", palette="muted")
plt.xticks(rotation=-90)
sns.factorplot( x="categorie", y="proportie",  data=SLAAP_MT_select_count, kind="bar", palette="muted")
plt.xticks(rotation=-90)

########################
#TOT_SLAAP: hoelang duurt het tot iemand in slaap valt
#continu
slaap = df[["TOT_SLAAP"]]
sns.set();
sns.kdeplot(slaap["TOT_SLAAP"])
#categorisch
##(1) need to define boundaries: welke boundaries nodig? gebasseerd op min en max value
slaap.describe() #min = 4, max = 90 minutes.
bins = [0,5,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,95]
##(2) need to define category names
names=['0-5', '5-10', '10-15', '15-20', '20-25', '25-30', '30-35', '35-40','40-45', '45-50',
       '50-55', '55-60', '60-65', '65-70', '70-75', '75-80', '80-85', '85-90', '90-95']
##(3) apply pd.cut to the desired numeric column
slaap["TOT_SLAAP_cat"] = pd.cut(slaap["TOT_SLAAP"], bins, labels=names)

##(4) aantal waarden per categorie tellen; proportie opvragen en verdeling nagaan. 
slaap_count = slaap.groupby(["TOT_SLAAP_cat"]).count()
slaap_count["categorie"] = names
slaap_count["proportie"] = slaap_count["TOT_SLAAP"]/40
slaap_count.columns = ['aantal', 'categorie', 'proportie']
slaap_count = slaap_count[["categorie", "aantal", "proportie"]]

sns.pointplot(x="categorie", y="aantal", data=slaap_count, markers='o')
plt.xticks(rotation=-90)
sns.pointplot(x="categorie", y="proportie", data=slaap_count, markers='o')
plt.xticks(rotation=-90)
sns.factorplot( x="categorie", y="aantal",  data=slaap_count, kind="bar", palette="muted")
plt.xticks(rotation=-90)
sns.factorplot( x="categorie", y="proportie",  data=slaap_count, kind="bar", palette="muted")
plt.xticks(rotation=-90)

#is dat gelinkt met hun #minuten gebruik voor de slaap die ze rapporteren? 
#wordt nu dus continu bekeken via regressieplot. 
#MIN_VR_SLAAP onderdeel van SLAAP
regressie_slaap = df[["MIN_VR_SLAAP", "TOT_SLAAP"]]
sns.regplot (x = "MIN_VR_SLAAP", y = "TOT_SLAAP", data = regressie_slaap)
#suggereert een positief verband: meer minuten voor slapen, later slaap; maar ziet er totaal niet significant uit. 

#SLAAPKWALITEIT algemeen (kan dan nog per puntje bekeken worden)
#hoe hoger de waarde van sleep quality, hoe slechter de slaap kwaliteit.

#hoe ziet de continue verdeling eruit? 
SK = df[["sleepquality"]]
sns.kdeplot(SK["sleepquality"])
sns.distplot(SK["sleepquality"])

SK_reg = df[["sleepquality", "MIN_VR_SLAAP", "TOT_SLAAP"]]

#regressieplot: 
#(1) sleepquality & min_vr_slaap (gebruik)
sns.regplot(x = "sleepquality", y="MIN_VR_SLAAP", data = SK_reg)
#dit ziet er er positief verband uit: hoe hoger de waarde van slaapkwaliteit, hoe slechter de slaapkwaliteit ; hoe vroeger men aangeeft de smartphone 
#aan de kant te leggen. Want lagere waarde MIN_VR_SLAAP = smartphone korter voor de slaap gebruiken = contra-intuitief? enkel door outliers? 

#(2) sleepquality & TOT_slaap  (kan indicatie zijn van slaapkwaliteit)
sns.regplot(x = "sleepquality", y="TOT_SLAAP", data = SK_reg)
#dit is eveneens een positief verband: hoe slechter de slaapkwaliteit, hoe meer minuten men nodig heeft om in slaap te raken. 

#(3) sleepquality & min_vr_slaap (gebruik) afh van de score die de participanten gegeven hebben op SK_[0-3]
SLAAP = df[["sleepquality", "MIN_VR_SLAAP", "TOT_SLAAP", "SK_[0-3]"]]
sns.lmplot(x = "sleepquality", y="MIN_VR_SLAAP", col="SK_[0-3]", data = SLAAP )
#(4) sleepquality & TOT_slaap afh van de score die de participanten gegeven hebben op SK_[0-3]
sns.lmplot(x = "sleepquality", y="TOT_SLAAP", col="SK_[0-3]", data = SLAAP )
#####
###########HEAT MAPS VAN ANTWOORDPATRONEN VRAGENLIJSTEN.
###Multitasking (schaling van 1 - 7) (omgeschaalde waarden rechtstreeks gebruiken)
multitasking = df[["ppn", "MT_1", "MT_2", "MT_3", "MT_4", "MT_5", "MT_6", "MT_7",  "MT_8", "MT_9", "MT_10", "MT_11_R", "MT_12", "MT_13", "MT_14_R", "MT_VGL_R"]]
#hoeveel keer werd elke waarde gekozen per vraag. (1) welke vraag, (2) welke waarde, (3) hoeveel keer. 
#dwz in long format krijgen 
bed_wek_long = pd.melt(bed_wek, id_vars="ppn", value_vars=["BEDTIJD", "WEKTIJD"])
bed_wek_long_count = bed_wek_long.groupby(["variable", "value"]).count()

multitasking_long = pd.melt(multitasking, id_vars = "ppn", value_vars = ["MT_1", "MT_2", "MT_3", "MT_4", "MT_5", "MT_6", "MT_7",  "MT_8", "MT_9", "MT_10", "MT_11_R", "MT_12", "MT_13", "MT_14_R", "MT_VGL_R"])
multitasking_long_count = multitasking_long.groupby(["variable", "value"]).count()
multitasking_long_count.to_excel("multitasking_long_count.xlsx")

MultiTask = pd.read_excel("C:/Users/beheerder/multitasking_long_count.xlsx")

#daaruit nu dus een headmap krijgen. 
heat_MultiTask = MultiTask.pivot("vraag","waarde", "aantal")
heat_MultiTask.to_excel("heat_MultiTask.xlsx")
#handig om vragen snel in de juiste volgorde te plaatsen.
heat_MultiTask = pd.read_excel("C:/Users/beheerder/heat_MultiTask.xlsx")
#de kolom die vragen aangeeft, als index zetten nadat ze vanuit excel worden opgehaald. 
heat_MultiTask.set_index("vraag", inplace=True)
sns.heatmap(heat_MultiTask, cmap="YlGnBu", linewidths=.1)
#helemaal niet akkoord weegt overwegend door. 

###Sleep Quality
#include df: 1_1[0-3], 1-2[0-3], 1_3[0 - 3], 1_4[0-3], 1_5[0-3], 1_6[0-3], 1_7[0-3], 1_8[0-3], SK_[0-3], enth [0-3],
# SM [0-3], WB [0-3]

SQ = df[["ppn", "1_1 [0 - 3]", "1_2 [0 - 3]", "1_3 [0 - 3]", "1_4 [0-3]", "1_5[0-3]", "1_6[0-3]", "1_7[0-3]", "1_8 [0-3]",
         "SK_[0-3]", "enth [0-3]", "SM [0-3]", "WB [0-3]"]]
SQ_long = pd.melt(SQ, id_vars = "ppn", value_vars = ["1_1 [0 - 3]", "1_2 [0 - 3]", "1_3 [0 - 3]", "1_4 [0-3]", "1_5[0-3]", "1_6[0-3]", "1_7[0-3]", "1_8 [0-3]",
         "SK_[0-3]", "enth [0-3]", "SM [0-3]", "WB [0-3]"])
SQ_long_count = SQ_long.groupby(["variable", "value"]).count()
SQ_long_count.to_excel("SQ_long_count.xlsx")
#handig om vragen snel in de juiste volgorde te plaatsen.
heat_SQ = pd.read_excel("C:/Users/beheerder/SQ_long_count.xlsx")
heat_SQ= heat_SQ.pivot("vraag","waarde", "aantal")
sns.heatmap(heat_SQ, cmap="YlGnBu", linewidths=.1)

df_q.to_excel('df_q.xlsx')