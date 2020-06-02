"""Usage: depot [options] <package> [<package> ...]

-h --help                    show this help message and exit
--version                    show program's version number and exit
-s URI --storage=URI         URI for storage provider, checks $DEPOT_STORAGE or local://
-c NAME --codename=NAME      Debian distribution codename [default: lucid]
--component=NAME             Debian component name [default: main]
-a ARCH --architecture=ARCH  package architecture if not specified in package
-k KEYID --gpg-key=KEYID     GPG key ID to use for signing
--no-sign                    do not sign this upload
--no-public                  do not make cloud files public-readable
--force                      force upload, even if overwriting
--pool-path=PATH             override pool path for the package
--base-path=PATH             Base path where all begins ;-)
--passphrase=PASSPHRASE      The Passphrase generated using gpg --generate-key

Example:
depot -s s3://nr-repo-apt \
    -c precise \
    --gpg-key=258912FEA8A556A83881187D1099BA4A1F5BB4C0 \
    --base-path=infrastructure_agent/linux/apt \
    --pool-path=pool/main/n/nri-redis/nri-redis_1.4.0-1_amd64.deb \
    ../nri-redis_1.4.0-1_amd64.deb \
    --force

"""

from __future__ import print_function
import os
import sys

import docopt

from .apt import AptRepository
from .gpg import GPG
from .storage import StorageWrapper
from .version import __version_info__, __version__  # noqa


def main():
    args = docopt.docopt(__doc__, version='depot '+__version__)
    if args.get('--pool-path') and len(args['<package>']) > 1:
        print('--pool-path can only be specified for a single package', file=sys.stderr)
        sys.exit(1)
    if not args['--storage']:
        args['--storage'] = os.environ.get('DEPOT_STORAGE', 'local://')
    if args['--no-sign']:
        gpg = None
    else:
        gpg = GPG(args['--gpg-key'], args['--passphrase'])
    storage = StorageWrapper(args['--storage'], args['--no-public'])
    repo = AptRepository(storage, gpg, args['--codename'], args['--component'], args['--architecture'], args['--base-path'])
    for pkg_path in args['<package>']:
        if '@' in pkg_path:
            print('Copying package {0}'.format(pkg_path))
            repo.copy_package(pkg_path)
        else:
            print('Uploading package {0}'.format(pkg_path))
            fileobj = StorageWrapper.file(pkg_path)
            if not repo.add_package(pkg_path, fileobj, args['--force'], args['--base-path'] + '/' + args['--pool-path']):
                print('{0} already uploaded, skipping (use --force to override)'.format(pkg_path))
            fileobj.close()
    print('Uploading metadata')
    repo.commit_metadata()
