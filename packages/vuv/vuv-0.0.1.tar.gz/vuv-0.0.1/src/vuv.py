import pandas as pd
import sys
import subprocess as sp
import matplotlib.pyplot as plt
import numpy as np
sp.call('wget -nc https://data.cdc.gov/api/views/3rge-nu2a/rows.csv',shell=True)
d=pd.read_csv('rows.csv')
months=d.month.unique()
days=[]
#age=18-29,30-49,50-64,65-79,80+
if len(sys.argv)==1: 
 print('enter one of five age groups: vuv 80+')
 print('18-29,30-49,50-64,65-79,80+')
 sys.exit(0)
else:
 age=sys.argv[1]
for i in months:
 for j in range(4):
  days.append(i+'.'+str(j))
 vwo=d.loc[(d.outcome=='death') & (d['Age group']==age),'Vaccinated with outcome']
 fvp=d.loc[(d.outcome=='death') & (d['Age group']==age),'Fully vaccinated population']
 v=vwo/fvp
 uwo=d.loc[(d.outcome=='death') & (d['Age group']==age),'Unvaccinated with outcome']
 up=d.loc[(d.outcome=='death') & (d['Age group']==age),'Unvaccinated population']
 u=uwo/up
def main():
 days.append("")
 days.append("")
 #print(len(days),len(vwo),len(fvp),len(uwo),len(up))
 plt.plot(days,v,'-k')
 plt.plot(days,u,'--k')
 plt.xticks(days[::4],rotation=90)
 plt.legend(('vaccinated','unvaccinated'))
 plt.title('COVID-19 mortality for '+age+' age group')
 plt.savefig(age+'.png',bbox_inches='tight')
 print(age+'.png image file is generated')
 plt.close()
main()
