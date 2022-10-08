# produkt-18

Collect ambient sensor data from the Fritz!Box

# Setup

pip3 install fritzconnection

# Usage

Supply configuration file parameter **--config**. The contents of the file should be as follows

    [node]
    hostname = <foobar>

    [auth]
    username = <user>
    password = <password>

# Munin

Put or link the approptiate plugin to your local munin plugins installation (normally located under */etc/munin/plugins/*)

Supply applicable munin confguration (/etc/munin/plugin-conf.d/<plugin_name>):
    [<plugin_name>]
    env.hostname = <foobar>
    env.auth_username = <user>
    env.auth_password = <password>

