//
// Copyright (C) 2006 Levente Meszaros
/*
 * Copyright (C) 2017 Elisa Rojas(1), SeyedHedayat Hosseini(2);
 *                    (1) GIST, University of Alcala, Spain.
 *                    (2) Iran.
 *
 * Main paper:
 * Rojas, Elisa, et al. "GA3: scalable, distributed address assignment
 * for dynamic data center networks." Annals of Telecommunications (2017): 1-10.�
 * DOI: http://dx.doi.org/10.1007/s12243-017-0569-4
 *
 * Developed in OMNet++5.2, based on INET framework.
 * LAST UPDATE OF THE INET FRAMEWORK: inet3.6.2 @ October 2017
*/
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU Lesser General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with this program; if not, see <http://www.gnu.org/licenses/>.
//

#ifndef GA3_SRC_LINKLAYER_ETHERNET_ETHERMACFULLDUPLEXGA3_H
#define GA3_SRC_LINKLAYER_ETHERNET_ETHERMACFULLDUPLEXGA3_H

#include "inet/common/INETDefs.h"

#include "inet/linklayer/ethernet/EtherMACBase.h"

using namespace inet;
namespace GA3 {
/**
 * A simplified version of EtherMAC. Since modern Ethernets typically
 * operate over duplex links where's no contention, the original CSMA/CD
 * algorithm is no longer needed. This simplified implementation doesn't
 * contain CSMA/CD, frames are just simply queued up and sent out one by one.
 */
class EtherMACFullDuplexGA3 : public EtherMACBase
{
  public:
    EtherMACFullDuplexGA3();

  protected:
    virtual int numInitStages() const override { return NUM_INIT_STAGES; }
    virtual void initialize(int stage) override;
    virtual void initializeStatistics() override;
    virtual void initializeFlags() override;
    virtual void handleMessage(cMessage *msg) override;

    // finish
    virtual void finish() override;

    // event handlers
    virtual void handleEndIFGPeriod();
    virtual void handleEndTxPeriod();
    virtual void handleEndPausePeriod();
    virtual void handleSelfMessage(cMessage *msg);

    // helpers
    virtual void startFrameTransmission();
    virtual void processFrameFromUpperLayer(EtherFrame *frame);
    virtual void processMsgFromNetwork(cPacket *pk);
    virtual void processReceivedDataFrame(EtherFrame *frame);
    virtual void processPauseCommand(int pauseUnits);
    virtual void scheduleEndIFGPeriod();
    virtual void scheduleEndPausePeriod(int pauseUnits);
    virtual void beginSendFrames();

    // statistics
    simtime_t totalSuccessfulRxTime;    // total duration of successful transmissions on channel
};

} // namespace GA3

#endif // ifndef GA3_SRC_LINKLAYER_ETHERNET_ETHERMACFULLDUPLEXGA3_H

