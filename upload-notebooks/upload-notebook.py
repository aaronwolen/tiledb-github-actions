#!/usr/bin/env python

# Upload notebook to TileDB Cloud
#
# Usage:
#     python upload-notebook.py <path/to/notebook.ipynb>
#
# Variables read from the environment:
#   - TILEDB_CLOUD_TOKEN: API token for TileDB Cloud account (required)
#   - TILEDB_CLOUD_NAMESPACE: Namespace for TileDB Cloud (required)
#   - TILEDB_CLOUD_STORAGE_PATH: Storage path on TileDB Cloud (optional)
#   - TILEDB_CLOUD_STORAGE_CREDENTIAL_NAME: Storage credentials to use on TileDB Cloud (optional)


import os
import sys

import tiledb.cloud

token = os.environ.get("TILEDB_CLOUD_TOKEN")
namespace = os.environ.get("TILEDB_CLOUD_NAMESPACE")
storage_path = os.environ.get("TILEDB_CLOUD_STORAGE_PATH")
storage_credential_name = os.environ.get("TILEDB_CLOUD_STORAGE_CREDENTIAL_NAME")

if tiledb.cloud.Config()['rest.token'] == '':
    tiledb.cloud.login(token=token)
user = tiledb.cloud.user_profile()
sys.stdout.write("Logged into TileDB Cloud as %s\n" % (user.username))

args = sys.argv
if len(args) != 2:
    sys.stderr.write("Usage: python upload-notebook.py <path/to/notebook.ipynb>\n")
    sys.exit(1)

notebook = args[1]
if not os.path.exists(notebook):
    sys.stderr.write("Notebook file does not exist: %s\n" % (notebook))
    sys.exit(1)

notebook_name, ext = os.path.splitext(notebook)
notebook_name = os.path.basename(notebook_name)
if ext != ".ipynb":
    sys.stderr.write("Notebook file extension must be '.ipynb', not '%s'\n" % (ext))
    sys.exit(1)

try:
    tiledb.cloud.upload_notebook_from_file(
        ipynb_file_name=notebook,
        namespace=namespace,
        array_name=notebook_name,
        storage_path=storage_path,
        storage_credential_name=storage_credential_name,
        on_exists=tiledb.cloud.notebook.OnExists.OVERWRITE,
    )
except tiledb.cc.TileDBError:
    # If it's a new file, can't use OVERWRITE
    tiledb.cloud.upload_notebook_from_file(
        ipynb_file_name=notebook,
        namespace=namespace,
        array_name=notebook_name,
        storage_path=storage_path,
        storage_credential_name=storage_credential_name,
    )
