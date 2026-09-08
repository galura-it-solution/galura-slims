#!/bin/sh

# Write environment variables to env.php
cat <<EOF >/var/www/html/config/env.php
<?php
\$env = "${ENV}";
\$conditional_environment = "${ENV}";
\$based_on_ip = false;
\$range_ip = [''];
if (\$based_on_ip) {
    if (array_key_exists('HTTP_X_FORWARDED_FOR', \$_SERVER) && in_array(\$_SERVER['HTTP_X_FORWARDED_FOR'], \$range_ip)) {
        \$env = \$conditional_environment;
    } else if (in_array(\$_SERVER['REMOTE_ADDR'], \$range_ip)) {
        \$env = \$conditional_environment;
    }   
}
EOF

echo "PHP configuration file created: /var/www/html/config/env.php"
cat /var/www/html/config/env.php

# Write environment variables to database.php
cat <<EOF >/var/www/html/config/database.php
<?php
return [
    'default_profile' => 'SLiMS',
    'proxy' => false,
    'nodes' => [
        'SLiMS' => [
            'host' => '${DB_HOST}',
            'database' => '${DB_NAME}',
            'port' => '${DB_PORT}',
            'username' => '${DB_USER}',
            'password' => '${DB_PASS}',
            'options' => [
                'storage_engine' => 'MyISAM'
            ]
        ]
    ]
];
EOF

echo "PHP configuration file created: /var/www/html/config/database.php"
cat /var/www/html/config/database.php

# Ensure all sample configuration files exist
for sample in /var/www/html/config/*.sample.php; do
    [ -f "$sample" ] || continue
    target="/var/www/html/config/$(basename "$sample" .sample.php).php"
    if [ ! -f "$target" ]; then
        cp "$sample" "$target"
    fi
done

# Ensure directory permissions for config and mounted volumes
chown -R www-data:www-data /var/www/html/config /var/www/html/files /var/www/html/images /var/www/html/repository 2>/dev/null || true
chmod -R 775 /var/www/html/config /var/www/html/files /var/www/html/images /var/www/html/repository 2>/dev/null || true

# Wait for database to be ready
echo "Waiting for database to be ready..."
until php -r "
\$conn = new mysqli(getenv('DB_HOST'), getenv('DB_USER'), getenv('DB_PASS'), getenv('DB_NAME'), (int)getenv('DB_PORT'));
exit(\$conn->connect_error ? 1 : 0);
" 2>/dev/null; do
    echo "  Database not ready, retrying in 2s..."
    sleep 2
done
echo "Database is ready."

# Auto-initialize database schema if tables don't exist yet
echo "Checking database schema..."
TABLE_EXISTS=$(php -r "
\$conn = new mysqli(getenv('DB_HOST'), getenv('DB_USER'), getenv('DB_PASS'), getenv('DB_NAME'), (int)getenv('DB_PORT'));
\$res = \$conn->query(\"SHOW TABLES LIKE 'setting'\");
echo (\$res && \$res->num_rows > 0) ? '1' : '0';
\$conn->close();
" 2>/dev/null)

if [ "$TABLE_EXISTS" != "1" ]; then
    if [ -f "/usr/local/share/slims/senayan.sql" ]; then
        echo "Database tables missing. Importing base schema from /usr/local/share/slims/senayan.sql..."
        mysql -h "${DB_HOST}" -P "${DB_PORT}" -u "${DB_USER}" -p"${DB_PASS}" "${DB_NAME}" < /usr/local/share/slims/senayan.sql
        echo "Base schema imported successfully."
    else
        echo "Warning: /usr/local/share/slims/senayan.sql not found!"
    fi
else
    echo "Database schema already initialized."
fi

# Randomize admin password on first startup only
INIT_FLAG="/var/www/html/files/.admin_initialized"
if [ ! -f "$INIT_FLAG" ]; then
    ADMIN_PASS=$(openssl rand -base64 12 | tr -dc 'A-Za-z0-9' | head -c 16)
    export ADMIN_PASS
    ADMIN_HASH=$(php -r "echo password_hash(getenv('ADMIN_PASS'), PASSWORD_BCRYPT);")
    export ADMIN_HASH

    php -r "
\$conn = new mysqli(getenv('DB_HOST'), getenv('DB_USER'), getenv('DB_PASS'), getenv('DB_NAME'), (int)getenv('DB_PORT'));
if (\$conn->connect_error) {
    echo 'DB connection failed: ' . \$conn->connect_error . PHP_EOL;
    exit(1);
}
\$stmt = \$conn->prepare('UPDATE user SET passwd=? WHERE username=?');
\$hash = getenv('ADMIN_HASH');
\$user = 'admin';
\$stmt->bind_param('ss', \$hash, \$user);
\$stmt->execute();
if (\$stmt->affected_rows > 0) {
    echo 'Admin password updated successfully.' . PHP_EOL;
} else {
    echo 'Warning: admin user not found or password unchanged.' . PHP_EOL;
}
\$stmt->close();
\$conn->close();
"

    touch "$INIT_FLAG"
    unset ADMIN_HASH

    echo ""
    echo "========================================================"
    echo "  SLIMS FIRST-TIME SETUP - ADMIN CREDENTIALS"
    echo "  Username : admin"
    echo "  Password : ${ADMIN_PASS}"
    echo "  Please change your password immediately after login!"
    echo "========================================================"
    echo ""

    unset ADMIN_PASS
else
    echo "Admin password already initialized, skipping."
fi

# Start the PHP application
exec "$@"
