#!/usr/bin/env python

import sys
from nova import config
from nova import context
from nova.conductor import api
from nova.openstack.common.rpc import impl_kombu, common

# not entirely sure what happens here, but once this is
# run we have access to all the CONF keys/values
config.parse_args([])
conductor_api = api.API()
#ctxt = context.RequestContext(user_id="admin", project_id="admin",
#                              is_admin=True)
ctxt = context.get_admin_context()

try:
    #instances = conductor_api.instance_get_all(context)
    instances = conductor_api.instance_get_all_by_host(ctxt, api.CONF.host)
except common.Timeout:
    print "status timeout"
    sys.exit(1)

count = 0

for i in instances:
    if i['vm_state'] == 'error':
        count += 1

print "status success"
print "metric error int32 %d" % count
#print "metric error int32 10"
