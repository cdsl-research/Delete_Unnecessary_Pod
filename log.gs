function onMyEdit(e) {
	var logSheetName = 'Log';

	var ss = SpreadsheetApp.getActiveSpreadsheet();

	var ssName = ss.getName();

	var sheet = ss.getActiveSheet();

	var sheetName = sheet.getName();

	if (sheetName == logSheetName) {
		return;
	}


	var range = sheet.getActiveRange();

	var rowIndex = range.getRowIndex();

	var colIndex = range.getColumnIndex();

	var v = sheet.getRange(rowIndex, colIndex, 1, 1).getValue();

	if (v == '') {
		v = 'Delete';
	}





	var logSheet = ss.getSheetByName(logSheetName);

	logSheet.insertRowBefore(1);


	logSheet.getRange(1, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');
	logSheet.getRange(1, 1).setValue(new Date());

	logSheet.getRange(1, 2).setValue(sheet.getRange(rowIndex, 2, 1, 1).getValue());

  logSheet.getRange(1, 3).setNumberFormat('@');
	logSheet.getRange(1, 3).setValue(sheet.getRange(1, colIndex, 1, 1).getValue());

	logSheet.getRange(1, 4).setNumberFormat('@');  
	logSheet.getRange(1, 4).setValue(v);
}

