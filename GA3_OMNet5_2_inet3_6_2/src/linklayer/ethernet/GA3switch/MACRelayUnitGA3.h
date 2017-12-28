/*
 * Copyright (C) 2017 Elisa Rojas(1), SeyedHedayat Hosseini(2);
 *                    (1) GIST, University of Alcala, Spain.
 *                    (2) Iran.
 *
 * Main paper:
 * Rojas, Elisa, et al. "GA3: scalable, distributed address assignment
 * for dynamic data center networks." Annals of Telecommunications (2017): 1-10.þ
 * DOI: http://dx.doi.org/10.1007/s12243-017-0569-4
 *
 * Developed in OMNet++5.2, based on INET framework.
 * LAST UPDATE OF THE INET FRAMEWORK: inet3.6.2 @ October 2017
*/


//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with this program.  If not, see http://www.gnu.org/licenses/.
//

#ifndef GA3_SRC_LINKLAYER_ETHERNET_MACRELAYUNITGA3_H
#define GA3_SRC_LINKLAYER_ETHERNET_MACRELAYUNITGA3_H

#include "inet/common/INETDefs.h"

#include "inet/common/lifecycle/ILifecycle.h"
#include "inet/linklayer/ethernet/switch/IMACAddressTable.h"
#include "src/linklayer/ethernet/GA3switch/IHLMACAddressTable.h"

using namespace inet;

namespace GA3 {
class inet::EtherFrame;

class MACRelayUnitGA3 : public cSimpleModule, public ILifecycle
{
  protected:
    // GA3 parameters
    // Switch parameters
    unsigned int broadcastSeed = 0;     //Seed for random broadcasting (to be configured at the *.ini file)

    bool isCoreSwitch = false;
    int corePrefix = -1;            // main core prefix, seted by ned parameter
    HLMACAddress *switchPrio = nullptr; //switch priority
    std::vector<int> corePrefixes;  //other core prefixes
    // port parameters
    int *ports;         // a mapping between port# & id, indexs indicate port#, values indicate IDs for each port
    HLMACAddress **prio = nullptr; // a mapping between port# & highest Priority for each port, indexs indicate port#, values indicate highest Priority for each port

    IHLMACAddressTable *hlmacTable = nullptr;

    //cMessage *startCoreEvent = nullptr;
    cMessage *startPortEvent;
    int startPortQueue = -1;
    double timeBetweenCores, timeBetweenPorts;

    //inet parameters
    IMACAddressTable *addressTable = nullptr;
    int numPorts = 0;

    // Parameters for statistics collection
    long numProcessedFrames = 0;
    long numDiscardedFrames = 0;

    bool isOperational = false;    // for lifecycle

  protected:
    virtual void initialize(int stage) override;
    virtual int numInitStages() const override { return NUM_INIT_STAGES; }
    /**
     * Updates address table with source address, determines output port
     * and sends out (or broadcasts) frame on ports. Includes calls to
     * updateTableWithAddress() and getPortForAddress().
     *
     * The message pointer should not be referenced any more after this call.
     */
    virtual void handleAndDispatchFrame(EtherFrame *frame);

    /**
     * Utility function: sends the frame on all ports except inputport.
     * The message pointer should not be referenced any more after this call.
     */
    virtual void broadcastFrame(EtherFrame *frame, int inputport);

    virtual void generateSendSequence(std::vector<int>& sequence);

    //using in GA3
    void startGA3Process();

    //using in GA3
    virtual void flood(EtherFrame *frame, int inputport);

    //using in GA3
    virtual void startCore(int core,int port);

    //using in GA3
    virtual void receiveMessage(EtherFrame *SetHLMAC,int inputPort);



    /**
     * Calls handleIncomingFrame() for frames arrived from outside,
     * and processFrame() for self messages.
     */
    virtual void handleMessage(cMessage *msg) override;

    /**
     * Writes statistics.
     */
    virtual void finish() override;

    // for lifecycle:

  public:
    virtual bool handleOperationStage(LifecycleOperation *operation, int stage, IDoneCallback *doneCallback) override;

  protected:
    virtual void start();
    virtual void stop();
};

} // namespace GA3

#endif // ifndef GA3_SRC_LINKLAYER_ETHERNET_MACRELAYUNITGA3_H

