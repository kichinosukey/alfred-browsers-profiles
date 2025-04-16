#!/usr/bin/env python3

import os
import sys
import json
from lib.chromium import get_chromium_profiles
from lib.helpers import get_browsers


def get_profile_path(browser_name, profile_folder):
    """Get the path to the profile's Preferences file

    Args:
        browser_name (str): The name of the browser (e.g., "chromium").
        profile_folder (str): The name of the profile folder.
    Returns:
        str: The path to the profile's Preferences file.
    """
    home = os.path.expanduser("~")
    supported_browsers = get_browsers()

    # Find the browser by name
    browser = None
    for b in supported_browsers.get("chromium", []):
        if b["name"] == browser_name:
            browser = b
            break
    if not browser:
        return None

    # Get the profile file path
    path_profile = f"{home}/{browser['path']}"

    # Get the list of profiles
    profiles = get_chromium_profiles(browser, path_profile)
    if not profiles:
        return None

    # Find profile file
    profile_file = None
    target_arg = f"{browser_name} {profile_folder}"
    for p in profiles:
        if p.get("arg") == target_arg:
            profile_dir = p.get("arg").replace(f"{browser_name} ", "")
            profile_file = os.path.join(path_profile, profile_dir, "Preferences")
            break
    if not profile_file:
        return None

    return profile_file


def rename_profile(profile_file, new_name=None):
    """Rename the profile directly
    Args:
        profile_file (str): The path to the profile file.
        new_name (str): The new name for the profile.
    Returns:
        bool: True if the profile was renamed successfully, False otherwise.
    """
    try:
        # Read the current profile data
        with open(profile_file) as f:
            data = json.load(f)

        # Extract current profile name
        current_name = data.get("profile", {}).get("name", "Unknown")
        # browser_info = os.path.basename(os.path.dirname(profile_file))

        # Update the profile name
        data["profile"]["name"] = new_name

        # Write back to file
        with open(profile_file, "w") as f:
            json.dump(data, f)

        print(f'Profile name changed from "{current_name}" to "{new_name}"')
        return True

    except Exception as e:
        print(f"Error renaming profile: {e}")
        return False


def main():
    # Split the command line arguments
    print("sys.argv:", sys.argv, file=sys.stderr, flush=True)  # debug
    if len(sys.argv) < 3:
        print("Usage: rename_profile.py <new_name> <browser_and_profile>")
        sys.exit(1)

    new_name = sys.argv[1]
    input_string = sys.argv[2]
    parts = input_string.split()
    if len(parts) < 2:
        print(f"Invalid input format: '{input_string}'")
        print("Expected format: 'BROWSER PROFILE'")
        sys.exit(1)

    # Get the browser name and profile file
    browser_name = parts[0]
    profile_folder = " ".join(parts[1:])
    profile_file = get_profile_path(browser_name, profile_folder)
    if not profile_file:
        sys.exit(1)

    # Check success of renaming the profile
    if not rename_profile(profile_file, new_name):
        sys.exit(1)
    print("Profile renamed successfully.")


if __name__ == "__main__":
    main()
