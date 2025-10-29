import re
from ansible.errors import AnsibleFilterError

class FilterModule(object):
    def filters(self):
        return {
            'normalize_releases_list': self.normalize_releases_list,
            'tools_path': self.get_tools_path,
            'get_newest_release': self.get_newest_release
        }

    def get_newest_release(self, items):

        def parse_release(release_str):
            """Parse a release string 'YYYY.X' into a tuple (year, minor)."""
            try:
                year_str, minor_str = release_str.split('.')
                return int(year_str), int(minor_str)
            except Exception as e:
                raise AnsibleFilterError(f"Invalid release format '{release_str}': {e}")

        if not isinstance(items, list):
            raise AnsibleFilterError("Input must be a list of dictionaries")

        try:
            return max(items, key=lambda x: parse_release(x['release']))
        except KeyError:
            raise AnsibleFilterError("Each item must have a 'release' attribute")
        except ValueError:
            raise AnsibleFilterError("List is empty or releases are invalid")

    def get_tools_path(self, base_path, release, tool):
        self.validate_release_format(release)
        year = int(release.split(".")[0])

        VALID_TOOLS = ["Vivado", "Vitis", "Vitis_HLS", "Model_Composer"]
        if not any(tool in t for t in VALID_TOOLS):
            raise AnsibleFilterError(
                    f"Invalid 'tool': '{tool}'. Expected any of: {', '.join(VALID_TOOLS)}"
            )

        path = base_path
        if year >= 2025:
            path = path + "/" + release + "/" + tool
        else:
            path = path + "/" + tool + "/" + release

        return path


    def validate_release_format(self, release):
        RELEASE_REGEX = r'^\d{4}\.\d$'

        if not re.match(RELEASE_REGEX, release):
            raise AnsibleFilterError(
                f"Invalid 'release' format: '{release}'. Expected format is 'YYYY.N' (e.g., '2024.1')"
            )

    def normalize_releases_list(self, item):
        # Filter to fill in all defaults of the amd_apm_releases list, when not provided
        #   When only a String is given, this is interpreted as the release string
        #   Otherwise a Dictionary is expected, with at least the release attribute. All missing attributes are filled in with defaults

        VALID_TOOLS_STATE = ['present', 'absent']
        VALID_TOOLS_INSTALL_METHODS = ['archive', 'installer']
        VALID_TOOLS_UPDATE_LEVELS = ['base', 'update1', 'update2']
        VALID_TOOLS_VIVADO_ONLY_VALUES = [False, True]



        if isinstance(item, str):
            self.validate_release_format(item)
            return {
                    'release': item,

                    'state': 'present',
                    'install_method': 'archive',
                    'update_level': 'base',
                    'vivado_only': False
            }
        elif isinstance(item, dict):
            if 'release' not in item:
                raise AnsibleFilterError("Missing required 'release' key in object")

            release = item['release']
            self.validate_release_format(release)

            tools_state = item.get('state', 'present')
            if tools_state not in VALID_TOOLS_STATE:
                raise AnsibleFilterError(
                    f"Invalid 'tools_state': '{tools_state}'. Must be one of: {', '.join(VALID_TOOLS_STATE)}"
                )

            tools_install_method = item.get('install_method', 'archive')
            if tools_install_method not in VALID_TOOLS_INSTALL_METHODS:
                raise AnsibleFilterError(
                    f"Invalid 'tools_install_method': '{tools_install_method}'. Must be one of: {', '.join(VALID_TOOLS_INSTALL_METHODS)}"
                )

            tools_update_level = item.get('update_level', 'base')
            if tools_update_level not in VALID_TOOLS_UPDATE_LEVELS:
                raise AnsibleFilterError(
                    f"Invalid 'tools_update_level': '{tools_update_level}'. Must be one of: {', '.join(VALID_TOOLS_UPDATE_LEVELS)}"
                )

            tools_vivado_only = item.get('vivado_only', False)
            if tools_vivado_only not in VALID_TOOLS_VIVADO_ONLY_VALUES:
                raise AnsibleFilterError(
                    f"Invalid 'tools_vivado_only': '{tools_vivado_only}'. Must be a boolean (True or False)"
                )

            return {
                'release': release,

                'state': tools_state,
                'install_method': tools_install_method,
                'update_level': tools_update_level,
                'vivado_only': tools_vivado_only
            }

        else:
            raise AnsibleFilterError(f"Unsupported type: {type(item)}")

