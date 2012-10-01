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
    s3slider_style = schema.Choice(
        title=_(u"label_s3slider_style",
                default=u"What stylesheet (css file) to use"),
        default="style.css",
        vocabulary=SimpleVocabulary([
            SimpleTerm("style.css", "style.css",
                _(u"label_s3slider_style_default",
                    default=u"Default")),
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
}

</style>
<link rel="stylesheet" type="text/css" href="%(style)s"/>
""" % {
        'staticFiles': self.staticFiles,
        'height': self.settings.s3_height,
        'width': self.settings.s3_width,
        'textwidth': self.settings.s3_textwidth,
        'style': style
       }
S3sliderSettings = createSettingsFactory(S3sliderDisplayType.schema)