console.log(test)
$("#mainPage").on("pageshow", function(e) {
    console.log("Ready to bring the awesome.");
    var sugList = $("#suggestions");

    $("#searchField").on("input", function(e) {
        var text = $(this).val();
        if(text.length < 1) {
            sugList.html("");
            sugList.listview("refresh");
        } else {
            $.get("service.cfc?method=getSuggestions", {search:text}, function(res,code) {
                var str = "";
                for(var i=0, len=res.length; i<len; i++) {
                    str += "<li>"+res[i]+"</li>";
                }
                sugList.html(str);
                sugList.listview("refresh");
                console.dir(res);
            },"json");
        }
    });

});