# dotty
Timelapse Video Creator For The Raspberry Pi Camera

## Setup

First, set Python 3.5 as the default python Raspberry Pi will be using:
* Set in your .bashrc, `alias python='/usr/bin/python3.5'`
* Set Python 3.5 system-wide:
`update-alternatives --list python`
    If you see this warning:

    `update-alternatives: error: no alternatives for python`
    no python alternatives has been recognized by update-alternatives command.
* If the above error occures, update your alternatives table and include both python2.7 and python3.5.
    `# sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1`
    `# sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.4 2`

Check the listing:
    `# update-alternatives --list python`

From now on, we can anytime switch between the above listed python alternative
versions using below command and entering a selection number:
`# update-alternatives --config python`

## Install ImageMagick:
`sudo apt-get install  libmagickwand-dev`



