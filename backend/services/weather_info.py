import os
import datetime
import pandas as pd


#  날씨 API 호출 결과를 정리하기위한 설정
w_items = {"POP": ["강수확률", "%"],
           "PTY": ["강수형태", ""],
           "R06": ["6시간 강수량", "mm"],
           "REH": ["습도", "%"],
           "S06": ["6시간 신적설", "cm"],
           "SKY": ["하늘상태", ""],
           "T3H": ["3시간 기온", "°C"],
           "TMN": ["아침 최저 기온", "°C"],
           "TMX": ["낮 최고 기온", "°C"],
           "UUU": ["풍속(동서성분)", "m/s"],
           "VVV": ["풍속(남북성분)", "m/s"],
           "WAV": ["파고", "m"],
           "VEC": ["풍향", ""],
           "WSD": ["풍속", "m/s"]}
wind_dict = {0: "N", 1: "NNE", 2: "NE", 3: "ENE", 4: "E", 5: "ESE", 6: "SE", 7: "SSE",
             8: "S", 9: "SSW", 10: "SW", 11: "WSW", 12: "W", 13: "WNW", 14: "NW", 15: "NNW", 16: "N"}
rain_dict = {0: "없음", 1: "비", 2: "진눈깨비", 3: "눈"}

# 동네예보조회 날씨 API 처리를 위한 함수 정의
# 가장 최근의 기상청 예보 시간(02:10 이후 3시간 단위) get


def get_rpt_time():
    base_time = datetime.datetime.now() - datetime.timedelta(hours=2) - \
        datetime.timedelta(minutes=10)
    hour = int(base_time.strftime("%H"))
    rehour = str(hour//3*3 + 2).zfill(2)
    return [base_time.strftime("%Y%m%d"), rehour + "00"]

# 풍향 계산용


def get_wind_type(i):
    return wind_dict[(i + 22.5 * 0.5)//22.5]

# 하늘 상태 표시용


def get_sky_status(i):
    if i >= 0 and i <= 2:
        return "맑음"
    elif i >= 3 and i <= 5:
        return "구름조금"
    elif i >= 6 and i <= 8:
        return "구름많음"
    elif i >= 9 and i <= 10:
        return "흐림"


def get_real_value(c, s):
    if str(c) == "VEC":
        return get_wind_type(int(str(s)))
    elif str(c) == "SKY":
        return get_sky_status(int(str(s)))
    elif str(c) == "PTY":
        return rain_dict[int(str(s))]
    return str(s)


def get_weather_location_XY(sido, gungu, dong):
    print("Weather Location : {} {} {}".format(sido, gungu, dong))
    try:
        path = os.path.dirname(os.path.realpath(__file__))
        excel_file = 'weather_loc.xlsx'

        excel_pullpath = os.path.join(path, excel_file)
        print("엑셀파일 읽기시작")
        print("엑셀파일 Path : {}".format(excel_pullpath))
        try:
            # 첫번째 시트 : index_col=0, sheet_name='최종업데이트파일_20210106'
            df_sheet = pd.read_excel(excel_pullpath, index_col=0)
        except Exception as e:
            print("판다 엑셀읽기 오류 : ",e)
            return [0, 0]

        df_result = df_sheet[(df_sheet['1단계'].str.contains(sido, na=False)) & (
            df_sheet['2단계'].str.contains(gungu, na=False)) & (df_sheet['3단계'] == dong)]
        rows = df_result.shape[0]
        print("Query Location rows: {}".format(str(rows)))

        if rows > 0:
            X_value = df_result.loc[df_result.index[0], '격자 X']
            Y_value = df_result.loc[df_result.index[0], '격자 Y']
            loc1 = df_result.loc[df_result.index[0], '1단계']
            loc2 = df_result.loc[df_result.index[0], '2단계']
            loc3 = df_result.loc[df_result.index[0], '3단계']
        else:
            X_value = 0
            Y_value = 0

        print("Weather Location X:{} Y:{}".format(str(X_value), str(Y_value)))
        print("Weather Location name:{}".format(loc1 + " " + loc2 + " " + loc3))

        return [X_value, Y_value, loc1 + " " + loc2 + " " + loc3]

    except Exception as e:    # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
        print('예외가 발생했습니다.', e)


if __name__ == "__main__":
    sido = ""
    gungu = ""
    dong = "연남동"
    XY_data = get_weather_location_XY(sido, gungu, dong)
    print(str(XY_data[0]), str(XY_data[1]), XY_data[2])
