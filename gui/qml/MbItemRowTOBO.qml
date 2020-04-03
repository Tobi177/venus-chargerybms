import QtQuick 1.1

/**
 * Perhaps not the most brilliant name, but a MbItemRow refers to a MenuItem
 * with a short description at the left side and the values(s) at  the right
 * side. It is kept out MbItem itself so top / down and slider like items,
 * which do not have a concept of left and right can directly derive from MbItem.
 * Since an arbitrary amount of Items can be inside a row no special Items have
 * to exist for 2 values, 3 value etc specific items.
 *
 *		MbItemRow {
 *			description: "bla"
 *			MbTextValue { bind: qwacsPrefix + "/AC/L3/Power" }
 *			MbTextValue { text: "test3" }
 *		}
 *
 */

MbItem {
	id: root
	editable: false

	property alias description: _description.text
	default property alias values: _values.data

	// The description of the values shown
	MbTextDescriptionTOBO {
		id: _description
		anchors {
			left: root.left; leftMargin: style.marginDefault
			verticalCenter: parent.verticalCenter
		}
	}

	// The actual values
	MbRow {
		id: _values

		anchors {
			right: parent.right; rightMargin: style.marginDefault
			verticalCenter: parent.verticalCenter
		}
	}
}
