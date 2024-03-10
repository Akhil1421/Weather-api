def get_required_attributes(response_dict):
    city_location = response_dict['location']
    city_current = response_dict['current']
    city_current_condition = city_current['condition']
    
    required_data = {
        'name' : city_location['name'],
        'country' : city_location['country'],
        'temperature': city_current['temp_c'],
        'humidity': city_current['humidity'],
        'condition': city_current_condition['text'],
        'icon': f"https:{city_current_condition['icon']}"
    }
    return required_data
