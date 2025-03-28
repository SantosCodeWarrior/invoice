
function print_today() {
  // ***********************************************
  // AUTHOR: WWW.CGISCRIPT.NET, LLC
  // URL: http://www.cgiscript.net
  // Use the script, just leave this message intact.
  // Download your FREE CGI/Perl Scripts today!
  // ( http://www.cgiscript.net/scripts.htm )
  // ***********************************************
  var now = new Date();
  var months = new Array('January','February','March','April','May','June','July','August','September','October','November','December');
  var date = ((now.getDate()<10) ? "0" : "")+ now.getDate();
  function fourdigits(number) {
    return (number < 1000) ? number + 1900 : number;
  }
  var today =  months[now.getMonth()] + " " + date + ", " + (fourdigits(now.getYear()));
  return today;
}



// from http://www.mediacollege.com/internet/javascript/number/round.html
function roundNumber(number,decimals) {
  var newString;// The new rounded number
  decimals = Number(decimals);
  if (decimals < 1) {
    newString = (Math.round(number)).toString();
  } else {
    var numString = number.toString();
    if (numString.lastIndexOf(".") == -1) {// If there is no decimal point
      numString += ".";// give it one at the end
    }
    var cutoff = numString.lastIndexOf(".") + decimals;// The point at which to truncate the number
    var d1 = Number(numString.substring(cutoff,cutoff+1));// The value of the last decimal place that we'll end up with
    var d2 = Number(numString.substring(cutoff+1,cutoff+2));// The next decimal, after the last one we want
    if (d2 >= 5) {// Do we need to round up at all? If not, the string will just be truncated
      if (d1 == 9 && cutoff > 0) {// If the last digit is 9, find a new cutoff point
        while (cutoff > 0 && (d1 == 9 || isNaN(d1))) {
          if (d1 != ".") {
            cutoff -= 1;
            d1 = Number(numString.substring(cutoff,cutoff+1));
          } else {
            cutoff -= 1;
          }
        }
      }
      d1 += 1;
    } 
    if (d1 == 10) {
      numString = numString.substring(0, numString.lastIndexOf("."));
      var roundedNum = Number(numString) + 1;
      newString = roundedNum.toString() + '.';
    } else {
      newString = numString.substring(0,cutoff) + d1.toString();
    }
  }
  if (newString.lastIndexOf(".") == -1) {// Do this again, to the new string
    newString += ".";
  }
  var decs = (newString.substring(newString.lastIndexOf(".")+1)).length;
  for(var i=0;i<decimals-decs;i++) newString += "0";
  //var newNumber = Number(newString);// make it a number if you like
  return newString; // Output the result to the form field (change for your purposes)
}

function update_total() {
  var total = 0;
  $('.price').each(function(i){
    price = $(this).html().replace("USD ","");   
    if (!isNaN(price)) total += Number(price);
  });

  total = roundNumber(total,2);
  $('#subtotal').html("USD "+total);
  $('#total').html("USD "+total);
  
  update_balance();
}

function update_balance(){
  var due = $("#total").html().replace("USD ","") - $("#paid").val().replace("USD","");
  due     = roundNumber(due,2);
  $('.due').html("USD "+due);
}

function update_price(){
  var row  = $(this).parents('.item-row');  
  var rate = $('.rate').val();
  var curr = $('.currencyx').val();
  var cl   = $('#client_namex').text();
  var bill = $('.billing_flag').text();
  
  if(cl=='Poompuhar Shipping Corporation Limited'){
    var price = row.find('.cost').val().replace(" ","") * row.find('.qty').val();
   // alert('eee')
  }

  //alert(bill);

  if(cl==bill){
    const date          = new Date();
    const currentYear   = date.getFullYear();
    const currentMonth  = date.getMonth() + 1;  
    const daysInJanuary = getDaysInMonth(currentYear, currentMonth);   
    var price           = row.find('.cost').val().replace(" ","") * row.find('.rate').val()/daysInJanuary;
  }

  else if(rate=='1.0'){
    var qt    = row.find('.qty').val();
    var price = row.find('.cost').val().replace(" ","") * qt;

  }
  else{
    //alert('ee44')
    var price = row.find('.cost').val().replace(" ","") * row.find('.qty').val() * row.find('.rate').val();
  }

  // if(curr=='USD'){
  //   price = row.find('.cost').val().replace(" ","") * row.find('.qty').val()//roundNumber(price,2);
  // }else{
  //   row.find('.cost').val().replace(" ","") * row.find('.qty').val() * row.find('.rate').val();
  // }
  isNaN(price) ? row.find('.price').html("N/A") : row.find('.price').html(price);
  update_total();
}

function getDaysInMonth(year, month) {
  return new Date(year, month, 0).getDate();
}

function bind() {
  $(".cost").blur(update_price);
  $(".qty").blur(update_price);
  $(".rate").blur(update_price);
}

$(document).ready(function() {  
    $(".delete").hide();
    $('input').click(function(){
      $(this).select();
  });

  $("#paid").blur(update_balance);
   

  var rate = $('.rate').val();
  
  if(rate!='1.0'){
    $("#addrow").click(function(){

      $(".item-row:last").after('<tr class="item-row"><td class="item-name"><div class="delete-wpr"><textarea class="s_no_text"> </textarea><a class="delete" href="javascript:;" title="Remove row">X</a></div></td><td class="description"><textarea class="desc_text"></textarea></td><td><textarea class="cost"></textarea></td><td><textarea class="qty"></textarea></td><td><textarea class="rate"></textarea></td><td><span class="price"></span></td></tr>');
      if ($(".delete").length > 1) $(".delete").show();    
      bind();
    });
  }
  else{
    $("#addrow").click(function(){     
      $(".item-row:last").after('<tr class="item-row"><td class="item-name"><div class="delete-wpr"><textarea class="s_no_text"> </textarea><a class="delete" href="javascript:;" title="Remove row">X</a></div></td><td class="description"><textarea class="desc_text"></textarea></td><td><textarea class="cost"></textarea></td><td><textarea class="qty">1</textarea></td><td><span class="price"></span></td></tr>');
      if ($(".delete").length > 1) $(".delete").show();    
      bind();
    });
  }
  
  bind();
  
  $(".delete").live('click',function(){
    $(this).parents('.item-row').remove();
    update_total();
    if ($(".delete").length < 2) $(".delete").hide();
    


  });
  
  $("#cancel-logo").click(function(){
    $("#logo").removeClass('edit');
  });
  $("#delete-logo").click(function(){
    $("#logo").remove();
  });
  $("#change-logo").click(function(){
    $("#logo").addClass('edit');
    $("#imageloc").val($("#image").attr('src'));
    $("#image").select();
  });
  $("#save-logo").click(function(){
    $("#image").attr('src',$("#imageloc").val());
    $("#logo").removeClass('edit');
  });
  
  $("#date").val(print_today());
  
});

