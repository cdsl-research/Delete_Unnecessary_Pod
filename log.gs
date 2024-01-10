function onMyEdit(e) {
	//Log保存用シートの名前
	var logSheetName = 'Log';

	// スプレッドシート
	var ss = SpreadsheetApp.getActiveSpreadsheet();
	// スプレッドシート名
	var ssName = ss.getName();

	// 選択シート
	var sheet = ss.getActiveSheet();
	// 選択シート名
	var sheetName = sheet.getName();
	// Logシートなら何もしない
	if (sheetName == logSheetName) {
		return;
	}

	// 選択セル範囲
	var range = sheet.getActiveRange();
	// セル範囲の行番号
	var rowIndex = range.getRowIndex();
	// セル範囲の列番号
	var colIndex = range.getColumnIndex();

	// getRange(始点行, 始点列, 取得する行数, 取得する列数)
	var v = sheet.getRange(rowIndex, colIndex, 1, 1).getValue();
	//内容が空だ
	if (v == '') {
		v = 'Delete';
	}



	//ここからLogシートに書き込み
	//Log保存用シート
	var logSheet = ss.getSheetByName(logSheetName);
	//引数で指定した行の前の行に1行追加
	logSheet.insertRowBefore(1);

	//日付
	logSheet.getRange(1, 1).setNumberFormat('yyyy-mm-dd hh:mm:ss');
	logSheet.getRange(1, 1).setValue(new Date());
	//行番号
	logSheet.getRange(1, 2).setValue(sheet.getRange(rowIndex, 2, 1, 1).getValue());
	//列番号
  logSheet.getRange(1, 3).setNumberFormat('@');
	logSheet.getRange(1, 3).setValue(sheet.getRange(1, colIndex, 1, 1).getValue());
	//変更セルの内容(Stringフォーマットにする)
	logSheet.getRange(1, 4).setNumberFormat('@');  
	logSheet.getRange(1, 4).setValue(v);
}

