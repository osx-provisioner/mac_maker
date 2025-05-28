# -*- mode: python ; coding: utf-8 -*-

import ansible
import os
import pkg_resources
import site
import sys

from PyInstaller.utils.hooks import exec_statement

block_cipher = None

certificates = exec_statement("""
    import ssl
    print(ssl.get_default_verify_paths().cafile)
""").strip().split()

cert_datas = [(f, 'lib') for f in certificates]

a = Analysis(
    ["entrypoint.py"],
    binaries=[
        (
            os.path.join(os.path.dirname(sys.executable)),
            "bin",
        )

    ],
    cipher=block_cipher,
    datas=[
        (
            os.path.join(site.getsitepackages()[0], "ansible"),
            "ansible",
        ),
        (
            os.path.join(site.getsitepackages()[0], "ansible_collections"),
            "ansible_collections",
        ),
        (
            os.path.join(site.getsitepackages()[0], "jsonschema_specifications"),
            "jsonschema_specifications",
        ),
        (
            os.path.join(
                site.getsitepackages()[0],
                f'mac_maker-{pkg_resources.get_distribution("mac_maker").version}.dist-info',
            ),
            f'mac_maker-{pkg_resources.get_distribution("mac_maker").version}.dist-info',
        ),
        (
            "mac_maker",
            "mac_maker",
        ),
    ] + cert_datas,
    excludes=[],
    hiddenimports=[
        "ansible.cli.galaxy",
        "ansible.cli.playbook",
        "ansible.utils.display",
        "configparser",
        "dataclasses",
        "distutils.version",
        "importlib_resources",
        "logging.handlers",
        "jinja2",
        "pty",
        "smtplib",
        "xml.dom",
        "xml.etree.ElementTree",
    ],
    hookspath=[],
    pathex=[],
    runtime_hooks=[],
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(
    pyz,
    a.binaries,
    a.datas,
    a.scripts,
    a.zipfiles,
    debug=False,
    bootloader_ignore_signals=False,
    bundle_identifier='com.mac_maker',
    console=True,
    info_plist={
      'NSPrincipalClass': 'NSApplication',
      'NSAppleScriptEnabled': False,
    },
    name="mac_maker",
)
