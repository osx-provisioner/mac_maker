# Project Documentation

## Mac Maker

A portable single binary configuration tool for OSX machines.

- Brings [Ansible](https://www.ansible.com/) powered Configuration Management to your Mac.
- Mix and match existing Ansible roles such [asdf](https://github.com/osx-provisioner/role-asdf), [clamav](https://github.com/osx-provisioner/role-clamav) and [homeshick](https://github.com/osx-provisioner/role-homeshick) with the huge array of Mac roles on [Ansible Galaxy](https://galaxy.ansible.com/).

### Generate a consistent, reproducible "profile" of your machine

- Start with a freshly installed Mac, and apply a `Mac Maker Profile` to add all the customizations and applications you want.
- Alternatively, start with an existing Mac you already use, and incrementally build a `Mac Maker Profile` putting all your existing apps and customizations under version control.

### Main Branch Builds
- GitHub:
  - [![mac_maker Generic Push](https://github.com/osx-provisioner/mac_maker/actions/workflows/push.yml/badge.svg?branch=main)](https://github.com/osx-provisioner/mac_maker/actions)

### Production Branch Builds
- GitHub:
  - [![mac_maker Generic Push](https://github.com/osx-provisioner/mac_maker/workflows/mac_maker-push/badge.svg?branch=production)](https://github.com/osx-provisioner/mac_maker/actions)

## Quick Start

### How do I use this?

If you'd like to try it out, head over to the [Mac Maker Releases](https://github.com/osx-provisioner/mac_maker/releases) and download a pre-built binary.

- There are builds available for both **Intel** and **Apple Silicon Macs**
- OSX versions Catalina through Sequoia are known to be compatible, but you must carefully select your download.

#### How do I select the right download ?

Each binary build is named to indicate the platform it was built with:

`mac_maker_XX_YY_ZZ.tar.gz`:
  - where XX: is the OSX version used to build the binary
  - where YY: is the CPU architecture used to build the binary
  - where ZZ: is the `mac_maker` software version used to build the binary

Each `mac_maker` binary is **forward-compatible** with all following versions of OSX, but it's not backwards compatible.  Consequently, builds on earlier versions of OSX tend to be more portable.  (This is simply how [pyinstaller](https://pyinstaller.org/en/latest/usage.html) works.)

First find a `mac_maker` binary that's compatible with your target OS version.  You're looking for a binary built on an **equal or earlier** version of OSX:  

| Target OS | Target OS Name | Compatible `mac_maker` OS builds |
|-----------|----------------|----------------------------------|
| 26        | Tahoe          | 10, 11, 12, 13, 14, 15, 26       |
| 15        | Sequoia        | 10, 11, 12, 13, 14, 15           |
| 14        | Sonoma         | 10, 11, 12, 13, 14               |
| 13        | Ventura        | 10, 11, 12, 13                   |
| 12        | Monterey       | 10, 11, 12                       |
| 11        | Big Sur        | 10, 11                           |
| 10        | Catalina       | 10                               | 

Lastly, make sure you also choose the right CPU architecture:

| Architecture | CPU Type      |
|--------------|---------------|
| arm64        | Apple Silicon |
| x86_64       | Intel         |

**Concrete Examples**:
- `mac_maker_12_x86_64_0.0.7.tar.gz`:
  - was built on Monterey, for Intel CPU's, using `mac_maker` version 0.0.7
  - your target machine's OS can be >= 12, but must use an Intel CPU 
- `mac_maker_13_arm64_0.0.6.tar.gz`:
  - was built on Venture, for Apple Silicon, using `mac_maker` version 0.0.6
  - your target machine's OS can be >= 13, but must use Apple Silicon

**Please Note**:
- The binaries are unsigned, and not notarized by Apple.
- As such, they will trigger a warning about software from an `unidentified developer` when executed.

### OK, but you still didn't tell me how to get started...

Are you on OS version Monterey or later?  It may not ship with python anymore!  We better check:
- open a terminal and type `python3`, and if prompted to install the [x-code](https://developer.apple.com/xcode/) cli tools click `install`.
- this is less than ideal, but it gets you into a compatible state quickly

Once you've confirmed [python](https://python.org) is present):
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

- Read about the `Mac Maker Profiles`, and how to build one [here](https://mac-maker.readthedocs.io/en/latest/project/4.profiles.html).
- Use [this template](https://github.com/osx-provisioner/profile-generator) to create your own custom profiles.
- Read about the `spec.json` file, and how to build one [here](https://mac-maker.readthedocs.io/en/latest/project/5.spec_files.html).

**Please Note:**
- We've had some user feedback that the `spec.json` files are a bit complicated to get started with.
- Although we'll continue to support them, we'll soon introduce the ability to simply specify the path to a `Mac Maker Profile` folder on the local filesystem.

## License

As this project effectively bundles Ansible, it must comply with the [GNU GPL](https://mac-maker.readthedocs.io/en/latest/project/7.license.html).
You are however free to use and modify this source, as long as the license's terms are respected.

(Pull requests are most welcome, as I sincerely hope this project can be of use to others.)

## Detailed Documentation

The project's full documentation can be found here:
  - [Mac Maker Documentation](https://mac-maker.readthedocs.io/)

Complete build instructions are included, so you can build your own binary.
