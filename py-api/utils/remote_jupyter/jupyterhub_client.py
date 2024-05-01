from io import StringIO
import pandas as pd
#from websocket import create_connection
import json
import requests
import datetime
import uuid
import time
import ssl
import websocket

class RemoteResponse:
    """
        Class to interpret response from Jupyter 
    """
    def __init__(self,msgs):
        self.msgs = msgs
        
    def __done__(self):
        self.reply = self.get_msg_type('execute_reply')
        return self
        
    
    def get_msg_type(self,msg_type):
        return [x for x in self.msgs if x['msg_type'] == msg_type]
        
    def is_error(self):
        """
            Checks if the message list has an error
            
            Returns:
                Boolean indicator True: if error, False if not. 
        """
        if len(self.reply) == 1:
            return self.reply[0]['content']['status'] == 'error'
        return False
        
    def error(self):
        """
            Return error in the message stream
            
            Returns:
                String error message
        """
        if len(self.reply) == 1:
            return self.reply[0]['content'].get('evalue')
        return ''
        
    def traceback(self):
        """
            Prints traceback in case of an error
        """
        if len(self.reply) == 1:
            traceback = self.reply[0]['content'].get('traceback')
            for x in traceback:
                print(x)
            return None
        return None
    
    def is_idle(self, rsp):
        """
            Checks if kernel has come back to ids
            
            Argument:
                rsp: Response Json
            
            Returns:
                Boolean flag indicating if the kernel is idle
        """
        
        if rsp['msg_type'] != 'status':
            return False
        
        content = rsp.get('content')
        if content is None:
            return False
        
        state = content.get('execution_state')
        return state is not None and state == 'idle'
    
    def is_stdout(self, rsp):
        """
            Checks if a message has standard output
            
            Arguments:
                rsp: Response Json
                
            Returns:
                Boolean flag indicating if the message contains standard output
        """
        return rsp['msg_type'] == 'stream' and rsp['content']['name'] == 'stdout'
    
    def append(self, rsp):
        """
            Appends message to the message list. Returns false if the kernel 
            is idle. The caller can exit listening to the socket
            
            Arguments:
                rsp: Response Json
                
            Returns:
                Boolean flag indicating if the kernel is idle. 
        """
        self.msgs.append(rsp)
        if self.is_stdout(rsp):
            print(rsp['content']['text'],end='')
        return not self.is_idle(rsp)
        
    def stdout(self):
        """
            Returns Standard Output from Jupyterhub server
        """
        return '\n'.join([x['content']['text'] for x in self.msgs if self.is_stdout(x)])
                          
    def message_content(self):
        """
            Returns message content as a list
        """
        return [x['content'] for x in self.msgs]
        
        
class RemoteJupyterClient:
    """
        Python wrapper to interact with Remote Jupyter environment using the REST and Websocket API
    """

    def __init__(self, user, token, url, verify = False):
        """
        Constructor for RemoteJupyter Client

        Arguments:
            user: Jupyterhub user
            token: Authorization token. Should be generated using Jupyterhub UI or admin API
            url: URL of 
        """
        self.user = user
        self.token = token
        self.url = url
        self.verify = verify
        self.headers = {'Authorization': 'Token ' + token}
        
    def _url_(self,svc,path):
        if path:
            return 'https://' + self.url + "/user/" + self.user + '/api/' + svc + '/' + path
        else:
            return 'https://' + self.url + "/user/" + self.user + '/api/' + svc 
        
    def _post_(self,svc,path,payload):
        url =  self._url_(svc,path)
        response = requests.post(url,headers=self.headers, verify = self.verify, json = payload)
        return json.loads(response.text)
    
    def _get_(self,svc,path):
        url =  self._url_(svc,path)
        response = requests.get(url,headers=self.headers, verify = self.verify)
        return json.loads(response.text)
    
    def content(self, path):
        """
            Gets content of a directory path on remote server
            
            Arguments:
                path: Path on the remote server
        """
        v = self._get_('contents',path)
        
        if v['type'] == 'file':
            if v['mimetype'] == 'text/csv':
                return pd.read_csv(StringIO(v['content']))
        
        if v['type'] == 'directory':
            return pd.DataFrame(v['content'])
        
        if v['type'] == 'notebook':
            return pd.DataFrame(v['content']['cells'])

        return(v)
    
    def notebooks(self,path):
        """
            Lists down notebooks on the remote server
            
            Arguments:
                path: Path on the remote server
        """
        data = self.content(path)
        return data[data.type == 'notebook']
    
    def kernels(self):    
        """
            Lists down running kernles
        """
        return pd.DataFrame(self._get_('kernels', None))
    
    def _ws_(self, kernel):
        channel = "wss://" + self.url + "/user/" + self.user + "/api/kernels/" + kernel + "/channels"
        ws = websocket.WebSocket(sslopt ={"cert_reqs": ssl.CERT_NONE})
        return ws.connect(channel, header = self.headers)
    
    def _wst_(self, terminal):
        channel = "wss://" + self.url + "/user/" + self.user + "/terminals/websocket/" + terminal
        ws = websocket.WebSocket(sslopt ={"cert_reqs": ssl.CERT_NONE})
        return ws.connect(channel, header = self.headers)
    
    def _wsheader_(self, msg_type = 'execute_request'):
        return { 
            'msg_id' : uuid.uuid1().hex, 
            'username': self.user, 
            'session': uuid.uuid1().hex, 
            'data': datetime.datetime.now().isoformat(),
            'msg_type': msg_type,
            'version' : '5.1'
        }
                          
    def _code_msg_(self, code):
        hdr = self._wsheader_()
        return { 'header': hdr, 'parent_header': hdr, 'metadata': {}, 'content': { 'code' : code, 'silent':False } }
    
    def execute(self, kernel, code):
        """
            Executes code on the remote server
            
            Arguments:
                kernel: UID of a running kernel
                code: Code to be executed
                
            Returns:
                Response object 
        """
        wsconn = self._ws_(kernel)
        try:
            msg = self._code_msg_(code)
            wsconn.send(json.dumps(msg))
            response = RemoteResponse([])
            while True:
                rsp = json.loads(wsconn.recv())
                if not response.append(rsp):
                    response = response.__done__()
                    if response.is_error():
                        response.traceback()
                    return response
                        
            raise Exception("Should never come here...")
        finally:
            wsconn.close()
