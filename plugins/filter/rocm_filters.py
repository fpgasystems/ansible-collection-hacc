import re
from ansible.errors import AnsibleFilterError
from packaging.version import Version

class FilterModule(object):
    def filters(self):
        return {
            'rocm_strip_patch': self.strip_patch,
            'rocm_incompatible': self.check_rocm_compatibility
        }

    def strip_patch(self, version):
        """
        Convert a version string 'X.Y.Z' to 'X.Y'.
        If the version is already 'X.Y', returns as is.
        """
        if not isinstance(version, str):
            raise AnsibleFilterError("Version must be a string")
        parts = version.split(".")
        if len(parts) < 2:
            raise AnsibleFilterError(f"Version '{version}' must have at least major.minor")
        return ".".join(parts[:2])

    def check_rocm_compatibility(self, rocm_versions, amdgpu_kernel_version, compatibility_dict):
        """
        Returns a list of incompatible ROCm versions (major.minor aware).
        """
        # Strip patch version
        stripped_kernel = self.strip_patch(amdgpu_kernel_version)
        stripped_rocm = [self.strip_patch(v) for v in rocm_versions]

        # Get compatible ROCm versions for the kernel
        compatible = compatibility_dict.get(stripped_kernel)
        if compatible is None:
            raise AnsibleFilterError(f"No compatibility info found for AMDGPU kernel '{stripped_kernel}'")

        # Return incompatible versions (original versions)
        incompatible = [orig for orig, stripped in zip(rocm_versions, stripped_rocm) if stripped not in compatible]
        return incompatible
