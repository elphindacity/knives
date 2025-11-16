import math
import json


class Target():

    def __init__(self, user, name='Default', shape='Square', num=2, size=[12, 24]):
        self.user = user
        self.name = name
        self.shape = shape
        self.num_rings = num
        self.ring_size = size
        self.area = self.get_area()

    def set_name(self, n):
        self.name = n

    def set_shape(self, shape):
        self.shape = shape

    def set_num_rings(self, x):
        self.num_rings = x

    def set_ring_size(self, size_list):
        self.ring_size = size_list

    def get_area(self):
        area_list = []
        for x in range(self.num_rings):
            if self.shape == 'Square':
                area = self.ring_size[x] * self.ring_size[x]
            else:
                area = math.pi * (self.ring_size[x] ** 2)
            area_list.append(area)
        return area_list

    def display(self):
        print("*** " + self.name + " ***")
        print("    Shape : " + self.shape)
        print("    Rings : " + str(self.num_rings))
        print("    Size  : " + str(self.ring_size))
        print("    Area  : " + str(self.area))


def save_target(target, filename='targets.json'):
    target_data = {
        'user': target.user,
        'name': target.name,
        'shape': target.shape,
        'num_rings': target.num_rings,
        'ring_size': target.ring_size,
        'area': target.area
    }
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    # Check if target name already exists for the same user
    existing_target = next((t for t in data if t['user'] == target.user and t['name'] == target.name), None)
    if existing_target:
        print(f"Target '{target.name}' already exists for user '{target.user}'. Saving cancelled.")
        return
    data.append(target_data)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    print(f"Target '{target.name}' saved successfully for user '{target.user}'.")

def delete_target(user, target_name, filename='targets.json'):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"No targets found in '{filename}'.")
        return
    # Find the target to delete
    target_to_delete = next((t for t in data if t['user'] == user and t['name'] == target_name), None)
    if target_to_delete:
        data.remove(target_to_delete)
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Target '{target_name}' deleted successfully for user '{user}'.")
    else:
        print(f"Target '{target_name}' not found for user '{user}'.")

def load_targets(user_name, filename='targets.json'):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    # Filter targets by user name
    user_targets = [target for target in data if target['user'] == user_name]
    # Convert target data to Target objects
    targets = [Target(
        user=target['user'],
        name=target['name'],
        shape=target['shape'],
        num=target['num_rings'],
        size=target['ring_size']
    ) for target in user_targets]
    return targets