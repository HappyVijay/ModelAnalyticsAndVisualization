var flag = 1;
$('#navbarbtn').click(function (e) { 
    $('#navone').toggle();;
    if (flag == 1){
        $(".faqcontainer").css({paddingLeft:"0px"});
        $("#container").width("100%");
        flag =  0
    }
    else{
        $(".faqcontainer").css({paddingLeft:"200px"});
        $("#container").width("75%");
        flag = 1
    }
});
$(".nav-item").on("click", function(){
    console.log("Me")
    $(".nav").find(".active").removeClass("active");
    $(this).addClass("active");
 });