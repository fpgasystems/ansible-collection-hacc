FROM ubuntu:22.04

# Install required tools
RUN apt-get update && \
    apt-get install -y dpkg-dev gzip gnupg2 apt-utils nginx && \
    rm -rf /var/lib/apt/lists/*

# Create repo directory
RUN mkdir -p /usr/share/nginx/html/deb-repo
WORKDIR /usr/share/nginx/html/deb-repo


# Configure Nginx to serve the repo
RUN echo 'server { \
        listen 80; \
        server_name localhost; \
        location / { \
            root /usr/share/nginx/html/deb-repo; \
            autoindex on; \
        } \
    }' > /etc/nginx/sites-available/default

# Expose HTTP port
EXPOSE 80

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
