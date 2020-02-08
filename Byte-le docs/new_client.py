from game.client.user_client import UserClient
from game.common.enums import *


Class Client(UserClient):
    def __init__(sel):
        super().__init__()


    def team_name(self):
        return 'Team 2'

    def city_name(self):
        return '# TODO name city'

    def city_type(self):
        return CityType.popular

    def take_turn(self, turn, actions, city, disasters):
