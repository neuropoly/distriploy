##########
Distriploy
##########

This tool can assist you to perform deployment of release artifacts.

Usage
#####

Typically called from your repo using:

.. code:: sh

   python -m distriploy

The repo should have been configured prior to that, see `configuration`_.


Configuration
#############

An enabled repository has a `.distriploy.yml` file in its root folder.


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

    Additional info may be provided if so:

    - `project`: string, OSF project key

    - `folder`: string, OSF file folder

    - `name`: string, optional (defaults to release artifact name)

      Useful if using OSF's revision system.

  - `rsync`: upload with rsync

    Additional info may be provided if so:

    - `remote`: string, rsync destination

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


License
#######

`MIT <LICENSE>`_.
