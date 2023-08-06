#!/usr/bin/env python3

import argparse
import requests
import os
import textwrap
from shared import ei


def download_folder(jwt, args, token, folder_path=''):
    # Get list of files portals/{portalId}/files
    # prefix gives the folder path to download from
    response = ei.do_jwt_post(jwt,
                              "portals/%s/files" % args.portal_id,
                              {"prefix": folder_path + "/"},
                              portal_token=token)
    for item in response["files"]:
        # If a folder (size == 0) then recurse down into next subfolder and download
        if item['size'] == 0:
            # print("\tSubfolder '%s' found, starting recursion..." %
            #       item['name'])
            download_folder(jwt, args, token, item['path'] + item['name'])
            continue
        # Get the download URL per file
        filepath = os.path.join(item["path"], item["name"])
        print("- %s..." % filepath, end="", flush=True)
        response = ei.do_jwt_post(jwt,
                                  "portals/%s/files/download" % args.portal_id,
                                  {"path": filepath},
                                  portal_token=token)
        response = requests.get(response["url"])
        # Make sure os.path.join doesn't think filepath is a root path
        if filepath.startswith("/"):
            filepath = filepath.strip("/")
        dest = os.path.join(args.path, filepath)
        # Make sure the directory we are saving to exists
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "wb").write(response.content)
        print(" downloaded to %s" % dest, flush=True)
    return


def main(args):
    # Get JWT token
    response = ei.get_jwt(args.username, args.password)
    jwt = response["token"]
    # Get portal token
    response = ei.do_jwt_get(
        jwt, "organizations/%s/portals/%s" % (args.org_id, args.portal_id))
    token = response["token"]
    # Download files in base folder
    print("Downloading the contents of portal %s" % args.portal_id, flush=True)
    download_folder(jwt, args, token, folder_path='')
    return


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=
        "Download the contents of an Edge Impulse organization portal",
        epilog=textwrap.dedent('''\
        Example:

            docker run -v <local/download/path>:/data \\
                       ijdoc/ei-portals-download:<version> \\
                       --username <ei_username> \\
                       --password <ei_password> \\
                       --portal-id <portal_id> \\
                       --org-id <org_id> \\
                       --path "/data"'''))
    parser.add_argument(
        "--org-id",
        help="the ID of the organization that the portal belongs to",
        type=str,
        required=True)
    parser.add_argument("--username",
                        help="the Edge Impulse username to login with",
                        type=str,
                        required=True)
    parser.add_argument("--password",
                        help="the Edge Impulse user password",
                        type=str,
                        required=True)
    parser.add_argument("--portal-id",
                        help="the ID of the portal to download files from",
                        type=str,
                        required=True)
    parser.add_argument(
        "--path",
        help=("the container path where the portal files should be " +
              "downloaded. This will most likely be a local " +
              "volume mounted with the -v or --mount docker argument."),
        type=str,
        required=True)
    main(parser.parse_args())
