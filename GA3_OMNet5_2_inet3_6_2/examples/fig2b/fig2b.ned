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

package GA3.examples.fig2b;

import inet.common.scenario.ScenarioManager;
import inet.examples.httptools.socket.tenserverssocket.ethernetline;
//import inet.common.lifecycle.LifecycleController;
//import inet.linklayer.configurator.L2NetworkConfigurator;
//import inet.linklayer.ieee8021d.tester.STPTester;
import inet.networklayer.configurator.ipv4.IPv4NetworkConfigurator;
//import inet.node.ethernet.EtherSwitch;
import GA3.src.node.EtherSwitchGA3;
import inet.node.inet.StandardHost;
//import inet.node.ethernet.EtherHost;

import ned.DatarateChannel;
import inet.common.misc.ThruputMeteringChannel;

//import GA3.src.node.EtherSwitchGA3;

network fig2b
{
    @display("bgb=693,452");
    types:
        channel C extends DatarateChannel
        {
            delay = 0.1us;
            datarate = 100Mbps;
        }
    submodules:
        host1: StandardHost {
            @display("p=24,274;i=device/pc");
            gates:

                ethg[1];

        }
        host2: StandardHost {
            @display("p=24,341;i=device/pc");
            gates:
                ethg[1];


        }
        host3: StandardHost {
            @display("p=24,418;i=device/pc");
            gates:
                ethg[1];
        }
        host4: StandardHost {
            @display("p=238,268;i=device/pc");
            gates:

                ethg[1];

        }
        host5: StandardHost {
            @display("p=238,341;i=device/pc");
            gates:

                ethg[1];

        }
        host6: StandardHost {
            @display("p=238,411;i=device/pc");
            gates:

                ethg[1];

        }
        switch5: EtherSwitchGA3 {
            parameters:
                @display("p=95,209");
            gates:
                ethg[5];
        }
        switch6: EtherSwitchGA3 {
            parameters:
                @display("p=184,209");
            gates:
                ethg[5];
        }
        switch3: EtherSwitchGA3 {
            parameters:
                @display("p=95,137");
            gates:
                ethg[3];
        }
        switch4: EtherSwitchGA3 {
            parameters:
                @display("p=184,137");
            gates:
                ethg[3];
        }
        switch1: EtherSwitchGA3 {
            parameters:
                @display("p=95,29");
            gates:
                ethg[1];
        }
        switch2: EtherSwitchGA3 {
            parameters:
                @display("p=184,29");
            gates:
                ethg[1];
        }
        configurator: IPv4NetworkConfigurator {
            @display("p=638,69");
        }
        //  l2NetworkConfigurator: L2NetworkConfigurator {
        //    @display("p=799.90625,377.01877");
        //}
        //  lifecycleController: LifecycleController {
        //    @display("p=130.89375,402.75");
        //}
        //       stpTester: STPTester {
        //         @display("p=848.0125,328.9125");
        //   }
        scenarioManager: ScenarioManager {
            @display("p=638,14");
        }
    connections:
        host1.ethg[0] <--> C <--> switch5.ethg[0];
        host2.ethg[0] <--> C <--> switch5.ethg[1];
        host3.ethg[0] <--> C <--> switch5.ethg[2];
        host4.ethg[0] <--> C <--> switch6.ethg[0];
        host5.ethg[0] <--> C <--> switch6.ethg[1];
        host6.ethg[0] <--> C <--> switch6.ethg[2];

        switch5.ethg[3] <--> C <--> switch3.ethg[0];
        switch6.ethg[3] <--> C <--> switch3.ethg[1];
        switch3.ethg[2] <--> C <--> switch1.ethg[0];
        switch2.ethg[0] <--> C <--> switch4.ethg[0];
        switch4.ethg[1] <--> C <--> switch6.ethg[4];
        switch4.ethg[2] <--> C <--> switch5.ethg[4];
        


}



