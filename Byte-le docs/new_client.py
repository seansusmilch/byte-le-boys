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

        self.sensor_to_disaster = {
            SensorType.tornado: DisasterType.tornado,
            SensorType.fire: DisasterType.fire,
            SensorType.blizzard: DisasterType.blizzard,
            SensorType.earthquake: DisasterType.earthquake,
            SensorType.monster: DisasterType.monster,
            SensorType.ufo: DisasterType.ufo,
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

    def team_name(self):
        return 'Team 2'

    def city_name(self):
        return '# TODO name city'

    def city_type(self):
        return CityType.popular

    def take_turn(self, turn, actions, city, disasters):
        avail_effort = city.population

        if city.structure < city.max_structure:
            max_struct = city.max_structure
            actions.add_effort(ActionType.repair_structure, (max_struct - avail_effort) * 2)
            avail_effort -= (max_struct - avail_effort) * 2
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
            if avail_effort > lasting_disasters[i].effort_remaining:
                avail_effort -= avail_effort - lasting_disasters[i].effort_remaining
            else:
                avail_effort -= avail_effort
            actions.add_effort(lasting_disasters[i], lasting_disasters[i].effort_remaining)

        avail_effort -= city.effort_remaining
        actions.add_effort(ActionType.upgrade_city, city.effort_remaining)
        if city.buildings[BuildingType.printer].level != BuildingLevel.level_one:
            actions.add_effort(city.buildings[BuildingType.printer], max(city.gold, avail_effort))

        if city.sensors[SensorType.ufo] != SensorLevel.level_three:
            actions.add_effort(city.sensors[SensorType.ufo], city.sensors[SensorType.ufo].effort_remaining)
        if city.sensors[SensorType.earthquake] != SensorLevel.level_three:
            actions.add_effort(city.sensors[SensorType.earthquake], city.sensors[SensorType.earthquake].effort_remaining)
        if city.sensors[SensorType.tornado] != SensorLevel.level_three:
            actions.add_effort(city.sensors[SensorType.tornado], city.sensors[SensorType.tornado].effort_remaining)


        #print("Effort Remaining: " + str(avail_effort))


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
            self.decree = self.disaster_to_decree[DisasterType.ufo]
        elif city.sensors[SensorType.earthquake].sensor_results >= .86:
            self.decree = self.disaster_to_decree[DisasterType.earthquake]
        elif city.sensors[SensorType.tornado].sensor_results >= .86:
            self.decree = self.disaster_to_decree[DisasterType.tornado]

        # elif city.sensors[SensorType.monster].sensor_results >= .86:
        #     self.decree = self.disaster_to_decree[DisasterType.monster]
        # elif city.sensors[SensorType.blizzard].sensor_results >= .86:
        #     self.decree = self.disaster_to_decree[DisasterType.blizzard]
        # elif city.sensors[SensorType.fire].sensor_results >= .86:
        #     self.decree = self.disaster_to_decree[DisasterType.fire]

        actions.set_decree(self.decree)
        if self.decree != self.previous_decree:
            print("\n--------------decree changed to " + self.decrees[self.decree])
            self.previous_decree = self.decree

        # sensors = dict()
        # for sensor_type, sensor in city.sensors.items():
        #     sensors[sensor_type] = sensor.sensor_results
        #
        # decree = self.disaster_to_decree[self.sensor_to_disaster[max(sensors.keys(), key=lambda k: sensors[k])]]
        # actions.set_decree(decree)