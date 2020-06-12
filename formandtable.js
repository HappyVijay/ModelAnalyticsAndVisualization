$.each(["one", "two"], function(i, value){
    console.log(value + 'array');
});


var columnheaders = []
function clearForm(){
    document.getElementById("form").reset();
}

var AID=0
function insertData(event){
    
    AID=AID+1
    var today = new Date()
    var date = today.getDate()+'/'+today.getMonth()+'/'+today.getFullYear()

    var modelName = document.getElementById("modelName").value
    var modelDesc = document.getElementById("modelDesc").value
    var modelFile = document.getElementById("modelFile").value
    
    $.ajax({
        url:"static/js/EQWT.csv",
        dataType:"text",
        success:function(data)
        {
        var employee_data = data.split(/\r?\n|\r/);
        columnheaders = employee_data[0].split(",");
        console.log(columnheaders);

        
    $.each(columnheaders, function(index, value){
        console.log(value);
        $('#checkboxtable').append('<tr class="form-check"> <td> <input class="form-check-input" type="checkbox" value=""><label class="form-check-label">'+value +'</label></td></tr>');
        $('.dropdown-menu1').each(function(index, element){
            console.log(element);
            $(this).append('<a class="dropdown-item dropdown-item1" href="#">'+value+'</a>');
        })
        $('.dropdown-menu2').each(function(index, element){
            console.log(element);
            $(this).append('<a class="dropdown-item dropdown-item2" href="#">'+value+'</a>');
        })
        $('.dropdown-menu3').each(function(index, element){
            console.log(element);
            $(this).append('<a class="dropdown-item dropdown-item3" href="#">'+value+'</a>');
        })
        $('.dropdown-menu4').each(function(index, element){
            console.log(element);
            $(this).append('<a class="dropdown-item dropdown-item4" href="#">'+value+'</a>');
        })
        $('.dropdown-menu5').each(function(index, element){
            console.log(element);
            $(this).append('<a class="dropdown-item dropdown-item5" href="#">'+value+'</a>');
        })

    });
            
    }
    }
        ); 




    var table = document.getElementById ("myTable");
    rows = table.getElementsByTagName("tr");
    ;
/*
    $('.dropdown-toggle').each(function (index, value) { 
         $(this).click(function (e) { 
             e.preventDefault();
            $('.dropdown-item').each(function(i, v){
                $(v).click(function(e){
                    e.preventDefault();
                    $(value).text($(v).text());
                });

            });
        });
    });
*/
    $('#dropdownScoreButton').click(function() {
        $('.dropdown-item1').each(function(i, v){
          $(v).click(function (e) { 
              e.preventDefault();
              $('#dropdownScoreButton').text($(v).text());
          });
        })
    })

    $('#dropdownOutcomeButton').click(function() {
        $('.dropdown-item2').each(function(i, v){
          $(v).click(function (e) { 
              e.preventDefault();
              $('#dropdownOutcomeButton').text($(v).text());
          });
        })
    })

    $('#dropdownhasAlertButton').click(function() {
        $('.dropdown-item3').each(function(i, v){
          $(v).click(function (e) { 
              e.preventDefault();
              $('#dropdownhasAlertButton').text($(v).text());
          });
        })
    })

    $('#dropdownhasBusinessActionButton').click(function() {
        $('.dropdown-item4').each(function(i, v){
          $(v).click(function (e) { 
              e.preventDefault();
              $('#dropdownhasBusinessActionButton').text($(v).text());
          });
        })
    })

    $('#dropdownhasEscalationButton').click(function() {
        $('.dropdown-item5').each(function(i, v){
          $(v).click(function (e) { 
              e.preventDefault();
              $('#dropdownhasEscalationButton').text($(v).text());
          });
        })
    })




    var row = table.insertRow (2)
    row.className="item"
    var cell1 = row.insertCell (0)
    var cell2 = row.insertCell (1)
    var cell3 = row.insertCell (2)
    var cell4 = row.insertCell (3)
    var cell5 = row.insertCell (4)
    var cell6 = row.insertCell(5)
    cell1.innerHTML = String(AID)
    cell2.innerHTML = String(modelName)
    cell3.innerHTML = String(modelDesc)
    cell4.innerHTML = "User"
    cell5.innerHTML = String(date)
    cell6.innerHTML = ""
    clearForm()


    $("tr")
        .attr("data-toggle", "modal")
        .attr("data-target", "#mymodel");
    }


