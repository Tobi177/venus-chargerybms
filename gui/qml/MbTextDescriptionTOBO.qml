import QtQuick 1.1

/*
 * Default format for descriptions in the menus typically at the left side.
 * Using default colors and default font as used for description.
 *
 * Note: it is assumed that this objects its parent contains the isCurrentItem
 * property from the ListView (like the MbItem). If that is not the case,
 * isCurrentItem must be set explicitly.
 */

Text {
	property bool isCurrentItem: parent.ListView.isCurrentItem
	property MbStyle style: MbStyle{}

	color: "#ffffff"
	font.family: style.fontFamily
	font.pixelSize: style.fontPixelSize
	font.bold: true
}
