'''
Created on 4 Mar 2020

@author: nilesh
'''

from jupyter_client import KernelClient, BlockingKernelClient
from traitlets import Type
from jupyter_client.asynchronous.channels import ZMQSocketChannel
from jupyter_client.channels import HBChannel
import queue

def reqrep(meth, channel='shell'):
    def wrapped(self, *args, **kwargs):
        reply = kwargs.pop('reply', False)
        timeout = kwargs.pop('timeout', None)
        msg_id = meth(self, *args, **kwargs)
        if not reply:
            return msg_id

        return self._recv_reply(msg_id, timeout=timeout, channel=channel)
    
class CustomJupyterKernelClient(KernelClient):

    # The classes to use for the various channels
    shell_channel_class = Type(ZMQSocketChannel)
    iopub_channel_class = Type(ZMQSocketChannel)
    stdin_channel_class = Type(ZMQSocketChannel)
    hb_channel_class = Type(HBChannel)
    control_channel_class = Type(ZMQSocketChannel)

    # replies come on the shell channel
    execute = reqrep(KernelClient.execute)
    history = reqrep(KernelClient.history)
    complete = reqrep(KernelClient.complete)
    inspect = reqrep(KernelClient.inspect)
    kernel_info = reqrep(KernelClient.kernel_info)
    comm_info = reqrep(KernelClient.comm_info)

    # replies come on the control channel
    shutdown = reqrep(KernelClient.shutdown, channel='control')
    
    def __init__(self):
        super(CustomJupyterKernelClient, self).__init__()
        self._init_connection(connection_file="/home/nilesh/.local/share/jupyter/runtime/kernel-28477.json")
    
    def _init_connection(self, connection_file=None):
        self.load_connection_file(connection_file)
    
    def start_channel(self, shell=True, iopub=True, stdin=True, hb=True):
        self.start_channels(self, shell=shell, iopub=iopub, stdin=stdin, hb=hb)
        
    def execute(self, code, silent=False, store_history=True,
                user_expressions=None, allow_stdin=None, stop_on_error=True):

        content = dict(code=code, silent=silent, store_history=store_history,
                       user_expressions=user_expressions,
                       allow_stdin=allow_stdin, stop_on_error=stop_on_error
                       )
        print(content)
        msg = self.session.msg('execute_request', content)
        #msg = self.session.msg('calculate_bs', content)
        self.shell_channel.send(msg)
        return msg['header']['msg_id']

    def compute_option_pricing(self, code, silent=False, store_history=True,
                user_expressions=None, allow_stdin=None, stop_on_error=True):

        content = dict(code=code, silent=silent, store_history=store_history,
                       user_expressions=user_expressions,
                       allow_stdin=allow_stdin, stop_on_error=stop_on_error
                       )
        msg = self.session.msg('calculate_request', content)
        #msg = self.session.msg('calculate_bs', content)
        self.shell_channel.send(msg)
        return msg['header']['msg_id']

# 

Test = CustomJupyterKernelClient()
msg_id = Test.compute_option_pricing("2+2")
io_msg = Test.get_iopub_msg(msg_id)
print(io_msg)

    
    
    
    