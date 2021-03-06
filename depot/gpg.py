import getpass
import os

import gnupg


class GPG(object):
    def __init__(self, keyid, passphrase=None, key=None, home=None):
        self.gpg = gnupg.GPG(use_agent=False, gnupghome=home)
        if key:
            if not home:
                raise ValueError('Cowardly refusing to import key in to default key store')
            results = self.gpg.import_keys(key)
            keyid = results.fingerprints[0]
        self.keyid = keyid
        if not self.keyid:
            # Compat with how Freight does it.
            self.keyid = os.environ.get('GPG')
        self.passphrase = None
        self._verify(passphrase)

    def _verify(self, passphrase):
        """Some sanity checks on GPG."""
        if not self.keyid:
            raise ValueError('No GPG key specified for signing, did you mean to use --no-sign?')
        sign = self.gpg.sign('', keyid=self.keyid)
        if 'secret key not available' in sign.stderr:
            raise ValueError('Key not found')
        elif 'NEED_PASSPHRASE' in sign.stderr:
            self.passphrase = getpass.getpass('Passphrase for GPG key: ')
        else:
            self.passphrase = passphrase

    def sign(self, data, detach=False):
        sign = self.gpg.sign(data, keyid=self.keyid, passphrase=self.passphrase, detach=detach)
        if not sign:
            raise ValueError(sign.stderr)
        return str(sign)

    def public_key(self):
        return self.gpg.export_keys(self.keyid)
