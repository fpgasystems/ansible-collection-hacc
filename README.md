# Ansible Collection - fpga_systems.hacc
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Collection of roles to manage serers that contain AMD FPGAs and GPUs. These roles are developed and used for the HACC cluster at ETH Zürich. Feel free to use the collection for your own heterogeneous compute setups.

___

## Collection Overview

This Ansible collection provides modules, roles, and plugins to manage FPGAs and GPUs for a multi user server setup.

#### Roles:
  - [`fpga_toolchain`](roles/fpga_toolchain) - Manages installation of Vivado and Vitis
  - [`aved`](roles/aved) - Alveo Versal Example Design for Versal V80 FPGAs
  - [`xrt`](roles/xrt) - Xilinx RunTime for Alveo FPGAs and Versal VCK5000
  - [`rocm`](roles/rocm) - GPU runtime runtime for AMD GPUs
  - [`hdev`](roles/hdev) - HACC Development custom wrapper tool for easy user interactions
  - [`flexnet`](roles/flexnet) - Docker container for Xilinx/AMD License server
  - [`deb_repo`](roles/deb_repo) - Docker container for hosting a custom package repository

## Installation

#### Using Git submodule
This adds the collection as a git submodule locally to your Ansible project.
```
cd </path/to/project>
mkdir -p collections/ansible_collections/fpga_systems/hacc
git submodule add https://github.com/fpgasystems/ansible-collection-hacc.git collections/ansible_collections/fpga_systems/hacc
```

You can select a specific release or commit of the collection in the submodule.
```
cd collections/ansible_collections/fpga_systems/hacc
git switch --detach <tag-name>
```

Then commit the use of this tag to your main Ansible project git repo to save this state.
```
cd </path/to/project>
git add collections/ansible_collections/fpga_systems/hacc
git commit
```

If you want to clone your ansible project from a remote source (GitHub, GitLab etc), then you need to also have git pull the submodules.
```
git clone <url-of-your-ansible-project-git-repo>
git submodule update --init --recursive
```
or do it all in one step using the following
```
git clone --recurse-submodules <url-of-your-ansible-project-git-repo>
```

Read more about git submodules if you are unfamiliar with this git feature: https://git-scm.com/book/en/v2/Git-Tools-Submodules

#### Using Ansible Galaxy
This adds the collection globaly to the system (only the latest commit on 'main').
```
ansible-galaxy collection install git+https://github.com/fpgasystems/ansible-collection-hacc.git
```

## Supported Platforms
The collection is heavily tested for targets running Ubuntu Server 22.04

## Contributing

Contributions are welcome! Feel free to open an issue or create a Pull Request.
