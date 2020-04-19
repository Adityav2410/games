from car import CarRaceEngine

if __name__ == "__main__":
    import json
    with open("config.json", "r") as f:
        config = json.load(f)
    
    engine = CarRaceEngine(config)
    engine.start()