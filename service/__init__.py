# Copyright 2016, 2021 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging
and SQL database
"""
from flask import Flask

# Create Flask application
app = Flask(__name__)
# app.config.from_object("config")

# Import the routes AFTER the Flask app is created
# pylint: disable=wrong-import-position, cyclic-import
from service import routes
from service.utils import log_handler

# Set up logging for production
print(f"Setting up logging for {__name__}...")
log_handler.initialize_logging()

app.logger.info(70 * "*")
app.logger.info("  H I T   C O U N T E R   S E R V I C E  ".center(70, "*"))
app.logger.info(70 * "*")

# try:
#     models.init_db(app)  # make our sqlalchemy tables
# except Exception as error:
#     app.logger.critical("%s: Cannot continue", error)
#     # gunicorn requires exit code 4 to stop spawning workers when they die
#     sys.exit(4)

app.logger.info("Service initialized!")
