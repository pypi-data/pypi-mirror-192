# -*- coding: utf-8 -*-
from .taggable import Taggable
from .urn import Urn, parseUrn, makeUrn
from fdi.dataset.odict import ODict

import logging
# create logger
logger = logging.getLogger(__name__)
# logger.debug('level %d' %  (logger.getEffectiveLevel()))

# List of Housekeeping DBs
# some new ####
HKDBS = ['classes', 'tags', 'urns', 'dTypes', 'dTags']


def get_missing(self, urn, datatype, sn, no_check=False):
    """ make URN(s) if datatype and sn(s) are given and vice versa.

    Parameters
    ----------

    no_check: bool
        Do not Check if `datatype` and `sn` are in the pool's HK.
        Default is `False`
    Return
    ------
    tuple
    str, str, int
        Refer tp `parseUrn`.

    Raises
    ------
    ValueError if urn not found or not from this pool.
    KeyError if datatype does not exist.
    IndexError if sn does not exist.
    """
    if urn is None and datatype is None and sn is None:
        return None, None, None

    if datatype is None or sn is None and urn is not None:
        # new ###
        poolname, datatype, sn = parseUrn(urn, int_index=True)
    else:
        # datatype+sn takes priority over urn
        urn = makeUrn(self._poolname, datatype, sn)

    u = urn.urn if issubclass(urn.__class__, Urn) else urn
    # new ###
    if not no_check:
        dat = datatype
        sns = sn
        if not issubclass(sn.__class__, (list, tuple)):
            dat = [datatype]
            sns = [sn]
            for d, s in zip(dat, sns):
                if d not in self._dTypes:
                    raise KeyError(
                        f'{d} not found in pool {self._poolname}')
                if s not in self._dTypes[d]['sn']:
                    raise IndexError('%s:%d not found in pool %s.' %
                                     (d, s, self._poolname))
    # /new ###
    if 0:
        if u not in self._urns:
            raise ValueError(urn + ' not found in pool ' + self._poolname)
    return u, datatype, sn


def add_tag_datatype_sn(tag, datatype, sn, dTypes=None, dTags=None):
    """Static function to  add a tag to datatype-sn to pool fmt 2.0

    Parameters
    ----------
    tag : str
        A tag. Multiple tags have to make multiple calls. `None` and empty tags are ignored.
    datatype : str
        The class name of the data item, new or existing.
    sn : int
        The serial number in integer.
    dTypes : dict
        the first nested mapping of pool fmt 2.
    dTags : dict
        the tag mapping of pool fmt 2.

    """
    if not tag:
        return
    snt = dTypes[datatype]['sn'][sn]['tags']
    if tag not in snt:
        snt.append(tag)
    # dTags saves datatype:sn
    typ = datatype
    if tag not in dTags:
        dTags[tag] = {}
    t = dTags[tag]
    if typ not in t:
        t[typ] = [str(sn)]
    else:
        t[typ].append(str(sn))


class DictHk(Taggable):
    """
    Definition of services provided by a product storage supporting versioning.
    """

    def __init__(self, **kwds):
        super(DictHk, self).__init__(**kwds)
        # {tag->{'urns':[urn]}
        self._tags = dict()
        # {urn->{'tags':[tag], 'meta':meta}}
        self._urns = dict()
        # new ###
        self._dTypes = dict()
        self._dTags = dict()

    def getTags(self, urn=None, datatype=None, sn=None):
        """ 
        Get all of the tags that map to a given URN or a pair of data type and serial number.

        Get all known tags if input arenot specified.
        mh: returns an iterator.

        If datatype and sn are given, use them and ignore urn.
        """

        urn, datatype, sn = self.get_missing(
            urn=urn, datatype=datatype, sn=sn)
        if urn is None:
            return self._dTags.keys()

        # new ###
        if 0:
            assert self._urns[urn]['tags'] == self._dTypes[datatype]['sn'][sn]['tags']
            return self._urns[urn]['tags']

        return self._dTypes[datatype]['sn'][sn]['tags']

    get_missing = get_missing

    def getTagUrnMap(self):
        """
        Get the full tag->urn mappings.

        mh: returns an iterator
        csdb: csdb/v1/storage/tag?tag=tag1,tag2
        """
        # new ###
        return self._dTags

        if 0:
            return zip(self._tags.keys(), map(lambda v: v['urns'], self._value()))

    def getUrn(self, tag):
        """
        Gets the URNs corresponding to the given tag.

        Returns an empty list if `tag` is not `None` and does not exist.
        curl -X GET "http://123.56.102.90:31702/csdb/v1/storage/info?urns=urn%3Apoolbs%3A20211018%3A1" -H "accept: */*"

        """
        if 0:
            if tag not in self._tags:
                return []
        if tag not in self._dTags:
            return []
        # new ###
        if 0:
            assert list(self._tags) == list(self._dTags)
            assert list(self._tags[tag]['urns']) == list(':'.join(
                ['urn', self._poolname, cl, sn]) for cl in self._dTags[tag] for sn in self._dTags[tag][cl])
            return self._tags[tag]['urns']
        # datatype:[sn] -> [urn:poolname:datatype:sn]
        # return ['urn:%s:%s' % (self._poolname, t) for t in self._dTags[tag]]
        t = self._dTags[tag]
        pn = self._poolname
        return list(':'.join(['urn', pn, cl, sn]) for cl in t for sn in t[cl])

    def getUrnObject(self, tag):
        """
        Gets the URNobjects corresponding to the given tag.
        Returns an empty list if `tag` does not exist.
        """

        if 0:
            assert list(self._tags[tag]['urns']) == list(self._dTags[tag])
            return [Urn(x) for x in self._tags[tag]['urns']]
        return [Urn(x) for x in self._dTags[tag]]

    def getAllUrns(self):
        """ Returns a list of all URNs in the pool."""
        res = []
        poolname = self.poolname
        for cls, v in self._dTypes.items():
            res.extend(f'urn:{poolname}:{cls}:{sn}' for sn in v['sn'])
        return res

    def removekey(self, key, thecontainer, thename, cross_ref_map, othername):
        """
        Remove the given key from `the map` and the counterpart key in the correponding `cross_referencing map`.
        """
        vals = thecontainer.pop(key, [])
        # remove all items whose v is key in cross_ref_map
        for val in vals[othername]:
            cross_ref_map[val][thename].remove(key)
            # if we have just removed the last key, remove the empty dict
            if len(cross_ref_map[val][thename]) == 0:
                cross_ref_map[val].pop(thename)
                # if this caused the cross_ref_map[val] to be empty, remove the empty dict
                if len(cross_ref_map[val]) == 0:
                    cross_ref_map.pop(val)

    def removeTag(self, tag):
        """
        Remove the given tag from the tag and urn maps.
        # TODO in CSDB
        """
        # new ##
        clsn_sns = self._dTags.pop(tag)
        for datatype, sns in clsn_sns.items():
            for sn in sns:
                sn = int(sn)
                ts = self._dTypes[datatype]['sn'][sn]['tags']
                if tag in ts:
                    ts.remove(tag)
                    if len(tags) == 0:
                        del ts
                else:
                    logger.warning('tag %s missing from %s:%s:%s.' %
                                   (tag, self._poolname, datatype, sn))
        if 0:
            self.removekey(tag, self._tags, 'tags', self._urns, 'urns')
        # new ##
        # assert list(self._tags) == list(self._dTags)

    def removeUrn(self, urn=None, datatype=None, sn=None):
        """
        Remove the given urn (or a pair of data type and serial number) from the tag and urn maps.

        Only changes maps in memory, not to write on disk here.
        """
        u, datatype, sn = self.get_missing(
            urn=urn, datatype=datatype, sn=sn,
            no_check=False)
        # new ##
        from .productpool import ProductPool
        dats, sns, alist = ProductPool.vectorize(datatype, sn)
        for d, s in zip(dats, sns):
            # if d not in self._dTypes:
            #     if self.ignore_error_when_delete:
            #         return -1
            #     else:
            #         raise ValueError(f'{d} not found in {self.poolname}.')
            _snd = self._dTypes[d]['sn']
            if s not in _snd:
                msg = f'{s} not found in pool {self.getId()}.'
                if not self.ignore_error_when_delete:
                    raise IndexError(msg)
                else:
                    logger.debug(msg)
                    continue
            if 'tags' in _snd[s]:
                for tag in _snd[s]['tags']:
                    if tag in self._dTags:
                        self._dTags[tag][d].remove(str(s))
                        if len(self._dTags[tag][d]) == 0:
                            del self._dTags[tag][d]
                            if len(self._dTags[tag]) == 0:
                                del self._dTags[tag]
                    else:
                        logger.warning('tag %s missing from %s.' %
                                       (tag, self._poolname))
                else:
                    if 0:
                        logger.warning('tag %s missing from %s:%s:%s.' %
                                       (tag, self._poolname, d, s))
            _snd.pop(s)
            if len(_snd) == 0:
                del self._dTypes[d]
            # /new ##

            if 0:
                self.removekey(u, self._urns, 'urns', self._tags, 'tags')
            # new ##
            # assert s not in self._dTypes[d]['sn']

    def setTag(self, tag, urn=None, datatype=None, sn=None):
        """
        Sets the specified tag to the given URN or a pair of data type and serial number.

        # TODO in CSDB
        """
        u, datatype, sn = self.get_missing(
            urn=urn, datatype=datatype, sn=sn, no_check=True)

        if 0:
            self._urns[u]['tags'].append(tag)

            if tag in self._tags:
                self._tags[tag]['urns'].append(u)
            else:
                self._tags[tag] = {'urns': [u]}

        # new ###
        add_tag_datatype_sn(tag, datatype, sn,
                            dTypes=self._dTypes, dTags=self._dTags)
        if 0:
            snt = self._dTypes[datatype]['sn'][sn]['tags']
            if tag not in snt:
                snt.append(tag)
            # dTags saves datatype:sn
            _, typ, sn = tuple(u.rsplit(':', 2))
            if tag not in self._dTags:
                self._dTags[tag] = {}
            t = self._dTags[tag]
            if typ not in t:
                t[typ] = [sn]
            else:
                t[typ].append(sn)

    def tagExists(self, tag):
        """
        Tests if a tag exists.

        """
        # new ##
        if 0:
            assert (tag in self._dTags) == (tag in self._tags)
            return tag in self._tags
        return tag in self._dTags
