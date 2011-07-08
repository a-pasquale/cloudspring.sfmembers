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
    $("#accordion").tabs("#accordion div.pane", {tabs: 'h3', effect: 'slide', event: 'mouseover', initialIndex: null});
  });
