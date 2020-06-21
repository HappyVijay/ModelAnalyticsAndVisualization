//var columnheaders = []
function clearForm() {
    document.getElementById("form").reset();
}

var columnheaders=[] 

b = {}
var AID = 0
function func(t) {
    var id = t.id;
   
    $.ajax({
        url: "/get_column_header",
        type: "POST",
        data: JSON.stringify(id),
        success: function (data) {
            columnheaders = data;
            console.log(columnheaders);
            $('.dropdown-menu1').empty()
            $('.dropdown-menu2').empty()
            $('.dropdown-menu3').empty()
            $('.dropdown-menu4').empty()
            $('.dropdown-menu5').empty()
           
            $("#checkboxtable").dataTable().fnDestroy();
            $("#checkboxtable1").empty();


            count=0
            $.each(columnheaders, function (index, value) {
                //console.log(value);
                count++;
                if (index <= 5){
                    b[value] = true
                    $('#checkboxtable1').append('<tr class="form-check"> <td> <input name = "featurecheckbox"  id=' + value + ' class="form-check-input" type="checkbox" onclick="addme(this)"  checked><label class="form-check-label" >' + value + '</label></td></tr>');
                }else{
                    $('#checkboxtable1').append('<tr class="form-check"> <td> <input name = "featurecheckbox"  id=' + value + ' class="form-check-input" type="checkbox" onclick="addme(this)" ><label class="form-check-label">' + value + '</label></td></tr>');
                    b[value] = false
                }
                $('.dropdown-menu1').each(function (index, element) {
                    
                    $(this).append('<a class="dropdown-item dropdown-item1" >' + value + '</a>');
                })
                $('.dropdown-menu2').each(function (index, element) {
                    //console.log(element);
                    $(this).append('<a class="dropdown-item dropdown-item2" >' + value + '</a>');
                })
                $('.dropdown-menu3').each(function (index, element) {
                    //console.log(element);
                    $(this).append('<a class="dropdown-item dropdown-item3" >' + value + '</a>');
                })
                $('.dropdown-menu4').each(function (index, element) {
                    //console.log(element);

                    $(this).append('<a class="dropdown-item dropdown-item4">' + value + '</a>');
                })
                $('.dropdown-menu5').each(function (index, element) {
                    //console.log(element);
                    $(this).append('<a class="dropdown-item dropdown-item5">' + value + '</a>');
                })

            });

            
            $('#checkboxtable').DataTable({
                "ordering": false,
                "paging": true,
                "lengthMenu": [5, 10],
                "lengthChange": false,
                "searching": false

            });



            var table = document.getElementById("myTable");
            rows = table.getElementsByTagName("tr");

            count = 0;
            $('#dropdownScoreButton').click(function () {

                $(this).css("width", "fit-content")
                $('.dropdown-item1').each(function (i, v) {
                    $(v).click(function (e) {
                        e.preventDefault();
                        $('#dropdownScoreButton').text($(v).text());
                        count++;
                        $('#l1').show();

                    });

                })

            })

            $('#dropdownOutcomeButton').click(function () {

                $(this).css("width", "fit-content")
                $('.dropdown-item2').each(function (i, v) {
                    $(v).click(function (e) {
                        e.preventDefault();
                        $('#dropdownOutcomeButton').text($(v).text());
                        count++;
                        $('#l2').show();
                    });
                })
            })

            $('#dropdownhasAlertButton').click(function () {
                $(this).css("width", "fit-content")
                $('.dropdown-item3').each(function (i, v) {
                    $(v).click(function (e) {
                        e.preventDefault();
                        $('#dropdownhasAlertButton').text($(v).text());
                        count++;
                        $('#l3').show();
                    });
                })
            })

            $('#dropdownhasBusinessActionButton').click(function () {
                $(this).css("width", "fit-content")
                $('.dropdown-item4').each(function (i, v) {
                    $(v).click(function (e) {
                        e.preventDefault();
                        $('#dropdownhasBusinessActionButton').text($(v).text());
                        count++;
                        $('#l4').show();
                    });
                })
            })

            $('#dropdownhasEscalationButton').click(function () {
                $(this).css("width", "fit-content")
                $('.dropdown-item5').each(function (i, v) {
                    $(v).click(function (e) {
                        e.preventDefault();
                        $('#dropdownhasEscalationButton').text($(v).text());
                        count++;
                        $('#l5').show();
                    });
                })
            })




            clearForm()


            $(rows)
                .attr("data-toggle", "modal")
                .attr("data-target", "#mymodel");

        



           // console.log(data)
           // console.log(t.id)
        }
    });
}




function addme(t) {
   // console.log(t.id)
    if($(t).prop("checked")){
        b[t.id] = true
    }
    else{
        b[t.id] = false
    }

    
}








$('#save').click(function() {
    console.log("Hello")
    //For the grand 5 columns
    a = {};
    a['score'] = $('#dropdownScoreButton').text();
    a['outcome'] =  $('#dropdownOutcomeButton').text();
    a['alert'] = $('#dropdownhasAlertButton').text();
    a['businessaction'] = $('#dropdownhasBusinessActionButton').text();
    a['escalation'] = $('#dropdownhasEscalationButton').text();  

    // For the great features
   
    console.log(a);
    console.log(b);

    
    var c = { a1: a, b1: b };
      $.ajax({
        url: "/get_data",
        type: "POST",
        data: JSON.stringify(c),
        success: function (data) {
            
        }
    });

});	


/*
function fun() {
    console.log("Hello")   
}*/