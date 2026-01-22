ROCm
=========

This role installs the amdgpu kernel and ROCm userspace libraries/tools for AMD GPUs.

Requirements
------------

none

Role Variables
--------------

```yaml
rocm_amdgpu_kernel_version: ""
```
Set the version of the amdgpu kernel module. An empty string ("") skips installation. See the `rocm_supported_amdgpu_kernel_versions` variable in `vars/main.yml` for the supported amdgpu kernel versions.

```yaml
rocm_versions: []
```
Set the versions of ROCm you want to install in a list of strings. See the `rocm_supported_verions` variable in `vars/main.yml` for the supported ROCm versions. Not all ROCm versions are compatible with your selected amdgpu kernel version, see `rocm_compatibility_matrix` in `vars/main.yml` for the compatibility between ROCm versions and the amdgpu kernel.

The `environment-modules` package is always installed to allow users to switch easily between ROCm versions using for example `module load rocm/6.3.3`. See the docs [https://modules.readthedocs.io/en/latest/](https://modules.readthedocs.io/en/latest/).

```yaml
rocm_strict_mode: false
```
Strict mode enforces strict isolation between the memory of AMD CPUs and AMD GPUs. It also disables IOMMU optimizations, making the IOMMU behavior (like TLB flushing, etc.) more predictable. Strict mode needs to be enabled when using [Coyote](https://github.com/fpgasystems/Coyote) in combination with AMD GPUs.

```yaml
rocm_device_group: "render"
```
The Linux group that is allowed to use the GPU devices. Change it to whatever Linux group you want to give these permissions. If you want to use a network group, then use the gid of this network group. During boot it is not assured that the name of a network group can be found and then the GPUs will be assigned to the root group instead. You find the gid of the network group using `getent group <name of network group>`.


Dependencies
------------

none

Example Playbook
----------------

```yaml
    - hosts: servers

      roles:
        - role: fpga_systems.hacc.rocm
          vars:
            rocm_amdgpu_kernel_version: "6.3.3"
            rocm_versions:
              - "6.3.3"
              - "7.1.0"
            rocm_device_group: "gpu_developers"
```

License
-------

MIT

Author Information
------------------

This role was created in 2025 by [Geert Roks](https://github.com/GeertRoks), maintainer for Heterogeneous Accelerated Compute Cluster (HACC) at the ETH Zürich, Systems Group.
