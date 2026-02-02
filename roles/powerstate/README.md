Powerstate
========

This role allows to control the power state of the system. Used to turn on and off the machine, or reboot it using Warm or Cold boots (ie. regular reboot or power cycle).

Requirements
------------

All except commands, except for `WarmBoot`, rely on having full "lights-out" remote control over the system. This is often available for servers through a Board Management Controller (BMC), often also referred to as IPMI or IDRAC. The RedFish API can talk to many BMCs and is used in this role to turn the server on or shutdown the server when the OS is non-responsive.

Role Variables
--------------

```yaml
powerstate_command: "TurnOn"
```
The state of the system that you want to achieve. By default "TurnOn". Supported options:
    -   `TurnOn`: Turn the system on
    -   `Shutdown`: Shutdown the system
    -   `WarmBoot`: A regular reboot
    -   `ColdBoot`: A reboot that fully shuts down first before starting up again. This resets FPGAs to their default fabric/shell.

```yaml
powerstate_bmc_vendor: ""
```
A captilized name indicating the vendor of the sever/BMC. Currently supported: `Dell` and `Supermicro`.

```yaml
powerstate_bmc_url: ""
powerstate_bmc_username: ""
powerstate_bmc_password: ""
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
        - role: fpga_systems.hacc.powerstate
          vars:
            powerstate_command: "ColdBoot"
            powerstate_bmc_vendor: "Dell"
            powerstate_bmc_url: "http://bmc.example.com"
            powerstate_bmc_username: "{{ vault_bmc_username }}"
            powerstate_bmc_password: "{{ vault_bmc_password }}"
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
