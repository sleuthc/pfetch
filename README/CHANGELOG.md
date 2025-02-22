# 1.0
Initial Release

# 1.1
- Code refactoring
- Added Support for downloading a whole channel / user
- Fixed an Issue with the progress bar
- Fixed typo issues
- Fixed the output path issue
- Changed License to LGPLv3 (The reason for this is, that I am stupid and I used the wrong license. Creative Commons is not valid to be used for developing with Qt. I didn't know that, I am sorry...)
# 1.2
- Added additional stuff to the metadata function (Likes, Image URL, Tags)
- Added border colours for input fields

# 1.3
- Added Threading Modes
- Single: Downloads will be executed within the main thread, and the GUI won't respond to your actions if the download isn't finished.

- Multiple: Download(s) will be executed with separate Threads (QThreads). This is mostly intended for single downloads. You can use that function also for multiple downloads, but that will ruin the progress bar, because it will jump between the different videos.

# 1.4

- Changed UI (stackedWidget)

# 1.5 

- Added CI 
- Made Readme.md and Build process simpler to understand

# 1.6

- Fixed 7 Bugs
- CLI is more stable
- Code refactoring
- Handling API timeout in Search function
- Created Security.md
- Created ROADMAP.md
- Created ISSUES.md
- Compiled Versions now compiled with Python 3.11.4


# 1.7

- Implemented an automated fix for the IndexError exception
- Improved overall code quality
- Split the code into multiple files, to be better readable 
- A lot of grammar fixes
- Added native support for Termux (See building from source : Android)
- Changed Qt Version from 6.5.1 to 6.5.2
- Changed Python version from 3.11.3 to 3.11.4
- Added automatic error reporting with Sentry.io
- Changed License to GPL 3
- Added CI/CD Actions for build and security checks
- Made the Readme.md A LOT more readable and more professionally
- Added license agreement script (implemented in 1.8)


# 1.8

- Implemented final License agreement
- Persistent settings (untested)
- Added Ubuntu to Install script
- Added installation script
- Added arch linux to install script
- Typo and grammar fixes
- Added Icons and images
- UI redesign
- Added some basic exceptions

# 1.9

- Fixed OS Error issue
- Added function to strip out special symbols in title, to prevent path issues

# 2.0

This release exists, but I don't remember the changes anymore.

# 2.1

- A complete new UI design
- UI is more fluent / flexible
- API updated to v3.1
- Thanks to Egsagons Update, most errors are fixed now
- Fixed Connection Error
- You can change the API language 
- You can change the UI language (only english supported now, see contribution for more)
- Added Keyboard shortcuts
- UI is much smaller now
- removed icons
- added more dependencies
- little bit code refactoring
- removed borders
- better windows support
- better automatic error handling
- included sentry reporting to more sections of the code
- added more filters, to prevent OS Error

# 2.2

- You can now log in with your PornHub Account
- You can now fetch your watched, liked, and recommended videos for your PornHub Account
- updated the CLI a little bit (not finished. It's my priority for the next release)
- API updated to v3.1-1
- a lot of typo fixes
- removed Security.md, because it was useless, and I don't really remember why I even added it
- added all files to the release page (thanks to Egsagon for telling me that I should do that :)

# 2.3 

- fixed some issues...


# 2.4

- If you use the file / model - user - channel functionality, then the TreeWidget will be used
  to let you select the videos that you want to download instead of downloading everything

- fixed an issue in the termux build script
- API updated to v3.1-4
- You can now select if you want to have a delay or not (enabling it is recommended!)
- OS error is fixed (FOR REAL!)
- Sentry strips out sensitive information and now only the exception, lines of code, server name is reported
  (Although I need to still test that.)

The next update will focus more on features / compatibility to other systems.
I hope that most issues are now fixed.

# 2.5

- Added search filters
- Move settings to a new page of stacked Widget
- Added keyboard shortcut and some buttons for it
- API Updated to v3.2
- Added function for downloading the thumbnail
- Fixed an error with the metadata function
- Removed file logging
- Recoded CLI

# 2.6

- API Updated to v3.2.1
- Redesign of the settings widget
- removed some things from the roadmap
- added a connection error exception

# 2.7

- API Updated to v4
- Huge stability and performance boost
- fixed setting Delay not working issue
- fixed #4 connection error / model error

# Version 2.8 Update Notes

### New Features:
- Added support for HQPorner.com.
- Introduced dynamic colors for CLI.
- Created STATUS.md for tracking upcoming releases.
- Implemented help buttons for threading and "high speed" (previously known as Delay).
- Added user metadata and info functionality.
- Included a new logo.

#### Interface & Design:
- Rolled out the final app design.
- Integrated qt resource file for better icon handling.
- Improved stylesheet logic in the GUI (reduces code by approx. 1500 lines).
- Unified to a single tree widget for all functionalities.

#### Performance & Efficiency:
- Removed 'get_graphics' function, enhancing UI start speed and eliminating setup requirement.
- Adjusted "Delay" to "High Speed" for clearer understanding.
- Defaulting to maximum api requests possible for faster downloads
- API updated to v4.1

#### CLI Updates:
- Updated CLI to version 4.1.
- Entirely refactored CLI.
- Fixed issues with Termux CLI build.

#### Build & Integration:
- Improved dependency handling in the build script.
- Added support for iSH in the build script.
- Integrated kivy build with CI/CD.

#### Removals & Deprecations:
- Eliminated Sentry from the project.
- Deleted unnecessary files: DOWNLOADS.md, ISSUES.md.
- Discontinued transparency support.
- Modified several minor elements in various files.

#### Miscellaneous:
- Updated thumbnail download to align with PHUB v4.
- Note: This Readme has been crafted with assistance from ChatGPT for professionalism.

#### Android:
- API Update to PHUB v4.1 from py-3.9 branch using custom fork
- You can now just paste the URL from the clipboard
- You can now choose the output folder without needing to enter it in to the input line
- improved visual look and progressbar

# 2.9

- API updated to 4.1.3
- Added Enhancement request from #11 (Skips already downloaded videos...)
- huge Performance increase when downloading (thanks to Egsagon's threaded preset) 
- Added a Semaphore (only 4 threads at once -- less overload and less CPU burning)
- Added Avatar downloading 

# 3.0
#### Entire rewrite of Porn Fetch, the CLI, the Android App and the HQPorner API.


## GUI
- Entire rewrite of the Porn Fetch GUI (Graphical User Interface)
- The GUI is now fully resizeable and works on all screen sizes
- The GUI now supports translations in German, Chinese and French
- The GUI now has a sidebar which is simpler than v2.9
- There's a third progressbar which tracks the total progress of all PornHub videos being downloaded
- The Tree Widget can now provide more information over the videos. Author, title and duration
- The Progressbars now have a dark design
- The License widget has now a dark design too
- The header of the QTreeWidget now supports Dark Mode.
- Updated to new improved icons.
- Global usage of the tree Widget.


## Performance
- There are three threading modes for different use cases
- The semaphore has been fixed, and you can now decide how many videos can be downloaded simultaneously (1-6)
- Implemented a Threading class for listing model videos.
- Transitioned all Metadata methods to use threading.
- Optimized the 'check_if_video_exists' function for greater efficiency.
- Strengthened the robustness of the config file integrity checking logic.
- Porn Fetch is now built with Python 3.12 (Android still 3.10)

## GitHub Repository
- A lot better project structure
- The Readme now has a translation guide
- Optimized all readmes

## Code Optimization
- Removed unnecessary signals and completed slots
- Improved threading classes
- Refactored the user settings functions
- Enhanced structure of the Q Resource file.
- Stylesheets have been reorganized and divided into multiple sections for better management.
- Changed the strip title function to allow non UTF-8 characters to support other language alphabets
- Comprehensive rewrite of the Command Line Interface (CLI).

## Translations
- Added German
- Added French
- Added Chinese

## Scripts
- Removed iOS build script (Porn Fetch isn't working on iOS sadly)
- Added support for macOS in the build script
- Added support for Windows (separate build script)

## Issues / Bug Fixes
- Fixed an issue with the config file location creation

# Deprecations
- Threading is now ALWAYS on. You can't disable it, because I see no reason for it.
- Removed Searching Filters

## Features
- Added support for Eporner.com
- Added support for xnxx.com
- Added support for xvideos.com
- New directory system to organize videos by model in separate folders.
- Videos can now be shown in reverse order [#17](https://github.com/EchterAlsFake/Porn_Fetch/issues/17)
- You can now also download by model on HQPorner
- You can now download by category on HQPorner
- You can now download by Top Porn on HQPorner
- You can now download a random video on HQPorner
- You can now search for videos on HQPorner
- FFMPEG will now be automatically downloaded and installed if checked as threading mode

# Android
- The Android App is now exactly the same as Porn Fetch desktop
- The Android app is now based on PySide6
- The Android app now supports all* features as the Desktop App

* except the QFileDialog, but this is an Issue from Qt itself.

## Contributors

- [Egsagon](https://github.com/Egsagon) French translations
- [Joshua-auhsoj](https://github.com/Joshua-auhsoj) Chinese translations & Enhancement [#17](https://github.com/EchterAlsFake/Porn_Fetch/issues/17)

# IMPORTANT FOR ANDROID USERS

Since Android changed a lot on their storage permission system, apps must nowadays ask for read / write permissions
at runtime. 
<br>I can't do this for some [reason](). You can ONLY use Porn Fetch on Android if you have the shared Download folder. It would be in
<br> `/storage/emulated/0/Download` Porn Fetch will automatically check this and notify you if it doesn't work. 

This is also the reason why Porn Fetch uses an older Android SDK, because with a lower SDK level I can get around the 
<br> Permission system, but there's no guarantee that this works.

I tested it on Android 12 & 13 on two devices.


# 3.1

# Features / Improvements
- Added playlist support #20
- Added model for EPorner
- Error handling if wrong URL was entered
- Added Disclaimer to the License agreement
- Added more ui popups into the translations
- Updated **ALL** Stylesheets. The GUI now looks a LOT better
- implemented logic, so that user can't log in to PornHub without entering actual credentials
- Added searching support for EPorner
- Implemented update mechanism
- Implemented a factory reset for the settings
- Reimplemented back the client delay (optional)
- Redesigned settings widget
- Added get_by_category for EPorner
- Added a setting for specifying the workers and timeout in the threaded preset


# Bug Fixes / Issues
- Fixed an issue, where the settings were displayed, instead of the download tab
- Fixed total progress callback for processed videos in file mode
- Fixed the issue that the downloaded ffmpeg .zip wasn't deleted on windows
- Fixed callback progress for HQPorner
- Fixed the total progress for FFMPEG
- Fixed the FFMPEG type error #21
- Fixed individual progress for FFMPEG
- Fixed searching (result) limit
- Fixed total progress for loading objects and stuff
- Handling `Client.call failed after 4 attempts`
- Fixed an issue that video reversing is not working
- Fixed overflow error
- Progress now gets only updated all 0.5 seconds
- Some issues in the CLI

# Code related
- Renamed UI widgets so that they make more sense
- Improved the load style function
- Added code comments
- Code refactoring (refactored all Signals)

# Android
- [x] Fixed the threaded presets for Android (may or may not work...)


# 3.2

## New Features
- Disabled limits in the settings e.g., the search limit
- You can now apply your own values for the timeout, max workers, delay and other network settings
- You can now export Video URLs from the tree widget directly into a file
- You can now stop loading video objects by clicking the button
- Porn Fetch is now able to install ffmpeg automatically for you. Go to the settings to do this.
- Added Searching support for xnxx
- Added Model support for xnxx
- Porn Fetch will now automatically write some metadata to the files and convert the .ts files into a valid .mp4 header file.
  (This requires FFmpeg. If it is not installed, it will be skipped.)

## Bug Fixes
- Fixed the Overflow Error
- Fixed logger debug / error connections (only relevant for local development with Android)
- Fixed several typo issues, e.g., #34
- Fixed some PHUB errors related to #33 #30 #27 #12 #4


## Other
- Rewrite of the README
- Rewrite of the CLI of Porn Fetch
- A lot of code optimizations