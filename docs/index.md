# General

## Controller
- The controller has an ARM CPU
- It is running Linux with busybox
- The Vantage stuff is in `/opt/vantage/ic`
- The microsd card is mounted to /media/mc

## Passwords
- The administrator password defaults to your controller's serial number
- If someone has changed this (most of the time this is true) you can reset it from the buttons on the controller

## SSH Access

- There is an SSH server on the controller.
- You can ssh with username `root` and your vantage administrator password.

## Scripting

Vantage "Drivers" are scripts written in the "Pawn" programming language, and compiled into a .drv file.
Scripts are written in .sma files and includes are .inc files.