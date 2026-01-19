from ansible.module_utils.basic import AnsibleModule
import os
import re


RELEASE_RE = re.compile(r"(\d{4}\.\d)")
VIVADO_RE = re.compile(r"Vivado")
VITIS_RE = re.compile(r"Vitis_HLS")


def find_installed_releases(base_path):
    vivado = set()
    vitis = set()
    err = set()

    # If the base_path does not exist, then nothing is installed
    if not os.path.isdir(base_path):
        return vivado, vitis, err

    # releases of 2025.1 and newer
    dirs = [
        name
        for name in os.listdir(base_path)
        if os.path.isdir(os.path.join(base_path, name)) and RELEASE_RE.search(name)
    ]
    VIVADO_RE = re.compile(r"Vivado")
    VITIS_RE = re.compile(r"Vitis_HLS")
    for d in dirs:
        first_level_dir = os.path.join(base_path, d)
        r_dirs = [
            name
            for name in os.listdir(first_level_dir)
            if os.path.isdir(os.path.join(first_level_dir, name))
        ]
        for di in r_dirs:
            match_release_vitis = VITIS_RE.search(di)
            match_release_vivado = VIVADO_RE.search(di)
            if match_release_vitis:
                vitis.add(d)
                continue
            elif match_release_vivado:
                vivado.add(d)
                continue
            else:
                continue

    # releases of 2024.2 and older
    xinstall_path = os.path.join(base_path, ".xinstall")
    dirs_xinstall = [
        name
        for name in os.listdir(xinstall_path)
        if os.path.isdir(os.path.join(xinstall_path, name))
    ]
    VIVADO_RE = re.compile(r"Vivado_(\d{4}\.\d)")
    VITIS_RE = re.compile(r"Vitis_(\d{4}\.\d)")
    for di in dirs_xinstall:
        match_vitis = VITIS_RE.search(di)
        match_vivado = VIVADO_RE.search(di)
        if not match_vitis and not match_vivado:
            continue
        release = di.split("_")[1]
        if match_vitis:
            vitis.add(release)
        elif match_vivado:
            vivado.add(release)

    # Report the releases that seem to be of both vitis and vivado
    err = vivado.intersection(vitis)
    for r in err:
        vitis.remove(r)
        vivado.remove(r)

    return vivado, vitis, err

def normalize_releases(releases):
    normalized = []
    for r in releases:
        item = dict(r)
        item.setdefault("state", "present")
        item.setdefault("vivado_only", False)
        normalized.append(item)
    return normalized


def main():
    module = AnsibleModule(
        argument_spec=dict(
            install_path=dict(type="path", required=True),
            releases=dict(type="list", elements="dict", required=True),
            uninstall_dangling=dict(type="bool", default=False),
        ),
        supports_check_mode=True,
    )

    install_path = module.params["install_path"]
    wanted = normalize_releases(module.params["releases"])
    uninstall_dangling = module.params["uninstall_dangling"]

    vivado_present, vitis_present, currently_invalid = find_installed_releases(install_path)

    wanted_releases = {r["release"] for r in wanted}

    install = []
    uninstall = []
    reinstall = []
    correct = []

    for r in wanted:
        rel = r["release"]
        state = r["state"]
        vivado_only = r["vivado_only"]

        is_vivado_only = rel in vivado_present
        is_vitis = rel in vitis_present

        if state == "absent":
            if is_vivado_only or is_vitis:
                uninstall.append(rel)
            continue

        # state == present
        if not is_vivado_only and not is_vitis:
            install.append(rel)
            continue

        if vivado_only:
            if is_vitis:
                reinstall.append(rel)
            else:
                correct.append(rel)
        else:
            if is_vitis:
                correct.append(rel)
            else:
                reinstall.append(rel)

    # reinstall = uninstall + install
    install.extend(reinstall)
    uninstall.extend(reinstall)

    # also remove currently invalid installed versions
    uninstall.extend(currently_invalid)

    dangling = (vivado_present | vitis_present) - wanted_releases
    if uninstall_dangling:
        uninstall.extend(sorted(dangling))
    else:
        correct.extend(sorted(dangling))

    # de-dup
    install = sorted(set(install))
    uninstall = sorted(set(uninstall))
    reinstall = sorted(set(reinstall))
    correct = sorted(set(correct))

    result = dict(
        changed=False,
        current_state=dict(
            vivado=sorted(vivado_present),
            vitis=sorted(vitis_present),
            invalid=sorted(currently_invalid),
        ),
        install=install,
        uninstall=uninstall,
        reinstall=reinstall,
        correct=correct,
    )

    module.exit_json(**result)


if __name__ == "__main__":
    main()
