from game.client.user_client import UserClient
from game.common.enums import *


class Client(UserClient):
    def __init__(self):
        super().__init__()

        self.previous_disaster = None

        self.lasting_disasters = [DisasterType.fire, DisasterType.blizzard, DisasterType.monster]
        self.instant_disasters = {
            DisasterType.tornado: SensorType.tornado,
            DisasterType.earthquake: SensorType.earthquake,
            DisasterType.ufo: SensorType.ufo
        }

        self.disaster_to_decree = {
            DisasterType.fire: DecreeType.anti_fire_dogs,
            DisasterType.tornado: DecreeType.paperweights,
            DisasterType.blizzard: DecreeType.snow_shovels,
            DisasterType.earthquake: DecreeType.rubber_boots,
            DisasterType.monster: DecreeType.fishing_hook,
            DisasterType.ufo: DecreeType.cheese,
        }

        self.decrees = [
            "fire",
            "tornado",
            "blizzard",
            "earthquake",
            "monster",
            "ufo"
        ]

        # For setting decrees
        self.decree = DecreeType.none
        self.previous_decree = DecreeType.none
        self.decree_lag = 0

    def team_name(self):
        return 'Team 2'

    def city_name(self):
        return '# TODO name city'

    def city_type(self):
        return CityType.popular

    def take_turn(self, turn, actions, city, disasters):
        avail_effort = city.population

        if city.structure < city.max_structure - 20:
            actions.add_effort(ActionType.repair_structure, (city.max_structure - avail_effort) * 2)
            avail_effort -= (city.max_structure - avail_effort) * 2
            # add effort to repair city if structure below 50

        if city.population < city.structure:
            actions.add_effort(ActionType.regain_population, (city.structure - avail_effort) * 2)
            avail_effort -= (city.structure - avail_effort) * 2

        lasting_disasters = []
        for disaster in disasters:
            if disaster.type in self.lasting_disasters:
                lasting_disasters.append(disaster)

            self.previous_disaster = disaster
        try:
            lasting_disasters.sort(key=lambda x: lasting_disasters[0].effort_remaining)
        except IndexError:
            pass

        for i in range(len(lasting_disasters)):
            actions.add_effort(lasting_disasters[i], lasting_disasters[i].effort_remaining)
            if avail_effort > lasting_disasters[i].effort_remaining // 3 + 10:
                avail_effort -= avail_effort - lasting_disasters[i].effort_remaining
            else:
                avail_effort -= avail_effort

        try:
            lasting_disasters.sort(key=lambda x: lasting_disasters[0].effort_remaining)
        except IndexError:
            pass

        actions.add_effort(city.buildings[BuildingType.billboard], avail_effort)
        avail_effort -= avail_effort

        # print(
        #     "blizz " + str(city.sensors[SensorType.blizzard].sensor_results) \
        #     + "\nearth " + str(city.sensors[SensorType.earthquake].sensor_results) \
        #     + "\nfire " + str(city.sensors[SensorType.fire].sensor_results) \
        #     + "\nmonster " + str(city.sensors[SensorType.monster].sensor_results) \
        #     + "\ntornado " + str(city.sensors[SensorType.tornado].sensor_results) \
        #     + "\nufo " + str(city.sensors[SensorType.ufo].sensor_results)
        #     )
        # print(str(self.previous_disaster) + "----------------")

        if city.sensors[SensorType.ufo].sensor_results >= .86:
            self.decree_lag = 4
            self.decree = self.disaster_to_decree[DisasterType.ufo]
        elif city.sensors[SensorType.earthquake].sensor_results >= .86:
            self.decree_lag = 4
            self.decree = self.disaster_to_decree[DisasterType.earthquake]
        elif city.sensors[SensorType.tornado].sensor_results >= .86:
            self.decree_lag = 4
            self.decree = self.disaster_to_decree[DisasterType.tornado]
        # elif city.sensors[SensorType.monster].sensor_results >= .86:
        #     self.decree_lag = 4
        #     self.decree = self.disaster_to_decree[DisasterType.monster]
        # elif city.sensors[SensorType.blizzard].sensor_results >= .86:
        #     self.decree_lag = 4
        #     self.decree = self.disaster_to_decree[DisasterType.blizzard]
        # elif city.sensors[SensorType.fire].sensor_results >= .86:
        #     self.decree_lag = 4
        #     self.decree = self.disaster_to_decree[DisasterType.fire]

        # if self.decree_lag < 2:
        actions.set_decree(self.decree)
        if self.decree != self.previous_decree:
            print("\n--------------decree changed to " + self.decrees[self.decree])
            self.previous_decree = self.decree
        self.decree_lag -= 1