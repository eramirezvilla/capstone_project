
Gus Brigantino
gusbrig97@gmail.com

valFile.cpp, BLEService.cpp and gui.py

    This project is meant to simulate a public trasportation fare gate system using BLE beacons as virtual tickets. 
BLEService.cpp gets the output from the command: $ sudo timeout -s INT 0.25s btmgmt find, compares the output 
(MAC addresses and RSSI values) to a list of pre-authorized beacons, then selects the beacon with the lowest RSSI value. 
The valFile.cpp file is the main state machine that runs the system. It waits for the BLEService file to return a 
pre-authorized beacon's MAC address, checks a pre-loaded csv file, which serves as the backend database with balance 
and name information, to ensure the beacon is in the system and has enough funds to purchase a ticket. If the beacon is 
found and has enough funds the valFile systems processes the beacon's account by modifying the current balance. Whether 
or not the beacon's account is authorized to make a ticket purchase, the account information then is sent to gui.py via an 
IP socket. With the information shared, the gui system is able to make a decision on which screen to display, based on the 
account's current state. 

Configuring MAC addresses
1. Add to Acct.csv
    -               MAC address,Name,Balance
    -example entry: 04:91:62:97:8B:38,Gus,63.0
2. Edit BLEService.cpp
    -Within this file you will find a function called InitDesiredAddrs()
    -This function inserts the MAC address of all authorized beacons for the BLEService to compare its scans to
    -Insert all desired MAC addresses here
    -example entry: desiredAddrs.insert("04:91:62:97:8B:38");

Run GUI and Validator on same machine
1. In gui.py change IPAddress to '127.0.0.1'
2. In valFile.h change SERVER_ADDR to 127.0.0.1
3. Make sure PORT_NUMBER in valFile.h and portNumber in gui.py are the same 
4. Open two terminal windows
5. In one terminal window run the GUI: 
    $ python3 gui.py
6. In the other terminal window compile valFile.cpp AND BLEService.cpp (they must be compiled together or will not link):
    $ g++ -std=c++17 -Wall -pedantic -o validatorFile BLEService.cpp valFile.cpp
7. Run the executable:
    $ ./validatorFile


Run GUI and Validator on different machines
1. Ensure both machines are connected to the same network
2. Get the IP address of the machine that will run the GUI (server)
    -To get IP address of a Raspberry Pi from Mac Terminal:
        $ ping raspberrypi.local 
    -To get IP address of Raspberry Pi from its own terminal:
        $ hostname -I
    -To get IP address of a Mac machine from Mac Terminal:
        $ ipconfig getifaddr en0
3. In gui.py change IPAddress variable to the IP address of the server
2. In valFile.h change SERVER_ADDR to the IP address of the server
3. Make sure PORT_NUMBER in valFile.h and portNumber in gui.py are the same 
4. On one machine run the GUI: 
    $ python3 gui.py
6. On the other machine compile valFile.cpp AND BLEService.cpp (they must be compiled together or will not link):
    $ g++ -std=c++17 -Wall -pedantic -o validatorFile BLEService.cpp valFile.cpp
7. Run the executable:
    $ ./validatorFile


Things left undone:
1. Within BLEService.cpp, I think it would be beneficial to store valid beacon address and rssi and scan twice more,
    only taking another 800ms, to ensure this is the closest beacon, then pass to valFile.cpp. This would slow the proccess down.
    
2. Within valFile.cpp, there are functions called InitRecentlyProcessedAddrs() and UpdateRecentlyProcessedAddrs(). These serve 
    to block a beacon from being processed for a cetain amount of time (PROCD_WAIT_TIME), after its initial process. This handles
    the situation that may occur if a patron enters through the gate but remains within range of the validator. This was actually 
    another very crucial problem that was not discussed within the scope of the project. Therefore I had to come up with a quick solution.
    I used an unordered_map to store the MAC addresses of recently processed beacons which mapped to the number of iterations of the state
    machine since its process. I believe there is a better solution to this because occasionally this results in a segmentation fault.
    So if a segmentation fault ever occurs while running this program look to UpdateRecentlyProcessedAddrs().

3. Within gui.py, there are two things that I wish were better. One is the scalability of the images and texts used to create the 
    interface. Currently the GUI only supports two options, either displaying on a screen the size of a normal computer or on a screen
    about half of that size, which the program will decide on its own based on the size of the screen. I would like for the GUI to be 
    scalable to all screens sizes and have the GUI dynamically modify fonts and image sizes. Secondly, I would like to have timed the
    GUI dynamically. Meaning different times eloted while different screens were displayed. And even checking to see of there is a waiting 
    request for connection from valFile.cpp and the shortening the time for all. 