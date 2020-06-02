Depot
=====

Used to push, it is a replacement for reprepro+s3cmd sync and whatnot.

It does incremental updates of a repo, so you don't need to keep a full local copy of the repo anymore.

You just feed it each package as they are made and it updates all the various metadata files as needed.

Usage
-----

```
  Usage: depot [options] <package> [<package> ...]

  -h --help                    show this help message and exit
  --version                    show program's version number and exit
  -s URI --storage=URI         URI for storage provider, checks $DEPOT_STORAGE or local://
  -c NAME --codename=NAME      Debian distribution codename [default: lucid]
  --component=NAME             Debian component name [default: main]
  -a ARCH --architecture=ARCH  package architecture if not specified in package
  -k KEYID --gpg-key=KEYID     GPG key ID to use for signing
  --no-sign                    do not sign this upload
  --no-public                  do not make cloud files public-readable
  --base-path=PATH             Base path where all begins ;-)
  --passphrase=PASSPHRASE      The Passphrase generated using gpg --generate-key
```

Example
-------

```
  depot -s s3://nr-repo-apt \
    --component precise \
    --gpg-key=258912FEA8A556A83881187D1099BA4A1F5BB4C0 \
    --passphrase=PASSPHRASE \
    --base-path=infrastructure_agent/linux/apt \
    --pool-path=pool/main/n/nri-redis/nri-redis_1.4.0-1_amd64.deb \
    ../nri-redis_1.4.0-1_amd64.deb \
    --force
```


Repo dir structure
-------------------
```
└── infrastructure_agent/linux/apt/
    ├── pool/
    │   └── main/
    │       └── n/
    │           ├── nri-redis/
    │           │   └── nri-redis_1.4.0-1_amd64.deb
    │           └── nri-fafka/
    └── dists/
        ├── precise/
        │   └── main/
        │       ├── binary-all/
        │       ├── binary-amd64/
        │       │   ├── Packages
        │       │   ├── Packages.bz2
        │       │   └── Packages.gz
        │       └── source/
        └── bionic
```

Storage Location
----------------

Storage locations are given as URIs like local:///srv/repo or s3://key:secret@bucket. Any scheme supported
by libcloud should work, but only local and s3 have been tested so far.

S3 Credentials
--------------

You can pass your AWS access key ID and secret access key as the username and password in the storage URI,
or if not present depot will check the $AWS_ACCESS_KEY_ID and $AWS_SECRET_ACCESS_KEY environment variables.


Credits
-------
Thanks to coderanger https://github.com/coderanger/depot
