#!/usr/bin/python3
from utils import wordpress, conn


# Do the ping
conn.ping()
# Generate the zip
wordpress.generate_package()
# Check the tags
conn.check_tags()
# Deploy the zip
conn.deploy_plugin()
