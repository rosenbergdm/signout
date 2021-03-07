#Apache Config:


`
~~~~~~~~~~~~~~~~~~~~~~~
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
`
