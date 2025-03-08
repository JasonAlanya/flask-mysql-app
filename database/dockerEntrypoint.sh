#!/bin/bash
# Start the MySQL service in the background
docker-entrypoint.sh mysqld &

# Wait until MySQL is fully ready
until mysql -u root -p$MYSQL_ROOT_PASSWORD -e "SELECT 1"; do
    echo "Waiting for MySQL to be ready..."
    sleep 2
done

sed -i "s/{API_USER}/$API_USER/g" /init-scripts/init.sql
sed -i "s/{API_PASSWORD}/$API_PASSWORD/g" /init-scripts/init.sql

# Manually execute the SQL script with environment variables
mysql -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE < /init-scripts/init.sql

# Wait indefinitely to keep the container running
wait