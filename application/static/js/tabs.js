console.log("jalan")
var jawab_arr = new Array();
console.log(jawab_arr)
// deleteCookie("jawaban");
console.log(document.cookie)
deleteCookie("jawaban")
if(document.cookie){
  console.log(document.cookie)
  var x = document.cookie.split('=');
  console.log(x)
  var jawaban = x[1].split(',');
  if (jawaban[jawaban.length] == null) {
    var currentTab = jawaban.length - 1;
  }else{
    var currentTab = jawaban.length;
  }
  
  for (i = 0; i < currentTab; i++) {
      jawab_arr.push(jawaban[i]);

      if (jawaban[i] == '4') {
        var name = 'radio_4_'+i;
        document.getElementById(name).checked = true;
      }else if(jawaban[i] == '3'){
        var name = 'radio_3_'+i;
        document.getElementById(name).checked = true;
      }else if (jawaban[i] == '2') {
        var name = 'radio_2_'+i;
        document.getElementById(name).checked = true;
      }else{
        var name = 'radio_1_'+i;
        document.getElementById(name).checked = true;
      }
      console.log(jawaban[i]);
  }
 console.log(x);
}else{
  var currentTab = 0; // Current tab is set to be the first tab (0)  
  console.log(currentTab)
}

showTab(currentTab); // Display the current tab

function showTab(n) {
  console.log(n)
  // This function will display the specified tab of the form...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";
  //... and fix the Previous/Next buttons:
  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  //... and run a function that will display the correct step indicator:
  fixStepIndicator(n)
}

function nextPrev(n) {
  console.log(n)
  console.log(currentTab)
  console.log($("input[name='radio"+currentTab+"']:checked").val())
  // This function will figure out which tab to display
if ($("input[name='radio"+currentTab+"']:checked").val() || n == -1 && currentTab<21) {
   // if(isChecked){
  var x = document.getElementsByClassName("tab");
  
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
    jawab_arr[currentTab] = $("input[name='radio"+currentTab+"']:checked").val();
    console.log(jawab_arr[currentTab] )
    setCookie("jawaban",jawab_arr);
    console.log(document.cookie);
  
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form...
  if (currentTab >= x.length) {
    // ... the form gets submitted:
    
    document.getElementById("regForm").submit();
    
    deleteCookie("jawaban");
    
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
  console.log(x);
  // }
}
else{  // if(isChecked){
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
    jawab_arr[currentTab] = $("input[name='radio"+currentTab+"']:checked").val();
    console.log(jawab_arr[currentTab] )
    setCookie("jawaban",jawab_arr);
    console.log(document.cookie);
  
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form...
  if (currentTab >= x.length) {
    // ... the form gets submitted:
    
    document.getElementById("regForm").submit();
    
    deleteCookie("jawaban");
    
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
  console.log(x);
  // }

}
  
  
}

function validateForm() {
  // This function deals with validation of the form fields
  var x, y, i, valid = true;
  x = document.getElementsByClassName("tab");
  y = x[currentTab].getElementsByTagName("input");
  // A loop that checks every input field in the current tab:
  for (i = 0; i < y.length; i++) {
    // If a field is empty...
    if (y[i].value == "") {
      // add an "invalid" class to the field:
      y[i].className += " invalid";
      // and set the current valid status to false
      valid = false;
    }
  }
  // If the valid status is true, mark the step as finished and valid:
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }
  return valid; // return the valid status
}

function fixStepIndicator(n) {
  // This function removes the "active" class of all steps...
  var i, x = document.getElementsByClassName("step");
  for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
  }
  //... and adds the "active" class on the current step:
  x[n].className += " active";
}

function showPassword() {
  var x = document.getElementById("showPass");
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function setCookie(cname, cvalue) {
  document.cookie = cname + "=" + cvalue;
}
function deleteCookie(cname){
  // document.cookie = cname + "=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
  document.cookie = cname+"= ; expires = Thu, 01 Jan 1970 00:00:00 GMT"
}