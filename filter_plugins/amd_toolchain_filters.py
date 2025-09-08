import re
from ansible.errors import AnsibleFilterError

class FilterModule(object):
    def filters(self):
        return {
            'normalize_releases_list': self.normalize_releases_list
        }

    def normalize_releases_list(self, item):
        # Filter to fill in all defaults of the amd_apm_releases list, when not provided
        #   When only a String is given, this is interpreted as the release string
        #   Otherwise a Dictionary is expected, with at least the release attribute. All missing attributes are filled in with defaults

        RELEASE_REGEX = r'^\d{4}\.\d$'

        VALID_TOOLS_STATE = ['present', 'absent']
        VALID_TOOLS_INSTALL_METHODS = ['archive', 'installer']
        VALID_TOOLS_UPDATE_LEVELS = ['base', 'update1', 'update2']
        VALID_TOOLS_VIVADO_ONLY_VALUES = [False, True]


        def validate_release_format(release):
            if not re.match(RELEASE_REGEX, release):
                raise AnsibleFilterError(
                    f"Invalid 'release' format: '{release}'. Expected format is 'YYYY.N' (e.g., '2024.1')"
                )

        if isinstance(item, str):
            validate_release_format(item)
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
            validate_release_format(release)

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

