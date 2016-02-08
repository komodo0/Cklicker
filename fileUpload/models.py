from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

    def __str__(self):
        return \
            "<table>" \
                "<tr>" \
                    "<td style='width:250px; text-align:center; vertical-align:middle;'>" \
                        "<img src='" + self.docfile.url + "' style='max-height:100px;'/>" \
                    "</td>" \
                    "<td style='text-align:left; vertical-align:middle; cursor:default!important;' >" \
                        "<textarea style='resize: none; width:100%; height:18px;'>" \
                            "&lt;img src='" + self.docfile.url + "'/&gt;" \
                        "</textarea>" \
                    "</td>" \
               "</tr>" \
            "</table>"
    __str__.allow_tags = True