'''
Created on 8 Mar 2020

@author: nilesh
'''
import asyncio
from jupyter_client.asynchronous.client import AsyncKernelClient

class CustomJupyterKernelClient(AsyncKernelClient):
    
    def __init__(self):
        super(CustomJupyterKernelClient, self).__init__()
        self._init_connection(connection_file="/home/nilesh/.local/share/jupyter/runtime/kernel-32350.json")
    
    def _init_connection(self, connection_file=None):
        self.load_connection_file(connection_file)

    async def compute_option_pricing(self, code, silent=False, store_history=True,
                user_expressions=None, allow_stdin=None, stop_on_error=True):

        content = dict(code=code, silent=silent, store_history=store_history,
                       user_expressions=user_expressions,
                       allow_stdin=allow_stdin, stop_on_error=stop_on_error
                       )
        msg = self.session.msg('calculate_request', content)
        self.shell_channel.send(msg)
        return msg['header']['msg_id']

async def main():
    kc = CustomJupyterKernelClient()
    while True:
        res = await kc.compute_option_pricing("2+2")
        msg = await kc.get_iopub_msg()
        print(msg)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
    