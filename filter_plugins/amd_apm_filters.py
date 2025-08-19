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
        VALID_INSTALL_METHODS = ['archive', 'installer']
        VALID_STATES = ['present', 'absent']
        VALID_UPDATE_LEVELS = ['base', 'update1', 'update2']
        VALID_VIVADO_ONLY_VALUES = [False, True]
        VALID_INSTALL_RUNTIME_VALUES = [True, False]


        def validate_release_format(release):
            if not re.match(RELEASE_REGEX, release):
                raise AnsibleFilterError(
                    f"Invalid 'release' format: '{release}'. Expected format is 'YYYY.N' (e.g., '2024.1')"
                )

        if isinstance(item, str):
            validate_release_format(item)
            return {
                'release': item,
                'install_method': 'archive',
                'state': 'present',
                'update_level': 'base',
                'vivado_only': False,
                'install_runtime': True
            }
        elif isinstance(item, dict):
            if 'release' not in item:
                raise AnsibleFilterError("Missing required 'release' key in object")

            release = item['release']
            validate_release_format(release)

            install_method = item.get('install_method', 'archive')
            if install_method not in VALID_INSTALL_METHODS:
                raise AnsibleFilterError(
                    f"Invalid 'install_method': '{install_method}'. Must be one of: {', '.join(VALID_INSTALL_METHODS)}"
                )

            state = item.get('state', 'present')
            if state not in VALID_STATES:
                raise AnsibleFilterError(
                    f"Invalid 'state': '{state}'. Must be one of: {', '.join(VALID_STATES)}"
                )

            update_level = item.get('update_level', 'base')
            if update_level not in VALID_UPDATE_LEVELS:
                raise AnsibleFilterError(
                    f"Invalid 'update_level': '{update_level}'. Must be one of: {', '.join(VALID_UPDATE_LEVELS)}"
                )

            vivado_only = item.get('vivado_only', False)
            if vivado_only not in VALID_VIVADO_ONLY_VALUES:
                raise AnsibleFilterError(
                    f"Invalid 'vivado_only': '{vivado_only}'. Must be a boolean (True or False)"
                )

            install_runtime = item.get('install_runtime', True)
            if install_runtime not in VALID_INSTALL_RUNTIME_VALUES:
                raise AnsibleFilterError(
                    f"Invalid 'install_runtime': '{install_runtime}'. Must be a boolean (True or False)"
                )

            return {
                'release': release,
                'install_method': install_method,
                'state': state,
                'update_level': update_level,
                'vivado_only': vivado_only,
                'install_runtime': install_runtime
            }

        else:
            raise AnsibleFilterError(f"Unsupported type: {type(item)}")

