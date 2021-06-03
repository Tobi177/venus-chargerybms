import QtQuick 1.1
import com.victron.velib 1.0

MbPage {
	id: root

	property variant service
	property string bindPrefix

	property VBusItem hasSettings: VBusItem { bind: service.path("/Settings/HasSettings") }
	property VBusItem productId: VBusItem { bind: service.path("/ProductId") }
	property VBusItem socItem: VBusItem { bind: service.path("/Info/Soc") }
	property VBusItem voltItem: VBusItem { bind: service.path("/Voltages/Sum") }
	property VBusItem currentItem: VBusItem { bind: service.path("/Info/Current") }

	title: service.description
	summary: [socItem.text, voltItem.text, currentItem.text ]

	model: VisualItemModel {

		MbItemRow {
			id: battvol
			description: qsTr("Battery Status")
			values: [
				MbTextBlock { item { bind: service.path("/Info/CurrentMode"); } height: 25 },
				MbTextBlock { item { bind: service.path("/Info/Current"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Voltages/Sum"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("State of Charge")
			values: [
				MbTextBlock { item { bind: service.path("/Voltages/BatteryCapacityWH"); } height: 25 },
				MbTextBlock { item { bind: service.path("/Voltages/BatteryCapacityAH"); }  width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Info/Soc"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("Relays (Charge/Discharge)")
			values: [
				MbTextBlock { item { bind: service.path("/Info/ChargeRelayStatus"); }  width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Info/DischargeRelayStatus"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("Temperature Sensors (1/2)")
			values: [
				MbTextBlock { item { bind: service.path("/Raw/Info/Temp/Sensor1"); } width: 70; height: 25; item.decimals: 1; item.unit: "°C" },
				MbTextBlock { item { bind: service.path("/Raw/Info/Temp/Sensor2"); } width: 70; height: 25; item.decimals: 1; item.unit: "°C" }
			]
		}


		MbItemRow {
			description: qsTr("Voltages (Min/Max/Diff)")
			values: [
				MbTextBlock { item { bind: service.path("/Voltages/Min"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Voltages/Max"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Voltages/Diff"); } width: 70; height: 25 }
			]
		}


		MbItemRow {
			description: qsTr("Impedances (Min/Max/Sum)")
			values: [
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Min"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" },
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Max"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" },
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Sum"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" }
			]
		}


		MbItemRow {
			description: qsTr("Data Timestamp")
			values: [
				MbTextBlock { item { bind: service.path("/Info/UpdateTimestamp"); } width: 215; height: 25 }
			]
		}


		MbSubMenu {
			description: qsTr("Cell Voltages")
			subpage: Component {
				PageBatteryChargeryBMSVoltages {
					bindPrefix: service.path("")
				}
			}
		}

		MbSubMenu {
			description: qsTr("Cell Impedances")
			subpage: Component {
				PageBatteryChargeryBMSImpedances {
					bindPrefix: service.path("")
				}
			}
		}


		MbSubMenu {
			description: qsTr("Device")
			subpage: Component {
				PageDeviceInfo {
					title: qsTr("Device")
					bindPrefix: service.path("")
				}
			}
		}

	}
}
