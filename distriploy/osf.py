#!/usr/bin/env python
# -*- coding: utf-8 vi:et

import sys, io, os, logging
import urllib.request, urllib.error

import osfclient


logger = logging.getLogger(__name__)


def upload_to_osf(osf_project_id, osf_username, osf_password, asset_path, osf_folder, osf_location=None):
    """
    Uploads new version of the data to the Open Science Framework.

    :return: osf download url of the newly uploaded asset.
    """

    upload_path = "/" + osf_folder
    if osf_location is not None:
      upload_path += "/" + osf_location
    else:
      upload_path += "/" + os.path.basename(asset_path)

    osf = osfclient.OSF()

    osf.login(username=osf_username, password=osf_password)

    project_storage = osf.project(osf_project_id).storage()

    logger.info("Uploading asset to OSF (project id:%s)", osf_project_id)

    with io.open(asset_path, "rb") as fup:
        project_storage.create_file(upload_path, fup)

        for file in project_storage.files:
            # compare strings instead of os.path.samefile() because objects are in different file systems.
            if file.path == upload_path:
                return file._download_url

