
with open('C:/Users/user/Desktop/Final_PJ/amt_final.bin', 'rb') as f:
    amt = pickle.load(f)    

pop.keys()

blue = pd.read_csv('C:/Users/user/Desktop/Final_PJ/blues_index(임시).csv')

base = pop[['GU_CD','GU_NM','ADM_DR_CD','ADM_DR_NM']]

base.rename(columns = {'ADM_DR_CD':'DONG_CD','ADM_DR_NM':'DONG_NM'}, inplace = True)

base['GEO_SCORE'] = np.zeros((len(base),1))
base['BLUE_SCORE'] = np.zeros((len(base),1))
base['AMT_SCORE'] = np.zeros((len(base),1))
base['ALONE_SCORE'] = np.zeros((len(base),1))

i = 1

'신사동' in dong_list

for i in dong_list:
    base.loc[base['DONG_NM'] == i, 'ALONE_SCORE'] = alone.loc[alone['DONG_NM'] == i, 'CNT'].item()
    base.loc[base['DONG_NM'] == i, 'GEO_SCORE'] = pop.loc[pop['ADM_DR_NM'] == i, 'GEO_DIST'].item()
    base.loc[base['DONG_NM'] == i, 'AMT_SCORE'] = amt.loc[amt['DONG_NM'] == i, 'rate'].item()

base.loc[base['DONG_NM'] == '신사동', :]
alone.loc[alone['DONG_NM'] == '신사동', :]
pop.loc[pop['ADM_DR_NM'] == '신사동', :]
amt.loc[amt['DONG_NM'] == '신사동', :]

# 강남구
base.loc[354, 'ALONE_SCORE'] = alone.loc[12,'score'].item()
base.loc[354, 'GEO_SCORE'] = pop.loc[354,'GEO_SCORE'].item()
base.loc[354, 'AMT_SCORE'] = amt.loc[14,'scale'].item()

# 관악구
base.loc[325, 'ALONE_SCORE'] = alone.loc[78,'score'].item()
base.loc[325, 'GEO_SCORE'] = pop.loc[325,'GEO_SCORE'].item()
base.loc[325, 'AMT_SCORE'] = amt.loc[85,'scale'].item()

gu_list = list(blue['구'])
for i in gu_list:
    small_gu_list = list(base.loc[base['GU_NM'] == i, :].index)
    for j in small_gu_list:
        base.loc[j,'stress_pop'] = gu_pop.loc[gu_pop['GU_NM']== i,'stress_pop'].item()


for i in gu_list:
    small_gu_list = list(base.loc[base['GU_NM'] == i, :].index)
    for j in small_gu_list:
        base.loc[j,'society_pop'] = gu_pop.loc[gu_pop['GU_NM']== i,'society_pop'].item()
        
for i in gu_list:
    small_gu_list = list(base.loc[base['GU_NM'] == i, :].index)
    for j in small_gu_list:
        base.loc[j,'blue_pop'] = gu_pop.loc[gu_pop['GU_NM']== i,'blue_pop'].item()


####
base['stress_pop'] = gu_pop['stress_pop']
base['society_pop'] = gu_pop['society_pop']
base['blue_pop'] = gu_pop['blue_pop']
###

#BLUE 스케일 조정
max_x = base['BLUE_SCORE'].max()
min_x = base['BLUE_SCORE'].min()
base['BLUE_SCORE'] = base['BLUE_SCORE'].map(lambda x: (x-min_x)/(max_x-min_x))


with open('C:/Users/user/Desktop/Final_PJ/FIANL_OUTPUT.bin', 'wb') as f:
    pickle.dump(base, f)


## 단순 거리를 10000으로 나누는형식으로 변형하게되면