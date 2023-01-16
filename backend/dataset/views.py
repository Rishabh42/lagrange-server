import os

from flask import jsonify, Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from backend import db
from backend.obj_model import update_record
from backend.obj_model.dataset import Dataset
from backend.obj_model.file import File
from backend.obj_model.user import get_user, User
from lagrange_server import app

dataset_bp = Blueprint(
    "dataset_bp", __name__, template_folder="templates", static_folder="static"
)


@app.route('/dataset', methods=['Get'])
def get_datasets_deprecated():
    datasets = Dataset.query.filter_by()
    data_list = []
    for dataset in datasets:
        data_list.append(dataset.to_dict())
    return jsonify(datasets=data_list), 200


@app.route('/datasets', methods=['Get'])
def get_datasets():
    datasets = Dataset.query.filter_by(is_public=True)
    data_list = []
    for dataset in datasets:
        data_list.append(dataset.to_dict())
    return jsonify(datasets=data_list), 200


@app.route('/datasets/<string:name>', methods=['Get'])
def get_dataset_detail(name):
    dataset = Dataset.query.filter_by(name=name).first()
    return jsonify(dataset=dataset.to_dict()), 200


@app.route('/datasets', methods=['PUT'])
@jwt_required()
def create_dataset():
    public_address = get_jwt_identity()
    user: User = get_user(public_address)
    is_public = request.form.get("is_public")
    name = request.form.get("name")
    data_schema = request.form.get("data_schema")

    dataset = Dataset(name=name, data_schema=data_schema, is_public=is_public, user_id=user.id)
    db.session.add(dataset)
    db.session.commit()
    db.session.refresh(dataset)

    return jsonify(dataset=name), 200


# update dataset
@app.route('/datasets/<string:name>', methods=['POST'])
@jwt_required()
def update_dataset():
    public_address = get_jwt_identity()
    user: User = get_user(public_address)
    name = request.form.get("name")
    is_public = request.form.get("is_public")
    dataset = Dataset.query.filter_by(name=name, user_id=user.id).first()
    dataset.name = name
    dataset.is_public = is_public
    session = db.session
    update_record(dataset, session)
    return jsonify(dataset=name), 200


@app.route('/datasets/<string:name>/files', methods=['PUT'])
@jwt_required()
def upload_dataset_files():
    public_address = get_jwt_identity()
    user: User = get_user(public_address)
    name = request.form.get("name")
    is_public = request.form.get("is_public")
    dataset = Dataset.query.filter_by(name=name, user_id=user.id).first()
    dataset.name = name
    dataset.is_public = is_public
    session = db.session
    update_record(dataset, session)
    return jsonify(dataset=name), 200

