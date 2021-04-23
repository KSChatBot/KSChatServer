from bs4 import BeautifulSoup
import requests as req
import json
import pandas as pd
import datetime
from flask import Response, request, json, jsonify
from flask_restx import Resource, Namespace, fields
from database.models import Contents, User
import services.weather_info as wf

WeatherInfo_NS = Namespace(
    name="WeatherInfo",
    description="날씨 정보를 공공데이터나 네이버로 보터 가져오는 API.",
)

weaherinfo_fields = WeatherInfo_NS.model('WeatherInfo', {  # Model 객체 생성
    'api_name': fields.String(description='a Contents', required=True, example="날씨정보"),
    'sido': fields.String(description='날씨조회를 위한 시도명'),
    'gungu': fields.String(description='날씨조회를 위한 시군구명'),
    'dong': fields.String(description='날씨조회를 위한 동네명', required=True)
})


@WeatherInfo_NS.route('/get_naver')
class WeatherInfoNaver(Resource):
    @WeatherInfo_NS.expect(weaherinfo_fields)
    @WeatherInfo_NS.response(200, 'Success')
    @WeatherInfo_NS.response(500, 'Failed')
    def post(self):
        print('네이버 날씨 크롤링 시작!')
        try:
            data_json = request.data
            data_dict = json.loads(data_json)
            print("======네이버 날씨 크롤링정보=======")
            print(data_dict)
            print("======end 네이버 날씨 크롤링정보=======")

            api_name = data_dict.get('api_name')
            apicontent = Contents.objects.get(api_name=api_name)
            sido = data_dict.get('sido')
            gungu = data_dict.get('gungu')
            dong = data_dict.get('dong')

            # api_endpoint = 'https://search.naver.com/search.naver?'
            # payload = "query=" + sido + '+' + gungu + '+' + dong + '+' + "날씨"
            # print("네이버날씨URL:{}".format(callback_url + payload))
            # api_endpoint
            # api_key
            base_url = apicontent.api_endpoint + "query={}+{}+{}+날씨"
            url = base_url.format(sido, gungu, dong)
            print("url:",url)

            res = req.get(url)

            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                data1 = soup.find('div', {'class': 'weather_box'})
            elif res.status_code == 404:
                print('Not Found.')
                return {}, 200

            find_address = data1.find('span', {'class': 'btn_select'}).text
            # print('현재 위치: '+find_address)

            find_currenttemp = data1.find('span', {'class': 'todaytemp'}).text
            # print('현재 온도: '+find_currenttemp+'℃')

            data2 = data1.findAll('dd')
            find_dust = data2[0].find('span', {'class': 'num'}).text
            find_ultra_dust = data2[1].find('span', {'class': 'num'}).text
            find_ozone = data2[2].find('span', {'class': 'num'}).text
            # print('현재 미세먼지: '+find_dust)
            # print('현재 초미세먼지: '+find_ultra_dust)
            # print('현재 오존지수: '+find_ozone)

            data3 = data1.findAll('ul', {"class": "info_list"})

            find_currenttemp_desc = data3[0].find(
                'p', {'class': 'cast_txt'}).text
            find_today_low_temp = data3[0].find('span', {'class': 'min'}).text
            find_today_high_temp = data3[0].find('span', {'class': 'max'}).text
            find_today_exp_temp = data3[0].find('span', {'class': 'sensible'}).text

            print('네이버 날씨 크롤링 종료!')

            # return result_json_object, 200
            return { '현재위치': find_address,
                     '현재온도': find_currenttemp+'℃',
                     '날씨설명': find_currenttemp_desc,
                     '최저온도': find_today_low_temp,
                     '최고온도': find_today_high_temp,
                     '체감온도': find_today_exp_temp,
                     '미세먼지': find_dust,
                     '초미세먼지': find_ultra_dust,
                     '오존지수': find_ozone
            }, 200

        except:
            print("WeatherInfoNaver Exception error!")

@WeatherInfo_NS.route('/get_public_data')
class WeatherInfoPublicData(Resource):
    @WeatherInfo_NS.expect(weaherinfo_fields)
    @WeatherInfo_NS.response(200, 'Success')
    @WeatherInfo_NS.response(500, 'Failed')
    def post(self):
        print('공공데이터 동네예보조회 시작!')
        try:
            data_json = request.data
            data_dict = json.loads(data_json)
            print("======공공데이터 동네예보조회정보=======")
            print(data_dict)
            print("======end 공공데이터 동네예보조회정보=======")

            api_name = data_dict.get('api_name')
            apicontent = Contents.objects.get(api_name=api_name)
            sido = data_dict.get('sido')
            gungu = data_dict.get('gungu')
            dong = data_dict.get('dong')

            XY_data = wf.get_weather_location_XY(sido, gungu, dong)
            nx = XY_data[0]
            ny = XY_data[1]
            loc_name = XY_data[2]

            if ((nx < 0) or (ny < 0)):
                return {}, 404

            # api_endpoint = 'https://search.naver.com/search.naver?'
            # payload = "query=" + sido + '+' + gungu + '+' + dong + '+' + "날씨"
            # print("네이버날씨URL:{}".format(callback_url + payload))
            # api_endpoint
            # api_key
            # 동네예보조회 날씨 API 호출 처리를 위한 입력값 정의(Payload)
            date = wf.get_rpt_time()

            #     "numOfRows=10" + "&" +\
            #     "pageNo=1" + "&" +\

            payload = "serviceKey=" + apicontent.api_key + "&" +\
                "dataType=JSON" + "&" +\
                "numOfRows=10" + "&" +\
                "pageNo=1" + "&" +\
                "base_date=" + date[0] + "&" +\
                "base_time=" + date[1] + "&" +\
                "nx=" + str(nx) + "&" +\
                "ny=" + str(ny)

            # 동네예보조회 날씨 API 호출결과  처리 - 정상적 호출결과인 Json형태 여부 체크
            res = req.get(apicontent.api_endpoint + payload)

            if 'json' in res.headers.get('Content-Type'):
                data = json.loads(res.text)
            else:
                print('Response content is not in JSON format.')
                return {}, 404

            # 판다스이용 테이블 자료로 변환
            df_res = pd.DataFrame(data['response']['body']['items']['item'])

            # 출력 결과를 JSON으로 가공 출력
            result = {}
            result["현재위치"] =  loc_name    
            for index, row in df_res.iterrows():
                print("\t", wf.w_items[str(row['category'])][0], " : ", wf.get_real_value(row['category'], row['fcstValue']), end = "")
                result[wf.w_items[str(row['category'])][0]] =  wf.get_real_value(row['category'], row['fcstValue'])    
                if wf.w_items[str(row['category'])][1]  != "":
                    result[wf.w_items[str(row['category'])][0]] =  wf.get_real_value(row['category'], row['fcstValue']) + wf.w_items[str(row['category'])][1] 
                    print(wf.w_items[str(row['category'])][1])
                else:
                    print()

            print('공공데이터 동네예보조회 종료!')

            # Serializing json
            # result_json_object = json.dumps(result, indent = 4, ensure_ascii = False)  

            # return result_json_object, 200
            # return json.dumps(result, indent = 4, ensure_ascii = False), 200
            return result, 200

        except Exception as e:
            print("WeatherInfoPublicData Exception error! ==> ",e)
