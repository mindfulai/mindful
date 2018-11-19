## 登录
URL: /user/<int:user_id>/authorized
Method: GET

Response:
```json
{
    "tiwtter_auth": "Boolean",
    "facebook_auth": "BOolean"
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

## 获取用户地理位置接口
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
    "msg": "success"
}
```
