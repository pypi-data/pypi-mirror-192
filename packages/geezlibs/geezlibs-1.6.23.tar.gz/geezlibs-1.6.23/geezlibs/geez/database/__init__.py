# Copyright (C) 2020-2021 by DevsExpo@Github, < https://github.com/DevsExpo >.
#
# This file is part of < https://github.com/DevsExpo/FridayUB > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/DevsExpo/blob/master/LICENSE >
#
# All rights reserved.

import logging

from config import MONGO_URL
import motor.motor_asyncio

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)

db_x = mongo_client["Geez-Pyro"]
