import urllib.request           # 웹 페이지 URL 요청 및 데이터를 가져오기 위한 기능을 제공하는 모듈
import datetime                 # 날짜/시간을 처리하기 위한 기능을 제공하는 모듈 
import json                     # json 데이터 처리를 위해 필요한 기능을 제공하는 모듈
import pandas as pd             # 데이터 시각화 라이브러리,( 엑셀에 저장할 데이터를 테이블형태로 출력 )

# 공공데이터 신청 인증키 
ServiceKey="zSzg4Y4jSKTiGIFnteuCLXegYYwxYddOKuxlcHIJNMqsDxJcYu5AxwUbjBsqb7%2BY4f7oJ83nuhY%2FG4GP1HF9GA%3D%3D"


#[CODE 1]
def getRequestUrl(url):                                                             # url 매개변수를 받는 함수를 정의, URL 요청을 위한 함수 
    req = urllib.request.Request(url)                                               # URL 요청을 Request 클래스를 통해 해당 요청에 대한 인스턴스를 받아오는 코드 
    try:                                                                            # 예외처리 구문 
        response = urllib.request.urlopen(req)                                      # req 객체를 Url Open 함수로 호출합니다. 
        if response.getcode() == 200:                                               # 정상적인 API 요청일때 getcode() 함수는 Http 상태코드 200을 반환하며 정상적으로 요청이 온 경우에 위에 If문 실행            
            print ("[%s] 보건 공공데이터 호출" % datetime.datetime.now())           # http 요청 성공시 성공시간, 성공문구를 Print 
            return response.read().decode('utf-8')                                  # URL 응답리턴값을 UTF-8 로 인코딩하여 받아온다. 
    except Exception as e:                                                          # 요청 실패시 에러문구와 요청 실패 URl Print 
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

#[CODE 2]
def getServiceCenterItem(pageNo, numRs, yyyymm):                                    # 공공API 데이터 요청을 위한 문자열 파라미터 값 세팅 ( 파라미터 : 인증키, 페이지 번호, 페이지 결과 수, 데이터유형, 연도 )
    service_url = "http://apis.data.go.kr/1352000/ODMS_STAT_27/callStat27Api"       # 호출 URL 
    parameters = "?serviceKey=" + ServiceKey                                        # 서비스키 
    parameters += "&pageNo=" + pageNo
    parameters += "&numOfRows=" + numRs
    parameters += "&apiType=JSON"
    parameters += "&year=" + yyyymm

    url = service_url + parameters
    
    retData = getRequestUrl(url)                                                    #[CODE 1] 함수를 파라미터 세팅된 URL로 호출 
    
    if (retData == None):                                                           # 리턴값이 없거나 요청오류일때 None 반환 
        return None
    else:
         return json.loads(retData)                                                 # Json 모듈의 loads 함수를 이용하여 Json 데이터를 파이썬 객체로 변환한다.


#[CODE 3]
def getServiceCenter(pageNo, numRs, yyyymm):
    jsonResult = [] 
    result = [] 
    dvsd = ""

    # 1. 재가노인복지시설_소계, 2. 노인보호전문기관, 3. 노인여가복지시설(노인복지관), 4. 노인일자리지원기관
    center = [0, 0, 0, 0]
    
    total = 0
    
    jsonData = getServiceCenterItem(pageNo, numRs, yyyymm)                  #[CODE 2] 공공데이터 API 호출

    if (jsonData['resultCode'] == '00'):                                    # 정상적인 호출일 때 서비스코드 00
        print("API 데이터 호출 성공")
    for item in jsonData["items"]:
        dvsd = item['dvsd']
        
        center[0] = int(0 if item['hmwlfSbtlNmfcl'] == "null" else item['hmwlfSbtlNmfcl'])
        center[1] = int(0 if item['snptNmfcl'] == "null" else item['snptNmfcl'])
        center[2] = int(0 if item['snwlfc']  == "null" else item['snwlfc'])
        center[3] = int(0 if item['sempsNmfcl']  == "null" else item['sempsNmfcl'])

        total = center[0] + center[1] + center[2] + center[3]
        print("[지역: %s, 1. 재가노인복지시설_소계: %d, 2. 노인보호전문기관: %d, 3. 노인여가복지시설(노인복지관): %d, 4. 노인일자리지원기관: %d, 총 개수 : %d]"
              % (dvsd, center[0], center[1], center[2], center[3], total))
        
        result.append([dvsd, center[0], center[1], center[2], center[3], total]) # 원소로 데이터 저장 
        
    return result

#[CODE 0]
def main():
    result = []
    
    print("<< 전국 노인복지시설 통계 데이터를 수집합니다. >>")
    yyyymm = input('수집연도를 입력하세요(2015 ~ 2019): ')         #수집연도 입력
    
    result = getServiceCenter("1", "500", yyyymm)       #[CODE 3] 파이썬 크롤링 함수 호출

    if(len(result) == 0):
        print('데이터가 전달되지 않았습니다. 공공데이터포털의 서비스 상태를 확인하기 바랍니다.')
    else:
                      
        #파일저장 : csv 파일, 받은 데이터를 csv 파일로 저장, pandas 라이브러리 데이터프레임 이용  
        columns = ["지역", "재가노인복지시설_소계", "노인보호전문기관_소계", "노인여가복지시설_소계", "노인일자리지원기관_소계", "총 합계"]
                      
        result_df = pd.DataFrame(result, columns = columns)
        
        # index : index 출력여부, encoding = 한글이 깨지지 않기 위해 완성형 한글로 지정
        result_df.to_csv('./%s년 노인복지시설 현황.csv' % yyyymm, index=False, encoding='cp949') 
        print("*******************************")
        print("파일저장 완료!")
        
    
if __name__ == '__main__':          # 인터프린터에서 실행시 __name__ 변수에 __main__ 저장, 모듈 실행시엔 executeThisModule 저장  
    main()
