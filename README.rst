##########
Distriploy
##########

This tool can assist you to perform deployment of release artifacts.


Installation
############

distriploy is available on pypi:

.. code:: sh

   python -m pip install --user distriploy


or you can grab a release or clone the repository and use it.


Configuration
#############

Before starting using `distriploy`, you need to make sure that:

- The repository you'd like to make a release of has been cloned with ssh (not https);
- The repository contains a `.distriploy.yml` file in its root folder.

See `this repo's <.distriploy.yml>`_ for inspiration.

The file is YAML, it contains an object with the following members:

- `release`: release information object
- `release.method`: release method. Supported values are:

  - `github`: the project has a github repo.

    Additional info may be provided if so:

    - `release.remote`: string, optional (defaults to `origin`)

      The local git repo remote corresponding to github.

    - `postrelease.add_mirror_urls`: bool (defaults to `false`)

      Whether to add to the release description a list of mirrors.
      Limited use because if github is down, the list is not
      accessible.

    - Environment variable `GITHUB_TOKEN`, must be populated by user,
      contains a token string created from
      https://github.com/settings/tokens

      Set it up with eg.:

      .. code:: sh

         read GITHUB_TOKEN
         export GITHUB_TOKEN

      Or add it to an environment file *not under revision control*.


- `mirrors`: mirroring information object, containing members whose
  key is a mirror handle.

  Each entry contains:

  `mirrors.${mirror}.method`: mirroring upload method. Supported
  values (unsupported are ignored, with a warning) are (TODO):

  - `osf`: upload to https://osf.io

    Use requires installation with `osf` option, or subsequent
    installation of the `osfclient` dependency.

    Additional info may be provided if so:

    - `project`: string, OSF project key

    - `folder`: string, OSF file folder

    - `name`: string, optional (defaults to release artifact name)

      Useful if using OSF's revision system.

    - Environment variables `OSF_USERNAME` and
      `OSF_PASSWORD`.

      Set it up with eg.:

      .. code:: sh

         read OSF_USERNAME OSF_PASSWORD
         export OSF_USERNAME OSF_PASSWORD

      Or add it to an environment file *not under revision control*.


  - `rsync`: upload with rsync

    Additional info may be provided if so:

    - `remote`: string, rsync destination
    - `public`: string, public URI prefix, accessible once upload is completed

  - `academictorrents`: create torrent file, and upload to https://academictorrents.com

    The torrent file will be generated in cwd, named like the release
    artifact and added`.torrent` extension.


    Additional info may be provided if so:

    - `params`: object, academictorrents upload params, to be POST'ed

    - Environment variables `ACADEMICTORRENTS_USERNAME` and
      `ACADEMICTORRENTS_PASSWORD`, must be populated by user,
      they come from uid & pass in https://academictorrents.com/about.php#apikeys

      Set it up with eg.:

      .. code:: sh

         read ACADEMICTORRENTS_USERNAME ACADEMICTORRENTS_PASSWORD
         export ACADEMICTORRENTS_USERNAME ACADEMICTORRENTS_PASSWORD

      Or add it to an environment file *not under revision control*.


Usage
#####

The repo should have been configured prior to that, see `configuration`_.

After its `installation`_, distriploy is typically called from your repo's
root folder using:

.. code:: sh

   distriploy

or:

.. code:: sh

   python -m distriploy

Run it with `--help` to get to know the options.

Prior to running `distriploy`, you might want to create a custom tag. It will be used to name the release. E.g.:

.. code:: sh

   git tag -s r$(date +%Y%m%d)



TODO
####

- get some use and feedback



License
#######

`MIT <LICENSE>`_.


Releasing
#########

.. code:: sh

   read version # eg. 0.14
   sed -i -e 's/^version = .*/version = "'${version}'"/g' setup.py
   git add setup.py
   git commit -m "preparation for v${version}"
   git tag --annotate --message "" v${version}
   git push; git push --tags
   rm -rf dist; python setup.py sdist && twine upload dist/* -r pypi
   python -m distriploy

