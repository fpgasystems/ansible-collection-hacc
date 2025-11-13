import re
from ansible.errors import AnsibleFilterError

class FilterModule(object):
    def filters(self):
        return {
            'xrt_normalize_releases_list': self.normalize_releases_list,
            'xrt_get_latest_release': self.get_latest_release,
            'xrt_pick_target': self.pick_target
        }

    def pick_target(self, releases, target):
        """
        Choose the appropriate deployment/development target version.

        Args:
            releases (list): list of release entries (strings or dicts)
            target (str): one of "latest", "absent", or a version string like "2024.2"

        Returns:
            str | None: the selected version string, or None if no valid match
        """
        if releases is None:
            releases = []

        if target == "absent":
            return None

        if target == "latest":
            return self.get_latest_release(releases) if releases else None

        # Match regex: YYYY.X (year + single digit)
        if re.match(r"^\d{4}\.\d$", to_text(target)):
            return target

        # Otherwise invalid
        return None

    def get_latest_release(self, items):

        def parse_release(release_str):
            """Parse a release string 'YYYY.X' into a tuple (year, minor)."""
            try:
                year_str, minor_str = release_str.split('.')
                return int(year_str), int(minor_str)
            except Exception as e:
                raise AnsibleFilterError(f"Invalid release format '{release_str}': {e}")

        if not isinstance(items, list):
            raise AnsibleFilterError("Input must be a list of release strings")

        try:
            return max(items, key=lambda x: parse_release(x))
        except ValueError:
            raise AnsibleFilterError("List is empty or releases are invalid")


    def validate_release_format(self, release):
        RELEASE_REGEX = r'^\d{4}\.\d$'

        if not re.match(RELEASE_REGEX, release):
            raise AnsibleFilterError(
                f"Invalid 'release' format: '{release}'. Expected format is 'YYYY.N' (e.g., '2024.1')"
            )

    def normalize_releases_list(self, item):
        # Filter to fill in all defaults of the xrt_releases list, when not provided
        #   When only a String is given, this is interpreted as the release string
        #   Otherwise a Dictionary is expected, with at least the release attribute. All missing attributes are filled in with defaults

        VALID_STATE = ['present', 'absent']

        if isinstance(item, str):
            self.validate_release_format(item)
            return {
                    'release': item,
                    'state': 'present'
            }
        elif isinstance(item, dict):
            if 'release' not in item:
                raise AnsibleFilterError("Missing required 'release' key in object")

            release = item['release']
            self.validate_release_format(release)

            state = item.get('state', 'present')
            if state not in VALID_STATE:
                raise AnsibleFilterError(
                    f"Invalid 'state': '{state}'. Must be one of: {', '.join(VALID_STATE)}"
                )

            return {
                'release': release,
                'state': state
            }

        else:
            raise AnsibleFilterError(f"Unsupported type: {type(item)}")

