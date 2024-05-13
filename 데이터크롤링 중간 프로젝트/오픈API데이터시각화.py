import pandas as pd 
import matplotlib.pyplot as plt   # 막대그래프 시각화 라이브러리
import matplotlib
from matplotlib import font_manager, rc
import numpy as np 

df = pd.read_csv("2019년 노인복지시설 현황.csv", encoding="cp949")
print(df)


# 1. 다중막대그래프 생성 코드

x = df['지역']

y_label = ['총 합계', '재가노인복지시설_소계', '노인보호전문기관_소계', '노인여가복지시설_소계', '노인일자리지원기관_소계']
y_color = ['#FF033E', '#FFA07A', '#FFF700', '#98FB98', '#00FFFF']

# 글자 폰트 지정 
font_location = "C:/Windows/fonts/malgun.ttf"
font_name = font_manager.FontProperties(fname = font_location).get_name()
matplotlib.rc("font", family = font_name)

fig, ax = plt.subplots(figsize=(12,6))
bar_width = 0.15

index = np.arange(17)

# 각 복지수 별로 5개의 bar를 순서대로 나타내는 과정, 각 그래프는 0.15의 간격을 두고 그려짐

for i in range(1, 6):
    plt.bar(index + i * bar_width, df[y_label[i-1]], bar_width, color=y_color[i-1], label=y_label[i-1])

# x축 위치를 정 가운데로 조정하고 x축의 텍스트 정보와 매칭
plt.xticks(index + 2 * bar_width, x, rotation=45)
plt.title('노인복지시설 지역별 현황')

# x축, y축 이름 및 범례 설정
plt.xlabel('지역', size = 13)
plt.ylabel('노인복지시설 개수', size = 13)
plt.legend()
plt.tight_layout()
plt.show()

# 2. 파이차트 그래프 생성코드
sizes = df['총 합계']

# 파이 차트 그리기
fig, ax = plt.subplots()

threshold = 200  # 200 미만의 데이터는 기타로 간주 
df['지역'] = df.apply(lambda row: row['지역'] if row['총 합계'] >= threshold else '기타', axis=1)
df = df.groupby('지역')['총 합계'].sum().reset_index()

ax.pie(df['총 합계'], labels=df['지역'], autopct='%1.1f%%', startangle=90)
ax.axis('equal')

# 중앙에 텍스트 추가 (옵션)
plt.text(0, 0, '노인 복지시설', horizontalalignment='center', verticalalignment='center', fontsize=12, fontweight='bold')
plt.show()



