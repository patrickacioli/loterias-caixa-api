$(document).ready(function() {
  $( "#process" ).submit(function( event ) {
    $("#load").prop("disabled", true);
    $("#load").html(
     `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>Executando...`
    );
  });
  $( "#verify" ).click(function( event ) {
    var value = $("#verify-select").prop("value")
    window.location.replace("api/"+value);
    event.preventDefault();
  });
});
