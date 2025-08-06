# ![UC-PACT](frontend/public/images/logo_blue-green-for-light-background.png)

---

This repository is used to generate UC DSL in a web-based graphical user interface.
When run via docker compose, both the frontend and backend are built and then run in docker containers.

## Compatibility and System Requirements

### Working Operating Systems/Implementations

- Ubuntu v22.04 LTS
  - As host OS on a x86_64 machine/physical server
  - As guest OS in a Virtual Machine on Windows 10 host OS
    - With VMware Workstation Pro v16 and v17 (v17 is recommended; paid license)
    - With VirtualBox (free and open-source) v6.x (not officially supported by Oracle anymore, but 7.x should work)
  - Within Windows Subsystem for Linux (WSL) v2 using an Ubuntu-v24.04 distro
    - With WSL kernel v2.2.4 or later on a Windows 11 host OS
    - With WSL kernel v2.3.26 or later on a Windows 10 host OS
      - One caveat: on IT-managed PCs you might need to use [localhost:3000/](http://localhost:3000/) rather than [localhost/](http://localhost/).
      - If you need to use the `:3000` port, you are limited to Single-User mode with the `dev` profile.
- Ubuntu v24.04 LTS
  - Same as above, though not actually tested in VMware or VirtualBox
- MacOS (latest version)
  - As host OS on a x86_64 machine/physical server
    - With Docker Desktop for Mac [https://docs.docker.com/desktop/setup/install/mac-install/](https://docs.docker.com/desktop/setup/install/mac-install/) and Docker Compose [https://docs.docker.com/compose/install/](https://docs.docker.com/compose/install/)

### Not Working or Unsupported Systems/Implementations

- Docker Desktop in Windows 11 or 10 **(requires changes to the `docker-compose.yaml` files)**
- Linux OS versions other than Ubuntu v22.04 and v24.04 LTS **(not tested)**
- MacOS on the new Apple silicon chips such as the `M4` series rather than the previously used Intel CPUs **(not tested)**
- Running the UC-PACT web server in development or production modes on cloud-hosted containers/servers **(not tested)**

### Software Requirements

- Ubuntu (as host or guest OS on a VM)
  - Latest version of Docker Engine Community Edition (Docker CE), which does not run natively on Windows machines
  - Docker Compose version 2.x
- Windows (host OS)
  - Latest version of Windows Subsystem for Linux (be sure to install Ubuntu v22.04 or v24.04 as the distro)
    - Only available on a Windows 11 or 10 (build 1903 or later) host OS
    - If using Windows 11 or 10 (build 2004 or later), use the PowerShell command `wsl --install` as described in [https://learn.microsoft.com/en-us/windows/wsl/install](https://learn.microsoft.com/en-us/windows/wsl/install)
    - Otherwise (or to troubleshoot), follow these instructions: [https://learn.microsoft.com/en-us/windows/wsl/install-manual](https://learn.microsoft.com/en-us/windows/wsl/install-manual)
- MacOS (host OS)
  - Docker Desktop (latest version)
    - Requires one of the 3 latest (currently supported) versions of MacOS
    - Installation instructions: [https://docs.docker.com/desktop/setup/install/mac-install/](https://docs.docker.com/desktop/setup/install/mac-install/)
- Any OS that supports the following browsers (may be a separate machine if backend is hosted on a network)
  - Firefox or Chrome (latest versions) to configure Keycloak via its admin UI, and to access the UC-PACT client UI
    - For Virtual Machines, it's preferred to run the browser within the guest (Ubuntu) OS, not the host
    - For WSL, you should be able to access everything from either browser running on your Windows 11/10 host OS
    - For MacOS, simply open either of the 2 browsers that you have previously installed on your Apple computer

### Important Considerations

If you need help installing Docker CE and Docker Compose v2.x on an Ubuntu host or guest OS (virtual machine), we recommend following these instructions: [https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository](https://docs.docker.com/engine/install/ubuntu/#install-using-the-repository).

If you would rather use Windows Subsystem for Linux (WSL), these instructions should work for you: [https://dev.to/felipecrs/simply-run-docker-on-wsl2-3o8](https://dev.to/felipecrs/simply-run-docker-on-wsl2-3o8).

Note that WSL and older versions of VMware Workstation (v16 or earlier) or VirtualBox do not cooperate well as described here: [https://learn.microsoft.com/en-us/windows/wsl/faq#will-i-be-able-to-run-wsl-2-and-other-3rd-party-virtualization-tools-such-as-vmware--or-virtualbox-](https://learn.microsoft.com/en-us/windows/wsl/faq#will-i-be-able-to-run-wsl-2-and-other-3rd-party-virtualization-tools-such-as-vmware--or-virtualbox-).

### System Requirements

System requirements have not been investigated in detail, but UC-PACT's server should run on most 64-bit x86 machines (individual or network server) with at least 2 CPU cores and 8 GB of RAM for Ubuntu OS or 16 GB of RAM for Windows hosts.

Basic minimum requirements estimated from testing:

- UC-PACT server-side (platform used to launch/host the application)
  - Individual machine running Ubuntu host OS
    - x86 64-bit architecture
    - 2-4 CPU cores (recent Intel or AMD processor)
    - 8 GB of RAM
    - 120 GB of free disk space, mostly for Docker (HDD or SSD)
    - No dedicated GPU required
  - Individual machine running VMware Workstation Pro or Oracle VirtualBox
    - See system requirements for respective virtual machine provider
    - Virtual Machines in both VMware and VirtualBox should be setup with at least
      - 2 virtual CPU cores
      - 8 GB of RAM
      - A 40-60 GB virtual disk. Note that VMware Workstation Pro allows you to expand certain virtual disks if necessary without recreating the VM. However, be cautious with VirtualBox's VMs or with any non-resizeable virtual disks, as Docker can easily eat up lots of space over time.
  - Individual machine running WSL2 in Windows 11 or 10 host OS
    - Hardware Virtualization Support (enabled in the BIOS)
    - 2-4 CPU cores (recent Intel or AMD processor)
    - 8-16 GB of RAM
    - 40-60 GB of free disk space (HDD or SSD)
    - No dedicated GPU required
  - Individual machine running Docker Desktop in MacOS
    - A supported version of MacOS as described in this link: [https://docs.docker.com/desktop/setup/install/mac-install/#system-requirements](https://docs.docker.com/desktop/setup/install/mac-install/#system-requirements)
    - x86 64-bit architecture
    - 2-4 CPU cores (recent Intel processor)
    - 8 GB of RAM
    - 120 GB of free disk space, mostly for Docker (HDD or SSD)
    - No dedicated GPU required
  - Shared physical server running a supported Ubuntu version
    - x86 64-bit architecture
    - 4-8 CPU cores (scale based on # of simultaneous users)
    - 32-64 GB of RAM (scale based on # of simultaneous users)
    - 60-100 GB of free disk space (SSD might be better)
    - No dedicated GPU(s) required
  - Hosting on cloud servers has not been tested
- UC-PACT client-side (machine may be different only when UC-PACT is hosted on a network-enabled server)
  - Any desktop platform that supports the latest versions of Firefox and/or Chrome with a minimum screen resolution of 1920x1080
  - Web app has not been optimized for any mobile devices, including tablets

## How to launch the web application

### Using Docker Compose directly

It is fairly simple to get UC-PACT up and running. Simply run
`docker compose --profile default build` followed by `docker compose --profile default up`.

If run in daemon mode, you can bring down the containers by running
`docker compose --profile default down`.

For development mode (avoids the need to build the frontend again after minor edits), use
`docker compose --profile dev build` once, and then `docker compose --profile dev up`.

After spinning up with either the `default` or `dev` profiles, proceed to the `Keycloak` admin interface at [http://localhost:8080/admin](http://localhost:8080/admin), and follow the instructions [below](#keycloak).

To run frontend tests (does not use Keycloak), use `docker compose --profile tests build` once, and then `docker compose --profile tests up`. The tests will run automatically. For backend tests, use the `--profile pytest` argument instead.

### Using convenience scripts (New)

For a simpler and more interactive method, run `./launch.sh` and follow the prompts to select a `profile` and to optionally save test results to a log file. After you press `Ctrl-C` in the terminal to stop the containers, the script will automatically take down (remove) all the containers.

### Single-user mode

Single-user mode is designed to be used locally on individual (not shared) machines. All authentication is disabled internally, with protections in place to prevent any remote client users from deactivating Keycloak authentication if a server is launched in the (default) multi-user mode.

Although this mode only supports a single user on the same local machine as the applications's backend, that user may still open multiple models in different tabs, windows, or browsers, while still preserving the existing read-only protections.

The primary benefit of single-user mode is a much quicker startup (especially if the frontend has already been built), since a Docker "spin-up" doesn't need to initialize Keycloak authentication, and the user-creation and login steps are completely eliminated.

To launch UC-PACT in single-user mode, first run `cd single_user_config` before using the same `docker compose` commands, or simply run `./launch_single_user.sh` in the top-level repo folder for an equivalent interactive experience.

After launching with either the `default` or `dev` profiles, navigate to [http://localhost/](http://localhost/). However, depending on your system set up you may need to use [http://localhost:3000/](http://localhost:3000/).

## How to access Keycloak's admin UI (multi-user mode only) {#keycloak}

To access the admin UI for `Keycloak`, go to [http://localhost:8080/admin](http://localhost:8080/admin)
and login with `username="admin"` and `password="admin"`.

### Adding a new user

To add a new user, first switch the realm in the upper left corner from `master` to `UCPACT-Realm`. Next, in the left navigation, click `Users`. Next click `Add User`. Only the username is a required field. Enter it, and click `Create`.

After clicking `Create`, you should have new options above. Click `Credentials` and `Set password`. Enter a password and toggle off `Temporary` as to not be prompted to change the password later.

Navigate to [http://localhost/](http://localhost/) and sign in to UC-PACT with the username and password you created.

## Resetting Docker Engine (for troubleshooting purposes)

> **Warning:** This will delete **all** of the Docker images and containers which are contained in that installation of Docker Engine/Desktop (not just for UC-PACT), as well as the builder cache. Dockerfiles and any `docker-compose.yaml` files will be preserved, but any subsequent Docker builds will have to start from scratch.

### Using Docker Commands directly

Run the following commands within `bash` in sequence.

```bash
if [[ "$(docker ps -a -q)" ]] ; then docker stop $(docker ps -a -q) ; fi

docker container prune -f
docker image prune -a -f
docker builder prune -a -f
```

### Using Convenience Script

Run `./reset_docker.sh` in `bash` and confirm when prompted by entering `y`.

## Deployment Notes

**Be sure to change Keycloak's `admin` password within `docker-compose.yml` before deployment!**

## Contact

You can contact the UC-PACT team by reaching out to [harden@riversideresearch.org](mailto://harden@riversideresearch.org)

For more information about Universal Composability and the UC DSL see the [EasyUC](https://github.com/easyuc) repository and the EasyUC User Guide in the docs folder of this repository.

---

ACKNOWLEDGMENT

This material is based upon work supported by the Defense Advanced Research Projects Agency (DARPA) under Contract No. N66001-22-C-4020. Any opinions, findings, and conclusions or recommendations expressed in this material are those of the author(s) and do not necessarily reflect the views of the Defense Advanced Research Projects Agency (DARPA).

Distribution A: Approved for Public Release
