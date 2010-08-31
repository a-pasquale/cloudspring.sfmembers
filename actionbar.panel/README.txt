Introduction
============

actionbar.panel provides an admin/action panel at the bottom of your Plone
site, similar to the one used on the now old facebook style.

I took a lot of the css from Soh Tanaka's excellent tutorial:
* http://www.sohtanaka.com/web-design/facebook-style-footer-admin-panel-part-1/

Adding new actions:
-------------------

The actionbar is fully extendible. It is a viewlet manager, with the name
'actionbar.panel'. This means that you can add new actions and links to the 
panel by creating and registering viewlets for it in your own Plone add-ons.

See actionbar/panel/browser/configure.zcml for widget registrations.

If you want to publish eggs with add-on actions for the actionbar, please consider
releasing them under the actionbar.* namespace.

Installing:
-----------

actionbar.panel should be a 'drop-in' installation. Just add 'actionbar.panel'
to your eggs section in your buildout.cfg. Then use Plone's control panel, or
the portal_quickinstaller in the Zope management interface to install the
package.

Once you've done this, the panel and some default actions should be visible in
Plone.

Configuring:
------------

You can hide or rearrange the actions on the panel. You can also hide the
entire panel itself. To do this, go to the viewlet managent screen by appending
'/@@manage-viewlets' to the root URL of your Plone site. The panel
viewlet manager and its actions will be near the bottom of the page.

Compatibility:
--------------

actionbar.panel has been tested on Plone 4 and Plone 3.3.5.
It should work on older versions of Plone 3 as well. 

Icons:
------

The icons used in this release were created by Liam McKay
(http://wefunction.com/) and are released under the GPL.

http://www.woothemes.com/2009/09/woofunction-178-amazing-web-design-icons/

Contact:
--------

Please contact me if you have any questions, compatibility problems or improvement suggestions.

- brand at syslab dot com


