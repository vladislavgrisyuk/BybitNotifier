import requests

URL = 'https://api2.bybit.com/fapi/beehive/public/v1/common/order/list-detail?timeStamp=1658218420604&leaderMark=lnOkBfOK6yeMGFaxdw4iFA%3D%3D'

print(requests.get(URL, headers={
    'User-Agent': 'vladislav'
}).status_code)
