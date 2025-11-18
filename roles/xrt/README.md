Xilinx RunTime (XRT)
=========

This role installs the Xilinx Runtime (XRT) for Alveo FPGA cards.

Requirements
------------

Due to restrictive export protection policies, AMD does not provide the development files in their official debian packages repository (except for the Development files for the VCK5000). Therefore if you want to install development files using this role, you need to download these yourself from the [AMD website](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vitis.html) and serve them with your own package repository. See TODO for instructions on how to setup this repository. You also have the option to download the XRT and deployment packages that are in the official Xilinx package repo, but instead serve them with your own package repo. This may be a good safeguard if you don't want to rely on the uptime of the servers of AMD/Xilinx.

> NOTE: keep your pacakge repo private and don't share it publicly as long as you don't have explicit permisions of AMD/Xilinx to do so. The development packages are downloaded under an NDA.

##### Instructions for downloading XRT .deb package files
1) Go to the [AMD website](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vitis.html)
2) Select the 'Alveo Packages' drop down menu
3) Select the item for your target platform
4) Select 'Vitis Design Flow' in the ribbon bar
5) Select your target distribution from the list (click on 'Previous Versions' if you want the files of an older release)
6) From the drop down menu select the download button for the 'XRT', 'Deployment Target Platform' and/or 'Development Target Platform' packages.

Role Variables
--------------

This role uses both `defaults` and `vars`. The `defaults` are variables that the user should change to their desires. The `vars` store a dictionary of the various package/archive names for the AMD tools (Vivado, Vitis, Runtime, etc.).

### Package variables

The role will automatically include the correct package names from the `vars` folder, based on the `ansible_distribution` and `ansible_distribution_version` global variables. This loads the `xrt_packages`, `xrt_deployment_packages` and `xrt_development_packages` dictionaries with all information needed for the target distribution. It is best to leave the values in this dictionary as is.

### User variables

Below are the available variables for the user with their default values. These are defined in `defaults/main.yml`.

```yaml
xrt_release: null
```
The XRT release that needs to be installed by this role. This can be defined either by the Vivado release format, eg. `"2024.2"`, or the XRT release format, eg. `"2.18.179"`. Currently there is no option for installing multiple XRT releases side by side.

```yaml
xrt_deployment_targets: true
xrt_development_targets: false
```
These define wheter the role should attempt to install deployment and/or development targets on the remote.

> NOTE: as mentioned in the [requirements section](#Requirements), for development targets to be installed a selfhosted package repo needs to be served with the development packages and this repo needs to be configured on the remote server.

```yaml
xrt_use_official_package_repo: true
```
When set to `true`, then the role will setup apt to use the official AMD/Xilinx repo for the XRT and Deployment packages.

```yaml
xrt_devices: []
```
A list of strings indicating which AMD/Xilinx Alveo platforms are installed in the target machine. Supported options: `"vck5000"`, `"u55c"`, `"u50d"`, `"u280"`, `"u250"`.

```yaml
xrt_set_bash_environment_variables: true
```
Boolean that sets whether the XRT setup script should be added to the bash profile, so that it loads xrt for all users by default.

Dependencies
------------

None

Example Playbook
----------------

```yaml
    - hosts: servers

      roles:
        - role: fpga_systems.hacc.xrt
          vars:
            xrt_release: "2024.2"
            xrt_devices:
              - "u55c"
              - "vck5000"

License
-------

MIT

Author Information
------------------

This role was created in 2025 by [Geert Roks](https://github.com/GeertRoks), maintainer for Heterogeneous Accelerated Compute Cluster (HACC) at the ETH Zürich, Systems Group.
