#/bin/bash
LOG_PATH=/usr/local/nginx/logs/
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)

PID=/usr/local/nginx/logs/nginx.pid
ACCESSLOG=${LOG_PATH}access.log
SSL_ERRORLOG=${LOG_PATH}ssl_error.log
if [ -f "$ACCESSLOG" ]; then
mv ${ACCESSLOG} ${LOG_PATH}access-${YESTERDAY}.log
fi
if [ -f "$SSL_ERRORLOG" ]; then
mv ${SSL_ERRORLOG} ${LOG_PATH}ssl_error-${YESTERDAY}.log
fi
#kill -USR1 `cat ${PID}` 没有权限kill，用下面的sudo
echo 'Admin@bpm01'|sudo -S /usr/local/nginx/sbin/nginx -s reload
