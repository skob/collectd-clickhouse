'''
clickhouse plugin written in Python.
For details on plugin's architecture, see: man 5 collectd-python
'''

import collectd
import requests

PLUGIN_NAME = 'clickhouse'
INTERVAL = 5 # seconds

URL = "http://localhost:8123"
User = "default"
Password = ""

def configure(configobj):
    '''Configure this plugin based on collectd.conf parts.

    Example configuration:
    <LoadPlugin python>
	   Globals true
    </LoadPlugin>
    ...
    <Plugin python>
        ModulePath "/usr/local/lib/collectd/python/"
        LogTraces true
        Interactive false
        Import "clickhouse"
        <Module clickhouse>
            URL "http://localhost:8123/"
            User "default"
            Password ""
        </Module>
    </Plugin>
    '''
    global URL
    global User
    global Password

    config = {c.key: c.values for c in configobj.children}
    URL = next(iter(config.get('URL', 'http://localhost:8123')))
    User = next(iter(config.get('User', 'default')))
    Password = next(iter(config.get('Password', '')))

def read(data=None):
    global URL
    global User
    global Password

    rs = requests.get( URL + "/?query=SELECT%20*%20FROM%20system.asynchronous_metrics%20FORMAT%20JSON", auth=(User, Password) )
    json = rs.json()
    for metric in json['data']:
        vl = collectd.Values(type='asynchronous_metrics', type_instance=metric['metric'])
        vl.plugin = PLUGIN_NAME
        vl.values = [metric['value']]
        vl.dispatch()

    rs = requests.get( URL + "/?query=SELECT%20*%20FROM%20system.metrics%20FORMAT%20JSON", auth=(User, Password) )
    json = rs.json()
    for metric in json['data']:
        vl = collectd.Values(type='metrics', type_instance=metric['metric'])
        vl.plugin = PLUGIN_NAME
        vl.values = [metric['value']]
        vl.dispatch()

    rs = requests.get( URL + "/?query=SELECT%20*%20FROM%20system.events%20FORMAT%20JSON", auth=(User, Password) )
    json = rs.json()
    for metric in json['data']:
        vl = collectd.Values(type='events', type_instance=metric['event'])
        vl.plugin = PLUGIN_NAME
        vl.values = [metric['value']]
        vl.dispatch()

collectd.register_config(configure)
collectd.register_read(read, INTERVAL)
