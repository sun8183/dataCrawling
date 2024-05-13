import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager, rc

# 수집 데이터 읽어오기 
dfCenter = pd.read_csv("2019년 노인복지시설 현황.csv", encoding="cp949")
dfPerson = pd.read_csv("주민등록인구(고령 인구현황)_OldAge.csv", encoding="cp949")

# 여기서 할 작업은 노인 인구수 대비 복지시설이 적절하게 있는지 확인하기 위한 작업 

dicCenter = dfCenter.to_dict()
dicPerson = dfPerson.to_dict()

local = [i for i in dicCenter['지역'].keys()]   # 변수 초기화

# 지역값에 맞게 딕셔너리로 선언 
dataCenter = {}
dataPerson = {}
dataResult = {}

num = 0

for item in dicCenter['지역'].values():
    local[num] = item.replace(" ", "")
    num = num + 1

num = 0

for item in dicCenter['총 합계'].values():
    dataCenter[local[num]] = item
    num = num + 1

num = 0

for item in dicPerson['지역'].values():
    if item == "전국" :
        continue
    else :
        local[num] = item.replace(" ", "")
        num = num + 1

num = 0

row = False

for item in dicPerson['65세이상전체'].values():
    if num == 0 and not row :
        row = True
    else :
        dataPerson[local[num]] = item.replace(",", "")
        num = num + 1
        
for item in local:
    result = int(dataPerson[item]) // int(dataCenter[item])
    dataResult[item] = result       # 노인 인구수 대비 복지시설 현황 데이터 

# 글자 폰트 지정 
font_location = "C:/Windows/fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname = font_location).get_name()
matplotlib.rc("font", family = font_name)

# 레이블과 데이터 추출
labels = dataResult.keys()
values = dataResult.values()

# 막대그래프를 그립니다.
plt.figure(figsize=(8, 6))  # 그래프 크기 설정
plt.bar(labels, values)  # 막대그래프 그리기
plt.xlabel('지역')  # x 축 레이블 설정
plt.ylabel('노인인구수 대비 복지시설')  # y 축 레이블 설정
plt.title('노인인구수 대비 복지시설 현황')  # 그래프 제목 설정

# 그래프를 보여줍니다.
plt.show()
