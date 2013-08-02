#!/usr/bin/env python

import sys
from nova import config
from nova import context
from nova.conductor import api
from nova.openstack.common.rpc import impl_kombu, common

def main(filter):
    # not entirely sure what happens here, but once this is
    # run we have access to all the CONF keys/values
    config.parse_args([])
    conductor_api = api.API()
    #ctxt = context.RequestContext(user_id="admin", project_id="admin",
    #                              is_admin=True)
    ctxt = context.get_admin_context()

    # can't filter by {'host': None} for whatever reason :-/
    if filter == "all":
        filters = {'vm_state': 'error'}
    else:
        filters = {'host': 'ha-controller2', 'vm_state': 'error'}

    try:
        instances = conductor_api.instance_get_all_by_filters(ctxt, filters)
    except common.Timeout:
        print "status timeout"
        sys.exit(1)

    count = 0

    for i in instances:
        # we skip these instances as they'll be accounted for when run from
        # the compute node
        if filter == "all" and i['host'] is not None:
            continue

        count += 1

    print "status success"
    print "metric error int32 %d" % count
    #print "metric error int32 10"

if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] in ('all', 'one'):
            filter = sys.argv[1]
        else:
            print "status invalid argument"
            sys.exit(1)

        main(filter)
