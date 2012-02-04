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
    $('.profile_overlay a').prepOverlay({
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

    $('#my-content-tabs').tabs('> div');
    /*
    $('ul.tabs').tabs('> div');
    $("#accordion").tabs("#accordion div.pane", {tabs: 'h3', effect: 'slide', event: 'mouseover', initialIndex: null});
    $("#my_accordion").tabs("#my_accordion div.pane", {tabs: 'h3', effect: 'slide', event: 'mouseover', initialIndex: null});
    */

    // Load the site stream into the drawer
    $('#pane3').load('/@@pubsub-feed?node=people');

    // This is the overlay for creating new content
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
                    var title = $('.pb-ajax #wizard-input-title'); 
                    if (index > 0 && title.val() == '') {
                      /* now we are initializeside the onBeforeClick event */
                      // ensure that there is a title for the post.
                      title.parent().addClass("error");
                      // when false is returned, the user cannot advance to the  next tab
                      return false;
                    }

                    // everything is ok. remove possible red highlight from the terms
                    title.parent().removeClass("error");
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

                  function handleContentCreation(state) {
                    // Copy the title
                    var title = $(".pb-ajax #wizard-input-title").val();
                    $("#archetypes-fieldname-title #title").val(title);
                    // Copy the content
                    var mce_instance = $('.pb-ajax #wizard-content .ploneSkin textarea').attr('id');
                    var content = tinyMCE.get(mce_instance).getContent();
                    $("textarea#text").val(content);
                    
                    // Move the keyword tags back
                    $(".pb-ajax textarea#subject_keywords").appendTo("#fieldset-categorization");
                    
                    // Submit the form
                    var form = $("#blog_entry-base-edit");
                    $.ajax( {
                        url: form.attr('action'), 
                        type: "post",
                        data: form.serialize(), 
                        success: function(data) {
                          $(".overlay").fadeOut('slow');
                          $("#exposeMask").fadeOut('slow');
                          $(".overlay-ajax").remove();
                          tinymce.EditorManager.execCommand('mceRemoveControl',true, mce_instance);
                          $("#wizard-tags #archetypes-fieldname-subject").remove();
                        },
                        complete: function(data, textStatus) {
                          if (state == "draft") {
                            // CHANGE ME to private workflow action
                            var post_url = $("#contentview-view a", data.responseText).attr('href') + '/content_status_modify?workflow_action=publish';
                            $.ajax( {
                              url: post_url,
                              success: function(data) {
                                $.gritter.add({
                                  title: 'Saved as a draft',
                                  text: "Don't forget to finish me later."
                                });
                              }
                            });
                          } else {
                            // Default action is to make publicly available.
                            // Give user a message saying post succeeded.
                            if (data.textStatus == "OK") {
                              $.gritter.add({
                                title: '<h2>Woohoo!</h2>',
                                text: 'You wrote something cool.',
                              });
                            };
                          }
                        }
                    });

                  }

                  $(".pb-ajax .post-type").click(function() {
                    // When you click on a post type, store that type
                    // in the content item and move to the next tab.
                    $("input#postType").val($(this).data("post-type"));
                    api.next();
                  });
                    
                  $(".pb-ajax input#overlay_save").click(function() {
                    handleContentCreation();
                  });
                  $(".pb-ajax input#overlay_draft").click(function() {
                    var data = handleContentCreation("draft");
                  });
                  
                  $(document).ready(function() {
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
