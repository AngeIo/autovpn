# autoVPN

Connect to your Ivanti Secure Access Client (formerly Pulse Secure Client) automatically when booting Windows!

## Features / To-do list
- [x] Easy auto-connect to the VPN when logging-in to your Windows computer!
- [x] Easy installation using included script!
- [ ] Easy installation (improve first time setup with password generation etc.)
- [ ] Support for Linux (only tested on Windows)

## Installation

Please make sure you have the following prerequisites:

- [Git](https://git-scm.com/downloads)
- [Python 3](https://www.python.org/downloads/) (tested with 3.10.11)
- [Ivanti Secure Access Client](https://www.ivanti.com/products/secure-unified-client) (tested with 22.6.1 - 26825)
<details>
<summary>Show details for Ivanti</summary>

```
Name: Ivanti Secure Access Client for Desktop 22.6R1 Build 26825
File name: ps-pulse-win-22.6r1.0-b26825-64bit-installer.msi
File Size: 57 MB
SHA-256 Checksum: bb7571e84941cd6018d47c2fff25a13dfa0846dd593bc8070d41458f5ff70778
Last Updated: 2023-09-24
```

</details>

### Downloading the source code

Clone the repository:

```shell
git clone https://github.com/AngeIo/autovpn
```

To update the source code to the latest commit, run the following command inside the `autovpn` directory:

```shell
git pull
```

## Usage

### Dependencies
Download all the required packages for the script by running the following command in your terminal:

```shell
pip install -r requirements.txt
```

### Encryption of your password
Utilize the dedicated script in the `utils` directory to generate an encrypted version of your *Horoquartz* password. Save the result for later use. Run the following command:

```shell
python utils/pwgen.py "MyStrongPassword"
```

### Variables configuration
You have to:

- Rename `variables.py.template` to `variables.py`.
- Copy and paste your encrypted password in the `vpn_pw` variable.
- Modify all other variables in `variables.py` to match your environment.

### Compile & install
Run the compiler and installation scripts using the following command:

```shell
python utils/make.py
```

### Run the Script
To execute the script, start your Windows PC to run `autovpn`!

## License
The source code for "autovpn" is using a *???* license (we haven't decided yet).

## Authors
* GERARD Angelo

