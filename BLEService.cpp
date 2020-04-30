#include "BLEService.h"

//map of all MAC addrs and their RSSI values in a scan
std::unordered_map<std::string, int> foundAddrs;                        //could make local var in BLEService and pass to parser functions

//set of predefined MAC addrs valid for processing
std::unordered_set<std::string> desiredAddrs; 


//Is called within valFile.cpp main 
void InitDesiredAddrs()
{
    desiredAddrs.insert("04:91:62:97:8B:37");
    desiredAddrs.insert("04:91:62:97:8B:38");
    desiredAddrs.insert("04:91:62:97:8B:39");
    //more addresses can be added here
}


//resets BLE 
void BLEReset()
{
    system("sudo hciconfig hci0 down");
    system("sudo hciconfig hci0 up");
}


//parses the terminal output by newline char first
//then parses those lines by space to separate the name and addr
void ParseHcitoolLescan(std::string terminalOutput) 
{
    std::stringstream ss(terminalOutput);
    std::string to;

    if(!terminalOutput.empty())
    {
        while(getline(ss,to,'\n'))
        {
           std::stringstream to_ss(to);
           std::string finalAddress;

           if(!to.empty())
           {
               while(getline(to_ss,finalAddress,' '))
               {
                   if(finalAddress.size() == MAC_ADDR_LEN)
                   {
                        foundAddrs[finalAddress] = 0;       
                   }
               }
           }
        }
    }
}


void ParseBtmgmtFind(std::string terminalOutput) 
{
    std::stringstream lineStream(terminalOutput);
    std::string lineHolder;

    std::string devAddr;
    std::string devRssi;

    if(!terminalOutput.empty())
    {
        while(getline(lineStream, lineHolder))
        {
            std::stringstream tokenStream(lineHolder);
            std::string tokenHolder;
            std::vector<std::string> line;

            while(getline(tokenStream, tokenHolder, ' '))       //would like to break if [1] not "dev_found" instead of tokenizing whole string no matter what
            {
                line.push_back(tokenHolder);
            }
            
            if(line[1].compare("dev_found:") == 0)              //if equal meaning correct line with the info
            {
                devAddr = line[MAC_INDEX_BT];                   //addr index in cmd line output
                devRssi = line[RSSI_INDEX_BT];                  //rssi index in cmd line output

                devRssi = devRssi.erase(0, 1);                  //erase '-' in front of rssi to get only int value cmd output: "-22" we want "22"
                int rssi = stoi(devRssi);                       //cast to int

                foundAddrs[devAddr] = rssi;                     //save addr and rssi in map
            }
        }
    }
}


std::string GetStdoutFromCommand(std::string cmd) 
{
    std::string data;
    FILE * stream;
    const int max_buffer = 256;
    char buffer[max_buffer];
    cmd.append(" 2>&1");

    BLEReset();

    stream = popen(cmd.c_str(), "r");

    if(stream) 
    {
        while(!feof(stream))
        {
            if(fgets(buffer, max_buffer, stream) != NULL) 
            {
                data.append(buffer);
            }
	    }
        pclose(stream);
    }
    return data;
}


std::string BLEService()
{
    //may of all MAC addrs and their RSSI found in the scan that are ready to be processed
    std::unordered_map<std::string, int> approvedAddrs; 

    bool beaconFound = false;

    //iterators
    std::unordered_map<std::string, int>:: iterator foundAddrsItr;
    std::unordered_set<std::string>:: iterator desiredAddrsItr;
    std::unordered_map<std::string, int>:: iterator approvedAddrsItr;
    
    std::string cmnd = GetStdoutFromCommand(BTMGMT_FIND);                                               //gets all output from command line
    
    ParseBtmgmtFind(cmnd);                                                                              //gets desired output into foundAddrs

    for(foundAddrsItr = foundAddrs.begin(); foundAddrsItr != foundAddrs.end(); foundAddrsItr++)         //iterates through all of the addrs found in the scan
    {
        desiredAddrsItr = desiredAddrs.find(foundAddrsItr->first);                                      //searches for found addr in the set of predefined addrs for a match
        if(desiredAddrsItr != desiredAddrs.end() && foundAddrsItr->second < 55)                  
        {
            approvedAddrs[foundAddrsItr->first] = foundAddrsItr->second;                                //adds matches and their rssi value to map of approved addrs
            beaconFound = true;
        }
    }
    foundAddrs.clear();                                                                                 //clears all found addrs for next scan

    //RSSI Check
    if(beaconFound)
    {
        int currRssi, minRssi = (approvedAddrs.begin())->second;                                        //set the minimum rssi to the first approved addrs rssi and compare from there
        std::string minKey = (approvedAddrs.begin())->first;

        for(approvedAddrsItr = approvedAddrs.begin(); approvedAddrsItr != approvedAddrs.end(); approvedAddrsItr++) //iterate through approved addrs
        {
            currRssi = approvedAddrsItr->second;                                                        //set current rssi to next element

            if(currRssi < minRssi)                                                                      //comapre and switch accordingly to get min rssi out of the approved addrs
            {
                minRssi = currRssi;
                minKey = approvedAddrsItr->first;
            }
        }
        
        approvedAddrs.erase(minKey);                                                                    //may be redundant since approvedAddrs in delecared every function call
        return minKey;
    }
    else
    {
        return NULL_STR;
    }
}
