from fuzzylogic.classes import rule_from_table
from fis import fis

# The big amount of imports is (an unfortunate) consequence of using fuzzylogic.classes.rule_from_table
# TODO: we can potentially import all this dynamically, however, it should also be correctly added to globals namespace for rule_from_table() to work
#inputs:
from variables.fuel import fuel
from variables.ride_time import ride_time
from variables.temperature import temperature
from variables.traffic_congestion import traffic_congestion
from variables.daytime import daytime
from variables.visibility import visibility
from variables.daytime import daytime
from variables.car_maintenance_history import car_maintenance_history
from variables.poi import poi

# outputs:
from variables.gas_station import gas_station
from variables.route_recalculation import route_recalculation
from variables.supply_amenities import supply_amenities
from variables.ride_sharing import ride_sharing
from variables.speed_adjustment import speed_adjustment
from variables.headlight_intensity import headlight_intensity
from variables.car_goes_for_maintenance import car_goes_for_maintenance
from variables.recommendation_for_stopping import recommendation_for_stopping
from variables.open_windows import open_windows


# Add a rule to the FIS
@fis.rule
def gas_station_rule():
    # Define a 2-input, 1-output rule, see fuzzylogic documentation for details
    gas_station_table = """
                        fuel.empty          fuel.some           fuel.enough         fuel.full
    ride_time.short     gas_station.some    gas_station.no      gas_station.no      gas_station.no
    ride_time.average   gas_station.some    gas_station.some    gas_station.no      gas_station.no
    ride_time.long      gas_station.large   gas_station.some    gas_station.no      gas_station.no
    ride_time.very      gas_station.large   gas_station.large   gas_station.some    gas_station.no
    """

    # !!! the name must be the same as the file name AND the variable!
    output_domain_name = "gas_station"
    # tell the FIS which input is required
    input_list = ["ride_time", "fuel"]
    # create a Rule
    rule = rule_from_table(gas_station_table, globals())
    return (output_domain_name, input_list, rule)

@fis.rule
def route_recalculation_rule():
    # Define a 2-input, 1-output rule, see fuzzylogic documentation for details
    route_recalculation_table = """
                        traffic_congestion.uncongested   traffic_congestion.average        traffic_congestion.highly_congested
    ride_time.short     route_recalculation.no           route_recalculation.no            route_recalculation.recommended
    ride_time.average   route_recalculation.no           route_recalculation.no            route_recalculation.highly
    ride_time.long      route_recalculation.no           route_recalculation.recommended   route_recalculation.highly
    ride_time.very      route_recalculation.no           route_recalculation.recommended   route_recalculation.highly
    """

    # !!! the name must be the same as the file name AND the variable!
    output_domain_name = "route_recalculation"
    # tell the FIS which input is required
    input_list = ["ride_time", "traffic_congestion"]
    # create a Rule
    rule = rule_from_table(route_recalculation_table, globals())
    return (output_domain_name, input_list, rule)

@fis.rule
def supply_amenities_rule():
    # Define a 2-input, 1-output rule, see fuzzylogic documentation for details
    supply_amenities_table = """
                          ride_time.short                ride_time.average              ride_time.long                 ride_time.very
    temperature.cold      supply_amenities.no            supply_amenities.no            supply_amenities.recommended   supply_amenities.highly 
    temperature.cool      supply_amenities.no            supply_amenities.no            supply_amenities.recommended   supply_amenities.highly
    temperature.warm      supply_amenities.no            supply_amenities.no            supply_amenities.recommended   supply_amenities.highly
    temperature.hot       supply_amenities.recommended   supply_amenities.recommended   supply_amenities.highly        supply_amenities.highly
    temperature.extreme   supply_amenities.highly        supply_amenities.highly        supply_amenities.highly        supply_amenities.highly
    """

    # !!! the name must be the same as the file name AND the variable!
    output_domain_name = "supply_amenities"
    # tell the FIS which input is required
    input_list = ["temperature", "ride_time"]
    # create a Rule
    rule = rule_from_table(supply_amenities_table, globals())
    return (output_domain_name, input_list, rule)

@fis.rule
def ride_sharing_rule():
    # Define a 2-input, 1-output rule, see fuzzylogic documentation for details
    ride_sharing_table = """
                      traffic_congestion.uncongested   traffic_congestion.average        traffic_congestion.highly_congested
    daytime.morning   ride_sharing.recommended         ride_sharing.highly               ride_sharing.highly 
    daytime.dawn      ride_sharing.no                  ride_sharing.recommended          ride_sharing.recommended 
    daytime.day       ride_sharing.recommended         ride_sharing.recommended          ride_sharing.recommended 
    daytime.evening   ride_sharing.no                  ride_sharing.highly               ride_sharing.highly 
    daytime.night     ride_sharing.no                  ride_sharing.no                   ride_sharing.recommended 
    """
    
    # !!! the name must be the same as the file name AND the variable!
    output_domain_name = "ride_sharing"
    # tell the FIS which input is required
    input_list = ["daytime", "traffic_congestion"]
    # create a Rule
    rule = rule_from_table(ride_sharing_table, globals())
    return (output_domain_name, input_list, rule)

@fis.rule
def speed_adjustment_rule():
    speed_adjustment_table = """
                                        visibility.clear                visibility.hazy                 visibility.drizzle              visibility.rainy                visibility.foggy
    traffic_congestion.uncongested      speed_adjustment.fast           speed_adjustment.fast           speed_adjustment.moderate       speed_adjustment.moderate       speed_adjustment.slow 
    traffic_congestion.average          speed_adjustment.moderate       speed_adjustment.moderate       speed_adjustment.moderate       speed_adjustment.slow           speed_adjustment.very_slow
    traffic_congestion.highly_congested speed_adjustment.slow           speed_adjustment.slow           speed_adjustment.slow           speed_adjustment.very_slow      speed_adjustment.very_slow
    """

    output_domain_name = "speed_adjustment"
    input_list = ["traffic_congestion", "visibility"]
    rule = rule_from_table(speed_adjustment_table, globals())
    return (output_domain_name, input_list, rule)

@fis.rule
def headlight_intensity_rule():

    headlight_intensity_table = """
                                        visibility.clear                visibility.hazy                 visibility.drizzle              visibility.rainy                visibility.foggy
    daytime.dawn                        headlight_intensity.high        headlight_intensity.high        headlight_intensity.high        headlight_intensity.high        headlight_intensity.high
    daytime.morning                     headlight_intensity.medium      headlight_intensity.medium      headlight_intensity.high        headlight_intensity.high        headlight_intensity.high
    daytime.day                         headlight_intensity.low         headlight_intensity.medium      headlight_intensity.medium      headlight_intensity.high        headlight_intensity.high
    daytime.evening                     headlight_intensity.medium      headlight_intensity.medium      headlight_intensity.high        headlight_intensity.high        headlight_intensity.high
    daytime.night                       headlight_intensity.high        headlight_intensity.high        headlight_intensity.high        headlight_intensity.high        headlight_intensity.high                              
    """

    output_domain_name = "headlight_intensity"
    input_list = ["daytime", "visibility"]
    rule = rule_from_table(headlight_intensity_table, globals())

    return (output_domain_name, input_list, rule)

@fis.rule
def recommendation_for_stopping_rule():

    recommendation_for_stopping_table = """
                                        poi.abundant                            poi.many                                poi.moderate                            poi.few                                     poi.scarce
    temperature.cold                    recommendation_for_stopping.optional    recommendation_for_stopping.optional    recommendation_for_stopping.optional    recommendation_for_stopping.notAdvised      recommendation_for_stopping.notAdvised
    temperature.cool                    recommendation_for_stopping.advised     recommendation_for_stopping.optional    recommendation_for_stopping.optional    recommendation_for_stopping.notAdvised      recommendation_for_stopping.notAdvised
    temperature.warm                    recommendation_for_stopping.advised     recommendation_for_stopping.advised     recommendation_for_stopping.advised     recommendation_for_stopping.optional        recommendation_for_stopping.notAdvised
    temperature.hot                     recommendation_for_stopping.advised     recommendation_for_stopping.optional    recommendation_for_stopping.notAdvised  recommendation_for_stopping.notAdvised      recommendation_for_stopping.notAdvised
    temperature.extreme                 recommendation_for_stopping.optional    recommendation_for_stopping.notAdvised  recommendation_for_stopping.notAdvised  recommendation_for_stopping.notAdvised      recommendation_for_stopping.notAdvised                             
    """

    output_domain_name = "recommendation_for_stopping"
    input_list = ["temperature", "poi"]
    rule = rule_from_table(recommendation_for_stopping_table, globals())

    return (output_domain_name, input_list, rule)

@fis.rule
def car_goes_for_maintenance_rule():

    car_goes_for_maintenance_table = """
                                        car_maintenance_history.very_well                       car_maintenance_history.well                            car_maintenance_history.moderately                      car_maintenance_history.poorly                      car_maintenance_history.very_poorly
    ride_time.short                     car_goes_for_maintenance.not_recommended                car_goes_for_maintenance.not_recommended                car_goes_for_maintenance.not_recommended                car_goes_for_maintenance.recommended                car_goes_for_maintenance.highly_recommended
    ride_time.average                   car_goes_for_maintenance.not_recommended                car_goes_for_maintenance.not_recommended                car_goes_for_maintenance.recommended                    car_goes_for_maintenance.highly_recommended         car_goes_for_maintenance.highly_recommended
    ride_time.long                      car_goes_for_maintenance.not_recommended                car_goes_for_maintenance.recommended                    car_goes_for_maintenance.recommended                    car_goes_for_maintenance.highly_recommended         car_goes_for_maintenance.highly_recommended
    ride_time.very                      car_goes_for_maintenance.recommended                    car_goes_for_maintenance.recommended                    car_goes_for_maintenance.recommended                    car_goes_for_maintenance.highly_recommended         car_goes_for_maintenance.highly_recommended

    """
    
    output_domain_name = "car_goes_for_maintenance"
    input_list = ["ride_time", "car_maintenance_history"]
    rule = rule_from_table(car_goes_for_maintenance_table, globals())

    return (output_domain_name, input_list, rule)

@fis.rule
def open_windows_rule():
    open_windows_table = """
                            poi.abundant        poi.many            poi.moderate        poi.few             poi.scarce
    visibility.clear        open_windows.hig    open_windows.hig    open_windows.rec    open_windows.rec    open_windows.rec
    visibility.hazy         open_windows.hig    open_windows.rec    open_windows.rec    open_windows.no     open_windows.rec         
    visibility.drizzle      open_windows.rec    open_windows.no     open_windows.no     open_windows.no     open_windows.rec         
    visibility.rainy        open_windows.rec    open_windows.no     open_windows.no     open_windows.no     open_windows.no         
    visibility.foggy        open_windows.no     open_windows.no     open_windows.no     open_windows.no     open_windows.no                              
    """
    # !!! the name must be the same as the file name AND the variable!
    output_domain_name = "open_windows"
    # tell the FIS which input is required
    input_list = ["poi", "visibility"]
    # create a Rule
    rule = rule_from_table(open_windows_table, globals())
    return (output_domain_name, input_list, rule)