# Project Documentation

## Mac Maker

A portable single binary configuration tool for OSX machines.

- Brings [Ansible](https://www.ansible.com/) powered Configuration Management to your Mac.
- Mix and match existing Ansible roles such [asdf](https://github.com/osx-provisioner/role-asdf), [clamav](https://github.com/osx-provisioner/role-clamav) and [homeshick](https://github.com/osx-provisioner/role-homeshick) with the huge array of Mac roles on [Ansible Galaxy](https://galaxy.ansible.com/).

### Generate a consistent, reproducible "profile" of your machine

- Start with a freshly installed Mac, and apply a `Mac Maker Profile` to add all the customizations and applications you want.
- Alternatively, start with an existing Mac you already use, and incrementally build a `Mac Maker Profile` putting all your existing apps and customizations under version control.

### Master Branch Builds
- GitHub:
  - [![mac_maker Generic Push](https://github.com/osx-provisioner/mac_maker/workflows/mac_maker-push/badge.svg?branch=master)](https://github.com/osx-provisioner/mac_maker/actions)

### Production Branch Builds
- GitHub:
  - [![mac_maker Generic Push](https://github.com/osx-provisioner/mac_maker/workflows/mac_maker-push/badge.svg?branch=production)](https://github.com/osx-provisioner/mac_maker/actions)
- Bitrise:
  - [![bitrise M1 Binaries](https://app.bitrise.io/app/9a06da738bba2e7a/status.svg?token=fngmPo_dY5PcqQ-uCNRnaQ&branch=production)](https://app.bitrise.io/app/9a06da738bba2e7a)

## Quick Start

### How do I use this?

If you'd like to try it out, head over to the [Mac Maker Releases](https://github.com/osx-provisioner/mac_maker/releases) and download a pre-built binary.

- There are builds available for **Catalina**, **Big Sur** and **Monterey** for **Intel Macs**.
- There are now builds for **Monterey** available for **Apple Silicon Macs**.  (Thanks to the folks at [bitrise](https://bitrise.io/))

If you are unsure, use the tables below to help you find the right binary for your Mac:

|Version Number|   OS Name    |
|--------------|--------------|
|12            | Monterey     |
|11            | Big Sur      |
|10            | Catalina     |

|Architecture  |   CPU Type   |
|--------------|--------------|
|arm64         | Apple Silicon|
|x86_64        | Intel        |

**Please Note**:
- They are unsigned, and not notarized by Apple.
- As such, they will trigger a warning about software from an unidentified developer.

### OK, but you still didn't tell me how to get started...

Are you on Monterey?  It may not ship with python anymore!  We better check:
- open a terminal and type `python3`, and if prompted to install the [x-code](https://developer.apple.com/xcode/) cli tools click `install`.
- this is less than ideal, but it gets you into a compatible state quickly

For Catalina, Big Sur and Monterey (once you've confirmed [python](https://python.org) is present):
- Copy the `mac_maker` binary to the OSX machine you'd like to put under configuration management.
- If you have a working internet connection, you can start working with `Mac Maker Profiles`.  
- To try creating your own `Profile`, check out [this](https://github.com/osx-provisioner/profile-generator) repository.
- To learn more about `Mac Maker Profiles`, and to try out a simple example, continue reading here.

### Mac Maker Profiles

Mac Maker uses the concept of `Profiles`, to bundle together the Ansible configuration required to configure your Mac.

Here's an [example profile](https://github.com/osx-provisioner/profile-example) for you to test out:

1. Start Mac Maker: `./mac_maker`
2. Run the these commands, to check and apply the profile
  - `precheck github https://github.com/osx-provisioner/profile-example`
  - `apply github https://github.com/osx-provisioner/profile-example`

You can work with `Profiles` in one of two ways:

- Create a public GitHub Repository that contains your profile, taking care NOT to included privileged content.
- Create your profile in any private git repository, and clone it to a USB key (or other portable media).  Add a `spec.json` file to the USB stick telling Mac Maker how to find it.

To find out more:

- Read about the `Mac Maker Profiles`, and how to build one [here](https://mac-maker.readthedocs.io/en/latest/project/3.profiles.html).
- Use [this template](https://github.com/osx-provisioner/profile-generator) to create your own custom profiles.
- Read about the `spec.json` file, and how to build one [here](https://mac-maker.readthedocs.io/en/latest/project/4.spec_files.html).

## License

As this project effectively bundles Ansible, it must comply with the [GNU GPL](https://mac-maker.readthedocs.io/en/latest/project/6.license.html).
You are however free to use and modify this source, as long as the license's terms are respected.

(Pull requests are most welcome, as I sincerely hope this project can be of use to others.)

## Detailed Documentation

The project's full documentation can be found here:
  - [Mac Maker Documentation](https://mac_maker.readthedocs.io/)

Complete build instructions are included, so you can build your own binary.
