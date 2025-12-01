#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
import re

def read_hosts(path):
    try:
        with open(path, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        return []

def write_hosts(path, lines):
    with open(path, "w") as f:
        f.writelines(lines)

def main():
    module = AnsibleModule(
        argument_spec=dict(
            path=dict(type="str", default="/etc/hosts"),
            ip=dict(type="str", required=True),
            names=dict(type="list", elements="str", required=True),
            state=dict(type="str", choices=["append", "exact"], default="append"),
            backup=dict(type="bool", default=False),
        ),
        supports_check_mode=True
    )

    path = module.params["path"]
    ip = module.params["ip"]
    names = module.params["names"]
    state = module.params["state"]

    new_line = None
    changed = False

    ip_no_mask = ip.split("/")[0]  # allow CIDR but match plain IP

    lines = read_hosts(path)
    new_lines = []
    found = False

    pattern = re.compile(rf"^{re.escape(ip_no_mask)}\s+")

    for line in lines:
        if pattern.match(line):
            found = True
            existing_names = line.strip().split()[1:]

            if state == "append":
                merged = sorted(set(existing_names + names))
            else:  # state == "exact"
                merged = sorted(set(names))

            new_line = f"{ip_no_mask} {' '.join(merged)}\n"

            if new_line != line:
                changed = True
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    # If IP not found — append new line at bottom
    if not found:
        new_line = f"{ip_no_mask} {' '.join(names)}\n"
        new_lines.append(new_line)
        changed = True

    if changed and not module.check_mode:
        if module.params["backup"]:
            module.backup_local(path)
        write_hosts(path, new_lines)

    module.exit_json(changed=changed, line=new_line)

if __name__ == "__main__":
    main()
