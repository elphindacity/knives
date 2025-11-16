class Bullseye():

    def __init__(self, name, target, knives=3, rounds=3):
        self.name = name
        self.target = target
        self.knives = knives
        self.rounds = rounds
        self.current_knife = 0
        self.current_round = 0
        self.points = self.create_points()

    def display(self):
        print("*** " + self.name + " ***")
        for x in range(self.rounds):
            self.display_round(x)

    def display_round(self, x):
        print("ROUND " + str(x))

    def create_points(self):
        total_points = []
        for x in range(self.rounds):
            round_points = []
            for y in range(self.knives):
                round_points.append(0)
            total_points.append(round_points)
        return total_points

# def save_bullseye(target, filename='bullseye.json'):
#     target_data = {
#         'user': target.user,
#         'name': target.name,
#         'shape': target.shape,
#         'num_rings': target.num_rings,
#         'ring_size': target.ring_size,
#         'area': target.area
#     }
#     try:
#         with open(filename, 'r') as f:
#             data = json.load(f)
#     except FileNotFoundError:
#         data = []
#     # Check if target name already exists for the same user
#     existing_target = next((t for t in data if t['user'] == target.user and t['name'] == target.name), None)
#     if existing_target:
#         print(f"Target '{target.name}' already exists for user '{target.user}'. Saving cancelled.")
#         return
#     data.append(target_data)
#     with open(filename, 'w') as f:
#         json.dump(data, f, indent=4)
#     print(f"Target '{target.name}' saved successfully for user '{target.user}'.")