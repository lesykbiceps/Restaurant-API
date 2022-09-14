from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models import RestaurantModel
from app.decorators import admin_group_required

restaurants_bp = Blueprint('restaurants', __name__)


@restaurants_bp.route("/restaurants", methods=["GET"])
@jwt_required()
@admin_group_required
def get_restaurants():
    """
        Get all restaurants. Only admins can get restaurants.
            Returns:
                All restaurants as list of dictionaries.
        """
    restaurants = RestaurantModel.return_all()
    return jsonify(restaurants)


@restaurants_bp.route("/restaurants/<int:id_>", methods=["GET"])
@jwt_required()
@admin_group_required
def get_restaurant(id_):
    """
        Get some specific restaurants from database. This function  accept id_ parameters.
            Args:
                id_: id of restaurants what you want to get
            Returns:
                Restaurants with bring id.
        """
    restaurant = RestaurantModel.find_by_id(id_)
    if not restaurant:
        return jsonify({"message": "Restaurant not found."}), 404

    return jsonify(restaurant)


@restaurants_bp.route("/restaurants", methods=["POST"])
@jwt_required()
@admin_group_required
def create_restaurant():
    """
        Create  restaurant with some fields. Only admins can create restaurant
                Example:
                    >> {"name":'ClodMone', "resp_username":"bob"}
                Returns:
                    "id":1, "name": "ClodMone", "resp_username":"bob"
        """
    if not request.json:
        return jsonify({"message": 'Please, specify "name".'}), 400

    name = request.json.get("name")
    resp_username = request.json.get("resp_username")
    if not (name and resp_username):
        return jsonify({"message": 'Please, specify "name" and "resp_username".'}), 400

    restaurant = RestaurantModel(
        name=name, resp_username=resp_username)

    restaurant.save_to_db()

    return jsonify({"id": restaurant.id, "name": restaurant.name, "resp_username": restaurant.resp_username}), 201


@restaurants_bp.route("/restaurants/<int:id_>", methods=["PATCH"])
@jwt_required()
@admin_group_required
def update_restaurant(id_):
    """
        Update some field in restaurant object or all fields. Only admins can update restaurant.
        If restaurant doesn't exist it will return message: "Restaurant not found"
            Example:
                >> {"name":'Richadin'}
            Args:
                id_: id of restaurant what you want to update
            Returns:
                "message":"Updated"
        """
    name = request.json.get("name")

    restaurant = RestaurantModel.find_by_id(id_, to_dict=False)
    if not restaurant:
        return jsonify({"message": "Restaurant not found."}), 404

    if name:
        restaurant.name = name
    restaurant.save_to_db()
    return jsonify({"message": "Updated"})


@restaurants_bp.route("/restaurant/<int:id_>", methods=["DELETE"])
@jwt_required()
@admin_group_required
def delete_restaurant(id_):
    """
        Delete restaurant object by id. Only admins can delete restaurant.
        If restaurant doesn't exist it will return message: "Restaurant not found"
            Args:
                id_: id of restaurant what you want to delete
            Returns:
                "message":"Restaurant was successfully deleted"
        """
    code = RestaurantModel.delete_by_id(id_)
    if code == 404:
        return jsonify({"message": "Restaurant not found."}), 404

    return jsonify({"message": "Restaurant was successfully deleted"})
