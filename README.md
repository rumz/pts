pts
===

##Install Notes for Windows Dev Environment

 * python (via installer)
 * git (via installer)
 * pip via get-pip.py - http://pip.readthedocs.org/en/latest/installing.html
 * django (via pip)   
 * postgres (via installer)  use username/password: postgres/postgres
 * psycopg2 (via installer)  http://www.stickpeople.com/projects/python/win-psycopg/
 * create philhealth db via pgadmin
 * git clone https://github.com/elmschaym/pts
 * run manage.py syncdb (create superuser)
 * run python populate_tickets.py
 * run census/weekdays_functions.sql in pgadmin


### Postgres Notes

Installing Postgres on Windows Server 2008

1. I create user "postgres"
2. Add user "postgres" to the group "Administrators"
3. Copy postgresql-9.1.9-1-windows-x64.exe on the disk c:
4. install
  1. runas /user:postgres cmd.exe
  2. c:
  3. cd c:\
  4. postgresql-9.1.9-1-windows-x64.exe

 * http://gis.stackexchange.com/questions/70183/is-it-real-to-install-postgresql-9-on-the-virtual-machine-windows-server-r2


Open listening ports for remote access (pgadmin from other pcs)
 * http://stackoverflow.com/questions/18580066/how-to-allow-remote-access-to-postgresql-database
 * http://www.postgresql.org/docs/9.1/static/auth-pg-hba-conf.html
