<h1>Setting up GPG</h1>

ContainerSSH requires all contributors to sign their commits using GPG. GPG authenticates the committer using their GPG key. This serves two purposes:

1. **Security.** In Git anyone can make commit in the name of anyone. Using GPG commits makes sure we don't accidentally merge a commit pretending to be one of the core contributors.
2. **Licensing.** As you may notice, we don't have a Contributor License Agreement to make it as simple as possible for people to contribute. By signing your commits we verify that you have indeed made that commit yourself and you presumably understand that this software is open source under the MIT license. It's not 100% legally bullet proof, but it's a good tradeoff preventing contributors from having to read several pages of legalese.

## Setting up GPG

=== "Linux / WSL"
    On Linux or Windows Subsystem for Linux GPG is already included in the package manager. You can install it using the following commands:
    
    **Ubuntu**
    ```
    sudo apt-get update
    sudo apt-get install gnupg2
    ```
    **RHEL/CentOS**
    ```
    yum install gnupg2
    ```
    **Fedora**
    ```
    dnf install gnupg2
    ```
    **Gentoo**
    ```
    emerge --ask app-crypt/gnupg
    ```
    
    !!! tip
        You may want to install the [Kleopatra GUI](https://www.openpgp.org/software/kleopatra/) for easier access.

=== "Windows"
    
    [GPG4Win](https://gpg4win.org/) is a full suite for managing GPG keys on Windows. We recommend installing it with the Kleopatra GUI.
    
=== "MacOS"
    
    **Homebrew**
    ```
    brew install gnupg2
    ```
    **MacPorts**
    ```
    sudo port install gnupg2
    ```
    **GUI**
    [GPGTools](https://gpgtools.org/) offers a graphical version of GPG.

## Creating your GPG key

=== "CLI (GPG 2.1.17+)"
    Run the following command:
    ```
    gpg --full-generate-key
    ```
    
    - Select `RSA and RSA` as the key format.
    - Select `4096 bits` for the bit size.
    - When prompted for your **user information** make sure that the **e-mail address matches your GitHub e-mail and the one in your Git config**, otherwise your push may be rejected. If you do not wish to publish your e-mail address [GitHub gives you a privacy option](https://docs.github.com/en/free-pro-team@latest/github/setting-up-and-managing-your-github-user-account/setting-your-commit-email-address#setting-your-commit-email-address-in-git).

=== "Kleopatra"
    - Select File &rarr; New Key Pair...
    - Select "Create a personal OpenPGP key pair"
    - Set your name and the same e-mail address you have on your GitHub account. If you do not wish to publish your e-mail address [GitHub gives you a privacy option](https://docs.github.com/en/free-pro-team@latest/github/setting-up-and-managing-your-github-user-account/setting-your-commit-email-address#setting-your-commit-email-address-in-git).
    - Follow the wizard to create your GPG key.
    
=== "GPGTools (MacOS)"
    - Please follow the [GPGTools guide to create your key](https://gpgtools.tenderapp.com/kb/how-to/first-steps-where-do-i-start-where-do-i-begin-setup-gpgtools-create-a-new-key-your-first-encrypted-mail).
    - When prompted for your **user information** make sure that the **e-mail address matches your GitHub e-mail and the one in your Git config**, otherwise your push may be rejected. If you do not wish to publish your e-mail address [GitHub gives you a privacy option](https://docs.github.com/en/free-pro-team@latest/github/setting-up-and-managing-your-github-user-account/setting-your-commit-email-address#setting-your-commit-email-address-in-git).

=== "CLI (GPG 2.1.16-)"
    Run the following command:
    ```
    gpg --default-new-key-algo rsa4096 --gen-key
    ```
    
    - Select `RSA and RSA` as the key format.
    - Select `4096 bits` for the bit size.
    - When prompted for your **user information** make sure that the **e-mail address matches your GitHub e-mail and the one in your Git config**, otherwise your push may be rejected. If you do not wish to publish your e-mail address [GitHub gives you a privacy option](https://docs.github.com/en/free-pro-team@latest/github/setting-up-and-managing-your-github-user-account/setting-your-commit-email-address#setting-your-commit-email-address-in-git).
    
## Adding your key to GitHub

=== "CLI"
    First, list your GPG keys with the key IDs:
    
    ```
    $ gpg --list-secret-keys --key-format LONG
    ------------------------------------------------
    sec   rsa4096/YOUR-KEY-ID 2020-06-18 [SC]
    ...
    ```
    
    Copy the key ID as you will need it for the next steps, then export your public key:
    
    ```
    gpg --armor --export YOUR-KEY-ID
    ```
    
    Go to [GitHub &rarr; Settings &rarr; SSH and GPG keys](https://github.com/settings/keys) and add a GPG key. Paste the key you just copied into the interface.
    
=== "Kleopatra"

    - Right click the key generated in the previous step.
    - Select "Export...".
    - Save the file on your machine.
    - Open the file in a text editor.
    - Copy the key.
    - Go to [GitHub &rarr; Settings &rarr; SSH and GPG keys](https://github.com/settings/keys) and add a GPG key. Paste the key you just copied into the interface.
    
=== "GPGTools (MacOS)" 

    - Select the previously generated key.
    - Click the "Export" icon in the toolbar.
    - Click Save.
    - Open the file in a text editor.
    - Copy the key.
    - Go to [GitHub &rarr; Settings &rarr; SSH and GPG keys](https://github.com/settings/keys) and add a GPG key. Paste the key you just copied into the interface.

## Setting up GPG signing in Git

=== "Global"
    This method sets up automatic code signing for all git repositories on your computer. Run the following commands under your user account:
    
    ```
    git config --global user.name "Your Name"
    git config --global user.email "your-gpg-email@example.com"
    git config --global commit.gpgsign true
    git config --global tag.gpgsign true
    git config --global user.signingkey YOUR-KEY-ID
    ```

=== "Per repository"
   
    Run the following commands **in the directory** where you cloned the repository:
    
    ```
    git config user.name "Your Name"
    git config user.email "your-gpg-email@example.com"
    git config commit.gpgsign true
    git config tag.gpgsign true
    git config user.signingkey YOUR-KEY-ID
    ```
    
    !!! warning
        This method sets up GPG signing in a single repository. You must configure this **every time you clone a new ContainerSSH repository**.  
        
That's it! You can now continue with [setting up the toolchain](golang.md)!  