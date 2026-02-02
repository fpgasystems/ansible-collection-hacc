Coldboot
========

A cold boot removes the power fully from a system before starting the system back up. This often resets more then doing a regular `reboot` which are also called 'Warm boot'. This is especially useful for FPGA development to reset an FPGA back to its default fabric/shell.

Requirements
------------

To use this coldboot role you need remote "full-lights-out" control over the node. This is often available for servers through a Board Management Controller (BMC), often also referred to as IPMI or IDRAC. The RedFish API can talk to many BMCs and is used in this role to turn the server on or shutdown the server when the OS is non-responsive.


Role Variables
--------------

```yaml
coldboot_bmc_vendor: ""
```
A captilized name indicating the vendor of the sever/BMC. Currently supported: `Dell` and `Supermicro`.

```yaml
coldboot_bmc_url: ""
coldboot_bmc_username: ""
coldboot_bmc_password: ""
```
The url or ip of the BMC management port and the credentials to login. The credentials should be for an account that can change the power state of the server.

Dependencies
------------

None

Example Playbook
----------------

```yaml
    - hosts: servers

      roles:
        - role: fpga_systems.hacc.coldboot
          vars:
            coldboot_bmc_vendor: "Dell"
            coldboot_bmc_url: "http://bmc.example.com"
            coldboot_bmc_username: "{{ vault_bmc_username }}"
            coldboot_bmc_password: "{{ vault_bmc_password }}"
```

It is recommended to store BMC credentials safely using Ansible Vault
```yaml
vault_bmc_username: "root"
vault_bmc_password: "Password123"
```

License
-------

MIT

Author Information
------------------

This role was created in 2025 by [Geert Roks](https://github.com/GeertRoks), maintainer for Heterogeneous Accelerated Compute Cluster (HACC) at the ETH Zürich, Systems Group.
