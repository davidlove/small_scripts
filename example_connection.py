#!/usr/bin/env python

import connect
import sys

systems = connect.connection_list(user='username', folder='by name', remote='~/documents', delete=True, dryrun=True);
systems.add_rsync(name='system1', system='some.url.com')
systems.add_rsync(name='system_not_default', system='some.other.url.net', user='otheruser', remote='/other/remote/path')

systems.rsync_run_arguments(sys.argv[1:])

