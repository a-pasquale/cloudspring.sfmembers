  $(document).ready(function() {
    // This snippet actives the overlay for the member profile·
    $('._overlay a').prepOverlay({
      subtype :  'ajax',
      filter  :  '#content > *',
      config  :  {
        onLoad: function() {
          $.noConflict();
          $('ul.tabs').tabs('> .pane');
          $("#accordion").tabs("#accordion div.pane", {tabs: 'h3', effect: 'slide', event: 'mouseover', initialIndex: null}); 
        }
      }
    });

    $(".member .picture").tooltip({effect:'fade'});

    $('ul.tabs').tabs('> .pane');
    $("#my_accordion").tabs("#my_accordion div.pane", {tabs: 'h3', effect: 'slide', event: 'mouseover', initialIndex: null});
    $("#accordion").tabs("#accordion div.pane", {tabs: 'h3', effect: 'slide', event: 'mouseover', initialIndex: null});

    $('#name').editInPlace({
      url: './@@inline_edit_view',
      params: "name",
      value_required: 'true',
      success: function(update_value){
          $('#name').html(update_value);
          if (document.getElementById("my-home-folder") != null) {
              $('#portlet-profile .portletHeader div a h2').html(update_value);
              $('#page-title a').html(update_value + "'s Blog");
          }
      }
    });
     $('#email').editInPlace({
      url: './@@inline_edit_view',
      params: "email",
      value_required: 'true',
      success: function(update_value){
          $('#email').html(update_value);
          if (document.getElementById("my-home-folder") != null) {
              $('#portlet-profile #profile-email a').html(update_value);
          }
      }
    });
  });
