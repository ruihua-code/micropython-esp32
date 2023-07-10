import uasyncio as asyncio
from zrh_wifi import do_connect
from zrh_http_api import do_http_api


do_connect()
loop = asyncio.get_event_loop()
loop.run_until_complete(do_http_api())
