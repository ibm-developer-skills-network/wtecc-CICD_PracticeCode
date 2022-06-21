######################################################################
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
######################################################################

"""
Module for Hit Counter Service Routes
"""

import os
from redis import Redis
from redis.exceptions import ConnectionError as RedisConnectionError
from flask import jsonify, url_for, abort
from service.utils import status
from service import app

# Connext to the Redis database
# pylint: disable=invalid-name, global-variable-not-assigned
counter: Redis = None


############################################################
# Index page
############################################################
@app.route("/")
def index():
    """Root URL"""
    app.logger.info("Request for Base URL")
    return jsonify(
        status=status.HTTP_200_OK,
        message="Hit Counter Service",
        version="1.0.0",
        url=url_for("list_counters", _external=True),
    )


############################################################
# List counters
############################################################
@app.route("/counters", methods=["GET"])
def list_counters():
    """List counters"""
    app.logger.info("Request to list all counters...")
    try:
        counters = [
            dict(name=key, counter=int(counter.get(key))) for key in counter.keys("*")
        ]
    except RedisConnectionError as error:
        abort(status.HTTP_503_SERVICE_UNAVAILABLE, str(error))

    return jsonify(counters)


############################################################
# Create counters
############################################################
@app.route("/counters/<name>", methods=["POST"])
def create_counters(name):
    """Create counters"""
    app.logger.info("Request to Create counter...")
    try:
        count = counter.get(name)
        if count is not None:
            abort(status.HTTP_409_CONFLICT, f"Counter [{name}] already exists")

        counter.set(name, 0)
    except RedisConnectionError as error:
        abort(status.HTTP_503_SERVICE_UNAVAILABLE, str(error))

    location_url = url_for("read_counters", name=name, _external=True)
    return (
        jsonify(name=name, counter=0),
        status.HTTP_201_CREATED,
        {"Location": location_url},
    )


############################################################
# Read counters
############################################################
@app.route("/counters/<name>", methods=["GET"])
def read_counters(name):
    """Read counters"""
    app.logger.info("Request to Read counter...")
    count = counter.get(name)
    if count is None:
        abort(status.HTTP_404_NOT_FOUND, f"Counter [{name}] does not exist")

    return jsonify(name=name, counter=int(count))


############################################################
# Update counters
############################################################
@app.route("/counters/<name>", methods=["PUT"])
def update_counters(name):
    """Update counters"""
    app.logger.info("Request to Update counter...")
    count = counter.get(name)
    if count is None:
        abort(status.HTTP_404_NOT_FOUND, f"Counter [{name}] does not exist")

    count = counter.incr(name)
    return jsonify(name=name, counter=count)


############################################################
# Delete counters
############################################################
@app.route("/counters/<name>", methods=["DELETE"])
def delete_counters(name):
    """Delete counters"""
    app.logger.info("Request to Delete counter...")
    count = counter.get(name)
    if count is not None:
        counter.delete(name)

    return "", status.HTTP_204_NO_CONTENT


############################################################
# U T I L I T Y   F U N C T I O N S
############################################################
def reset_counters():
    """Resets all counters"""
    global counter
    if app.testing and counter:
        counter.flushall()


@app.before_first_request
def init_db():
    """Initializes the database"""
    global counter  # pylint: disable=global-statement
    app.logger.info("Initializing Redis database connection")
    try:
        if "DATABASE_URI" in os.environ:
            DATABASE_URI = os.getenv("DATABASE_URI")
            counter = Redis.from_url(
                DATABASE_URI, encoding="utf-8", decode_responses=True
            )
        else:
            REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
            REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
            counter = Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                encoding="utf-8",
                decode_responses=True,
            )
    except RedisConnectionError as error:
        abort(status.HTTP_503_SERVICE_UNAVAILABLE, str(error))
