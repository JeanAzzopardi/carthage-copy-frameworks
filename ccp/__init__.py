#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
# The MIT License (MIT)
#
# Copyright (c) 2015 Lorenzo Villani
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#

from __future__ import print_function

import os
import os.path
import subprocess
import sys


HERE = os.path.abspath(os.path.dirname(__file__))


def main():
    sanity_check()

    built_products_dir = os.environ["BUILT_PRODUCTS_DIR"]
    frameworks_folder_path = os.environ["FRAMEWORKS_FOLDER_PATH"]
    srcroot = os.environ["SRCROOT"]

    dest = os.path.join(built_products_dir, frameworks_folder_path)
    frameworks_dir = os.path.abspath(os.path.join(srcroot, "Carthage", "Build", "iOS"))

    frameworks = [f for f in os.listdir(frameworks_dir) if f.endswith(".framework")]

    # Skip speed-up trick for Release builds.
    if os.environ["CONFIGURATION"] != "Release":
        frameworks = [f for f in frameworks if not already_there(dest, f)]
    else:
        print("This is a release build, skipping presence checks.")

    # Do we have anything to do?
    if not frameworks:
        print("Not copying any framework. Perform a clean build to copy them again.")

        return
    else:
        print("Copying:\n    " + "\n    ".join(frameworks))

    # Export environment variables needed by Carthage
    os.environ["SCRIPT_INPUT_FILE_COUNT"] = str(len(frameworks))

    for i, framework in enumerate(frameworks):
        os.environ["SCRIPT_INPUT_FILE_" + str(i)] = os.path.join(frameworks_dir, framework)

    subprocess.check_call(["carthage", "copy-frameworks"])


def sanity_check():
    must_have = ["BUILT_PRODUCTS_DIR", "FRAMEWORKS_FOLDER_PATH", "SRCROOT"]

    for envvar in must_have:
        if not envvar in os.environ:
            lines = [
                "You must launch this tool from an Xcode build step.",
                "",
                "See installation instructions at: ",
                "https://github.com/lvillani/carthage-copy-frameworks/blob/master/README.md",
            ]

            for line in lines:
                print(line)

            sys.exit(1)


def already_there(dest, framework_name):
    return os.path.isdir(os.path.join(dest, framework_name))


if __name__ == "__main__":
    main()
