graph = {
    "S": {
        "C1": 12,
        "C2": 8,
        "C4": 15
    },

    "C1": {
        "C3": 9,
        "C5": 6
    },

    "C2": {
        "C3": 7,
        "C5": 10,
        "C4": 5,
        "C6": 5
    },

    "C3": {
        "T": 11
    },

    "C4": {
        "C6": 18
    },

    "C5": {
        "T": 14
    },

    "C6": {
        "T": 9
    },

    "T": {}
}
print("Water Distribution Network")
print(graph)