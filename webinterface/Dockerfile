#Pull image for Linux Alpine with Python 3.8
FROM python:3.8.0-alpine
MAINTAINER Team Web, Janus Bo Andersen

#Set the working directory inside the Alpine Container
ENV APP_HOME=/usr/src/webinterface
WORKDIR $APP_HOME

#Make a directory for serving the staticfiles
RUN mkdir $APP_HOME/staticfiles

#Set environment variables
#don't write .pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
#don't buffer stdout, as that causes errors
ENV PYTHONUNBUFFERED 1

#Install dependencies for PostgreSQL (Psycopg2)
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev shadow curl \
    postgresql-client zlib-dev jpeg-dev

    #tiff freetype liblcms libwebp tk openjpeg

#Install suid for crontab to work
RUN apk add --update busybox-suid
#RUN apk add --no-cache dcron
RUN set -ex && apk --no-cache add sudo

#Install dependencies inside container
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/webinterface/requirements.txt
RUN pip install -r requirements.txt
# LDFLAGS=-L/usr/lib/x86-64-linux-gnu/, --no-binary
#Copy the entry point file
COPY ./entrypoint.sh /usr/src/webinterface/entrypoint.sh

#Copy all project files (Later: set up an auto sync)
COPY . /usr/src/webinterface/

# Allow anyone to run the script
RUN chmod 777 /usr/src/webinterface/entrypoint.sh

# https://github.com/dubiousjim/dcron
#RUN groupadd cron
#RUN chgrp cron /usr/local/bin/crontab
#RUN chmod 4750 /usr/local/bin/crontab
RUN touch /var/log/cron.log
RUN touch /var/spool/cron/crontabs/nonrootuser

# Allow the nonrootuser to edit his own crontab
RUN echo nonrootuser > /etc/cron.allow
#RUN echo -e "\n" > /var/spool/cron/crontabs/${u}
RUN chmod 777 /var/spool/cron/crontabs/nonrootuser

#Create a user to avoid running as root. DO NOT DO THIS, IF root in line 36
RUN adduser -D nonrootuser cron

#Give ownership permission to write files to the staticfiles
RUN chown -R nonrootuser:nonrootuser $APP_HOME

#RUN adduser -D -s /bin/sh -h /home/${u} -g "User" ${u}
# Create a sudo'er without required password
#RUN adduser -D -s /bin/sh dude
#RUN echo "dude ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/dude
USER nonrootuser
ENTRYPOINT ["/usr/src/webinterface/entrypoint.sh"]


#Run entrypoint, positional arguments can be added later
#ENTRYPOINT ["/usr/src/webinterface/entrypoint.sh"]

