# Containerized server setup for Pro3 and Pro4 :rocket:

This repo contains files for setting up all needed server services for the Web interface for Pro3 and Pro4.

The containers are live on our development server, the Webinterface is accessed at: http://auteam2.mooo.com:8000/

> _Be aware: We have now switched fully to the PostgreSQL database. If you experience any issues, remove your data-volume, re-create it, rebuild the docker-compose image, and try again. If the issue persists, tell someone... :monkey:..._

- [Services](#Services)
- [How to use](#How-to-use)
- [Running on Windows with Docker Toolbox](#Running-on-Windows-with-Docker-Toolbox)
- [Troubleshooting](#Troubleshooting)
- [Future timebox development](#Future-timebox-development)

## Services
The docker-compose now contains the following services:
- Django webinterface, hosted via it's own temporary development server.
- PostgreSQL database server.
- Nginx webserver.
- Mosquitto MQTT server.

### Docker-compose
The *docker-compose.yml* file handles:
- Coordination of construction, startup, shutdown and destruction of the services (running in containers).
- Creation of networking bridges between running services (between containers). 
- Mapping of ports between containers and the host OS.
- Specification of storage volumes and mapping to local folders.


## How to use
Before running the services the first time, see the sections:
- [Creating volumes](#Creating-volumes)
- [Building Webinterface image](#Building-the-Webinterface-image)
- [Running on Windows with Docker Toolbox](#Running-on-Windows-with-Docker-Toolbox)

The services are created using `docker-compose up -d`. The `-d` options creates the services in a detached state, i.e. running in the background.

If you want to see console and log output from the services, run in foreground as `docker-compose up`.

The services are destroyed using `docker-compose down`. If running in the foreground, stop them using *Ctrl-C*.

You can see running services with `docker-compose ps`.

### Creating and destroying versus starting and stopping
Services that are already built can be started and stopped without re-building, using `docker-compose start` and `docker-compose stop`. This is good for production, but if you change the build instructions, you are not guaranteed that your changes are included in the running services.

The calls `docker-compose up -d --build` and `docker-compose down` ensure a re-build and destruction of containers at each run, which is good during development, ensuring that any changes to build specs are captured in the services.

To see the built images on your computer, run `docker-compose images`.

### Creating volumes
To make data persistent outside the Docker container, we use volumes. This is essentially just attached storage. 
To make the needed volumes:
- For the database, run `docker volume create data-volume`, and
- for the mosquitto server, run `docker volume create mqtt-volume`.

### Building the Webinterface image
The first build of the Webinterface image takes a while, as many different libraries must be fetched and installed.
- Build all the images for all services, without starting them, run: `docker-compose build`, or
- Build and _start_ all services: `docker-compose up -d --build`.

### Issuing commands to services
Commands can be issued to the containers through docker-compose:
- `docker-compose exec <service_name>` executes a command in an already running container of service: *service_name*,
- `docker-compose run <service_name>` starts up a new container to perform the command.

Useful commands on the Webinterface:
- Start a new project, if you don't have the webinterface/manage.py file and webinterface/webinterface folder: `docker-compose run webinterface sh -c "django-admin.py startproject webinterface ."`.
- Update database (requires services already running): `docker-compose exec python manage.py migrate --no-input`. 
- Create a new superuser (requires services already running): `docker-compose exec python manage.py createsuperuser --username ditnavn --email din@email.dk`.

Useful commands on database server to look inside the database:
- Start a psql client to look inside the database: `docker-compose exec db psql --username=team2 --dbname=webinterface_dev`.
- Find psql guides [here](https://github.com/AUTeam2/tools/blob/master/cheatsheets.md#PostgreSQL).

If you want to see what's inside a data volume, just mount it to a simple container:
- Try: `docker run -it --rm -v data-volume:/vol busybox ls -l /vol`.


## Running on Windows with Docker Toolbox

To run on Windows, you must:
- Ensure LF line endings via Git.
- Share local folders via VirtualBox.
- Run a special startup command in Docker Toolbox.
- Find your docker-machine IP address.

**LF line endings:** Before cloning the directory, ensure that your Git doesn't automatically modify files. Otherwise, Git will automatically convert to Windows style CRLF endings. It must be set up to keep Unix-style LF line endings. Run the command `git config --global core.autocrlf false`.

You can read more about it here: [Configuring Git to handle line endings](https://help.github.com/en/github/using-git/configuring-git-to-handle-line-endings).

If you forget to do this, you will get an error when the webinterface container tries to run the entrypoint script.

**Share local folders:** To share local files with the container (config files, etc.), you must set up a shared folder in VirtualBox:
  - The cloned folder **server-settings** (this repository) must be shared with the Docker Toolbox.
  - The name of the shared folder _must_ be `c/docker`.

**Startup:** To start the containers on Windows, run `docker-compose -f docker-compose-win.yml up -d`.

**IP address:** You can find the local IP address using `docker-machine ip Default`, and then access the services in your browser with the correct IP and port number, e.g. 192.168.99.100:8000.


## Troubleshooting
Try:
- Ensure all containers are off:
  - `docker-compose down`.
  - Check to confirm all is down: `docker-compose ps`.
  - Check to confirm none running: `docker container ls`.
    - Remove any using `docker stop <container_id>`.
    - If necessary, stop and restart your docker VM in VirtualBox:
      - Click on machine in VirtualBox. Run command: `sudo shutdown -h now`.

- Remove data volumes:
  - `docker volume rm data-volume`.
  - `docker volume rm mqtt-volume`.
  - Recreate the volumes as described elsewhere.

- Rebuild all images without using old cache, use {} only on Docker Toolbox on Win:
  - `docker-compose {-f docker-compose-win.yml} build --no-cache`.
  - `docker-compose {-f docker-compose-win.yml} up`.

- Inspect contents of data volume:
  - Should contain PostgreSQL files: `docker run -it --rm -v data-volume:/vol busybox ls -l /vol`.

- Attempt to log on to PostgreSQL server (must be running), use {} only on Docker Toolbox on Win:
  - `docker-compose {-f docker-compose-win.yml} exec db psql --username=team2 --dbname=webinterface_dev`.
  - `docker-compose {-f docker-compose-win.yml} exec db psql --username=team2`.


## Future timebox development
### Development server -> Production server
- [ ] Connect Nginx webserver with Django through gunicorn... Next Timebox:
  - Current service setup runs Django hosted on its own development server.
  - This server is unsafe, insecure, slow, doesn't serve staticfiles and doesn't handle multiple concurrent connections.
  - In the next timebox, we will connect Django and Nginx via a gateway interface (WSGI), we use gunicorn.

### Make it safer and smarter
- [ ] Build environment files... Next Timebox:
  - All secret keys into environment files.
  - All passwords.
  - Various flexible settings.

### Build a docker-compose-prod.yml file
- [ ] Make a production file for starting services in production mode:
  - Different database volume (don't do development using production database).
  - Different server chain (as above).
  - Different environment files (as above).

### Compatibility
- [ ] Test Windows compatibility of custom Python/Django image... Ongoing...


:rocket:
