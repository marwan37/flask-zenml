#  Copyright (c) ZenML GmbH 2024. All Rights Reserved.
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
from flask import Flask
from app.routers import auth, server_deployer, users, stacks, zen_store

app = Flask(__name__)

app.register_blueprint(auth.bp)
app.register_blueprint(users.bp)
app.register_blueprint(server_deployer.bp)
app.register_blueprint(stacks.bp)
app.register_blueprint(zen_store.bp)

if __name__ == "__main__":
    app.run(port=3001, debug=True)
