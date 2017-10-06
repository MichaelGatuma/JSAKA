'''
Created on Sep 23, 2017

@author: duncan
'''
from bs4 import BeautifulSoup
import logging   
#from mitmproxy import ctx


logger = logging.getLogger(__name__)
# load in the javascript to inject
with open('content.js', 'r') as f:
    content_js = f.read()

def response(flow):
    # only process 200 responses of html content
    try:
        if flow.response.headers['content-type'] != 'text/html':
            return
    except KeyError:
        logger.error("No content-type header")
        
    if not flow.response.status_code == 200:
        return

    # inject the script tag
    html = BeautifulSoup(flow.response.text, 'lxml')
    container = html.head or html.body
    if container:
        script = html.new_tag('script', type='text/javascript')
        script.string = content_js
        container.insert(0, script)
        flow.response.text = str(html)

       # ctx.log('Successfully injected the content.js script.')