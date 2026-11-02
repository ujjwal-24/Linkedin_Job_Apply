'''
Author:     Sai Vignesh Golla
License:    MIT License
            https://opensource.org/license/mit
GitHub:     https://github.com/GodsScion/Auto_job_applier_linkedIn

Loads user settings saved by the local control panel (see app.py) from
`user_config.json` at the project root, and applies them over the Python
defaults defined in the config/*.py files.

If `user_config.json` does not exist, everything here is a no-op and the tool
behaves exactly as it always has: configuration comes entirely from the
config/*.py defaults. This keeps the classic "edit the .py files" workflow
fully working for existing users.
'''

import os
import json

# This file lives in <project_root>/config/, so the project root is one level up.
_CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
_ROOT_DIR = os.path.dirname(_CONFIG_DIR)
USER_CONFIG_PATH = os.path.join(_ROOT_DIR, "user_config.json")

EXPERIENCE_LEVELS = (
    "Internship", "Entry level", "Associate", "Mid-Senior level", "Director", "Executive",
)


def normalize_setting(section: str, key: str, value):
    """Accept common experience-level shorthand without guessing unknown values."""
    if section != "search" or key != "experience_level" or not isinstance(value, list):
        return value
    aliases = {level.casefold(): level for level in EXPERIENCE_LEVELS}
    aliases.update({"mid-senior": "Mid-Senior level", "entry": "Entry level"})
    return [aliases.get(item.strip().casefold(), item.strip())
            if isinstance(item, str) else item for item in value]


def load_user_config() -> dict:
    '''
    Returns the full override dictionary from `user_config.json`, or an empty
    dict if the file is missing, unreadable, or not valid JSON. Never raises.
    '''
    try:
        with open(USER_CONFIG_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            if not isinstance(data, dict):
                return {}
            search = data.get("search")
            if isinstance(search, dict) and "experience_level" in search:
                search["experience_level"] = normalize_setting(
                    "search", "experience_level", search["experience_level"])
            return data
    except (FileNotFoundError, json.JSONDecodeError, OSError, ValueError):
        return {}


def apply(module_name: str, module_globals: dict) -> None:
    '''
    Overrides a config module's existing globals with values from the matching
    section of `user_config.json`.

    - `module_name` is the module's `__name__` (e.g. "config.settings"); the last
      dotted part is the section name looked up in the JSON ("settings").
    - Only keys that ALREADY exist as globals in the module are applied, so the
      JSON can never introduce new names into the config namespace.
    '''
    section_name = module_name.split(".")[-1]
    section = load_user_config().get(section_name, {})
    if not isinstance(section, dict):
        return
    for key, value in section.items():
        if key in module_globals:
            module_globals[key] = value
