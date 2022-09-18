import QtQuick 1.1
import com.victron.velib 1.0
import "utils.js" as Utils

MbPage {
	id: root

	property string bindPrefix
	property BatteryDetails details: BatteryDetails { bindPrefix: root.bindPrefix }
	title: service.description + " | Cell Impedances"

	model: VisualItemModel {

		MbItemRow {
			id: currentState1
			description: qsTr("Measured Current")
			values: [
				MbTextBlock { item { bind: service.path("/Impedances/CurrentMode1"); } height: 25 },
				MbTextBlock { item { bind: service.path("/Impedances/Current1"); } width: 70; height: 25 }
			]
		}

		MbItemRow {
			description: qsTr("Min/Max/Avg/Sum")
			values: [
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Min"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" },
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Max"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" },
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Avg"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" },
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Sum"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" }
			]
		}

		MbItemRow {
			description: qsTr("Cells (1/2/3)")
			values: [
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Cell1"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" },
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Cell2"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" },
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Cell3"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" }
			]
		}

		MbItemRow {
			description: qsTr("Cells (4/5/6)")
			values: [
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Cell4"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" },
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Cell5"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" },
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Cell6"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" }
			]
		}

		MbItemRow {
			description: qsTr("Cells (7/8/9)")
			values: [
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Cell7"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" },
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Cell8"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" },
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Cell9"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" }
			]
		}

		MbItemRow {
			description: qsTr("Cells (10/11/12)")
			values: [
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Cell10"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" },
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Cell11"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" },
				MbTextBlock { item { bind: service.path("/Raw/Impedances/Cell12"); } width: 70; height: 25; item.decimals: 1; item.unit: "mΩ" }
			]
		}


		MbItemRow {
			description: qsTr("Data Timestamp")
			values: [
				MbTextBlock { item { bind: service.path("/Impedances/UpdateTimestamp"); } width: 215; height: 25 }
			]
		}

	}
}
