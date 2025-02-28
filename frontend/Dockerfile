FROM nginx:latest
# Copy custom configuration; override the default config in the container.
COPY default.conf /etc/nginx/conf.d/default.conf
# Copy static files
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY script.js /usr/share/nginx/html/
EXPOSE 80
