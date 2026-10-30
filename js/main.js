// 訪問者カウンター（それっぽく見せるだけ）
// 基準値に、2011年の最終更新日からの経過日数ぶん少しずつ足していく
(function () {
  var el = document.getElementById("counter");
  if (!el) return;

  var base = 44170;
  var since = new Date(2011, 10, 2);
  var days = Math.floor((Date.now() - since.getTime()) / 86400000);
  var count = base + Math.max(0, days) * 3;

  el.textContent = String(count).padStart(6, "0");
})();
