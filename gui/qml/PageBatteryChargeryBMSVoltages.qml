import QtQuick 1.1
import com.victron.velib 1.0
import "utils.js" as Utils

MbPage {
	id: root

	property string bindPrefix
	property BatteryDetails details: BatteryDetails { bindPrefix: root.bindPrefix }
	title: service.description + " | Cell Voltages"

	model: VisualItemModel {

		MbItemRow {
			description: qsTr("Voltages (Min/Max/Diff)")
			values: [
				MbTextBlock { item { bind: service.path("/Voltages/Min"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Voltages/Max"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Voltages/Diff"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("Cells (1/2/3)")
			values: [
				MbTextBlock { item { bind: service.path("/Voltages/Cell1"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Voltages/Cell2"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Voltages/Cell3"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("Cells (4/5/6)")
			values: [
				MbTextBlock { item { bind: service.path("/Voltages/Cell4"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Voltages/Cell5"); } width: 70; height: 25 },
				MbTextBlock { item { bind: service.path("/Voltages/Cell6"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("Charge End Voltage")
			values: [
				MbTextBlock { item { bind: service.path("/Info/ChargeEndVoltage"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("Data Timestamp")
			values: [
				MbTextBlock { item { bind: service.path("/Voltages/UpdateTimestamp"); } width: 215; height: 25 }
			]
		}

	}
}
