(function() {
  var $;
  $ = jQuery;
  $(function() {
    // Animate the drawer when the drawer tab is clicked.
    $('#drawer_tab').show();
    $('#drawer_tab').click(function() {
      var drawerWidth;
      drawerWidth = $("#drawer").outerWidth();
      if (parseInt($('#drawer').css('left')) === 0) {
        $('#page-wrapper, #light, #drawer_tab').animate({
          left: 0
        });
        $('#drawer').animate({
          left: -drawerWidth
        });
      } else {
        $('#page-wrapper, #light, #drawer_tab').animate({
          left: drawerWidth
        });
        $('#drawer').animate({
          left: 0
        });
      }
    });
    // Setup tabs for the drawer navigation.
    $('#drawer_nav ul').tabs("#panes > div");

    /*  don't think this is used currently.
    */
    $('#quick-post input').tooltip({
      position: "center right",
      offset: [-2, 20],
      effect: "fade",
      opacity: 0.7
    });
    $('#post-types').tabs('div.post-type-form');
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


    // This is for the MyContent portlet
    $(".sliding_div").hide();
    $('div.show_hide').toggle(
        function() {
          $(this).children('img').attr("src", "/++resource++cloudspring.sfmembers/orange-arrow-open.png");
          $(this).parent().addClass("expanded");
          $(this).parent().children('div.sliding_div').slideDown();
        },
        function () {
          $(this).children('img').attr("src", "/++resource++cloudspring.sfmembers/orange-arrow-closed.png");
          $(this).parent().removeClass("expanded");
          $(this).parent().children('div.sliding_div').slideUp();
        }
    );
    $('#review_state_form').buttonset();

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

    $(".member").tooltip({tipClass: 'member_tooltip', effect:'fade'});

    $("#my_accordion").tabs("#my_accordion div.pane", {tabs: 'h3', effect: 'slide', event: 'mouseover', initialIndex: null});
    $('ul.tabs').tabs('> div');
    $('#my-content-tabs').tabs('> div');
    $("#accordion").tabs("#accordion div.pane", {tabs: 'h3', effect: 'slide', event: 'mouseover', initialIndex: null});


    // Load the site stream into the drawer
    $('#pane3').load('/@@pubsub-feed?node=people');

    $('.create-blog-post a').prepOverlay({
          subtype: 'ajax',
          filter: '#blog-overlay',
          closeselector: '#overlay-cancel',
          config  :  {
              closeOnClick: false,
              onLoad: function() {
                  $.noConflict();
                  $('.pb-ajax #blog-overlay').show();
                  $('.pb-ajax #blog_entry-base-edit').hide();
                  var wizard = $(".pb-ajax #wizard")
                  // enable tabs that are contained within the wizard
                  $(wizard).tabs("div.panes > div.pane", function(event, index) {
                      /* now we are initializeside the onBeforeClick event */
                      // ensure that the "terms" checkbox    is checked.
                  });
                  // get handle to the tabs API
                  var api = $(wizard).data("tabs");
   
                  // "next tab" button
                  $("button.next", wizard).click(function() {
                      api.next();
                  });
    
                  // "previous tab" button
                  $("button.prev", wizard).click(function() {
                      api.prev();
                  });
                  $(".pb-ajax input#overlay_save").click(function() {
                    // Copy the title
                    var title = $(".pb-ajax #wizard-input-title").val();
                    $("#archetypes-fieldname-title #title").val(title);
                    // Copy the content
                    var content = tinyMCE.get("mce_2").getContent();
                    $("textarea#text").val(content);
                    
                    // Move the keyword tags back
                    $(".pb-ajax textarea#subject_keywords").appendTo("#fieldset-categorization");
                    
                    // Move the post type back
                    $(".pb-ajax select#assignment").appendTo("#archetypes-fieldname-assignment");

                    // Submit the form
                    var form = $("#blog_entry-base-edit");
                    /*
                    $.get('/Plone/getHomeFolderUrl', function(data) {
                      var blog_entry_id = form.attr('action').split('/').slice(-2,-1);
                      var url = data + "/blog/portal_factory/Blog%20Entry/" + blog_entry_id + "/atct_edit";
                      $.post(url, form.serialize());
                    });
                    */
                    $.post(form.attr('action'), form.serialize(), function(data) {
                        $.gritter.add({
                          title: '<h2>Woohoo!</h2>',
                          text: 'You wrote something cool.',
                        });
                        $(".overlay").fadeOut('slow');
                        $("#exposeMask").fadeOut('slow');
                          
                    });
                  });
                  
                  $(document).ready(function() {
                      // Move the select box for post type
                      $("select#assignment").appendTo("label#wizard-content-type");
                      // Move the keywords textarea
                      $("div.ArchetypesKeywordWidget").prependTo("div#wizard-tags");
                      // Initialize the eea.tags widget.
                      var widgets = jQuery('.ArchetypesKeywordWidget');
                      if(!widgets.length){ return; }
                      widgets.eeatags();
                  });
                  tinyMCE.init({
                            // General options
                            theme : "advanced",
                            mode : "textareas",
                            theme_advanced_toolbar_location : "top",
                            content_css : "/Plone/portal_skins/tinymce/themes/advanced/skins/plone/content.css",
                            editor_css : "/Plone/portal_skins/tinymce/themes/advanced/skins/plone/ui.css",
                  });
              }
          }
    });

    try {
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
    $('#my_website').editInPlace({
      url: './@@inline_edit_view',
      params: "website",
      success: function(update_value){
          $('#my_website').html(update_value);
          if (document.getElementById("my-home-folder") != null) {
              $('#portlet-profile #profile-website a').html(update_value);
          }
      }
    });}
    catch(err){}

  });
}).call(this);
