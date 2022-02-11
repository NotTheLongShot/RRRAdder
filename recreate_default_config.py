import json
import sys


def create_default_config(location="config.json"):
    default_config = {
        "pwcg_missions_dir": r"..\data\Missions\PWCG",
        "campaign_name": "TEST",
        "backup_original": True,
        "use_only_friendly": True,
        "run_missionresaver": True,
        "maintenanceRadius": 80,
        "repair": False,
        "heal": False,
        "rearm": True,
        "refuel": True,
        "repairTime":  0,
        "healTime":  0,
        "rearmTime":  1,
        "refuelTime":  1,

        "airfields": [
            "active_in_mission_box",
        ],
        "overrides": {}
        }

    with open(location, 'w') as f:
        f.write(json.dumps(default_config, indent=4))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        loc = sys.argv[1]
    else:
        loc = "config.json"
    create_default_config(location=loc)
