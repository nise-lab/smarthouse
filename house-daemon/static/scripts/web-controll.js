var webControll = {};
(function(ns) {
  var WATCH_INTERVAL_MSEC = 1000;
	var AJAX_DISACTIVE_CLASS	= 'btn-danger';
	var AJAX_ACTIVE_CLASS	= 'btn-default';
  ns.sections = {};
  ns.buttonsBySections = {};
  // { "room": { "brigter": jQueryObject,  ...}, ... }

  window.addEventListener('load', function () {
    $.ajax({
      type: 'GET',
      url: "/sections",
      dataType: 'json',
    }).done(function(sections){
      ns.sections = sections; // section を更新
      ns.createButtonsBySections(); // ボタンを集めとく
      ns.setUpdateCurrentCondition(); // インターバルセット
    }).fail(function(sections){
      console.log("sections の取得に失敗している．")
    });
  });

  ns.createButtonsBySections = function() {
    // buttonsBySections を作る
    $.each(ns.sections, function(sectionName, section) {
      buttons = {};

      $.each(section["conditions"], function(conditionName, condition) {
        conditionButton = $("#" + sectionName + "-" + conditionName);
        buttons[conditionName] = conditionButton;
      });

      ns.buttonsBySections[sectionName] = buttons;
    });
  };

  ns.setUpdateCurrentCondition = function() {
    $.ajax({
      type: 'GET',
      url: "/sections",
      dataType: 'json',
    }).done(function(sections){
      ns.sections = sections;
      ns.updateButtons();
    }).fail(function(sections){
      console.log("sections の取得に失敗している．")
    });

    setTimeout(ns.setUpdateCurrentCondition, WATCH_INTERVAL_MSEC);
  };

  ns.updateButtons = function() {
    $.each(ns.sections, function(sectionName, section) {
      var currentCondition = section["current_condition"];
      $.each(
        ns.buttonsBySections[sectionName],
        function(conditionName, button){
          // 現在の状態をもとに，ボタンの状態を更新
          if(currentCondition == conditionName) {
            // 現在の状態を示すボタンは Ajax ディスアクティブ
            button.removeClass(AJAX_ACTIVE_CLASS);
            button.addClass(AJAX_DISACTIVE_CLASS);

            // ここで，ボタンのイベントを削除
            button.off();
          } else {
            // 現在の状態以外を示すボタンは Ajax アクティブ
            button.removeClass(AJAX_DISACTIVE_CLASS);
            button.addClass(AJAX_ACTIVE_CLASS);

            // ここで，ボタンにイベントを登録
            button.off();
            button.on(
              'click',
              { sectionName: sectionName, conditionName: conditionName, button: button },
              ns.updateCondition
            );
          }
      });
    });
  };

  ns.updateCondition = function(event) {
    // コンディションを変更するための関数
    var sectionName = event.data.sectionName;
    var conditionName = event.data.conditionName;
    var button = event.data.button;
    $.ajax({
      type: 'PUT',
      url: "/sections/" + sectionName + "/condition",
      headers: { 'Content-Type': 'application/json' },
      data: JSON.stringify(
        { "condition": conditionName }
      ),
      dataType: 'json',
    }).done(function(result){
      console.log()
    }).fail(function(sections){
      console.log("conditon の変更に失敗した．")
    });
    button.off();
  }

})(webControll);
