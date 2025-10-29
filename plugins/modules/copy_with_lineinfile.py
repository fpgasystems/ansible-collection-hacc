
from ansible.module_utils.basic import AnsibleModule
import os
import re
import tempfile
import shutil
import pwd
import grp

def apply_lineinfile_logic(content, regexp, line):
    """
    Emulate Ansible's lineinfile:
    - If a line matches 'regexp', replace the full line with 'line'
    - If no line matches, append 'line' at the end
    """
    if not regexp or not line:
        return content

    lines = content.splitlines()
    new_lines = []
    matched = False
    pattern = re.compile(regexp)

    for l in lines:
        if pattern.search(l):
            new_lines.append(line)
            matched = True
        else:
            new_lines.append(l)

    if not matched:
        new_lines.append(line)

    return "\n".join(new_lines) + "\n"

def main():
    module = AnsibleModule(
        argument_spec=dict(
            src=dict(type='path', required=True),
            dest=dict(type='path', required=True),
            regexp=dict(type='str', required=False, default=None),
            line=dict(type='str', required=False, default=None),
            owner=dict(type='str', required=False),
            group=dict(type='str', required=False),
            mode=dict(type='str', required=False),
        ),
        supports_check_mode=True
    )

    src = module.params['src']
    dest = module.params['dest']
    regexp = module.params['regexp']
    line = module.params['line']
    owner = module.params['owner']
    group = module.params['group']
    mode = module.params['mode']

    # --- Handle source file ---
    local_src = None
    tmp_src = None

    # File should already exist on the target
    if not os.path.exists(src):
        module.fail_json(msg=f"Source file not found on target: {src}")
    local_src = src

    # --- Read source file content ---
    try:
        with open(local_src, 'r', encoding='utf-8') as f:
            src_content = f.read()
    except Exception as e:
        module.fail_json(msg=f"Unable to read source file: {e}")

    # --- Apply lineinfile modification ---
    new_content = apply_lineinfile_logic(src_content, regexp, line)

    # --- Compare with destination ---
    changed = False
    if os.path.exists(dest):
        try:
            with open(dest, 'r', encoding='utf-8') as f:
                dest_content = f.read()
            if dest_content != new_content:
                changed = True
        except Exception as e:
            module.fail_json(msg=f"Unable to read destination file: {e}")
    else:
        changed = True

    # --- Write new content if changed ---
    if changed and not module.check_mode:
        os.makedirs(os.path.dirname(dest), exist_ok=True)

        fd, tmp_path = tempfile.mkstemp(dir=os.path.dirname(dest))
        os.close(fd)
        try:
            with open(tmp_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            shutil.move(tmp_path, dest)
        except Exception as e:
            module.fail_json(msg=f"Unable to write destination file: {e}")
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

        # Set ownership and permissions
        if owner or group:
            uid = pwd.getpwnam(owner).pw_uid if owner else -1
            gid = grp.getgrnam(group).gr_gid if group else -1
            os.chown(dest, uid, gid)
        if mode:
            os.chmod(dest, int(mode, 8))

    module.exit_json(changed=changed, msg="File updated" if changed else "File unchanged")


if __name__ == '__main__':
    main()

