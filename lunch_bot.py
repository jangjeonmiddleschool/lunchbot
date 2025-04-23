from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

# 본인의 정보 입력하기
API_KEY = "95390d1b5c8a45dca471a46fd78ddbe1"
EDU_CODE = "C10"         # 서울교육청
SCHOOL_CODE = "7191033"  # 서울중학교 예시

def get_meal_info(date):
    url = f"https://open.neis.go.kr/hub/mealServiceDietInfo?KEY={API_KEY}&ATPT_OFCDC_SC_CODE={EDU_CODE}&SD_SCHUL_CODE={SCHOOL_CODE}&MLSV_YMD={date}&Type=json"
    res = requests.get(url)
    try:
        dish_info = res.json()['mealServiceDietInfo'][1]['row'][0]['DDISH_NM']
        dish_info = dish_info.replace("<br/>", "\n")
    except:
        dish_info = "해당 날짜의 급식 정보가 없습니다."
    return dish_info

@app.route("/lunch", methods=["POST"])
def today_lunch():
    today = datetime.today().strftime('%Y%m%d')
    meal = get_meal_info(today)
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": f"오늘의 급식입니다 🍽️\n\n{meal}"}}
            ]
        }
    })

@app.route("/lunch/tomorrow", methods=["POST"])
def tomorrow_lunch():
    tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y%m%d')
    meal = get_meal_info(tomorrow)
    return jsonify({
        "version": "2.0",
        "template": {
            "outputs": [
                {"simpleText": {"text": f"내일의 급식입니다 🍽️\n\n{meal}"}}
            ]
        }
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)