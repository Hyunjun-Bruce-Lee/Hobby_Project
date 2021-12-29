###
with open('C:/Users/user/Desktop/Final_PJ/수급자.bin', 'rb') as f:
    amt = pickle.load(f)

not_in_geo = list()
for i in list(amt['`ADMI_NM`']):
    if i in list(pop['ADM_DR_NM']):
        continue
    not_in_geo.append(i)
    print(i)

for i in not_in_geo:
    if i in list(amt['`ADMI_NM`']):
        amt.loc[amt['`ADMI_NM`']==i, '`ADMI_NM`'] = i.replace('.','·')
        
amt.rename(columns = {'`CTY_NM`': 'GU_NM', '`ADMI_NM`':'DONG_NM','`RSPOP_CNT`':'POP_CNT'}, inplace = True)

len(list(amt['DONG_NM']))
len(list(amt['DONG_NM'].unique()))

### 신사동제거
dong_list = list(amt['DONG_NM'].unique())
dong_list.remove('신사동')

pop.keys()
amt['geometry'] = np.zeros((len(amt),1))
for i in dong_list:
    amt.loc[amt['DONG_NM']== i, 'geometry'] = pop.loc[pop['ADM_DR_NM'] == i, 'geometry'].item()
    
amt[amt['DONG_NM']=='신사동']
##14: 강남구, 85 : 관악구
pop[pop['ADM_DR_NM']=='신사동']
## 325 관악구, 354 강남구
amt.loc[14,'geometry'] = pop.loc[354, 'geometry']
amt.loc[85,'geometry'] = pop.loc[325, 'geometry']

with open('C:/Users/user/Desktop/Final_PJ/amt_final.bin', 'wb') as f:
    pickle.dump(amt, f)