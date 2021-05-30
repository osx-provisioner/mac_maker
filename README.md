# Project Documentation

## Mac Maker

A portable single binary configuration tool for OSX machines.

- Brings [Ansible](https://www.ansible.com/) powered Configuration Management to your Mac.
- Install all the apps you need, and configure your Mac exactly how you like it.
- Mix and match existing Ansible roles such [asdf](https://github.com/osx-provisioner/role-asdf), [ClamAV](https://github.com/osx-provisioner/role-clamav) and [Homeshick](https://github.com/osx-provisioner/role-homeshick) with the huge array of Mac roles on [Ansible Galaxy](https://galaxy.ansible.com/).

### Master Branch Builds
- GitHub:
  - [![mac_maker Generic Push](https://github.com/osx-provisioner/mac_maker/workflows/mac_maker-push/badge.svg?branch=master)](https://github.com/osx-provisioner/mac_maker/actions)
- TravisCI: 
  - ![TravisCI](https://travis-ci.com/osx-provisioner/mac_maker.svg?branch=master)

### Production Branch Builds
- GitHub:
  - [![mac_maker Generic Push](https://github.com/osx-provisioner/mac_maker/workflows/mac_maker-push/badge.svg?branch=production)](https://github.com/osx-provisioner/mac_maker/actions)
- TravisCI:
  - ![TravisCI](https://travis-ci.com/osx-provisioner/mac_maker.svg?branch=production)

## Quick Start

### How do I use this?

Copy the `mac_maker` binary to the OSX machine you'd like to put under configuration management.
If you have a working internet connection, you can start installing `Mac Maker Profiles`.

### Mac Maker Profiles

Mac Maker uses the concept of "profiles", to bundle together the Ansible configuration required to configure your Mac.

Here's an [example profile](https://github.com/osx-provisioner/profile-example) for you to test out:

1. Start Mac Maker: `./mac_maker`
2. Run the these commands, to check and apply the profile
  - `precheck github https://github.com/osx-provisioner/profile-example`
  - `apply github https://github.com/osx-provisioner/profile-example`

You can work with "profiles" in one of two ways for now:

1) Create a public GitHub Repository that contains your profile, taking care NOT to included privileged content.
2) Create your profile in any private git repository, and clone it to a USB key (or other portable media).  Add a `spec.json` file to the USB stick telling Mac Maker how to find it.

### How do I create a Profile?

Use [this template](https://github.com/osx-provisioner/profile-generator) to create your own custom profiles.


### What's a spec.json file?

A Mac Maker profile has a specific directory structure.  The `spec.json` file lets you mix and match where the directories and files are. 
It's a bit inflexible in certain ways, because it requires absolute paths, but this makes it ideal to work off a USB stick or any portable media.

```json
{
  "workspace_root_path": "The absolute path to the root folder of your cloned profile repository.",
  "profile_data_path": "This absolute path usually points to the `profile` folder inside your profile repository.",
  "galaxy_requirements_file": "This absolute path usually points to the `profile_data_path/requirements.yml` file inside your profile repository.",
  "playbook": "This absolute path usually points to the `profile_data_path/install.yml` file inside your profile repository.",
  "roles_path": [
    "This absolute path usually points to the `profile_data_path/roles` folder inside your profile repository.",
    "You can append several roles directories here, they should all be absolute paths."
  ],
  "inventory": "This absolute path usually points to the `profile_data_path/inventory` file inside your repository."
}
```

Every Mac you bring your USB stick to will end up with the same configuration.

## License

As this project effectively bundles Ansible, it must comply with the [GNU GPL](./LICENSE).
You are however free to use and modify this source, as long as the license's terms are respected.

(Pull requests are most welcome, as I sincerely hope this project can be of use to others.)

## Detailed Documentation

The project's full documentation can be found here:
  - [Mac Maker Documentation](https://mac_maker.readthedocs.io/)

Complete build instructions are included, so you can build your own binary.
