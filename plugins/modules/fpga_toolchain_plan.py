from ansible.module_utils.basic import AnsibleModule
import os
import re

def find_installed_releases(base_path):
    vivado = set()
    vitis = set()
    err = set()

    xinstall_path = os.path.join(base_path, ".xinstall")
    release_dirs = [
        name
        for name in os.listdir(xinstall_path)
        if os.path.isdir(os.path.join(xinstall_path, name))
    ]
    VIVADO_RE = re.compile(r"Vivado")
    VITIS_RE = re.compile(r"Vitis")
    for release_dir in release_dirs:
        match_release = re.search(r'(\d{4})\.(\d)', release_dir)

        if not match_release:
            continue

        release_year = int(match_release.group(1))
        release_minor = int(match_release.group(2))
        release = f"{release_year}.{release_minor}"
        release_root_path = os.path.join(xinstall_path, release_dir)

        # releases between 2022.1 and 2024.2
        if release_year >= 2022 and release_year <= 2024:
            match_vitis = VITIS_RE.search(release_dir)
            match_vivado = VIVADO_RE.search(release_dir)

            if not match_vitis and not match_vivado:
                continue

            if match_vitis:
                vitis.add(release)
            elif match_vivado:
                vivado.add(release)

        elif release_year >= 2025:
            with open(os.path.join(release_root_path, "data/instRecord.dat"), "r") as f:
                content = f.read()

            latestInstalledProduct_found = re.findall(
                r"<latestInstalledProduct>(.*?)</latestInstalledProduct>",
                content,
                re.DOTALL
            )

            if not latestInstalledProduct_found:
                module.fail_json(
                    msg=f"Could not determine Vitis or Vivado for {release_dir}",
                    changed=False
                )

            product = latestInstalledProduct_found[-1]

            if VIVADO_RE.search(product):
                vivado.add(release)
            elif VITIS_RE.search(product):
                vitis.add(release)

        else:
            module.fail_json(
                msg=f"Releases from {release_year} are not (yet) supported",
                changed=False
            )

    # Report the releases that seem to be of both vitis and vivado
    err = vivado.intersection(vitis)
    for release in err:
        vitis.remove(release)
        vivado.remove(release)

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
