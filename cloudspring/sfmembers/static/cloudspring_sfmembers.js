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
                  var $ = jQuery_1_7_1;
                  $('.pb-ajax #blog-overlay').show();
                  $('.pb-ajax #blog_entry-base-edit').hide();
                  var tags = ["\n"];

                  function validate() {
                      if ($(".pb-ajax #wizard-input-title").val() == '') {
                          $(".pb-ajax #wizard-content").collapse("show");
                          $(".pb-ajax #wizard-content .alert").show();
                          $(".pb-ajax #wizard-post-type").collapse("hide");
                          $(".pb-ajax #wizard-tags").collapse("hide");
                          $(".pb-ajax #wizard-content .alert").show();
                          $(".pb-ajax #wizard-input-title").focus();
                          return false;
                      } 
                      return true;
                  }

                  function handleContentCreation(state) {
                    if (validate()) {
                      // Copy the title
                      var title = $(".pb-ajax #wizard-input-title").val();
                      $("#archetypes-fieldname-title #title").val(title);
                      // Copy the content
                      var mce_instance = $('.pb-ajax #wizard-content .ploneSkin textarea').attr('id');
                      var content = tinyMCE.get(mce_instance).getContent();
                      $("textarea[name='text']").val(content);
                      
                      // Append category tags to the subject_keywords textarea
                      $(".pb-ajax textarea[name='subject_keywords:lines']").val( $(".pb-ajax textarea[name='subject_keywords:lines']").val() + tags.join("\n") );
                      // Move the keyword tags back
                      $(".pb-ajax textarea[name='subject_keywords:lines']").appendTo("#fieldset-categorization");
                      
                      // Submit the form
                      var form = $("#blog_entry-base-edit");
                      $.ajax( {
                          url: form.attr('action'), 
                          type: "post",
                          data: form.serialize(), 
                          success: function(data) {
                            $("#exposeMask").fadeOut('slow');
                            tinymce.EditorManager.execCommand('mceRemoveControl',true, mce_instance);
                          },
                          complete: function(data, textStatus) {
                            if (state == "draft") {
                              // CHANGE ME to private workflow action
                              var draft_url = $("#contentview-view a", data.responseText).attr('href') + '/content_status_modify?workflow_action=publish';
                              $.ajax( {
                                url: draft_url,
                                success: function(data) {
                                  jQuery.gritter.add({
                                    title: 'Saved as a draft',
                                    text: "Don't forget to finish me later."
                                  });
                                }
                              });
                            } else {
                              // Default action is to make publicly available.
                              // Give user a message saying post succeeded.
                              if (textStatus == "success") {
                                jQuery.gritter.add({
                                  title: '<h2>Woohoo!</h2>',
                                  text: 'You wrote something cool.'
                                });
                              } else {
                                jQuery.gritter.add({
                                  title: '<h2>Uh oh!</h2>',
                                  text: 'Something went wrong.  The server responded with ' + textStatus + '.  Please contact the site administrator.'
                                });
                              }
                            }
                            $(".overlay-ajax").remove();
                          }
                      });
                    }
                  }

                  $(".pb-ajax .post-type").click(function() {
                      // When you click on a post type, store that type
                      // in the content item and move to the next tab.
                      $("input#postType").val($(this).data("post-type"));
                      $(".pb-ajax #wizard-content").collapse('show');
                      $(".pb-ajax #wizard-post-type").collapse('hide');
                      $(".pb-ajax #wizard-input-title").focus();
                  });

                  $(".pb-ajax #wizard-input-title").blur(function() {
                      if ($(".pb-ajax #wizard-input-title").val() == '') {
                          $(".pb-ajax #wizard-content .alert").show();
                          $(".pb-ajax #wizard-input-title").focus();
                      } else {
                          $(".pb-ajax #wizard-content .alert").hide();
                      }
                  });
                    
                  $(".pb-ajax a#overlay_save").click(function() {
                      handleContentCreation();
                  });
                  $(".pb-ajax a#overlay_draft").click(function() {
                      handleContentCreation("draft");
                  });

                  // Add tags from the tag cloud to the autocomplete tokeninput field.
                  $('.pb-ajax .vaporized-tag a').click(function(e) {
                      e.preventDefault();
                      var tag = $(this).text();
                      jQuery(".pb-ajax textarea[name='subject_keywords:lines']").tokenInput("add", {id: tag, name: tag});
                  });

                  // Add tags from the categories buttons to the autocomplete tokeninput field.
                  $('.pb-ajax #wizard-tags button').click(function(e) {
                      var tag = $(this).text();
                      if ($(this).hasClass("active")) {
                          var idx = tags.indexOf(tag);
                          if (idx!=-1) tags.splice(idx, 1);
                      } else {
                          tags.push(tag);
                      }
                  });
                  
                  $(document).ready(function() {
                      // Move the keywords textarea
                      $("div.ArchetypesKeywordWidget").appendTo(".wizard-tags-left");
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
