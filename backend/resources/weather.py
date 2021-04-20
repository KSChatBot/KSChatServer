from bs4 import BeautifulSoup
import requests as req
import json
import pandas as pd
import datetime
from flask import Response, request, json, jsonify
from flask_restx import Resource, Namespace, fields
from database.models import API_Content, User

WeaherInfo_NS = Namespace(
    name="WeaherInfo",
    description="날씨 정보를 공공데이터나 네이버로 보터 가져오는 API.",
)

weaherinfo_fields = WeaherInfo_NS.model('WeaherInfo', {  # Model 객체 생성
    'api_name': fields.String(description='a API_Content', required=True, example="날씨정보"),
    'sido': fields.String(description='날씨조회를 위한 시도명'),
    'gungu': fields.String(description='날씨조회를 위한 시군구명'),
    'dong': fields.String(description='날씨조회를 위한 동네명', required=True)
})


@WeaherInfo_NS.route('/get_naver')
# /<string:callback_url><string:sido><string:gungu><string:dong>
class WeaherInfoNaver(Resource):
    @WeaherInfo_NS.expect(weaherinfo_fields)
    @WeaherInfo_NS.response(200, 'Success')
    @WeaherInfo_NS.response(500, 'Failed')
    def post(self):
        print('네이버 날씨 크롤링 시작!')
        try:
            data_json = request.data
            data_dict = json.loads(data_json)
            print("======네이버 날씨 크롤링정보=======")
            print(data_dict)
            print("======end 네이버 날씨 크롤링정보=======")

            api_name = data_dict.get('api_name')
            apicontent = API_Content.objects.get(api_name=api_name)
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
            print("WeaherInfoNaver Exception error!")
