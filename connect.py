import os

class rsync_connect():
    def __init__(self, name, system, user, folder, remote, port=None, delete=False, dryrun=False):
        self.name = name
        self.system = system
        self.user = user
        self.folder = folder
        self.remote = remote
        if not self.remote[-1] == '/':
            self.remote = self.remote + '/'
        if not self.folder[-1] == '/':
            self.folder = self.folder + '/'
        if port is not None:
            self.rsh = '--rsh="ssh -p ' + str(port) + '"'
        else:
            self.rsh = None
        self.delete = delete
        self.dryrun = dryrun

    def _options(self, dryrun, delete):
        opts = '-vrtu --no-motd --progress'
        if self.rsh is not None:
            opts = opts + ' ' + self.rsh
        if dryrun is not None:
            if dryrun:
                opts = opts + ' -n'
        elif self.dryrun:
            opts = opts + ' -n'
        if delete is not None:
            if delete:
                opts = opts + ' --delete'
        elif self.delete:
            opts = opts + ' --delete'
        return opts

    def _remote_folder(self):
        return ''.join([self.user,'@',self.system,':',self.remote])

    def _local_folder(self):
        return self.folder

    def _rsync_up(self, dryrun, delete):
        opts = self._options(dryrun, delete)
        rsync_command = ' '.join(['rsync', opts
            ,self._local_folder()
            ,self._remote_folder()
            ])
        return rsync_command

    def _rsync_down(self, dryrun, delete):
        opts = self._options(dryrun, delete)
        rsync_command = ' '.join(['rsync', opts
            ,self._remote_folder()
            ,self._local_folder()
            ])
        return rsync_command

    def upstream(self, dryrun=None, delete=None):
        rsync_command = self._rsync_up(dryrun, delete)
        print('Copying files upstream to {}'.format(self.name))
        #print(rsync_command)
        os.system(rsync_command)

    def downstream(self, dryrun=None, delete=None):
        rsync_command = self._rsync_down(dryrun, delete)
        print('Copying files downstream from {}'.format(self.name))
        #print(rsync_command)
        os.system(rsync_command)

    def sync(self, dryrun=None):
        rsync_up = self._rsync_up(dryrun, delete=False)
        print('Copying files upstream to {}'.format(self.name))
        #print(rsync_up)
        os.system(rsync_up)

        rsync_down = self._rsync_down(dryrun, delete=False)
        print('Copying files downstream from {}'.format(self.name))
        #print(rsync_down)
        os.system(rsync_down)

class connection_list():
    def __init__(self, user=None, folder=None, by_name=None, remote=None, port=None, delete=False, dryrun=False):
        self._connections = []
        self._user = user
        self._remote = remote
        self._port = port
        self._delete = delete
        self._dryrun = dryrun
        self._folder = folder
        self._by_name = by_name

    def add_rsync(self, name=None, system=None, user=None, folder=None, remote=None, port=None, delete=None, dryrun=None):
        if user is None:
            user = self._user
        if remote is None:
            remote = self._remote
        if port is None:
            port = self._port
        if delete is None:
            delete = self._delete
        if dryrun is None:
            dryrun = self._dryrun
        if folder is None:
            if self._by_name is not None:
                folder = self._by_name + name
            else:
                folder = self._folder
        self._connections.append(rsync_connect(name=name, folder=folder, user=user, system=system, remote=remote, port=port, delete=delete, dryrun=dryrun))

    def _runlist(self, systemlist):
        names = [s.name for s in self._connections]
        runlist = []
        for a in systemlist:
            if a.lower() == 'all':
                runlist = names
                break
            elif a.lower() in names:
                runlist.append(a.lower())
        return runlist

    def upstream(self, systemlist):
        for n in self._runlist(systemlist):
            system = [s for s in self._connections if s.name == n][0]
            system.upstream()

    def downstream(self, systemlist):
        for n in self._runlist(systemlist):
            system = [s for s in self._connections if s.name == n][0]
            system.downstream()

    def sync(self, systemlist):
        for n in self._runlist(systemlist):
            system = [s for s in self._connections if s.name == n][0]
            system.sync()

    def rsync_run_arguments(self, arglist):
        connect_type = 'sync'
        for a in arglist:
            if a.lower() in ('up,down'):
                connect_type = a.lower()
                arglist.remove(a)

        if connect_type == 'sync':
            self.sync(arglist)
        elif connect_type == 'up':
            self.upstream(arglist)
        elif connect_type == 'down':
            self.downstream(arglist)

