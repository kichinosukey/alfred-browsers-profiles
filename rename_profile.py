#!/usr/bin/env python3

import os
import json
import sys
from lib.chromium import get_chromium_profiles_path
from lib.helpers import get_browsers


def get_profile_path(browser_name, profile_folder):
    """Get the path to the profile's Preferences file"""
    home = os.path.expanduser("~")
    supported_browsers = get_browsers()

    # Find the browser by name
    browser = None
    for b in supported_browsers.get("chromium", []):
        if b["name"] == browser_name:
            browser = b
            break

    if not browser:
        print(f"Browser '{browser_name}' not found")
        return None

    # Get the profile file path
    path_profile = f"{home}/{browser['path']}"
    profiles = get_chromium_profiles_path(browser, path_profile)

    # Find the profile folder in the list of profile paths
    profile_file = None
    for p in profiles:
        if f"/{profile_folder}/" in p:
            profile_file = p
            break

    if not profile_file:
        print(f"Profile folder '{profile_folder}' not found")
        return None

    return profile_file


def rename_profile(profile_file, new_name=None):
    """Rename the profile directly"""
    try:
        # Read the current profile data
        with open(profile_file) as f:
            data = json.load(f)

        # Extract current profile name
        current_name = data.get("profile", {}).get("name", "Unknown")
        browser_info = os.path.basename(os.path.dirname(profile_file))

        # Display info about the profile
        print(f"\nBrowser Profile: {browser_info}")
        print(f'Current profile name: "{current_name}"')

        # If no new name was provided, show instructions and exit
        if not new_name:
            print("\nTo rename this profile, provide a new name as an argument:")
            print(
                f"./main.py | jq -r '.items[1].arg' | ./rename_profile.py \"新しいプロファイル名\""
            )
            return False

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
    # Get new profile name from command line argument
    new_name = None
    if len(sys.argv) > 1:
        new_name = sys.argv[1]

    # Get the browser and profile info from input string
    input_string = sys.stdin.read().strip()

    # Split the input into browser name and profile folder
    parts = input_string.split()
    if len(parts) < 2:
        print(f"Invalid input format: '{input_string}'")
        print("Expected format: 'BROWSER PROFILE'")
        sys.exit(1)

    browser_name = parts[0]
    # The profile folder might contain spaces, so join the rest of the parts
    profile_folder = " ".join(parts[1:])

    # Get the profile file path
    profile_file = get_profile_path(browser_name, profile_folder)

    if not profile_file:
        sys.exit(1)

    # Rename the profile
    if not rename_profile(profile_file, new_name):
        sys.exit(1)

    print("Profile renamed successfully.")


if __name__ == "__main__":
    main()
