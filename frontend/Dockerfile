FROM nginx:alpine

RUN apk add --no-cache gettext

COPY index.html style.css script.js /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/templates/default.conf.template
COPY docker-entrypoint.sh /docker-entrypoint.sh

RUN chmod +x /docker-entrypoint.sh

EXPOSE 80

ENTRYPOINT ["/docker-entrypoint.sh"]
