#!/usr/bin/env python

__author__ = "Abhinav Sarkar <abhinav@abhinavsarkar.net>"
__version__ = "0.2"
__license__ = "GNU Lesser General Public License"
__package__ = "lastfm.mixins"

from lastfm.base import LastfmBase
from lastfm.decorators import cached_property, top_property

class Shoutable(object):
    def init(self, api):
        self._api = api
        
    @cached_property
    def shouts(self):
        """shouts for this ssubject"""
        from lastfm.shout import Shout
        from lastfm.user import User
        params = self._default_params({'method': '%s.getShouts' % self.__class__.__name__.lower()})
        data = self._api._fetch_data(params).find('shouts')
        return [
                Shout(
                      body = s.findtext('body'),
                      author = User(self._api, name = s.findtext('author')),
                      date = s.findtext('date') and s.findtext('date').strip() and \
                            datetime(*(time.strptime(s.findtext('date').strip(), '%a, %d %b %Y %H:%M:%S')[0:6]))
                      )
                for s in data.findall('shout')
                ]
    
    @top_property("shouts")
    def recent_shout(self):
        """recent shout for this subject"""
        pass
    
    def _default_params(self, extra_params = {}):
        return extra_params
    
from datetime import datetime
import time