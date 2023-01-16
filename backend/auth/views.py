import os

from flask import Blueprint
from flask import render_template, request, abort, jsonify

import time

from web3.auto import w3
from eth_account.messages import defunct_hash_message

from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from backend import db
from backend.obj_model.user import User, get_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    print("[+] creating session")

    print("info: " + (str(request.json)))


    public_address = request.json[0]
    signature = request.json[1]

    domain = os.getenv('DOMAIN')

    rightnow = int(time.time())
    sortanow = rightnow - rightnow % 600

    original_message = 'Signing in to {} at {}'.format(domain, sortanow)
    print("[+] checking: " + original_message)
    message_hash = defunct_hash_message(text=original_message)
    signer = w3.eth.account.recoverHash(message_hash, signature=signature)
    print("[+] fascinating")

    if signer == public_address:
        print("[+] this is fine " + str(signer))
        user: User = get_user(public_address)
        if user:
            print("[+] Found user " + user.public_address)
        else:
            user = User(public_address=public_address)
            db.session.add(user)
            db.session.commit()
            db.session.refresh(user)
    else:
        abort(401, 'could not authenticate signature')

    access_token = create_access_token(identity=public_address)

    resp = jsonify(access_token=access_token)
    # print(resp)
    # set_access_cookies(resp, access_token)
    return resp, 200
