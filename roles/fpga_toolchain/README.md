AMD FPGA Toolchain
=========

Installs the toolchain needed for development with AMD adaptive platforms (Alveo and Versal). The toolchain mainly consists of Vivado and Vitis. Note that this role is designed for deployment of adaptive platforms in data center environments, not for embedded applications.

Requirements
------------

Due to restrictive export protection policies, AMD does not support the programmatically downloading of tools. Therefore the files should be downloaded manually from the [AMD website](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vitis.html) and put in the `amd_fpga_toolchain_download_path` directory.

The files should be organized in directories by release name. For example:

```
/opt/amd/downloads/
├── 2024.2/
│   ├── FPGAs_AdaptiveSoCs_Unified_2024.2_1113_1001.tar
│   └── FPGAs_AdaptiveSoCs_Unified_2024.2_1113_1001_Lin64.bin
└── 2024.1/
    ├── FPGAs_AdaptiveSoCs_Unified_2024.1_0522_2023.tar.gz
    ├── FPGAs_AdaptiveSoCs_Unified_2024.1_0522_2023_Lin64.bin
    ├── Vivado_Vitis_Update_2024.1.1_0614_1525.tar.gz
    └── Vivado_Vitis_Update_2024.1.2_0906_0624.tar.gz
```
The root of this directory (`/opt/amd/downloads`) can be changed using the `amd_fpga_toolchain_download_path` variable as explained below.

##### Instructions for downloading toolchain installation files
1) Go to the [AMD website](https://www.xilinx.com/support/download/index.html/content/xilinx/en/downloadNav/vitis.html)
2) Select 'Vitis (SW Developer)' in the ribbon bar
3) Select the release you want (older versions are under the 'Vitis Archive' option)
4) Scroll down to find the `update_level` you want. The initial release is referred to as `base` in this role and is generally recommended.
5) Select the `install_method`, the BIN file for the installer and the SFD (Single File Download) for the archive.

Role Variables
--------------

This role uses both `defaults` and `vars`. The `defaults` are variables that the user should change to their desires. The `vars` store a dictionary of the various package/archive names for the AMD tools (Vivado, Vitis, Runtime, etc.).

### Package variables

The role will automatically include the correct package names from the `vars` folder, based on the `ansible_distribution` and `ansible_distribution_version` global variables. This loads the `amd_fpga_toolchain_packages` dictionary with all information needed for the target distribution. It is best to leave the values in this dictionary as is.

### User variables

Below are the available variables for the user with their default values. These are defined in `defaults/main.yml`.

#### General

```yaml
amd_fpga_toolchain_releases: []
```
The releases that need to be installed by the role are defined in a list in the `amd_fpga_toolchain_releases` variable. By default the list is empty, which will not install any release. The user should define a desired release in this list. Each item in the list represents a release.

```yaml
amd_fpga_toolchain_releases:
  - release: ""                   # (required) String with format YYYY.X indicating AMD tools/runtime release
                                  #            where YYYY is a 4 digit year and X is a number, eg. 2024.2

    state: present                # options: present, absent
    install_method: archive       # options: archive, installer
    update_level: base            # options: base, update1, update2
    vivado_only: False            # options: False, True

```
Each item in the list is an release object, providing multiple options per release. The `release` attribute is the only **required** attribute. The rest have sane defaults. There are several option subsections in this object, for different parts of the installation.

The other attributes are options for the installation of the specific release of the AMD Toolchain (Vivado and Vitis).
- `state` indicates if the specific release should have the toolchain installed.
- `install_method` refers to how the tools installation file is provided, either via an archive or installer. See [download instructions](#Instructions_for_downloading_toolchain_installation_files).
- `update_level` indicates which version (if there are multiple) of the release you want to install, where `base` is the initial release of the Toolchain and always a safe bet.
- `vivado_only` is a boolean indicating if only Vivado should be installed (True) or if alongside Vivado also Vitis should be installed (False).

The attributes `install_method`, `update_level` and `vivado_only` are irrelevant when `state: absent`.

```yaml
amd_fpga_toolchain_releases:
  - "2024.1"
```
A list item of just a string, will be interpreted as the release string with all other options set to the default.

```yaml
amd_fpga_toolchain_download_path: /opt/amd/downloads
```
This is the path where Ansible will look for downloaded assets from the AMD website, like the Toolchain install archive or installer, and the Runtime installers. As mentioned in [the requirements section](#Requirements), this directory needs to be populated with the installation files of the release that need to be installed by this role.

> TODO: if the file has not been found in the release dir, Ansible should also check if it is just in the root of the downloads path as fallback.

#### Tools
```yaml
amd_fpga_toolchain_install_path: /tools/amd
```
The location where the AMD toolchain is installed

```yaml
amd_fpga_toolchain_set_bash_environment_variables: True
```
Boolean that sets whether the installed tools should be loaded into the bash environment variables, so that they are immediately available. When set to False, the user should load the tools by themselves or run the program from the installation location. This option is set to False when there are more than one release is provided to the `amd_fpga_toolchain_releases` list.

```yaml
amd_fpga_toolchain_uninstall_dangling_releases: False
```
Boolean that defines whether the role should look for other installed tool releases and delete them. The tools are 'dangling' when they are not defined in the `amd_fpga_toolchain_releases` list, but are installed in the `amd_fpga_toolchain_install_path`.

```yaml
amd_fpga_toolchain_skip_disk_space_check: False
```
Boolean that defines whether the disk space check should be skipped. The disk space check does a conservative estimate of required disk space: 300GB/release for Vitis+Vivado, 100GB/release for Vivado only.

```yaml
amd_fpga_toolchain_enable_desktop_icons: False
```
Boolean that defines whether desktop icons should be created of the installed tools (**Not yet implemented**)

```yaml
amd_fpga_toolchain_license_servers: []
```
List containing the FlexNet license servers. The format of a license server is `<port>@<server>`, where the default port for AMD is `2100`. These values will be put in the [`XILINXD_LICENSE_FILE` environment variable](https://docs.amd.com/r/en-US/ug973-vivado-release-notes-install-license/Serve-Client-Machines-Pointing-to-a-Floating-License).

```yaml
amd_fpga_toolchain_enable_jtag: false
amd_fpga_toolchain_jtag_group: "fpga-jtag"
```
Settings for setting up the JTAG udev rules. This can be enabled or disabled. The jtag group is the linux group that has the priviledges to use the jtag.

```yaml
amd_user_email: null
amd_user_password: null
```
When `install_method` is set to installer for any release, these variables then need to be set with the email address and password of the users AMD account. This is needed to create an access token for the installer.

Dependencies
------------

None

Example Playbook
----------------

```yaml
    - hosts: servers
      vars_files:
        - vars/amd_fpga_toolchain.yml
      roles:
         - { role: fpga_systems.amd_fpga_toolchain }
```
Inside `vars/amd_fpga_toolchain.yml`
```yaml
amd_fpga_toolchain_releases:
  - "2025.1"
  - release: "2024.2"
  - release: "2024.1"
    vivado_only: true
  - release: "2022.2"
    state: absent
```
This setup installs both 2025.1 and 2024.2 fully with Vivado and Vitis. It only installs Vivado for release 2024.1 and makes sure release 2022.2 is not installed at all.

License
-------

MIT

Author Information
------------------

This role was created in 2025 by [Geert Roks](https://github.com/GeertRoks), maintainer of Heterogeneous Accelerated Compute Cluster (HACC) at the ETH Zürich, Systems Group.
