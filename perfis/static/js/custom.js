$(window).on("load", function() {
  var res = window.location.pathname.split("/");
  document.getElementById(res.pop()).className = 'active';
  $('.tooltipped').tooltip({delay: 50});
  $('.datepicker').pickadate({
    selectMonths: false,
    selectYears: 1
  });
});

$(document).ready(function() {
  $('.modal').modal({
    dismissible: false
  });
  $('select').material_select();
  $(".dropdown-button").dropdown({
    inDuration: 300,
    outDuration: 225,
    constrainWidth: false,
    hover: false,
    gutter: 0,
    belowOrigin: true,
    alignment: 'left',
    stopPropagation: false
  });
  $('.telefone').mask('(00) 00000-0000');
});