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
