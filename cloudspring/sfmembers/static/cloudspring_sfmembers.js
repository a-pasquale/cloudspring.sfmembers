(function() {
  var $;
  $ = jQuery;
  $(function() {
    $('#drawer_tab').show();

    $('#drawer_tab').click(function() {
      var drawerWidth;
      drawerWidth = $("#drawer").outerWidth();
      if (parseInt($('#drawer').css('left')) === 0) {
        $('#page').animate({
          left: 0
        });
        $('#light').animate({
          left: 0
        });
        $('#drawer_tab').animate({
          left: 0
        });
        $('#drawer').animate({
          left: -drawerWidth
        });
        return $('#foot-base').animate({
          left: 0
        });
      } else {
        $('#page').animate({
          left: drawerWidth
        });
        $('#light').animate({
          left: drawerWidth / 2
        });
        $('#drawer_tab').animate({
          left: drawerWidth
        });
        $('#drawer').animate({
          left: 0
        });
        return $('#foot-base').animate({
          left: drawerWidth
        });
      }
    });
    $('#quick-post input').tooltip({
      position: "center right",
      offset: [-2, 20],
      effect: "fade",
      opacity: 0.7
    });
    $('#post-types').tabs('div.post-type-form', {
      event: 'mouseover'
    });
    $('#drawer_nav ul').tabs("#panes > div");
    $('a.overlayLink').prepOverlay({
      subtype: 'ajax',
      filter: common_content_filter,
      config: {
        top: 130,
        mask: {
          color: '#000000',
          opacity: 0.5
        }
      }
    });
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

    $('ul.tabs').tabs('> div');
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
              $('#page-title').html(update_value + "'s Blog");
          }
      }
    });
    $('#my_email').editInPlace({
      url: './@@inline_edit_view',
      params: "email",
      success: function(update_value){
          $('#my_email').html(update_value);
          if (document.getElementById("my-home-folder") != null) {
              $('#portlet-profile #profile-email a').html(update_value);
          }
      }
    });
    return $('#my_website').editInPlace({
      url: './@@inline_edit_view',
      params: "website",
      success: function(update_value){
          $('#my_website').html(update_value);
          if (document.getElementById("my-home-folder") != null) {
              $('#portlet-profile #profile-website a').html(update_value);
          }
      }
    });
  });
}).call(this);
