from datetime import datetime

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required

from app.models import MenuModel, RestaurantModel, session
from app.decorators import admin_group_required

menus_bp = Blueprint('menus', __name__)


@menus_bp.route("/menus", methods=["GET"])
@jwt_required()
def get_menus():
    """
        Get all menus with some filter of restaurant and menu fields or without it. You can filter by: restaurant name,
        first dish, second dish, drink. User can see only menu for today.
            Example 1:
                >> /menus?first=borsch
            Returns:
                Menu(s) where menu first dish is borsch
        """
    drink = request.args.get('drink')
    restaurant_name = request.args.get('restaurant_name')
    first = request.args.get('first')
    second = request.args.get('second')
    sorted_menus = request.args.get('sort')
    result = MenuModel.return_all()
    if drink:
        result = MenuModel.find_by_drink(drink)
    if restaurant_name:
        result = MenuModel.find_by_name(restaurant_name)
    if first:
        result = MenuModel.find_by_first(first)
    if second:
        result = MenuModel.find_by_second(second)
    if sorted_menus == 'True' or sorted_menus == '1':
        menus = MenuModel.return_all()
        result = sorted(
            menus,
            key=lambda x: (x['number_votes']), reverse=True
        )
    return jsonify(result)


@menus_bp.route("/menu_today", methods=["GET"])
@jwt_required()
def get_menu():
    result = MenuModel.return_all()
    today = []
    if result:
        today = max(result, key=lambda x: x['number_votes'])
    return jsonify(today)


@menus_bp.route("/menus", methods=["POST"])
@jwt_required()
@admin_group_required
def create_menu():
    """
        Create  menu with some fields. Only admins can create menu.
            Example:
                >> {"restaurant_id":1, "resp_username":"test", "first":"borsch",
                 "drink":"apple juice","second":"turkey", "date":'2022-10-01 10:00:00'}
            Returns:
                "id":1, "date": '2022-10-01 10:00:00', "restaurant_id": 1
        """
    if not request.json:
        return jsonify({"message": 'Please, specify "restaurant_id", "resp_username",'
                                   ' "first", "second", "drink" and "date".'}), 400

    restaurant_id = request.json.get("restaurant_id")
    resp_username = request.json.get("resp_username")
    first = request.json.get("first")
    second = request.json.get("second")
    drink = request.json.get("drink")
    date = request.json.get("date")
    date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    restaurant = RestaurantModel.find_by_id(id_=restaurant_id)
    if resp_username == restaurant['resp_username']:
        menu = MenuModel(
            restaurant_id=restaurant_id, first=first, second=second,
            drink=drink, date=date)
        menu.save_to_db()

        return jsonify({"id": menu.id, "date": menu.date, "restaurant_id": menu.restaurant_id}), 201
    else:
        return jsonify({"message": 'Such "username" is not responsible for selected restaurant.'}), 400


@menus_bp.route("/menus/<int:id_>", methods=["DELETE"])
@jwt_required()
@admin_group_required
def delete_menu(id_):
    """
        Delete menus object by id. Only admins can delete menus.
        If menus doesn't exist it will return message: "Menu not found"
            Args:
                id_: id of menus what you want to delete
            Returns:
                "message":"Menu was successfully deleted"
                    """
    code = MenuModel.delete_by_id(id_)
    if code == 404:
        return jsonify({"message": "Menu not found."}), 404

    return jsonify({"message": "Menu was successfully deleted"})
