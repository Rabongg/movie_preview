def data_list_to_set(data_list: list[dict]) -> set:
    data_set = set()
    for data in data_list:
        data_set.add(data['title'])

    return data_set