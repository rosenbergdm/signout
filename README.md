# signout.py README.md

## Required programs

- External programs
  - Deployment
    - Apache with mod_wsgi referencing python3
    - [Docopts](https://github.com/docopt/docopts) shell command-line argument parser
    - PostgreSQL database with a database and user configured in settings file.
    - Bash > 4 for script execution
    - [jq](https://stedolan.github.io/jq/) is recommended but not required for json file management
  - Development
    - [Shellcheck](http://www.shellcheck.net) shell script linter
    - Black python linter
    - eslint
    - Prettier
    - GNU parallel
- Python modules
  - python3 is required
  - Deployment - use `requirements.txt`
  - Development - use `requirements.dev.txt`
- Other requirements
  - SSL Certs in place
  - DNS pointing url at apache

## Apache Config

```
<VirtualHost *:80>
ServerName signout.davidrosenberg.me
ServerAlias signout.localdomain
ServerAlias signout
ServerAdmin dmr@davidrosenberg.me

    WSGIDaemonProcess signout user=www-data group=www-data threads=15
    WSGIProcessGroup signout
    WSGIScriptAlias / /usr/local/src/signout/signout.wsgi

WSGIPassAuthorization On
Alias /static/ /usr/local/src/signout/static/

    ErrorLog /var/log/apache2/error.signout.log
    CustomLog /var/log/apache2/access.signout.log combined

    <Files /usr/local/src/signout/signout.wsgi>
     Require all granted
    </Files>
    <Directory /usr/local/src/signout/static>
     Require all granted
    </Directory>
    <Location />
     Require all granted
    </Location>

</VirtualHost>
```

## CONFIGURATION SETTINGS

- Modifying config values using CURL: (also copies the current dbsettings.json to a backup file and writes the updated file to dbsettings.json)

```
> curl -X POST -c cookie.txt -d "user_name=dmr" -d "rawpw=$PASSWORD" http://localhost:5000/login
> #creates the file cookie.txt
>
> curl -X POST -b cookie.txt 'http://localhost:5000/config?var=DEBUG_PAGES&val=1'
> #uses the cookie file to authenticate
```

- Viewing the full configuration: `http://localhost:5000/config?full=true`
- Configuration flags
  - `DEBUG_CALLBACKS`: When set, sends notifications to the number given in `DEBUG_TARGET_NUMBER`
  - `DEBUG_PRNIT_NOT_MESSAGE:` When set, prints to stdout instead of sending notifications

