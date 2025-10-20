docker run -it --rm -d \
 --name n8n \
 -p 5678:5678 \
 -e GENERIC_TIMEZONE="Asia/Seoul" \
 -e TZ="Asia/Seoul" \
 -e N8N_ENFORCE_SETTINGS_FILE_PERMISSIONS=true \
 -e N8N_RUNNERS_ENABLED=true \
 -v n8n_data:/home/node/.n8n \
 --add-host=host.docker.internal:host-gateway \
 docker.n8n.io/n8nio/n8n
