FROM openjdk:8-jre-alpine
LABEL docker_image=novartis-openrefine
LABEL version=1.0

# OpenRefine 3.4.1 as a based application
ENV OR_URL https://github.com/OpenRefine/OpenRefine/releases/download/3.4.1/openrefine-linux-3.4.1.tar.gz

WORKDIR /or

RUN set -xe && apk add --no-cache bash curl grep tar && curl -sSL ${OR_URL} | tar xz --strip 1

#ADD ./or-configuration/refine /or
ADD ./or-configuration/refine.ini /or
RUN mkdir /or/files
ADD workspace-files/* /or/files/

ADD ./or-configuration/extensions/ /or/webapp/extensions/
RUN cd /or/webapp/ && ls -l

ENV EXT_LOCAL_FILE_SYSTEM "/or/files"

# Enable/Disable OpenRefine feature to create a project from the user machine (Menu: This Computer)
ARG THIS_COMPUTER=true
RUN if [ "$THIS_COMPUTER" == false ]; \
    then sed -i '44,48 s/^/\/\//' /or/webapp/modules/core/scripts/index/default-importing-sources/sources.js; \
    fi

# Enable/Disable OpenRefine feature to create a project from the web (Menu: Web Addresses (URLs))
ARG WEB_ADDRESSES=true
RUN if [ "$WEB_ADDRESSES" == false ]; \
    then sed -i '75,79 s/^/\/\//' /or/webapp/modules/core/scripts/index/default-importing-sources/sources.js; \
    fi

# Enable/Disable OpenRefine feature to create a project from the Clipboard (Menu: Clipboard)
ARG CLIPBOARD=true
RUN if [ "$CLIPBOARD" == false ]; \
    then sed -i '114,118 s/^/\/\//' /or/webapp/modules/core/scripts/index/default-importing-sources/sources.js; \
    fi

# Enable/Disable OpenRefine extension database
ARG DATABASE=true
RUN if [ "$DATABASE" == false ]; \
    then rm -r /or/webapp/extensions/database; \
    fi

# Enable/Disable OpenRefine extension gdata
ARG GOOGLE=true
RUN if [ "$GOOGLE" == false ]; \
    then rm -r /or/webapp/extensions/gdata; \
    fi

# Enable/Disable OpenRefine extension workspace-data
ARG WORKSPACE=true
RUN if [ "$WORKSPACE" == false ]; \
    then rm -r /or/webapp/extensions/local-file-system; \
    fi

WORKDIR /or/data
VOLUME /or/data

EXPOSE 3333
ENTRYPOINT ["/or/refine"]
CMD ["-i", "0.0.0.0", "-p", "3333", "-d", "/or/data"]