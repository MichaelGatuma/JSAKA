# JSAKA
Highly Customizable Word Scrapper, with minimal foot print. Uses Scrapy for crawling and has a configuration panel to configure some crawlers behaviors.
JSAKA uses scrapy framework to develop spiders, the scrapped data is then stored. The web interface allows you to configure keywords that one should be alerted via email once they are detected in the scrapped data.

# Deploying using nginx and uwsgi (Centos)

Steps:

# Install Nginx:


If you dont have the epel repo in your machine, run:
  sudo yum install epel-release

Install nginx web and reverse proxy server:
  sudo yum install nginx
 
# Setup pip:

  sudo yum install python-pip python-devel gcc

# install and create python Virtual Environment

installation:

  sudo pip install virtualenv

Creating virtual env with virtualenv tool:

  mkdir ~/myproject
  cd ~/myproject
  virtualenv myprojectenv

The above will create a python virtual env in your project folder created (myprojectenv).
The above copies files for your default python interpreter to the virtual environment.
If you have multiple instances of python interpreter on your machine, you can specify the version to use as:

  virtaulenv --python=/location/to/python/touse myprojectenv
  eg: virtualenv --python=/usr/local/bin/python2.7 myprojectenv

# Activate and install project dependencies:

Activate the environment as follows:
  source myprojectenv/bin/activate

Now copy all sources from JSAKA into the project folder (myprojectenv).
The install the projects dependencies usinf the requirements.txt file in JSAKA by running:

  pip install -r requirements.txt

# Installing uwsgi server

Run:
  pip install uwsgi
  
# Configring Nginx

add the following directive to nginx conf file:

  server {
        listen 8080;
        server_name 0.0.0.0;


        location / {

        include uwsgi_params;
        uwsgi_pass unix:/tmp/jsaka.sock;
        }

        }

By default, our app uses unix socket to connect to nginx which is placed in the default location "/tmp/jsaka.sock"
This can be cahnged by editing jsaka.ini configuration file. Also ensure the path to .sock file has enough priveleges for this to be successful.

# Run JSAKA with uwsgi

  uwsgi --ini jsaka.ini
  
# Run Nginx

 type nginx on terminal as root.
 


# Screenshots
Keyword manager

![alt text](jsaka/screenshots/Keywords.png)

Subscription Manager

![alt text](jsaka/screenshots/Manage_Subs.png)


