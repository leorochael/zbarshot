# ZBarShot

Scriptlet to interpret the barcode of Brazillian _boletos_ or _convênios_ scanned
directly from your desktop screen.

## Dependencies:

ZBarShot depends on the following executables in your path:

 - `gnome-screenshot`
 - `notify-send`
 - `xclip`
 - `zbarimg`

On a Debian/Ubuntu derivative, these can be installed with:

    sudo apt install gnome-screenshot libnotify-bin xclip zbar-tools

## Installation

Run `./install.sh`. It will create symlinks in the following folders:

 - `~/.local/share/icons`
 - `~/.local/share/applications`
 - `~/bin`

The folders above will be created if they don't exist.

You might need to re-login before `~/bin` is available on your path or the desktop application is available on your desktop environment.

## Usage

 - With the barcode visible (and large) in your screen (i.e. in a zoomed-in PDF), start
   the application (either on the command line as `zbarshot`, or in your desktop
   environment as `ZBarShot`),
 - Drag a rectangle in your screen over the barcode. Try to make it as tight as possible.
 - The interpreted barcode will be available in the system clipboard.

## Credits:

[Barcode Scan](https://dev.materialdesignicons.com/icon/barcode-scan) icon in
`.desktop` file (`zbarshot.svg`) taken from
[Material Design Icons](https://materialdesignicons.com/).

## TODO

 - Release a proper package for installation with pipx or somesuch.
 - Uninstall script.

## Ideas

 - Have an indicator displayed while activated for dragging and another while holding
   the clipboard active.
