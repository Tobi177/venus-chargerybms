import QtQuick 1.1
import com.victron.velib 1.0
import "utils.js" as Utils


OverviewPage {
	id: root

	property string solarchargerPrefix: "com.victronenergy.solarcharger.ttyO2"
	property string batteryPrefix: "com.victronenergy.battery.ttyO4"
	property string chargeryBMSPrefix: "com.victronenergy.battery.ttyCHGBMS01"
	property VBusItem totalPower: VBusItem { bind: Utils.path(solarchargerPrefix, "/Yield/Power") }
	property VBusItem voltage: VBusItem { bind: Utils.path(solarchargerPrefix, "/Pv/V") }

	title: qsTr("System Overview")

	function remainingTime(time, returninfinite) {

		if (!time) {
			if (returninfinite == 1) {
				return "Infinite";
			} else {
				return "--";
			}
		}

		var secs = Math.round(time)
		var days = Math.floor(secs / 86400);
		var hours = Math.floor((secs - (days * 86400)) / 3600);
		var minutes = Math.floor((secs - (hours * 3600)) / 60);
		var seconds = Math.floor(secs - (minutes * 60));

		if (days > 0)
			return qsTr("%1d %2h").arg(days).arg(hours);
		if (hours)
			return qsTr("%1h %2m").arg(hours).arg(minutes);
		if (minutes)
			return qsTr("%1m %2s").arg(minutes).arg(seconds);

		return qsTr("%1s").arg(seconds);
	}

	function formatTime(minutes)
	{
		if (minutes === undefined)
			return "--:--"

		return Math.floor(minutes / 60) + ":" + Utils.pad(minutes % 60, 2)
	}

	function get_current()
	{
		if (!voltage.value || !totalPower.valid)
			return undefined
		return totalPower.value / voltage.value
	}	


	Column {

		Rectangle {
			id: overviewRectangle
			width: 480
			height: 28
			color: "#4789d0"

			Timer {
				id: wallClock
				running: true
				repeat: true
				interval: 1000
				triggeredOnStart: true
				onTriggered: time = Qt.formatDateTime(new Date(), "hh:mm:ss")
				property string time
			}
			
			MbTextDescriptionTOBO {
				anchors {
					left: overviewRectangle.left; leftMargin: 8
					verticalCenter: parent.verticalCenter
				}
				text: "System Overview"
			}
				
			Text { 
					anchors {
						right: overviewRectangle.right; rightMargin: 8
						verticalCenter: parent.verticalCenter
					}
			       color: "#ffffff"
				   font.pointSize: 18
				   font.bold: true
				   text: wallClock.time
				 }
		}


		Rectangle {
			id: batteryRectangle

			width: 480
			height: 70
			color: "#2cc36b"
			
			VBusItem {
				id: batteryTimeToGo
				bind: Utils.path(batteryPrefix, "/TimeToGo")
			}

			VBusItem {
				id: batteryTimeLastFullCharge
				bind: Utils.path(batteryPrefix, "/History/TimeSinceLastFullCharge")
			}

			MbItemRowTOBO {
				id: batterySoc
				description: qsTr("Soc | Used | Time")
				
				values: [
					MbTextBlock { item.bind: Utils.path(batteryPrefix, "/Soc"); item.unit: "%"; item.decimals: 1; width: 85; height: 25 },
					MbTextBlock { item.bind: Utils.path(batteryPrefix, "/ConsumedAmphours"); width: 85; height: 25 },
					MbTextBlock { item.text: remainingTime(batteryTimeToGo.value); width: 85; height: 25 }
				]
			}

			MbItemRowTOBO {
				id: batteryLoad
			 	anchors.top: batterySoc.bottom
				description: qsTr("Battery (V/A/W)")
				values: [
					MbTextBlock { item.bind: Utils.path(batteryPrefix, "/Dc/0/Voltage"); width: 85; height: 25 },
					MbTextBlock { item.bind: Utils.path(batteryPrefix, "/Dc/0/Current"); width: 85; height: 25 },
					MbTextBlock { item.bind: Utils.path(batteryPrefix, "/Dc/0/Power"); width: 85; height: 25 }
				]
			}
		}


		Rectangle {
			id: pvRectangle

			width: 480
			height: 105
			color: "#FF2D2D"

			MbItemRowTOBO {
				id : pvStateDisplay
				description: qsTr("State | Max (V/W)")

				SystemState {
					id: pvState
					bind: Utils.path(solarchargerPrefix, "/State")
				}

				values: [
					MbTextBlock { item.text: pvState.text; width: 85; height: 25 },
					MbTextBlock { item.bind: Utils.path(solarchargerPrefix, "/History/Daily/0/MaxPvVoltage"); item.decimals: 2; item.unit: "V"; width: 85; height: 25 },
					MbTextBlock { item.bind: Utils.path(solarchargerPrefix, "/History/Daily/0/MaxPower"); item.unit: "W"; width: 85; height: 25 }
				]
			}
			
			MbItemRowTOBO {
				id : pvDisplay
			 	anchors.top: pvStateDisplay.bottom
				description: qsTr("Solar (V/A/W)")

				values: [
					MbTextBlock { item.bind: Utils.path(solarchargerPrefix, "/Pv/V"); width: 85; visible: true; height: 25 },
					MbTextBlock { item.value: get_current(); item.decimals: 1; item.unit: "A"; width: 85; visible: true; height: 25 },
					MbTextBlock { item.bind: Utils.path(solarchargerPrefix, "/Yield/Power"); width: 85; height: 25 }
				]
			}

			MbItemRowTOBO {
				id : pvYield
			 	anchors.top: pvDisplay.bottom
				description: qsTr("Yield (Tod/D-1/D-2)")

				values: [
					MbTextBlock { item.bind: Utils.path(solarchargerPrefix, "/History/Daily/0/Yield"); width: 85; visible: true; height: 25 },
					MbTextBlock { item.bind: Utils.path(solarchargerPrefix, "/History/Daily/1/Yield"); width: 85; height: 25 },
					MbTextBlock { item.bind: Utils.path(solarchargerPrefix, "/History/Daily/2/Yield"); width: 85; height: 25 }
				]
			}

		}

		Rectangle {
			id: bmsRectangle

			width: 480
			height: 70
			color: "#404040"

			MbItemRowTOBO {
				id : bmsCellView1
				description: qsTr("Cells (Min/Max/Diff)")
				values: [
					MbTextBlock { item.bind: Utils.path(chargeryBMSPrefix, "/Voltages/Min"); width: 85; height: 25 },
					MbTextBlock { item.bind: Utils.path(chargeryBMSPrefix, "/Voltages/Max"); width: 85; height: 25 },
					MbTextBlock { item.bind: Utils.path(chargeryBMSPrefix, "/Voltages/Diff"); width: 85; height: 25 }
				]
			}
			
			MbItemRowTOBO {
				id : bmsCellView2
			 	anchors.top: bmsCellView1.bottom
				description: qsTr("Voltage | Temp (1/2)")
				values: [
					MbTextBlock { item.bind: Utils.path(chargeryBMSPrefix, "/Voltages/Sum"); width: 85; height: 25 },
					MbTextBlock { item.bind: Utils.path(chargeryBMSPrefix, "/Raw/Info/Temp/Sensor1"); width: 85; height: 25; item.decimals: 1; item.unit: "°C" },
					MbTextBlock { item.bind: Utils.path(chargeryBMSPrefix, "/Raw/Info/Temp/Sensor2"); width: 85; height: 25; item.decimals: 1; item.unit: "°C" }
				]
			}	

		}

	}

	
}


		
