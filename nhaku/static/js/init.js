(function($){
  $(function(){
    $('.button-collapse').sideNav();
    $('.dropdown-button').dropdown({
      inDuration: 600,
      outDuration: 600,
      hover: false,
      belowOrigin: false,
    });
  }); // end of document ready
})(jQuery); // end of jQuery name space
