//
// Copyright (C) 2013 OpenSim Ltd.
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

#include "inet/common/INETDefs.h"
//#include "inet/linklayer/common/MACAddress.h"
#include "src/linklayer/common/HLMACAddress.h"


#ifndef GA3_SRC_LINKLAYER_ETHERNET_GA3SWITCH_IHLMACADDRESSTABLE_H_
#define GA3_SRC_LINKLAYER_ETHERNET_GA3SWITCH_IHLMACADDRESSTABLE_H_

using namespace inet;
namespace GA3 {

class IHLMACAddressTable
{
  public:
    virtual bool isPortInTable(int portno, unsigned int vid = 0) = 0;

    /**
     * @brief For a known arriving port, V-TAG and destination MAC. It finds out the port where relay component should deliver the message
     * @param address MAC destination
     * @param vid VLAN ID
     * @return Output port for address, or -1 if unknown.
     */
    virtual int getPortForAddress(HLMACAddress& address, unsigned int vid = 0) = 0;

    /**
     * @brief Register a new MAC address at HLMACTable.
     * @return True if refreshed. False if it is new.
     */
    virtual bool updateTableWithAddress(int portno, HLMACAddress& address, unsigned int vid = 0) = 0;

    /**
     *  @brief Clears portno cache
     */
    virtual void flush(int portno) = 0;

    /**
     *  @brief Prints cached data
     */
    virtual void printState() = 0;

    /**
     * @brief Copy cache from portA to portB port
     */
    virtual void copyTable(int portA, int portB) = 0;

    /**
     * @brief Remove aged entries from a specified VLAN
     */
    virtual void removeAgedEntriesFromVlan(unsigned int vid = 0) = 0;
    /**
     * @brief Remove aged entries from all VLANs
     */
    virtual void removeAgedEntriesFromAllVlans() = 0;

    /*
     * It calls removeAgedEntriesFromAllVlans() if and only if at least
     * 1 second has passed since the method was last called.
     */
    virtual void removeAgedEntriesIfNeeded() = 0;

    /**
     * For lifecycle: clears all entries from the vlanHLMACTable.
     */
    virtual void clearTable() = 0;

    /*
     * Some (eg.: STP, RSTP) protocols may need to change agingTime
     */
    virtual void setAgingTime(simtime_t agingTime) = 0;
    virtual void resetDefaultAging() = 0;
};

} // namespace GA3

#endif // ifndef GA3_SRC_LINKLAYER_ETHERNET_GA3SWITCH_IHLMACADDRESSTABLE_H_

