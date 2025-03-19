FROM nginx:latest

COPY default.conf /etc/nginx/conf.d/default.conf
# Copy static files
COPY index.html /usr/share/nginx/html/
COPY styles.css /usr/share/nginx/html/
COPY script.js /usr/share/nginx/html/
EXPOSE 80
