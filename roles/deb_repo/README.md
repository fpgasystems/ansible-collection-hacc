Selfhosted Ubuntu Package Repository
====================================

Setup an Ubuntu .deb package repository server in a docker container for hosting packages that are not yet available in anyother package repository. It is intended as a local repository mainly for hosting of packages that are restricted by an NDA (e.g. the Xilinx/AMD XRT development packages). By hosting these packages you can install them using `apt` on your local servers when you set them up.

> [!NOTE]
> This currenlty only supports a flat repo. In the future supporting the standard repo layout would be interesting, but not needed at this point. It being a flat repo, it means that it does not support the deb822 format, thus not supporting the `deb822_repository` ansible module.

> [!WARNING]
> It is not recommended to make this repository public.


Requirements
------------

To use the local package repo, you need to add the repo to the apt lists of the machine you want to install the packages on.

Using Ansible without key checking

```yaml
- name: Add local ubuntu package repo to apt
  ansible.builtin.lineinfile:
    path: "/etc/apt/sources.list.d/deb-repo.list"
    line: 'deb [trusted=yes] http://<repo-ip-or-url>:{{ deb_repo_server_port }} ./'
    regexp: '^deb.*http://<repo-ip-or-url>:{{ deb_repo_server_port }}.*'
```

TODO: also support gpg key signing and checking

Role Variables
--------------

```yaml
deb_repo_install_path: /root/deb-repo
deb_repo_packages_path: /root/debs
```
The `deb_repo_install_path` is the project path where the docker files are stored on the remote server. The `deb_repo_packages_path` is the path on the remote server, where you manually put the .deb packages that need to be hosted by the repository.

```yaml
deb_repo_server_port: "8080"
```
The port on the host server, where the pacakge repository is reachable

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
        - role: fpga_systems.hacc.deb_repo
          vars:
            deb_repo_server_port: "9000"
            deb_repo_packages_path: /opt/packages
```

License
-------

MIT

Author Information
------------------

This role was created in 2025 by [Geert Roks](https://github.com/GeertRoks), maintainer for Heterogeneous Accelerated Compute Cluster (HACC) at the ETH Zürich, Systems Group.
