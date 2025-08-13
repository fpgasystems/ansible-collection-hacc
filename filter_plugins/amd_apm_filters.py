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
        if isinstance(item, str):
            return {
                'release': item,
                'install_method': 'zip',
                'state': 'present',
                'update_level': 'base',
                'vivado_only': False
            }
        elif isinstance(item, dict):
            if 'release' not in item:
                raise AnsibleFilterError("Missing required 'release' key in object")
            return {
                'release': item['release'],
                'install_method': item.get('install_method', 'zip'),
                'state': item.get('state', 'present'),
                'update_level': item.get('update_level', 'base'),
                'vivado_only': item.get('vivado_only', False)
            }
        else:
            raise AnsibleFilterError(f"Unsupported type: {type(item)}")

