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
