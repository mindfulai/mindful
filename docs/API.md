## 登录
URL: /user/<int:user_id>/authorized
Method: GET

Response:
```json
{
    "tiwtter_auth": "Boolean",
    "facebook_auth": "Boolean"
}
```

## Twitter 用户数据统计

URL: /twitter/<user_id>/summary
Method: GET
Data:
```json
{
    "datetime": "String",
    "period": "String"
}
```
Parameters:

参数      | 描述        | Example
-------- | ----------- | -------
datetime | 用户访问的时间 |
period   | 周期 | day / week / month


Response:
```json
{
    "tweets": "Integer",
    "mentions": "Integer"
}
```

## Facebook 用户统计接口

URL: /facebook/<user_id>/summary
Method: GET
Data:
```json
{
    "datetime": "String",
    "period": "String"
}
```
Parameters:

参数      | 描述        | Example
-------- | ----------- | -------
datetime | 用户访问的时间 |
period   | 周期 | day / week / month


Response:
```json
{
    "posts": "Integer",
}
```

## 存储用户地理位置及天气接口，并展示当日天气
URL: /user/<user_id>/location_and_weather/create
Method: POST
Data:
```json
{
    "latitude": "Float",
    "longitude": "Float"
}
```

Response:
```json
{
    "data": [
        {
            "apparentTemperatureHigh": 11.39,
            "apparentTemperatureHighTime": 1542693600,
            "apparentTemperatureLow": -0.46,
            "apparentTemperatureLowTime": 1542758400,
            "apparentTemperatureMax": 11.39,
            "apparentTemperatureMaxTime": 1542693600,
            "apparentTemperatureMin": -7.22,
            "apparentTemperatureMinTime": 1542657600,
            "cloudCover": 0.55,
            "dewPoint": -8.93,
            "humidity": 0.44,
            "icon": "partly-cloudy-night",
            "moonPhase": 0.39,
            "ozone": 335.53,
            "precipIntensity": 0,
            "precipIntensityMax": 0.0025,
            "precipIntensityMaxTime": 1542675600,
            "precipProbability": 0,
            "pressure": 1024.2,
            "summary": "Mostly cloudy throughout the day.",
            "sunriseTime": 1542668765,
            "sunsetTime": 1542704183,
            "temperatureHigh": 11.39,
            "temperatureHighTime": 1542693600,
            "temperatureLow": 0.66,
            "temperatureLowTime": 1542754800,
            "temperatureMax": 11.39,
            "temperatureMaxTime": 1542693600,
            "temperatureMin": -3.09,
            "temperatureMinTime": 1542657600,
            "time": 1542643200,
            "uvIndex": 2,
            "uvIndexTime": 1542682800,
            "visibility": 16.09,
            "windBearing": 21,
            "windGust": 4.1,
            "windGustTime": 1542704400,
            "windSpeed": 1.28
        }
    ]
}
```


## 创建心情接口
URL: /user/<user_id>/mood/create
Method: POST
Data:

```json
{
    "detail": "String",
    "score": "Integer"
}
```

Response:

```json
{
    "msg": "success"
}
```

## 展示心情列表接口
URL: /user/<user_id>/mood/list
Method: GET
Data:
```json
{
    "datetime": "2018-11-20 13:55:03+0800"
}
```

Response:

```json
[
    {
        "datetime": "Tue, 20 Nov 2018 05:03:40 GMT",
        "detail": "",
        "score": 4
    },
    {
        "datetime": "Tue, 20 Nov 2018 06:13:59 GMT",
        "detail": "happy",
        "score": 4
    }
]
```

## 展示心情平均值列表接口
URL: /user/<user_id>/mood/average/list
Method: GET
Data:
```json
{
    "datetime": "2018-11-20 13:55:03+0800",
    "period": "String"
}
```

Response:
```json
[
    {
        "datetime": "2018-11-20",
        "score": 4,
        "day_of_week": 2
    }
]
```
