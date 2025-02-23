import os
import sys
sys.path.append('../../../')

from bfxapi import Client, Order
from bfxapi.constants import WS_HOST, REST_HOST

API_KEY=os.getenv("BFX_KEY")
API_SECRET=os.getenv("BFX_SECRET")

# Sending order requires private hosts
bfx = Client(
  API_KEY=API_KEY,
  API_SECRET=API_SECRET,
  logLevel='DEBUG',
  ws_host=WS_HOST,
  rest_host=REST_HOST
)

@bfx.ws.on('order_snapshot')
async def cancel_all(data):
  await bfx.ws.cancel_all_orders()

@bfx.ws.on('order_confirmed')
async def trade_completed(order):
  print ("Order confirmed.")
  print (order)
  ## close the order
  # await order.close()
  # or
  # await bfx.ws.cancel_order(order.id)
  # or
  # await bfx.ws.cancel_all_orders()

@bfx.ws.on('error')
def log_error(msg):
  print ("Error: {}".format(msg))

@bfx.ws.on('authenticated')
async def submit_order(auth_message):
  await bfx.ws.submit_order(symbol='tBTCUSD', price=None, amount=0.01, market_type=Order.Type.EXCHANGE_MARKET)

# If you dont want to use a decorator
# ws.on('authenticated', submit_order)
# ws.on('error', log_error)

# You can also provide a callback
# await ws.submit_order('tBTCUSD', 0, 0.01,
# 'EXCHANGE MARKET', onClose=trade_complete)

bfx.ws.run()
