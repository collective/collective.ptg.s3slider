from zope.i18nmessageid import MessageFactory
from collective.plonetruegallery.utils import createSettingsFactory
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from collective.plonetruegallery.browser.views.display import BaseDisplayType
from collective.plonetruegallery.interfaces import IBaseSettings
from zope import schema

_ = MessageFactory('collective.ptg.s3slider')

class IS3sliderDisplaySettings(IBaseSettings):
    s3_width = schema.TextLine(
        title=_(u"label_s3_width",
            default=u"Width of the gallery"),
        default=u"600px")
    s3_height = schema.TextLine(
        title=_(u"label_s3_height",
            default=u"Height of the gallery"),
        default=u"350px")
    s3_textwidth = schema.TextLine(
        title=_(u"label_s3_textwidth",
            default=u"Width of the (black) text box"),
        default=u"150px")
        
    s3slider_overlay_opacity = schema.Choice(
        title=_(u"label_s3slider_overlay_opacity",
                default=u"Opacity on text overlay"),
        default=70,
        vocabulary=SimpleVocabulary([
            SimpleTerm(0, 0,
                _(u"label_s3slider_overlay_opacity0",
                    default=u"0 Off")),
            SimpleTerm(10, 10,
                _(u"label_s3slider_overlay_opacity1",
                    default=u"0.1 Light")),
            SimpleTerm(20, 20,
                _(u"label_s3slider_overlay_opacity2", default=u"0.2")),
            SimpleTerm(30, 30,
                _(u"label_s3slider_overlay_opacity3", default=u"0.3")),
            SimpleTerm(40, 40,
                _(u"label_s3slider_overlay_opacity4",
                    default=u"0.4 Medium")),
            SimpleTerm(50, 50,
                _(u"label_s3slider_overlay_opacity5", default=u"0.5")),
            SimpleTerm(60, 60,
                _(u"label_s3slider_overlay_opacity6",
                    default=u"0.6")),
            SimpleTerm(70, 70,
                _(u"label_s3slider_overlay_opacity7",
                    default=u"0.7 Dark")),
            SimpleTerm(80, 80,
                _(u"label_s3slider_overlay_opacity8",
                    default=u"0.8 Very Dark")),
            SimpleTerm(90, 90,
                _(u"label_s3slider_overlay_opacity9",
                    default=u"0.9 Almost Black")),
            SimpleTerm(99, 99,
                _(u"label_s3slider_overlay_opacity10",
                    default=u"1 Pitch Dark")
            )
        ]))
        
    s3slider_style = schema.Choice(
        title=_(u"label_s3slider_style",
                default=u"What stylesheet (css file) to use"),
        default="style.css",
        vocabulary=SimpleVocabulary([
            SimpleTerm("style.css", "style.css",
                _(u"label_s3slider_style_default",
                    default=u"Default")),
            SimpleTerm("styleII.css", "styleII.css",
                _(u"label_s3slider_styleII",
                    default=u"Right")),
            SimpleTerm("custom_style", "custom_style",
                _(u"label_s3slider_style_custom",
                    default=u"Custom css file")
            )
        ]))
    s3slider_custom_style = schema.TextLine(
        title=_(u"label_custom_style",
            default=u"Name of Custom css file if you chose that above"),
        default=u"mycustomstyle.css")


class S3sliderDisplayType(BaseDisplayType):

    name = u"s3slider"
    schema = IS3sliderDisplaySettings
    description = _(u"label_s3slider_display_type",
        default=u"s3slider")

    def javascript(self):
        return u"""
<script type="text/javascript"
    src="%(portal_url)s/++resource++ptg.s3slider/s3Slider.js"></script>

<script type="text/javascript">
(function($){

$(document).ready(function() {
   $('#s3slider').s3Slider({
      timeOut: %(delay)i
   });
});

})(jQuery);
</script>
        """ % {
        'portal_url': self.portal_url,
        'delay': self.settings.delay
        }

    def css(self):
        base = '%s/++resource++ptg.s3slider' % (
            self.portal_url)
        style = '%(base)s/%(style)s' % {
                'base': base,
                'style': self.settings.s3slider_style}

        if self.settings.s3slider_style == 'custom_style':
            style = '%(url)s/%(style)s' % {
                'url': self.portal_url,
                'style': self.settings.s3slider_custom_style}

        return u"""
        <style>
#s3slider {
   height: %(height)s;
   width: %(width)s;
   position: relative;
   overflow: hidden;
}

ul#s3sliderContent {
   width: %(width)s;
}

.s3sliderImage span {
   height: %(height)s;
   width: %(textwidth)s;
    filter: alpha(opacity=%(opacity)i);
   -moz-opacity: 0.%(opacity)i;
   -khtml-opacity: 0.%(opacity)i;
   opacity: 0.%(opacity)i;
}

</style>
<link rel="stylesheet" type="text/css" href="%(style)s"/>
""" % {
        'staticFiles': self.staticFiles,
        'height': self.settings.s3_height,
        'width': self.settings.s3_width,
        'textwidth': self.settings.s3_textwidth,
        'opacity': self.settings.s3slider_overlay_opacity,
        'style': style
       }
S3sliderSettings = createSettingsFactory(S3sliderDisplayType.schema)