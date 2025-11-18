Flexnet Licensing Server
=========

Setup a Flexera Flexnet licensing server in a docker container. It is mainly targeted for the Xilinx license server, but it would probably be usable for other vendors, reach out if you need another license server supported.


Requirements
------------

This role expects the license files are already on the target server in the `flexnet_licenses_path` directory. Additionally the lisence server needs to be copied over to the server. The Xilinx flexnet license server can be downloaded from [the AMD download page](https://www.xilinx.com/support/download/) (Go to the 'Vivado (HW developer)' tab -> download the 'Floating server tools Linux' from the License Management Tools section).

Role Variables
--------------

```yaml
flexnet_hostname: ""
flexnet_container_name: flexnet-license-server
```
The `flexnet_hostname` sets the hostname of the container. This is required and needs to match with the hostname defined in the license files. `flexnet_container_name` is the name of the container and can be set to your liking.

```yaml
flexnet_install_path: /root/flexnet-license-server
flexnet_licenses_path: /root/licenses
```
The install path allows you to define a location where the docker files are put. The `flexnet_licenses_path` is the directory where you put the license files manually on the server. The role will copy them to the install path to serve them. So if you want to add new licenses, just add them to the licenses path and rerun this role to set everything up.

```yaml
flexnet_server_file_path: /root
flexnet_server_file: "linux__flexm_v11.17.2.0.zip"
```
The `flexnet_server_file_path` is the directory where the `flexnet_server_file` is stored. This file needs to be downloaded from the vendor website and added to the server manually to the defined directory.

```yaml
flexnet_vendor_name: xilinxd
flexnet_vendor_port: "2200"
```
The `flexnet_vendor_name` is the name of the vendor as defined in the license file. The `flexnet_vendor_port` is the port you assign to this vendor, which is (as far as I understand) a personal choice and arbitrary.

Dependencies
------------

The role has two dependencies:

`geerlingguy.pip`: This is needed to install the docker pip package to build the docker image

`geerlingguy.docker`: This is needed to install docker on the server to run the docker container

Example Playbook
----------------

```yaml
    - hosts: servers

      roles:
        - role: fpga_systems.hacc.flexnet
          vars:
            flexnet_hostname: "license-server.example.com"
```

License
-------

MIT

Author Information
------------------

This role was created in 2025 by [Geert Roks](https://github.com/GeertRoks), maintainer for Heterogeneous Accelerated Compute Cluster (HACC) at the ETH Zürich, Systems Group.
