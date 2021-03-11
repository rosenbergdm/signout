#Apache Config:

.apacheconf~~~~~~~~~~~~~~~~~~~~~~
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
~~~~~~~~~~~~~~~~~~~~~~~


# Upgrade from v0.3 -> v0.4
- update dbsettings.json (some stuff changed case, lots new).  Look at dbsettings.json.test to see
- Ensure WSGIPassAuthorization is on in apache conf
- backup the db
- install the updates `cat ./scripts/{nf_assignments,fix_service_active}.sql | psql -U signout signout`
- backup the db again
- install jq
- install docopt (https://github.com/docopt/docopts)

- install required python3 packages `pip3 install twilio flask-HTTPAuth`
- reload apache
- Make sure everything works
- ENSURE apache's mod\_wsgi uses python3: `ldd "/usr/lib/apache2/modules/*wsgi*"` .  It should reference python3

# CONFIGURATION SETTINGS

DEBUG\_CALLBACKS: When set, sends notifications to the number given in DEBUG\_TARGET\_NUMBER
DEBUG\_PRNIT\_NOT\_MESSAGE: When set, prints to stdout instead of sending notifications
