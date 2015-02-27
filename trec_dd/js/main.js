now = ".overview";
flagtl = false;
flaggl = false;
flagds = false;
$(document).ready(function(){
	$.ajaxSetup({
		cache: false
	});
	$(".ovlink").click(function(){
		if (now != ".overview"){
			$(now).hide();
			$(".overview").show();
			now = ".overview";
		}
	})
	$(".tllink").click(function(){
		if (now != ".timeline"){
			$(now).hide();
			if (flagtl == false){
				flagtl = true;
				$(".timeline").load("timeline.html section");
			}
			else {
				$(".timeline").show();
			}
			now = ".timeline";
		}
	})
	$(".gllink").click(function(){
		if (now != ".guideline"){
			$(now).hide();
			if (flaggl == false){
				flaggl = true;
				$(".guideline").load("guideline.html section");
			}
			else {
				$(".guideline").show();
			}
			now = ".guideline";
		}
	})
	$(".dslink").click(function(){
		if (now != ".dataset"){
			$(now).hide();
			if (flagds == false){
				flagds = true;
				$(".dataset").load("dataset.html section");
			}
			else {
				$(".dataset").show();
			}
			now = ".dataset";
		}			
	})
})
