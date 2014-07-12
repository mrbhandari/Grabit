
    $("#mainPage").on("pageshow", function(e) {
    console.log("Ready to bring the awesome.");
    var sugList = $("#suggestions");

    $("#hcpcs").on("input", function(e) {
        jQuery(document).ready(function($){


        
        var text = $(this).val();
        if(text.length < 1) {
            sugList.html("");
            sugList.listview("refresh");
        } else {

            $.get("hcpcs_autosuggest/", {search:text}, function(res,code) {
                var str = "";
                console.log(res, code)
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
     });