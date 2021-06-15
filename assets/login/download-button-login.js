  // Get the modal
  var modal3 = document.getElementById("myModal3");

  // Get the button that opens the modal
  var btn = document.getElementById("myBtn3");
  
//   Get the <span> element that closes the modal
  var span = document.getElementsByClassName("close")[2];
  
  // When the user clicks on the button, open the modal
  btn.onclick = function () {
    modal3.style.display = "block";
  };
  
// //   When the user clicks on <span> (x), close the modal
  span.onclick = function () {
    modal3.style.display = "none";
  };
  
//   When the user clicks anywhere outside of the modal, close it
  // window.onclick = function (event) {
  //   if (event.target == modal3) {
  //     modal3.style.display = "none";
  //   }
  // };