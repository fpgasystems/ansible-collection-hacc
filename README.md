AMD Adaptive Platforms Management
=========

A brief description of the role goes here.
Installs the necessary programs needed for development with AMD adaptive platforms (Alveo and Versal). Note that this role is designed for deployment of adaptive platforms in data center environments, not for embedded applications.

Requirements
------------

Due to restrictive export protection policies, AMD does not support the programmatically downloading of tools. Therefore the files should be downloaded manually from the [AMD website](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vitis.html) and put in the `amd_apm_download_path` directory.

The files should be organized in directories by release name. For example:

```
/opt/amd/downloads/
├── 2024.2/
│   ├── FPGAs_AdaptiveSoCs_Unified_2024.2_1113_1001.tar
│   ├── FPGAs_AdaptiveSoCs_Unified_2024.2_1113_1001_Lin64.bin
│   └── xrt_202420.2.18.179_22.04-amd64-xrt.deb
└── 2024.1/
    ├── FPGAs_AdaptiveSoCs_Unified_2024.1_0522_2023.tar.gz
    ├── FPGAs_AdaptiveSoCs_Unified_2024.1_0522_2023_Lin64.bin
    ├── Vivado_Vitis_Update_2024.1.1_0614_1525.tar.gz
    ├── Vivado_Vitis_Update_2024.1.2_0906_0624.tar.gz
    └── xrt_202410.2.17.319_22.04-amd64-xrt.deb
```
The root of this directory (`/opt/amd/downloads`) can be changed using the `amd_apm_download_path` variable as explained below.

##### Instructions for downloading toolchain installation files
1) Go to the [AMD website](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vitis.html)
2) Select 'Vitis (SW Developer)' in the ribbon bar
3) Select the release you want (older versions are under the 'Vitis Archive' option)
4) Scroll down to find the `update_level` you want. The initial release is called `base` in this role and is generally recommended.
5) Select the `install_method`, the BIN file for the installer and the SFD (Single File Download) for the archive.

##### Instructions for downloading XRT installation files
1) Go to the [AMD website](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vitis.html)
2) Select the 'Alveo Packages' drop down menu
3) Select the 'U55C' item (Even if you don't have an U55C, it is safe to do this, as each item will have the same XRT install files)
4) Select 'Vitis Design Flow' in the ribbon bar
5) Select your target distribution from the list (click on 'Previous Versions' if you want the files of an older release)
6) From the drop down menu select the download button for the 'Xilinx Runtime'

##### Instructions for downloading device installation files
1) Go to the [AMD website](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vitis.html)
2) Select the 'Alveo Packages' drop down menu
3) Select the item for your target platform
4) Select 'Vitis Design Flow' in the ribbon bar
5) Select your target distribution from the list (click on 'Previous Versions' if you want the files of an older release)
6) From the drop down menu select the download button for the 'Deployment Target Platform' and/or 'Development Target Platform'

Role Variables
--------------

This role uses both `defaults` and `vars`. The `defaults` are variables that the user should change to their desires. The `vars` store a dictionary of the various package/archive names for the AMD tools (Vivado, Vitis, Runtime, etc.).

### Package variables

The role will automatically include the correct package names from the `vars` folder, based on the `ansible_distribution` and `ansible_distribution_version` global variables. This loads the `amd_apm_packages` dictionary with all information needed for the target distribution. It is best to leave the values in this dictionary as is.

### User variables

Below are the available variables for the user with their default values. These are defined in `defaults/main.yml`.

#### General

```yaml
amd_apm_releases: []
```
The releases that need to be installed by the role are defined in a list in the `amd_apm_releases` variable. By default the list is empty, which will not install any release. The user should define a desired release in this list. Each item in the list represents a release.

```yaml
amd_apm_releases:
  - release: ""                     # (required) String with format YYYY.X indicating AMD tools/runtime release
                                    #            where YYYY is a 4 digit year and X is a number, eg. 2024.2

    tools:                          # Subsection with options related to Tools installation
      state: present                  # options: present, absent
      install_method: archive         # options: archive, installer
      update_level: base              # options: base, update1, update2
      vivado_only: False              # options: False, True

    runtime:                        # Subsection with options related to Runtime installation
      state: present                  # options: absent, present
      type: xrt                       # options: xrt, aved

```
Each item in the list is an release object, providing multiple options per release. The `release` attribute is the only **required** attribute. The rest have sane defaults. There are several option subsections in this object, for different parts of the installation.

The `tools` subsection contains options for the installation of the AMD Toolchain (Vivado and Vitis).
- `state` indicates if the specific release should have the toolchain installed.
- `install_method` refers to how the tools installation file is provided, either via an archive or installer. See [download instructions](#Instructions_for_downloading_toolchain_installation_files).
- `update_level` indicates which version (if there are multiple) of the release you want to install, where `base` is the initial release of the Toolchain and always a safe bet.
- `vivado_only` is a boolean indicating if only Vivado should be installed (True) or if alongside Vivado also Vitis should be installed (False).

The attributes `install_method`, `update_level` and `vivado_only` are irrelevant when `state: absent`.


The `runtime` subsection contains options for the installation of the AMD Runtime (XRT, AVED).
- `state` indicates if the specific release should have the runtime installed.
- `type` indicates which runtime needs to be installed (**Not yet implemented**)

```yaml
amd_apm_releases:
  - "2024.1"
```
A list item of just a string, will be interpreted as the release string with all other options set to the default.

```yaml
amd_apm_download_path: /opt/amd/downloads
```
This is the path where Ansible will look for downloaded assets from the AMD website, like the Toolchain install archive or installer, and the Runtime installers. As mentioned in [the requirements section](#Requirements), this directory needs to be populated with the installation files of the release that need to be installed by this role.

> TODO: if the file has not been found in the release dir, Ansible should also check if it is just in the root of the downloads path as fallback.

```yaml
amd_apm_devices: []
```
A list of strings indicating which AMD adaptive platforms are installed in the target machine. Supported options: `"v80"`,`"vck5000"`, `"u55c"`, `"u50d"`, `"u280"`, `"u250"`. Due to incompatibility of the V80 with other adaptive platforms, this option is mutually exclusive with all other options. (TODO: find reference for this)

#### Tools
```yaml
amd_apm_tools_install_path: /tools/amd
```
The location where the AMD toolchain is installed

```yaml
amd_apm_tools_set_bash_environment_variables: True
```
Boolean that sets whether the installed tools should be loaded into the bash environment variables, so that they are immediately available. When set to False, the user should load the tools by themselves or run the program from the installation location. This option is set to False when there are more than one release is provided to the `amd_apm_releases` list.

```yaml
amd_apm_tools_uninstall_dangling_releases: False
```
Boolean that defines whether the role should look for other installed tool releases and delete them. The tools are 'dangling' when they are not defined in the `amd_apm_releases` list, but are installed in the `amd_apm_tools_install_path`.

```yaml
amd_apm_tools_skip_disk_space_check: False
```
Boolean that defines whether the disk space check should be skipped. The disk space check does a conservative estimate of required disk space: 300GB/release for Vitis+Vivado, 100GB/release for Vivado only.

```yaml
amd_apm_tools_enable_desktop_icons: False
```
Boolean that defines whether desktop icons should be created of the installed tools (**Not yet implemented**)

```yaml
amd_apm_user_email: null
amd_apm_user_password: null
```
When `install_method` is set to installer for any release, these variables then need to be set with the email address and password of the users AMD account. This is needed to create an access token for the installer.

#### Runtime
```yaml
amd_apm_runtime_install_path: /opt/amd
```
The location where the AMD Runtime is installed. XRT is installed in `{{ amd_apm_runtime_install_path }}/xrt` and AVED is installed in `{{ amd_apm_runtime_install_path }}/aved`.

```yaml
amd_apm_runtime_set_bash_environment_variables: True
```
Boolean that sets whether the installed runtime should be loaded into the bash environment variables, so that they are immediately available. When set to False, the user should load the runtime by themselves or run the program from the installation location. This option is set to False when there are more than one release is provided to the `amd_apm_releases` list.

```yaml
amd_apm_runtime_uninstall_dangling_releases: False
```
Boolean that defines whether the role should look for other installed runtime releases and delete them. The runtime is 'dangling' when it is not defined in the `amd_apm_releases` list, but is installed in the `amd_apm_runtime_install_path`.

Dependencies
------------

None

Example Playbook
----------------

```yaml
    - hosts: servers
      vars_files:
        - vars/amd_apm.yml
      roles:
         - { role: fpga_systems.amd_adaptive_platform_management }
```
Inside `vars/amd_apm.yml`
```yaml
amd_apm_releases:
  - "2025.1"
  - release: "2024.2"
  - release: "2024.1"
    tools:
      vivado_only: true
  - release: "2023.2"
    runtime:
      state: absent
  - release: "2022.2"
    tools:
      state: absent
    runtime:
      state: absent
```

License
-------

MIT

Author Information
------------------

This role was created in 2025 by [Geert Roks](https://github.com/GeertRoks), maintainer of Heterogeneous Accelerated Compute Cluster (HACC) at the ETH Zürich, Systems Group.
