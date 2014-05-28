import os

class rsync_connect():
    def __init__(self, name, system, user, folder, remote, delete=False, dryrun=False):
        self.name = name
        self.system = system
        self.user = user
        self.folder = folder
        self.remote = remote
        if not self.remote[-1] == '/':
            self.remote = self.remote + '/'
        if not self.folder[-1] == '/':
            self.folder = self.folder + '/'
        self.delete = delete
        self.dryrun = dryrun

    def _options(self, dryrun, delete):
        opts = '-vrtu --no-motd --progress'
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
    def __init__(self, user=None, folder=None, remote=None, delete=False, dryrun=False):
        self._connections = []
        self._user = user
        self._remote = remote
        self._delete = delete
        self._dryrun = dryrun
        if folder == 'by name' or folder is None:
            self._folder = 'by name'
        else:
            self._folder = folder

    def add_rsync(self, name=None, system=None, user=None, folder=None, remote=None, delete=None, dryrun=None):
        if user is None:
            user = self._user
        if remote is None:
            remote = self._remote
        if delete is None:
            delete = self._delete
        if dryrun is None:
            dryrun = self._dryrun
        if folder is None:
            folder = self._folder
            if folder == 'by name':
                folder = '$HOME/' + name
        self._connections.append(rsync_connect(name=name, folder=folder, user=user, system=system, remote=remote, delete=delete, dryrun=dryrun))

    def rsync_run_arguments(self, arglist):
        names = [s.name for s in self._connections]
        connect_type = 'sync'
        for a in arglist:
            if a.lower() in ('up,down'):
                connect_type = a.lower()
                arglist.remove(a)

        runlist = []
        for a in arglist:
            if a.lower() == 'all':
                runlist = names
                break
            elif a.lower() in names:
                runlist.append(a.lower())

        for n in runlist:
            system = [s for s in self._connections if s.name == n][0]
            if connect_type == 'sync':
                system.sync()
            elif connect_type == 'up':
                system.upstream()
            elif connect_type == 'down':
                system.downstream()

