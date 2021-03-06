# coding: utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Document(models.Model):
    class Meta():
        verbose_name = u"Файл"
        verbose_name_plural = u"Файлы"
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')

    def image(self):
        return \
            "<table>" \
                "<tr>" \
                    "<td style='max-width:250px; text-align:center; vertical-align:middle;'>" \
                        "<img src='" + self.docfile.url + "' style='max-height:100px;'/>" \
                    "</td>" \
                "</tr>" \
            "</table>"


    image.allow_tags = True

    def url(self):
        return "<table>" \
                    "<tr>" \
                        "<td style='text-align:left; vertical-align:middle;' >" \
                            "<textarea onmouseover='this.select()' style='resize: none; width:100%; height:18px;'>" \
                                "&lt;img src='" + self.docfile.url + "'/&gt;" \
                            "</textarea>" \
                        "</td>" \
                    "</tr>" \
                "</table>"

    url.allow_tags = True


    def __str__(self):
        return \
            "<table>" \
                "<tr>" \
                    "<td style='width:250px; text-align:center; vertical-align:middle;'>" \
                        "<img src='" + self.docfile.url + "' style='max-height:100px;'/>" \
                    "</td>" \
                    "<td style='text-align:left; vertical-align:middle;' >" \
                        "<textarea onmouseover='this.select()' style='resize: none; width:100%; height:18px;'>" \
                            "&lt;img src='" + self.docfile.url + "'/&gt;" \
                        "</textarea>" \
                    "</td>" \
               "</tr>" \
            "</table>"
    __str__.allow_tags = True