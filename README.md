<div id="top"></div>

<!-- PROJECT SHIELDS -->
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
      <ul>
        <li><a href="#preparing-for-the-shiny-hunt">Preparing for the Shiny Hunt</a></li>
        <li><a href="#shiny-hunting">Shiny Hunting</a></li>
        <li><a href="#additional-options">Additional Options</a></li>
      </ul>
    <li><a href="#frequently-asked-questions">Frequently Asked Questions</a></li>
    <li><a href="#future-plans">Future Plans</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project
This is a Python app for hunting shiny Pokemon. To do so it emulates a Nintendo Switch controller via bluetooth. The Pokemon available for this app to hunt for are as follows:

* Regice

### Built With
* [NXBT](https://github.com/Brikwerk/nxbt)
* [OpenCV](https://opencv.org/)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started
To get a local copy up and running follow these simple example steps.

</br>

### Prerequisites
1. Have a Linux distribution available

    _Note: In order to emulate the Bluetooth controller using NXBT, installation on a Linux distribution is necessary. If you are using Windows or macOS, please setup a Virtual Machine. For more info go to the [NXBT Windows and macOS Installation Page](https://github.com/Brikwerk/nxbt/blob/master/docs/Windows-and-macOS-Installation.md)_

2. Verify python has been installed. To do this use the following command in the command prompt:
    ```bash
    python -V
    ```
* If Python is installed, an output should be returned that is similar to: `Python 3.8.6 `
* If a Python version is not installed, it can be found at the [Python Downloads Page](https://www.python.org/downloads/)
* _Note: Its possible Python **IS** intalled and doesnt work by using the `python` command. Usually this is the case when Python 3 is installed in which case you should use the command `python3`_

3. Verify pip has been installed. This is usually installed by default with Python, but there are a few rare cases where it is not. To do so, use the following command in the command prompt:
    ```bash
    pip -V
    ```
* If pip is installed, an output should be returned that is similar to: `pip 22.0.4`
* If pip is not installed, instructions on how to install are often returned when attempting to run the `pip` command, or they can be found in the [pip documentation](https://pip.pypa.io/en/stable/installation/)
* _Note: Its possible pip **IS** intalled and doesnt work by using the `pip` command. Usually this is the case when pip3 is installed with Python3 in which case you should use the command `pip3`_

</br>

### Installation
1. Clone this repository to your desired folder.
    ```bash
    git clone https://github.com/ltoleary3/Bluetooth-Shiny-Bot.git
    ```

2. Install required libraries
    ```bash
    sudo pip install .
    ```

    _Note: NXBT needs root privileges to toggle the BlueZ Input plugin. If you're not comfortable running this program as root, you can disable the Input plugin manually, and install NXBT as a regular user_

<p align="right">(<a href="#top">back to top</a>)</p>

</br>

<!-- USAGE EXAMPLES -->
## Usage
Before starting the script, ensure you have saved the game where your character is standing directly in front of the Pokemon you wish to hunt for. _Note: To ensure that you have set up properly, all you should have to do after starting the game is press the 'A' button to start the battle_

All scripts in this project should be run while the Switch is on the Home screen hovering over the Pokemon game. For the additional option flags, please read the <a href="#additional-options">Additional Options</a> section.

If the user wishes to quit the hunt before a shiny is found, simply ensure that the active window is opened (This means the video stream window if the user indicated an output stream is desire, otherwise it is the command prompt) and then press "Q'.

</br>

### Preparing for the Shiny Hunt
This program sets up everything needed for the main script to function properly. In the folder where this app is downloaded:
```bash
sudo python prepHunt.py <Pokemon Name> [Additional Options]
```
Example:
```bash
sudo python prepHunt.py regice -Display -Update
```

* First, it will create a Bluetooth controller instance and attempt to connect to the Switch. If it is your first time using that computer to connect to that Switch, you will be required to navigate to the "Change Grip/Order" menu in the settings and then signal to the program that you have done so. _Note: There is a known issue where the controller will sometimes disconnect from the Switch when exiting this menu. If this happens to you, simply return to the home screen and rerun this script._
* Next, it will start the game. Once the game has loaded it will then start the battle with the Pokemon. When the battle is started it will then search for a valid frame from the video stream.
* After it has found the valid frame, it will then prompt you to confirm that the Pokemon is not shiny.
* Finally, if the user indicated that the Pokemon is not shiny, the program will store the files required to shiny hunt for that Pokemon.

This method needs to be done before shiny hunting a Pokemon for the first time in order to gather the proper information on it based on the input stream being recieved from the Switch.

_Note: The valid frames it uses to detect if the Pokemon is shiny or not are all found at the very beginning of the encounter. If the battle has progressed long enough that you are able to actually attempt to catch the Pokemon, it means that something has gone wrong finding these frames. You should be safe to stop the program and close the game. From there, verify that your device is able to properly recieve the video signal from the Switch and try again_

</br>

### Shiny Hunting
This program emulates a Switch controller and checks to see if the Pokemon is shiny. In the folder where this app is downloaded:
```bash
sudo python shinyHunt.py <Pokemon Name> [Additional Options]
```
Example:
```bash
sudo python shinyHunt.py regice -Update
```
* First, this program validates that the files required for the shiny hunt exist. If they do not, it calls `prepHunt.py` with the same inputs given to start this shiny hunt where it will then gather them.
* After it has verified that the required files exist, it will create the Bluetooth controller instance and attempt to connect to the Switch. Similarly to `prepHunt.py`, if it is your first time using that computer to connect to that Switch, you will be required to navigate to the "Change Grip/Order" menu in the settings and then signal to the program that you have done so. _Note: There is a known issue where the controller will sometimes disconnect from the Switch when exiting this menu. If this happens to you, simply return to the home screen and rerun this script._
* Next, the app starts the game. After it has loaded it will then start the battle and search for the same valid frames it found in `prepHunt.py`
* Once the valid frames are found, they are used to compare the Pokemon against the standard version that was verified in `prepHunt.py`
* If it detects that the current Pokemon is different from the standard version found in `prepHunt.py` it will ask the user to verify if the Pokemon is shiny or not. If the user then verifies that the Pokemon IS shiny, the app will then stop to allow the user to catch the Pokemon. If the user indicates that the Pokemon IS NOT shiny, it will continue as if it had not detected the difference. _Note: If the user experiences many false positives, please re-run the `prepHunt.py` script to reset the files it uses for the hunt._
* If the Pokemon was not shiny it will then close the game and restart it, thus continuing with another try.

_Note: The valid frames it uses to detect if the Pokemon is shiny or not are all found at the very beginning of the encounter. If the battle has progressed long enough that you are able to actually attempt to catch the Pokemon, it means that something has gone wrong finding these frames. You should be safe to stop the program and close the game. From there, verify that your device is able to properly recieve the video signal from the Switch and try again_

</br>

### Additional Options
When using this application to shiny hunt, there are additional options the user can choose to indicate when starting to activate them. All options are available to both `shinyHunt.py` and `prepHunt.py` and can be combined together to get the desired funtionality. These options are:

1. Update
</br>
    This is used to signify to the program that the game has an update available, but you do not wish to update to that version.

    Example:
    ```bash
    sudo python shinyHunt.py regice -update
    ```
2. Display
</br>
    This is used to signify to the program that the user wishes to display a window showing the input video stream being read by the propgram.

    Example:
    ```bash
    sudo python shinyHunt.py regice -display
    ```

    _Note: This option can potentially reduce the performance of the app. In most cases it will not affect the ability of the program to detect Pokemon, but in lower end machines it may be worth it to NOT display the video stream in order to increase accuracy_ 

    _Note: This option will not work if the user has connected to the device via ssh_ 

<p align="right">(<a href="#top">back to top</a>)</p>

</br>

<!-- FREQUENTLY ASKED QUESTIONS -->
## Frequently Asked Questions
If you're having an issue with the program, try these fixes to common issues. If the fixes do not work you can create an issue where more assistance can be given.

</br> 

1. The Pokemon I want to shiny hunt is not available. What can I do?

    1. If you want to add a Pokemon to the list of those available to hunt, you will need to have your switch in handheld mode (to ensure the image is at 720p) and then take a screenshot of the beginning of the encounter where the textbox at the bottom says "< Pokemon Name > Appeared!" and then crop the image so only the text shows like in the following image. _Note: The image should be formatted as a .jpg file in order for the image to be properly utilized_

        <img align="center" src="./assets/README/regiceAppeared.jpg"> 

    2. Next, go into the assets folder and create a subfolder named after the pokemon you're hunting. Upload the image to that subfolder and name the file in the format like `<lowercase pokemon name>Appeared.jpg`
    
        Example: `regiceAppeared.jpg`

    3. Finally, add the pokemon name to the list found on line 9 of `shinyHunt.py` and `prepHunt.py`
</br>
    For instructions on how to add those changes to the main application, please refer the <a href="#contributing">Contributing</a> section.
</br>

2. The emulated controller keeps disconnecting. What should I do?

    * Ensure that you have a Bluetooth device available to use. If you're using a VM make sure that the VM has access to the Bluetooth device. Integrated Bluetooth devices can be hit or miss based on testing.
    * Disconnect any other controllers connected to the Switch. This can be done by opening the "Change Grip/Order" menu while in handheld mode, then putting it back on the dock
    * If your device is using multiple Bluetooth connections (eg. headphones, mouse, keyboard, etc), those may interfere with each other as well.
    * Try setting your switch to Airplane mode, then enabling Bluetooth (it turns off by default when switching to Airplane mode)
</br>

3. The program isnt recognizing the Pokemon I'm hunting for. What can I do?
</br>
    or
</br>
    The program thinks every Pokemon is shiny. What can I do?
    * Try using the -Display option to ensure that the video stream your computer is receiving from the switch is normal. If the connection is loose the video can be distorted
    * Ensure that the software is capturing the proper device. In most cases it should already be set to the correct device, but if you have multiple devices connected like a webcam its possible its picking up the wrong device. Try incrementing the default src number on line 5 of `./tools/videostream.py`
    * Rerun `prepHunt.py` to reset the files used in the hunt
    * Use the -Display option and check the frame rate of the program. Its possible that the performance on low end devices is causing it to entirely miss the Pokemon
</br>

4. The program gets stuck in a battle or goes into a wrong menu. How do I fix this?
    * This is a known problem where the Switch will randomly change the Bluetooth frequency it recieves from the controller causing a momentary disconnect from the controller. This can either cause the emulated controller to miss a button press/press out of order or just disconnect entirely. Simply return to the Switch's Menu screen and restart the program. 

    * If this happens often, ensure that your Bluetooth device is connected properly. See FAQ #2 for examples of what to check.

    * If it still happens after the other common fixes, create an Issue where more support can be given

<p align="right">(<a href="#top">back to top</a>)</p>

</br>

<!-- FUTURE PLANS -->
## Future Plans
The following are ideas that **WILL** be implemented in the future (in no particular order):

* Stability patches
* Add more Pokemon that can be hunted
* Fine tune image detection

The following are ideas that **MIGHT** be implemented in the future based on feedback in the [Discussions page](https://github.com/ltoleary3/Bluetooth-Shiny-Bot/discussions) (in no particular order):

* Ability to scale output video
* Add a GUI option
* Add ability to use on future generations
* Add an overlay counter to the output stream

If you have an idea on how to make this project better that isn't listed above, be sure to go to the [Ideas Page](https://github.com/ltoleary3/Bluetooth-Shiny-Bot/discussions/categories/ideas) in the Discussions tab to share it or interact with others ideas. If an idea gets enough traction in the Discussions page, it may be added to the pipeline to implement into the project!

<p align="right">(<a href="#top">back to top</a>)</p>

</br>

<!-- CONTRIBUTING -->
## Contributing
Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Make and then commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a pull request into the development branch

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License
Distributed under the [MIT License](https://github.com/ltoleary3/Bluetooth-Shiny-Bot/blob/main/LICENSE)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- CONTACT -->
## Contact
Logan O'Leary - [Twitter](https://twitter.com/LoganTOleary) - Email: logantoleary.business@gmail.com

Project Link: [https://github.com/ltoleary3/Bluetooth-Shiny-Bot](https://github.com/ltoleary3/Bluetooth-Shiny-Bot)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[issues-shield]: https://img.shields.io/badge/ISSUES-open-yellow
[issues-url]: https://github.com/ltoleary3/Bluetooth-Shiny-Bot/issues
[license-shield]: https://img.shields.io/badge/LICENSE-MIT-green
[license-url]: https://github.com/ltoleary3/Bluetooth-Shiny-Bot/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/LINKEDIN-LoganOLeary-blue
[linkedin-url]: https://www.linkedin.com/in/logantoleary/