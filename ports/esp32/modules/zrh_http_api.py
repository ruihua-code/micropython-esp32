from microdot_asyncio import Microdot
from zrh_response_json import ZrhResponseJson
from zrh_gpio import do_led
from zrh_ble_central import do_ble_central, stop_ble_central
import uasyncio as asyncio

resJson = ZrhResponseJson()
app = Microdot()


@app.post("/cmd")
async def cmd(request):
    params = request.json
    print("params:", params)
    print("params[cmd]:", params['cmd'])
    if params['cmd'] == 'ON_LED':
        do_led(params['data'])
        resJson.success("成功")
    elif params['cmd'] == "ON_BLE":
        if params['data']:
            _loop= asyncio.get_event_loop()
            _loop.run_until_complete(do_ble_central())
            resJson.success("成功")
        else:
            stop_ble_central()
            resJson.success("成功")
    else:
        resJson.error("没有对应接口操作")
    return resJson.json()


@app.errorhandler(404)
def not_found(request):
    resJson.error("找不到接口，无法影响")
    return resJson.json(), 404


async def do_http_api():
    app.run(debug=True, port=80)
