# Cron tab settings

### Actual
```bash
# recreate ssl sert
0 0 */15 * * docker run -t --rm -v lmnad_certs:/etc/letsencrypt -v lmnad_certs_data:/data/letsencrypt -v /var/log/letsencrypt:/var/log/letsencrypt deliverous/certbot renew --webroot --webroot-path=/data/letsencrypt && docker kill -s nginx >/dev/null 2>&1
```

### Legacy
```bash
# backup - old
# 0 5 1 1-12 * /root/backup/backup.sh > /dev/null 2>&1

# certbot - old
# 0 0 * * * /root/certbot-auto renew --quiet --no-self-upgrade --post-hook "service nginx reload"
```
