'''
Created on 4 Mar 2020

@author: nilesh
'''

from jupyter_client.blocking.client import BlockingKernelClient

    
class CustomJupyterKernelClient(BlockingKernelClient):
    
    def __init__(self):
        super(CustomJupyterKernelClient, self).__init__()
        self._init_connection(connection_file="/home/nilesh/.local/share/jupyter/runtime/kernel-30840.json")
    
    def _init_connection(self, connection_file=None):
        self.load_connection_file(connection_file)

    def compute_option_pricing(self, code, silent=False, store_history=True,
                user_expressions=None, allow_stdin=None, stop_on_error=True):

        content = dict(code=code, silent=silent, store_history=store_history,
                       user_expressions=user_expressions,
                       allow_stdin=allow_stdin, stop_on_error=stop_on_error
                       )
        msg = self.session.msg('calculate_request', content)
        self.shell_channel.send(msg)
        return msg['header']['msg_id']



Test = CustomJupyterKernelClient()
msg_id = Test.compute_option_pricing("2+2")
io_msg = Test.get_iopub_msg(msg_id)
print(Test.get_iopub_msg())


    
    
    
    