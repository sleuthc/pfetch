Due to some stupid issues I had to revert back my changes to old commits. That menas, that I lost a lot of progress and need to do it again. 

This project will still take a lot of time. Lucky for me I can stay home for some days and don't have to go to school for some reasons and that means
I have more time for coding, but there's so much to do in other projects not just this one and my whole life is currently a hustle. 

It will take time, but I promise, when it's done, it's better than ever.



<p align="center">
  <img src="https://github.com/EchterAlsFake/Porn_Fetch/blob/V3.0/src/frontend/graphics/logo_transparent.png" alt="Logo"/>
</p>



# Dev Information:

I have currently not the time to maintain this. School in Germnay is really hard in October - December.
I'll make a big update. You can expect it at late December. Thanks everyone for supporting this project!

# Porn Fetch - A Free & Open-Source PornHub Downloader 

![Build](https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/python-app.yml/badge.svg)
![Build](https://github.com/EchterAlsFake/Porn_Fetch/actions/workflows/android.yml/badge.svg)
![CodeQL](https://github.com/EchterAlsFake/Porn_Fetch/workflows/CodeQL/badge.svg)
### [Download Current Version 2.9](https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/2.9)
### [Development Status V3.0](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/STATUS.md)
## Table of Contents

- [What is Porn Fetch?](#what-is-porn-fetch)
- [Features](#features)
- [Supported Platforms](#supported-platforms)
- [Supported Websites](#supported-websites)
- [Building from Source](#building-from-source)
- [Android](#android)
- [iOS](#ios)
- [Translating](#translating)
- [Useful Information](#useful-information)
- [Legal Rights](#legal-rights)
- [Credits](#credits)
- [License](#license)

## What is Porn Fetch?

Porn Fetch allows users to download, search, and interact with videos from PornHub, aiming to provide a free and open-source downloader for everyone. 

#### Avoid shady websites or paid software in 2023.

## Features:

- Downloading directly from PornHub
- Selectable quality for downloads
- Fetching metadata from videos / Users
- Downloading all videos from a whole Channel / User / Model account
- In-app video search and download
- Account login
- Fetch all liked, watched, and recommended videos for your account
- Threaded downloads
- Native dark mode
- CLI for systems without a graphical user interface
- No ads & restrictions
- No mandatory login / PornHub account
- Cross-platform compatibility


## Supported Platforms

- Windows: 10, 11 (lower versions may be compatible)
- Linux: X11 / Wayland - X64 (Testing on Hyprland - Wayland)
- macOS: Requires building from source or native run with Python
- Android: Native run with an .apk recommended; CLI available in Termux
- iOS: Can be run with iSH ([See Building from Source](#building-from-source))
- ARM devices: Native run with Python required

## Supported Websites

- PornHub.com [PHUB](https://github.com/Egsagon/PHUB)
- HQPorner.com (Supported Since v2.8) [hqporner_api](https://github.com/EchterAlsFake/hqporner_api)

## Building from Source

Automatic build script is available. Run the following in your terminal and select your system.

### Supported Platforms:

- Ubuntu
- Windows 10 / 11
- Arch Linux
- Termux
- iSH (iOS / Alpine) (Enter iSH on the App Store, and you'll find it) 
- Fedora
- OpenSUSE

```
wget -O - "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install.sh" | bash
```
#### Termux:
```
wget -O - "https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install_termux.sh" | bash
```
#### Windows:
```
# Enable powershell script execution:

# Run Powershell ad Administrator and run the following command:
$ Set-ExecutionPolicy RemoteSigned 
$ Set-ExecutionPolicy Bypass -Scope Process
$ Invoke-Expression (Invoke-WebRequest -Uri https://raw.githubusercontent.com/EchterAlsFake/Porn_Fetch/master/src/scripts/install_windows.ps1 -UseBasicParsing).Content

This will automatically install Python3 (if not installed) and build the project
```

# Android

#### Read carefully to prevent errors!

The development for Android has a separate branch named "android."
<br>Kivy is a whole new framework for me, so I will need my time to make it look good!

### DOWNLOAD: [0.2](https://github.com/EchterAlsFake/Porn_Fetch/releases/tag/2.9)

#### Supported are Android 5-13 (in theory)

If you like to build it by yourself, use [this script](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/src/scripts/build_android.sh) 

It will install all dependencies and use the buildozer.spec from my repo.
<br> YOU NEED UBUNTU 22.04.3 FOR BUILDING AND NOTHING ELSE!!!


# iOS
### iSH
You can use the CLI (Terminal version) of Porn Fetch via the App 'iSH.'
iSH is a terminal emulator for iOS that launches an Alpine Linux.
You can use the build script to automatically install everything. It's not 
the best solution, but it works at least :) 

### Building
It's possible to convert the Kivy created APP for Android easily into an iOS application, but I don't have an Apple device, so I cannot compile or even test it. You can do it by yourself, and if you think you got a successful stable build, contact me via Discord: echteralsfake | EchterAlsFake#7164, and we can merge your build into the releases!

(Your changes need to be documented in a FORK of my project. A recommendation would be a secondary iOS branch.)

# Translating

### Supported Languages:

* German (3.0)
* English

If you want to port Porn Fetch into your language, see [this Guide](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/TRANSLATING.md)
> I appreciate it a lot, and you'll be credited in further releases and in the Readme!


## Useful Information
- [Roadmap](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/ROADMAP.md)
- [Changelog](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/CHANGELOG.md)
- [Development Status](https://github.com/EchterAlsFake/Porn_Fetch/blob/master/README/STATUS.md)
# Legal Rights

> ! PornHub PROHIBITS downloading videos for unregistered users. <br>
> ! PornHub PROHIBITS scraping content on their website or usage of any automation tools in general

So what do we learn from this? This tool is probably NOT permitted by PornHub.
I am just the developer. Nobody will get you in jail because you downloaded a video from PornHub, but consider using a VPN to be safe.

# Credits

##### Project API : [PHUB](https://github.com/Egsagon/PHUB)
##### GUI : [Qt](https://qt.io) for Python
##### Android : Kivy, KivyMD
### External libraries:
- [colorama](https://github.com/tartley/colorama)
- [tqdm](https://github.com/tqdm/tqdm)
- [phub](https://github.com/Egsagon/PHUB)
- [sentry sdk](https://github.com/getsentry/sentry-python) Used in 1.7–2.7
- [requests](https://github.com/psf/requests)
- [hqporner_api](https://github.com/EchterAlsFake/hqporner_api)
- [pyside6](https://wiki.qt.io/Qt_for_Python)
- wget

### Android Specific:
- Kivy MD
- Kivy
- Buildozer
- Cython

### Graphics:

- <a href="https://iconscout.com/icons/information" class="text-underline font-size-sm" target="_blank">Information</a> by <a href="https://iconscout.com/contributors/petai-jantrapoon" class="text-underline font-size-sm">Petai Jantrapoon</a> on <a href="https://iconscout.com" class="text-underline font-size-sm">IconScout</a>
- <a href="https://iconscout.com/icons/tick" class="text-underline font-size-sm" target="_blank">Tick</a> by <a href="https://iconscout.com/contributors/endesignz" class="text-underline font-size-sm">Jessiey Sahana</a> on <a href="https://iconscout.com" class="text-underline font-size-sm">IconScout</a>
- <a href="https://iconscout.com/icons/top-arrow" class="text-underline font-size-sm" target="_blank">Top Arrow</a> by <a href="https://iconscout.com/contributors/creative-studio" class="text-underline font-size-sm" target="_blank">Mian Saab</a>
- <a href="https://iconscout.com/icons/down-arrow" class="text-underline font-size-sm" target="_blank">Down Arrow</a> by <a href="https://iconscout.com/contributors/adamicons" class="text-underline font-size-sm">Adam Dicons</a> on <a href="https://iconscout.com" class="text-underline font-size-sm">IconScout</a>
- <a href="https://iconscout.com/icons/tick" class="text-underline font-size-sm" target="_blank">Tick</a> by <a href="https://iconscout.com/contributors/kolo-design" class="text-underline font-size-sm" target="_blank">Kalash</a>

All other Icons are also from Icon Scout, but I wasn't given the author's name, so I can't credit them.

## Contributors:

> I consider enhancement requests also as a contribution!

- [Egsagon](https://github.com/Egsagon)
- [RSDCFGVHBJNKML](https://github.com/RSDCFGVHBJNKML) : Enhancement #11

# License:
LICENSE: [GPL 3](https://www.gnu.org/licenses/gpl-3.0.en.html)
<br>Copyright (C) 2023 Johannes Habel | EchterAlsFake

