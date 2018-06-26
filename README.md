# dotty
An s3 Enabled Timelapse Capture Tool For The Raspberry Pi, and it's PiCamera

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

## Add ENV variables to your bashrc file:
Accessing your .bashrc file: `sudo nano ~/.bashrc`
Then add the following:
```
## for dotty
alias python='/usr/bin/python3.5'
export PATH=~/.local/bin:$PATH
export AWS_ACCESS_KEY_ID='YOUR AWS SECRET KEY ID GOES HERE'
export AWS_SECRET_KEY='YOUR AWS SECRET KEY GOES HERE'
```

### If you're using Raspbian, in _Preferences/Interfaces_:
Enable: Camera
Enable: SSH (If you need it)
### In _Prefeferences/Localisation_ (if using Raspbian):
Set Locale, Timezone

## Install Python packages you need:
###  If you're getting errors pip installing:
Upgrade Pip: `/usr/bin/python -m pip installl --upgrade pip`
`sudo apt-get update`
`sudo apt-get upgrade`
`pip install arrow`
`pip install boto3`

## after cloning this repo, edit the cron.txt file as needed, then load it:
`crontab cron.txt`

## Check if cronjobs loaded correctly:
`crontab -l`
