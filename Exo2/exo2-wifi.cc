/* -*- Mode:C++; c-file-style:"gnu"; indent-tabs-mode:nil; -*- */
/*
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License version 2 as
 * published by the Free Software Foundation;
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include "ns3/basic-energy-source-helper.h"
#include "ns3/command-line.h"
#include "ns3/config.h"
#include "ns3/double.h"
#include "ns3/flow-monitor-helper.h"
#include "ns3/flow-monitor-module.h"
#include "ns3/internet-module.h"
#include "ns3/log.h"
#include "ns3/mobility-module.h"
#include "ns3/names.h"
#include "ns3/on-off-helper.h"
#include "ns3/packet-sink-helper.h"
#include "ns3/ssid.h"
#include "ns3/string.h"
#include "ns3/udp-client-server-helper.h"
#include "ns3/udp-server.h"
#include "ns3/wifi-radio-energy-model-helper.h"
#include "ns3/wifi-radio-energy-model.h"
#include "ns3/yans-wifi-channel.h"
#include "ns3/yans-wifi-helper.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("template");

int main(int argc, char *argv[]) {

    uint32_t num_nodes = 10;

    // Configuration du nombre de noeuds à partir de la ligne de commande
    CommandLine cmd;
    cmd.AddValue("num_nodes", "Number of nodes", num_nodes);
    cmd.Parse(argc, argv);

    // Configuration des noeuds et de l'AP
    NodeContainer ap;
    ap.Create(1);
    NodeContainer nodes;
    nodes.Create(num_nodes);

    // Configuration des positions des noeuds et de l'AP
    MobilityHelper mobility;
    mobility.SetPositionAllocator(
        "ns3::RandomDiscPositionAllocator", "X", DoubleValue(0.0), "Y",
        DoubleValue(0.0), "Rho",
        StringValue("ns3::UniformRandomVariable[Min=0|Max=10]"));
    mobility.SetMobilityModel("ns3::ConstantPositionMobilityModel");
    mobility.Install(nodes);
    mobility.Install(ap);

    // Configuration du canal Wi-Fi
    WifiHelper wifiHelper;
    wifiHelper.SetStandard(WIFI_STANDARD_80211ac);
    wifiHelper.SetRemoteStationManager("ns3::IdealWifiManager");

    YansWifiChannelHelper wifiChannel;
    wifiChannel.SetPropagationDelay("ns3::ConstantSpeedPropagationDelayModel");
    wifiChannel.AddPropagationLoss("ns3::RangePropagationLossModel");

    YansWifiPhyHelper wifiPhy;
    wifiPhy.SetChannel(wifiChannel.Create());

    WifiMacHelper wifiMac;
    // configuration du point d'accès
    Ssid ssid = Ssid("rsf-marra");
    wifiMac.SetType("ns3::ApWifiMac", "Ssid", SsidValue(ssid));
    NetDeviceContainer apDevices = wifiHelper.Install(wifiPhy, wifiMac, ap);

    // configuration des noeuds
    wifiMac.SetType("ns3::StaWifiMac", "Ssid", SsidValue(ssid), "ActiveProbing",
                    BooleanValue(true));
    NetDeviceContainer nodeDevices =
        wifiHelper.Install(wifiPhy, wifiMac, nodes);

    // Configuration des adresses IP
    InternetStackHelper stack;
    stack.Install(ap);
    stack.Install(nodes);

    Ipv4AddressHelper address;
    address.SetBase("10.0.0.0", "255.255.255.0");
    Ipv4InterfaceContainer apInterfaces = address.Assign(apDevices);
    Ipv4InterfaceContainer nodeInterfaces = address.Assign(nodeDevices);

    // configuration du model energy
    BasicEnergySourceHelper basicSourceHelper;
    WifiRadioEnergyModelHelper radioEnergyHelper;

    basicSourceHelper.Set("BasicEnergySourceInitialEnergyJ",
                          DoubleValue(10000)); // Energy in J
    basicSourceHelper.Set("BasicEnergySupplyVoltageV", DoubleValue(3.3));

    radioEnergyHelper.Set("TxCurrentA", DoubleValue(0.028));
    radioEnergyHelper.Set("SleepCurrentA", DoubleValue(0.0000015));
    radioEnergyHelper.Set("RxCurrentA", DoubleValue(0.0112));

    radioEnergyHelper.SetTxCurrentModel("ns3::ConstantLoraTxCurrentModel",
                                        "TxCurrent", DoubleValue(0.028));

    // install source on end devices' nodes
    EnergySourceContainer sources = basicSourceHelper.Install(nodes);
    Names::Add("/Names/EnergySource", sources.Get(0));

    // install device model
    DeviceEnergyModelContainer deviceModels =
        radioEnergyHelper.Install(nodeDevices, sources);

    // Configuration du trafic UDP

    // création d'un serveur UDP
    uint16_t port = 50000;

    Address sinkLocalAddress(
        InetSocketAddress(apInterfaces.GetAddress(0), port));

    PacketSinkHelper sinkHelper("ns3::UdpSocketFactory", sinkLocalAddress);
    ApplicationContainer sinkApp = sinkHelper.Install(ap.Get(0));

    sinkApp.Start(Seconds(1.0));
    sinkApp.Stop(Seconds(30.0));

    // création d'un client UDP
    OnOffHelper clientHelper("ns3::UdpSocketFactory", Address());
    clientHelper.SetAttribute("Remote", AddressValue(InetSocketAddress(
                                            apInterfaces.GetAddress(0), port)));
    clientHelper.SetConstantRate(DataRate("2Mb/s"), 1472);

    ApplicationContainer clientApps = clientHelper.Install(nodes);
    clientApps.Start(Seconds(1.0));
    clientApps.Stop(Seconds(30.0));

    // création d'une trace wireshark pour la station avec en-tête radio
    /*wifiPhy.SetPcapDataLinkType(WifiPhyHelper::DLT_IEEE802_11_RADIO);
    wifiPhy.EnablePcap("template", apDevices);*/

    // Configuration du moniteur de flux
    FlowMonitorHelper flowmonitor;
    Ptr<FlowMonitor> monitor = flowmonitor.InstallAll();

    // Lancement de la simulation
    Simulator::Stop(Seconds(30.0));
    Simulator::Run();

    // Récupération des statistiques
    monitor->CheckForLostPackets();
    FlowMonitor::FlowStatsContainer stats = monitor->GetFlowStats();

    uint32_t paquets_envoyes = 0;
    uint32_t paquets_recus = 0;
    double latence_moyenne = 0;
    for (auto it = stats.begin(); it != stats.end(); ++it) {

        // Récuperation de la latence moyenne des paquets reçus
        latence_moyenne +=
            it->second.delaySum.GetSeconds() / it->second.rxPackets;

        // Récuperation du nombre de paquets envoyés et reçus
        paquets_envoyes += it->second.txPackets;
        paquets_recus += it->second.rxPackets;
    }

    // Récuperation de la consommation énergétique pour chaque device
    double consommation_energetique = 0.0;
    for (auto iter = deviceModels.Begin(); iter != deviceModels.End(); iter++) {
        consommation_energetique += (*iter)->GetTotalEnergyConsumption();
    }

    std::cout << "Latence moyenne: " << latence_moyenne << std::endl;
    std::cout << "Paquets envoyés: " << paquets_envoyes << std::endl;
    std::cout << "Paquets reçus: " << paquets_recus << std::endl;
    std::cout << "Taux de succès des paquets (PDR): "
              << ((double)paquets_recus / (double)paquets_envoyes) * 100 << "%"
              << std::endl;
    std::cout << "Consommation énergétique totale: " << consommation_energetique
              << std::endl;
    std::cout << "Consommation énergétique moyenne: "
              << consommation_energetique / num_nodes << std::endl;
    std::cout << "Simulation terminée" << std::endl;
    Simulator::Destroy();

    return 0;
}
