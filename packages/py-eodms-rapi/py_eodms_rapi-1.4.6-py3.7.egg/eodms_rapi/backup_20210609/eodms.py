##############################################################################
# MIT License
# 
# Copyright (c) 2021 Her Majesty the Queen in Right of Canada, as 
# represented by the President of the Treasury Board
# 
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.
# 
##############################################################################

import os
import sys
import requests
import logging
import logging.config
import traceback
import urllib
import json
import csv
import datetime
import time
import re
import dateparser
from urllib.parse import urlencode
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from xml.etree import ElementTree

from tqdm.auto import tqdm

from .geo import EODMSGeo

# FIELD_MAP = {'RCMImageProducts': 
                # {
                    # 'Incidence Angle': 'SENSOR_BEAM_CONFIG.INCIDENCE_LOW,'\
                                        # 'SENSOR_BEAM_CONFIG.INCIDENCE_HIGH', 
                    # # 'BEAM_MODE_TYPE': 'RCM.SBEAM',
                    # 'Within Orbit Tube': 'RCM.WITHIN_ORBIT_TUBE'
                # }, 
            # 'Radarsat1': 
                # {
                    # 'Pixel Spacing': 'ARCHIVE_RSAT1.SAMPLED_PIXEL_SPACING_PAN', 
                    # 'Incidence Angle': 'SENSOR_BEAM_CONFIG.INCIDENCE_LOW,'\
                                        # 'SENSOR_BEAM_CONFIG.INCIDENCE_HIGH', 
                    # # 'BEAM_MODE': 'RSAT1.SBEAM', 
                    # 'Beam Mnemonic': 'RSAT1.BEAM_MNEMONIC', 
                    # 'Orbit': 'RSAT1.ORBIT_ABS'
                # }, 
            # 'Radarsat2':
                # {
                    # 'Pixel Spacing': 'ARCHIVE_RSAT2.SAMPLED_PIXEL_SPACING_PAN', 
                    # 'Incidence Angle': 'SENSOR_BEAM_CONFIG.INCIDENCE_LOW,'\
                                        # 'SENSOR_BEAM_CONFIG.INCIDENCE_HIGH', 
                    # # 'BEAM_MODE': 'RSAT2.SBEAM', 
                    # 'Beam Mnemonic': 'RSAT2.BEAM_MNEMONIC'
                # }, 
            # 'NAPL':
                # {
                    # 'Colour': 'PHOTO.SBEAM', 
                    # 'Roll': 'ROLL.ROLL_NUMBER'
                    # # 'PREVIEW_AVAILABLE': 'PREVIEW_AVAILABLE'
                # }
            # }
# logger = logging.getLogger('EODMSRAPI')

# warn_ch = logging.StreamHandler()
# warn_ch.setLevel(logging.WARNING)
# formatter = logging.Formatter('| %(name)s | %(levelname)s | %(message)s', '%Y-%m-%d %H:%M:%S')
# warn_ch.setFormatter(formatter)
# logger.addHandler(warn_ch)

# sh = logging.StreamHandler()
# sh.setLevel(logging.DEBUG)
# formatter = logging.Formatter('| %(name)s | %(levelname)s | %(message)s', '%Y-%m-%d %H:%M:%S')
# sh.setFormatter(formatter)
# logger.addHandler(sh)

OTHER_FORMAT = '| %(name)s | %(levelname)s: %(message)s', '%Y-%m-%d %H:%M:%S'
# INFO_FORMAT = '| %(name)s | %(message)s', '%Y-%m-%d %H:%M:%S'

# LOG_CONFIG = {'version': 1,
              # 'formatters': {'error': {'format': OTHER_FORMAT}, 
                            # 'warning': {'format': OTHER_FORMAT}, 
                            # 'debug': {'format': OTHER_FORMAT}, 
                            # 'info': {'format': INFO_FORMAT}}, 
              # 'handlers': {'console':{'class': 'logging.StreamHandler',
                                     # 'formatter': 'info',
                                     # 'level': logging.INFO}},
              # 'root': {'handlers':('console')}}
              
logger = logging.getLogger('EODMSRAPI')

# Set handler for output to terminal
logger.setLevel(logging.DEBUG)
ch = logging.NullHandler()
# formatter = logging.Formatter('| %(name)s | %(levelname)s: %(message)s') #, '%Y-%m-%d %H:%M:%S')
formatter = logging.Formatter('| %(name)s | %(asctime)s | %(levelname)s: ' \
                                '%(message)s', '%Y-%m-%d %H:%M:%S')
ch.setFormatter(formatter)
logger.addHandler(ch)

RECORD_KEYS = ["recordId", "overviewUrl", "collectionId", "metadata2", \
            "rapiOrderUrl", "geometry", "title", "orderExecuteUrl", \
            "thumbnailUrl", "metadataUrl", "isGeorectified", \
            "collectionTitle", "isOrderable", "thisRecordUrl", \
            "metadata"]

class QueryError:
    """
    The QueryError class is used to store error information for a query.
    """
    
    def __init__(self, msg):
        """
        Initializer for QueryError object which stores an error message.
        
        Parameters
        ----------
        msg : str
            The error message to print.
        """
        
        self.msg = msg
        
    def _get_msg(self):
        return self.msg
        
    def _set_msg(self, msg):
        self.msg = msg

class EODMSRAPI():
    
    def __init__(self, username, password):
    
        # print("\nInitializing EODMSRAPI, please wait...")
        
        # Create session
        self._session = requests.Session()
        self._session.auth = (username, password)
        
        self.rapi_root = "https://www.eodms-sgdot.nrcan-rncan.gc.ca/wes/rapi"
        
        self.rapi_collections = {}
        self.unsupport_collections = {}
        self.download_size = 0
        self.size_limit = None
        self.results = []
        self.res_mdata = None
        #self.default_queryLimit = 1000
        self.limit_interval = 1000
        self.name_conv = 'default'
        self.res_format = 'raw'
        self.stdout_enabled = True                          
        
        # self.name_conv: Determines what type of format for the field names.
        #                    - 'default': The original field names and labels from the RAPI.
        #                    - 'words': The label with spaces and words will be returned.
        #                    - 'camel': The format will be like 'CamelCase'.
        #                    - 'upper': The format will be all uppercase with underscore for spaces.
        # self.res_format: The type of format to return.
        #                - 'raw': Returns the JSON results straight from the RAPI.
        #                - 'full': Returns a JSON with full metadata information.
        #                - 'geojson': Returns a FeatureCollection of the results
        #                            (requires geojson package).
        
        self.timeout_query = 120.0
        self.timeout_order = 180.0
        self.attempts = 4
        self.indent = 3
        self.aoi = None
        self.dates = None
        self.start = datetime.datetime.now()
        
        self.geo = EODMSGeo(self)
        
        self._map_fields()
        
        self._header = '| EODMSRAPI | '
        
        self.failed_status = ['CANCELLED', 'FAILED', 'EXPIRED', \
                            'DELIVERED', 'MEDIA_ORDER_SUBMITTED', \
                            'AWAITING_PAYMENT']
        
        # print("Initialization complete.")
        
        return None
        
    def _check_complete(self, complete_items, record_id):
        
        for i in complete_items:
            if i['recordId'] == record_id:
                return True
                
        return False
        
    def _convert_date(self, date, in_forms=['%Y-%m-%d %H:%M:%S.%f'], 
                out='string', out_form="%Y%m%d_%H%M%S"):
        
        # print("date: %s" % date)
        #print("type(date): %s" % type(date))
        if isinstance(date, datetime.datetime):
            if out_form == 'iso':
                return date.isoformat()
            else:
                return date.strftime(out_form)
            
        elif isinstance(date, str):
            # if not '.' in date:
                # date += '.0'
                
            if isinstance(in_forms, str):
                in_forms = [in_forms]
            
            # print("in_forms: %s" % in_forms)
            for form in in_forms:
                try:
                    out_date = datetime.datetime.strptime(date, form)
                    if out == 'date':
                        return out_date
                    else:
                        return out_date.strftime(out_form)
                except ValueError as e:
                    msg = "%s. Date will not be included in query." % \
                        str(e).capitalize()
                    self._log_msg(msg, 'warning')
                    pass
                except:
                    msg = traceback.format_exc()
                    self._log_msg(msg, 'warning')
                    pass
        
    def _change_nameConv(self, val):
        
        if self.name_conv == 'camel':
            return ''.join([v.title() for v in val.split(' ')])
        elif self.name_conv == 'upper': 
            return '_'.join([v.upper() for v in val.split(' ')])
        elif self.name_conv == 'words':
            return ' '.join(re.findall('[A-Z][^A-Z]*', val))
        else:
            return val
        
    # def _download_image(self, url, dest_fn):
        # """
        # Downloads an image from the EODMS.
        
        # @type  url:     str
        # @param url:     The URL where the image is stored on the EODMS.
        # @type  dest_fn: str
        # @param dest_fn: The destination filename where the image will be 
                        # saved.
        # """
        
        # # Get authentication info and extract the username and password
        # auth = self._session.auth
        # user = auth[0]
        # pwd = auth[1]
        
        # # Setup basic authentication before downloading the file
        # pass_man = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        # pass_man.add_password(None, url, user, pwd)
        # authhandler = urllib.request.HTTPBasicAuthHandler(pass_man)
        # opener = urllib.request.build_opener(authhandler)
        # urllib.request.install_opener(opener)
        
        # # Download the file from the EODMS server
        # try:
            # urllib.request.urlretrieve(url, dest_fn, \
                # reporthook=self._print_progress)
        # except:
            # msg = "Unexpected error: %s" % traceback.format_exc()
            # # print("%s%s" % (self._header, msg))
            # logger.warning(msg)
            # pass
            
    def _download_image(self, url, dest_fn, fsize):
        '''
        Given a list of remote and local items, download the remote data if it is not already
        found locally

        Inputs:
          - remote_items: list of tuples containing (remote url, remote filesize)
          - local_items: list of local paths where data will be saved

        Outputs:
          - local_items: same as input 

        Assumptions:
          - length of remote_items and local_items must match
          - filenames in remote_items and local_items must be in sequence
          
        (Adapted from the eodms-api-client (https://pypi.org/project/eodms-api-client/) developed by Mike Brady)
        '''
        # remote_urls = [f[0] for f in remote_items]
        # remote_sizes = [f[1] for f in  remote_items]
        # for remote, expected_size, local in zip(remote_urls, remote_sizes, local_items):
        # # if we have an existing local file, check the filesize against the manifest
        if os.path.exists(dest_fn):
            # if all-good, continue to next file
            if os.stat(dest_fn).st_size == fsize:
                msg = "No download necessary. " \
                    "Local file already exists: %s" % dest_fn
                self._log_msg(msg)
                return None
            # otherwise, delete the incomplete/malformed local file and redownload
            else:
                msg = 'Filesize mismatch with %s. Re-downloading...' % \
                    os.path.basename(dest_fn)
                self._log_msg(msg, 'warning')
                os.remove(dest_fn)
                
        # use streamed download so we can wrap nicely with tqdm
        with self._session.get(url, stream=True) as stream:
            with open(dest_fn, 'wb') as pipe:
                with tqdm.wrapattr(
                    pipe,
                    method='write',
                    miniters=1,
                    total=fsize,
                    desc="%s%s" % (self._header, os.path.basename(dest_fn))
                ) as file_out:
                    for chunk in stream.iter_content(chunk_size=1024):
                        file_out.write(chunk)
                        
        msg = '%s has been downloaded.' % dest_fn
        self._log_msg(msg)
                        
        # return local_items
            
    def _fetch_metadata(self, max_workers=4, len_timeout=20.0):
        """
        Fetches all metadata for a given record
        
        (Adapted from: eodms-api-client (https://pypi.org/project/eodms-api-client/)
            developed by Mike Brady)
            
        :type  max_workers: int
        :param max_workers: The number of threads used for retrieving the metadata.
        :type  len_timeout: float
        :param len_timeout: The length of time in seconds before the thread returns
                            a timeout warning.
                            
        :rtype:  list
        :return: A list containing the metadata for all items in the self.results
        """
        
        metadata_fields = self._get_metaKeys()
        
        if isinstance(metadata_fields, QueryError):
            msg = "Could not generate metadata for the results."
            # print("\n%sWARNING: %s" % (self._header, msg))
            self._log_msg(msg, 'warning')
            return None
        
        meta_urls = [record['thisRecordUrl'] for record in \
                    self.results]
        n_urls = len(meta_urls)
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            res = list(
                tqdm(
                    executor.map(
                        self._fetch_single_record_metadata,
                        meta_urls,
                        [metadata_fields] * n_urls,
                        [len_timeout] * n_urls, 
                    ),
                    desc='%sFetching result metadata' % self._header,
                    total=n_urls,
                    miniters=1,
                    unit='item'
                )
            )
        
        return res
        
        # out_res = []
        # for r in self.results['results']:
            # full_rec = {}
            # full_rec['Record ID'] = r['recordId']
            # full_rec['Title'] = r['title']
            # full_rec['Collection'] = r['collectionId']
            # full_rec['Thumbnail URL'] = r['thumbnailUrl']
            # full_rec['Record URL'] = r['thisRecordUrl']
            
            # # Parse the metadata
            # for m in r['metadata2']:
                # full_rec[m['label']] = m['value']
                
            # out_res.append(full_rec)
            
        # return out_res
        
    def _fetch_single_record_metadata(self, url, keys, timeout):
        '''
        Fetch a single image's metadata
        
        (Adapted from: eodms-api-client (https://pypi.org/project/eodms-api-client/)
            developed by Mike Brady)
            
        :type  url:       str
        :param url:       The URL link to the metadata of the image.
        :type  keys:      list
        :param keys:      A list of metadata keys
        :type  timeout:   float
        :param timeout:   The time in seconds to wait before timing out
        
        :rtype:  dict
        :return: Dictionary containing the keys and geometry metadata for the given
            image.
        '''
        
        metadata = {}
        #r = self._session.get(url, timeout=timeout)
        r = self._submit(url, timeout, as_json=False)
        
        if isinstance(r, QueryError):
            err_msg = "Could not retrieve metadata due to: %s" % r._get_msg()
            # print("\n%sWARNING: %s" % (self._header, err_msg))
            self._log_msg(err_msg, 'warning')
        
        if r.ok:
            response = r.json()
            
            # Add all record info
            record_info = {}
            
            metadata['recordId'] = response['recordId']
            metadata['collectionId'] = response['collectionId']
            metadata['geometry'] = response['geometry']
            
            for k in response.keys():
                if not k == 'metadata2' and not k == 'metadata':
                    record_info[k] = response[k]
            
            recInfo_name = self._change_nameConv('Record Info')
            # print("recInfo_name: %s" % recInfo_name)
            # answer = input("Press enter...")
            metadata[recInfo_name] = record_info
            
            # Add remaining metadata
            for k in keys:
                mdata_key = res_key = k
                if isinstance(k, list):
                    mdata_key = k[0]
                    res_key = k[1]
                #if res_key in response.keys():
                mdata_key = self._change_nameConv(mdata_key)
                if res_key in response.keys():
                    metadata[mdata_key] = response[res_key]
                else:
                    vals = [f[1] for f in response['metadata'] \
                            if f[0] == res_key]
                    if len(vals) > 0:
                        metadata[mdata_key] = vals[0]
                    # else:
                        # print("Missing metadata tag: %s" % res_key)
            
            if self.res_format == 'full':
                metadata['geometry'] = self.geo.convert_imageGeom(\
                                    response['geometry'], 'wkt')
            
        #print("metadata: %s" % metadata)
        return metadata
        
    def _get_metaKeys(self):
        """
        Gets a list of metadata (fields) keys for a given collection
        
        :rtype:  list
        :return: A list of metadata keys
        """
        
        if not self.rapi_collections:
            self.get_collections()
            
        fields = self.rapi_collections[self.collection]['fields']\
                    ['results'].keys()
        sorted_lst = sorted(fields)
        
        # sorted_lst = [self._change_nameConv(k) for k in sorted_lst]
        # print("sorted_lst: %s" % sorted_lst)
        
        return sorted_lst
        
    # def _get_dateQueries(self):
        # """
        # Gets the date range based on the user's value
        # """
        
        # if self.dates is None or self.dates == '':
            # return ''
            
        
        
    def _get_exception(self, res, output='str'):
        """
        Gets the Exception text (or XML) from an request result.
        
        :type  in_xml: xml.etree.ElementTree.Element
        :param in_xml: The XML which will be checked for an exception.
        :type  output: str
        :param output: Determines what type of output should be returned 
                        (default='str').
                       Options:
                       - 'str': returns the XML Exception as a string
                       - 'tree': returns the XML Exception as a 
                                    xml.etree.ElementTree.Element
                                    
        :rtype:        str or xml.etree.ElementTree.Element
        :return:       The Exception XML text or element depending on 
                        the output variable.
        """
        
        in_str = res.text

        # If the input XML is None, return None
        if in_str is None: return None
        
        if self._is_json(in_str): return None
        
        # If the input is a string, convert it to a xml.etree.ElementTree.Element
        if isinstance(in_str, str):
            root = ElementTree.fromstring(in_str)
        else:
            root = in_str
        
        # Cycle through the input XML and location the ExceptionText element
        out_except = []
        for child in root.iter('*'):
            if child.tag.find('ExceptionText') > -1:
                if output == 'tree':
                    return child
                else:
                    return child.text
            elif child.tag.find('p') > -1:
                out_except.append(err)
                
        except_txt = ' '.join(out_except)
        
        query_err = QueryError(except_txt)
                
        return query_err
        
    def _get_fieldId(self, words, collection):
        """
        Gets the Field ID with a given title.
        
        Args:
            words (str or list): For exact match of the title, a string is 
                used. When contains is True, the title can contain a list
                of words which will be checked in order if more than one 
                match is found.
            collection (str): The Collection ID.
        """
        
        # Convert words to a list if it's a string
        if isinstance(words, str):
            words = [words]
        
        # Get the geometry field and add it to resultField
        fields = self.get_collections()[collection]['fields']['results']
        
        field_id = None
        
        # found_fields = [(key, val) for key, val in fields.items() \
                        # if w[0].lower() in key.lower()]
        
        for w in words:
            found_fields = {k: v for k, v in fields.items() \
                        if w.lower() in k.lower()}
            
            if len(found_fields) == 0:
                return field_id
            elif len(found_fields) == 1:
                field_id = list(found_fields.values())[0].get('id')
                return field_id
            elif len(found_fields) > 1:
                fields = found_fields
        
        return field_id
        
    def _get_fieldType(self, coll_id, field_id):
        
        if not self.rapi_collections:
            self.get_collections()
        
        for k, v in self.rapi_collections[coll_id]['fields']['search'].items():
            if v['id'] == field_id:
                return v['datatype']
                
    def _get_itemFromOrders(self, item_id, orders):
        
        for o in orders:
            # print("item_id: '%s'" % item_id)
            # print("o['itemId']: '%s'" % o['itemId'])
            # print(str(o['itemId']) == str(item_id))
            if 'parameters' in o.keys():
                if 'ParentItemId' in o['parameters'].keys():
                    if str(o['parameters']['ParentItemId']) == str(item_id):
                        return o
            
            if str(o['itemId']) == str(item_id):
                return o
                
    def _is_json(self, my_json):
        """
        Checks to see in the input item is in JSON format.
        
        :type  my_json: str
        :param my_json: A string value from the requests results.
        """
        try:
            json_object = json.loads(my_json)
        except (ValueError, TypeError) as e:
            return False
        return True
        
    def _build_or(self, field_id, op, values, d_type):
        if d_type == 'String':
            # (RCM.BEAM_MNEMONIC='16M11' OR RCM.BEAM_MNEMONIC='16M11')
            or_query = '%s' % ' OR '.join(["%s%s'%s'" % \
                        (field_id, op, v) for v in values])
        else:
            or_query = '%s' % ' OR '.join(["%s%s%s" % \
                        (field_id, op, v) for v in values])
                        
        return or_query
        
    def _log_msg(self, messages, msg_type='info', log_indent='', 
                out_indent=''):
        
        if isinstance(messages, list) or isinstance(messages, tuple):
            log_msg, out_msg = messages
        elif isinstance(messages, str):
            log_msg = out_msg = messages
        else:
            print("EODMSRAPI._log_msg: 'messages' parameter not valid.")
            return None
        
        # Log the message
        log_msg = "%s%s" % (log_indent, log_msg)
        log_msg = log_msg.replace('\n', '\\n').replace('\t', '\\t')
        eval_str = "logger.%s('%s')" % (msg_type, log_msg)
        eval("logger.%s('%s')" % (msg_type, log_msg))
        
        # If stdout is disabled, don't print message to terminal
        if not self.stdout_enabled: return None
        
        # Print message to terminal
        if msg_type == 'info':
            msg = "%s%s%s" % (out_indent, self._header, out_msg)
        else:
            msg = "%s%s %s: %s" % (out_indent, self._header, \
                msg_type.upper(), out_msg)
                
        print(msg)
    
    def _map_fields(self):
        
        self.field_map = {'COSMO-SkyMed1': 
                [{'collectionId': 'COSMO-SkyMed1', 
                    'fieldId': 'csmed.ORBIT_ABS', 
                    'uiField': 'Orbit Direction', 
                    'rapiField': 'Absolute Orbit'}, 
                 {'collectionId': 'COSMO-SkyMed1', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing', 
                    'rapiField': 'Spatial Resolution'}], 
            'DMC': 
                [{'collectionId': 'DMC', 
                    'fieldId': 'DMC.CLOUD_PERCENT', 
                    'uiField': 'Maximum Cloud Cover (Not all ' \
                            'vendors supply cloud cover data)', 
                    'rapiField': 'Cloud Cover'}, 
                 {'collectionId': 'DMC', 
                    'fieldId': 'Spatial Resolution', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'DMC', 
                    'fieldId': 'DMC.INCIDENCE_ANGLE', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Sensor Incidence Angle'}], 
            'Gaofen-1': 
                [{'collectionId': 'Gaofen-1', 
                    'fieldId': 'SATOPT.CLOUD_PERCENT', 
                    'uiField': 'Maximum Cloud Cover', 
                    'rapiField': 'Cloud Cover'}, 
                 {'collectionId': 'Gaofen-1', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'Gaofen-1', 
                    'fieldId': 'SATOPT.SENS_INC', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Sensor Incidence Angle'}], 
            'GeoEye-1': 
                [{'collectionId': 'GeoEye-1', 
                    'fieldId': 'GE1.CLOUD_PERCENT', 
                    'uiField': 'Maximum Cloud Cover', 
                    'rapiField': 'Cloud Cover'}, 
                 {'collectionId': 'GeoEye-1', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'GeoEye-1', 
                    'fieldId': 'GE1.SENS_INC', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Sensor Incidence Angle'}, 
                 {'collectionId': 'GeoEye-1', 
                    'fieldId': 'GE1.SBEAM', 
                    'uiField': 'Sensor Mode', 
                    'rapiField': 'Sensor Mode'}], 
            'IKONOS': 
                [{'collectionId': 'IKONOS', 
                    'fieldId': 'IKONOS.CLOUD_PERCENT', 
                    'uiField': 'Maximum Cloud Cover', 
                    'rapiField': 'Cloud Cover'}, 
                 {'collectionId': 'IKONOS', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'IKONOS', 
                    'fieldId': 'IKONOS.SENS_INC', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Sensor Incidence Angle'}, 
                 {'collectionId': 'IKONOS', 
                    'fieldId': 'IKONOS.SBEAM', 
                    'uiField': 'Sensor Mode', 
                    'rapiField': 'Sensor Mode'}], 
            'IRS': 
                [{'collectionId': 'IRS', 
                    'fieldId': 'IRS.CLOUD_PERCENT', 
                    'uiField': 'Maximum Cloud Cover', 
                    'rapiField': 'Cloud Cover'}, 
                 {'collectionId': 'IRS', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'IRS', 
                    'fieldId': 'IRS.SENS_INC', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Sensor Incidence Angle'}, 
                 {'collectionId': 'IRS', 
                    'fieldId': 'IRS.SBEAM', 
                    'uiField': 'Sensor Mode', 
                    'rapiField': 'Sensor Mode'}], 
            'PlanetScope': 
                [{'collectionId': 'PlanetScope', 
                    'fieldId': 'SATOPT.CLOUD_PERCENT', 
                    'uiField': 'Maximum Cloud Cover', 
                    'rapiField': 'Cloud Cover'}, 
                 {'collectionId': 'PlanetScope', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'PlanetScope', 
                    'fieldId': 'SATOPT.SENS_INC', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Sensor Incidence Angle'}], 
            'QuickBird-2': 
                [{'collectionId': 'QuickBird-2', 
                    'fieldId': 'QB2.CLOUD_PERCENT', 
                    'uiField': 'Maximum Cloud Cover', 
                    'rapiField': 'Cloud Cover'}, 
                 {'collectionId': 'QuickBird-2', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'QuickBird-2', 
                    'fieldId': 'QB2.SENS_INC', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Sensor Incidence Angle'}, 
                 {'collectionId': 'QuickBird-2', 
                    'fieldId': 'QB2.SBEAM', 
                    'uiField': 'Sensor Mode', 
                    'rapiField': 'Sensor Mode'}], 
            'Radarsat1': [{'collectionId': 'Radarsat1', 
                    'fieldId': 'RSAT1.ORBIT_DIRECTION', 
                    'uiField': 'Orbit Direction', 
                    'rapiField': 'Orbit Direction'}, 
                 {'collectionId': 'Radarsat1', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'Radarsat1', 
                    'fieldId': 'RSAT1.INCIDENCE_ANGLE', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Incidence Angle'}, 
                 {'collectionId': 'Radarsat1', 
                    'fieldId': 'RSAT1.SBEAM', 
                    'uiField': 'Beam Mode', 
                    'rapiField': 'Sensor Mode'}, 
                 {'collectionId': 'Radarsat1', 
                    'fieldId': 'RSAT1.BEAM_MNEMONIC', 
                    'uiField': 'Beam Mnemonic', 
                    'rapiField': 'Position'}, 
                 {'collectionId': 'Radarsat1', 
                    'fieldId': 'RSAT1.ORBIT_ABS', 
                    'uiField': 'Orbit', 
                    'rapiField': 'Absolute Orbit'}], 
            'Radarsat1RawProducts': [{'collectionId': 'Radarsat1RawProducts', 
                    'fieldId': 'RSAT1.ORBIT_DIRECTION', 
                    'uiField': 'Orbit Direction', 
                    'rapiField': 'Orbit Direction'}, 
                 {'collectionId': 'Radarsat1RawProducts', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'Radarsat1RawProducts', 
                    'fieldId': 'RSAT1.INCIDENCE_ANGLE', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Incidence Angle'}, 
                 {'collectionId': 'Radarsat1RawProducts', 
                    'fieldId': 'RSAT1.DATASET_ID', 
                    'uiField': 'Dataset Id', 
                    'rapiField': 'Dataset Id'}, 
                 {'collectionId': 'Radarsat1RawProducts', 
                    'fieldId': 'ARCHIVE_CUF.ARCHIVE_FACILITY', 
                    'uiField': 'Archive Facility', 
                    'rapiField': 'Reception Facility'}, 
                 {'collectionId': 'Radarsat1RawProducts', 
                    'fieldId': 'ARCHIVE_CUF.RECEPTION_FACILITY', 
                    'uiField': 'Reception Facility', 
                    'rapiField': 'Reception Facility'}, 
                 {'collectionId': 'Radarsat1RawProducts', 
                    'fieldId': 'RSAT1.SBEAM', 
                    'uiField': 'Beam Mode', 
                    'rapiField': 'Sensor Mode'}, 
                 {'collectionId': 'Radarsat1RawProducts', 
                    'fieldId': 'RSAT1.BEAM_MNEMONIC', 
                    'uiField': 'Beam Mnemonic', 
                    'rapiField': 'Position'}, 
                 {'collectionId': 'Radarsat1RawProducts', 
                    'fieldId': 'RSAT1.ORBIT_ABS', 
                    'uiField': 'Orbit', 
                    'rapiField': 'Absolute Orbit'}], 
            'Radarsat2': [{'collectionId': 'Radarsat2', 
                    'fieldId': 'RSAT2.ORBIT_DIRECTION', 
                    'uiField': 'Orbit Direction', 
                    'rapiField': 'Orbit Direction'}, 
                 {'collectionId': 'Radarsat2', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'Radarsat2', 
                    'fieldId': 'RSAT2.INCIDENCE_ANGLE', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Incidence Angle'}, 
                 {'collectionId': 'Radarsat2', 
                    'fieldId': 'CATALOG_IMAGE.SEQUENCE_ID', 
                    'uiField': 'Sequence Id', 
                    'rapiField': 'Sequence Id'}, 
                 {'collectionId': 'Radarsat2', 
                    'fieldId': 'RSAT2.SBEAM', 
                    'uiField': 'Beam Mode', 
                    'rapiField': 'Sensor Mode'}, 
                 {'collectionId': 'Radarsat2', 
                    'fieldId': 'RSAT2.BEAM_MNEMONIC', 
                    'uiField': 'Beam Mnemonic', 
                    'rapiField': 'Position'}, 
                 {'collectionId': 'Radarsat2', 
                    'fieldId': 'RSAT2.ANTENNA_ORIENTATION', 
                    'uiField': 'Look Direction', 
                    'rapiField': 'Look Direction'}, 
                 {'collectionId': 'Radarsat2', 
                    'fieldId': 'RSAT2.TR_POL', 
                    'uiField': 'Transmit Polarization', 
                    'rapiField': 'Transmit Polarization'}, 
                 {'collectionId': 'Radarsat2', 
                    'fieldId': 'RSAT2.REC_POL', 
                    'uiField': 'Receive Polarization', 
                    'rapiField': 'Receive Polarization'}, 
                 {'collectionId': 'Radarsat2', 
                    'fieldId': 'RSAT2.IMAGE_ID', 
                    'uiField': 'Image Identification', 
                    'rapiField': 'Image Id'}, 
                 {'collectionId': 'Radarsat2', 
                    'fieldId': 'RSAT2.ORBIT_REL', 
                    'uiField': 'Relative Orbit', 
                    'rapiField': 'Relative Orbit'}, 
                 {'collectionId': 'Radarsat2', 
                    'fieldId': 'ARCHIVE_IMAGE.ORDER_KEY', 
                    'uiField': 'Order Key', 
                    'rapiField': 'Order Key'}], 
            'Radarsat2RawProducts': [{'collectionId': 'Radarsat2RawProducts', 
                    'fieldId': 'RSAT2.ORBIT_DIRECTION', 
                    'uiField': 'Orbit Direction', 
                    'rapiField': 'Orbit Direction'}, 
                 {'collectionId': 'Radarsat2RawProducts', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'Radarsat2RawProducts', 
                    'fieldId': 'RSAT2.INCIDENCE_ANGLE', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Incidence Angle'}, 
                 {'collectionId': 'Radarsat2RawProducts', 
                    'fieldId': 'RSAT2.ANTENNA_ORIENTATION', 
                    'uiField': 'Look Orientation', 
                    'rapiField': 'Look Orientation'}, 
                 {'collectionId': 'Radarsat2RawProducts', 
                    'fieldId': 'RSAT2.SBEAM', 
                    'uiField': 'Beam Mode', 
                    'rapiField': 'Sensor Mode'}, 
                 {'collectionId': 'Radarsat2RawProducts', 
                    'fieldId': 'RSAT2.BEAM_MNEMONIC', 
                    'uiField': 'Beam Mnemonic', 
                    'rapiField': 'Position'}, 
                 {'collectionId': 'Radarsat2RawProducts', 
                    'fieldId': 'RSAT2.TR_POL', 
                    'uiField': 'Transmit Polarization', 
                    'rapiField': 'Transmit Polarization'}, 
                 {'collectionId': 'Radarsat2RawProducts', 
                    'fieldId': 'RSAT2.REC_POL', 
                    'uiField': 'Receive Polarization', 
                    'rapiField': 'Receive Polarization'}, 
                 {'collectionId': 'Radarsat2RawProducts', 
                    'fieldId': 'RSAT2.IMAGE_ID', 
                    'uiField': 'Image Identification', 
                    'rapiField': 'Image Id'}], 
            'RapidEye': [{'collectionId': 'RapidEye', 
                    'fieldId': 'RE.CLOUD_PERCENT', 
                    'uiField': 'Maximum Cloud Cover', 
                    'rapiField': 'Cloud Cover'}, 
                 {'collectionId': 'RapidEye', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'RapidEye', 
                    'fieldId': 'RE.SENS_INC', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Sensor Incidence Angle'}, 
                 {'collectionId': 'RapidEye', 
                    'fieldId': 'RE.SBEAM', 
                    'uiField': 'Sensor Mode', 
                    'rapiField': 'Sensor Mode'}], 
            'RCMImageProducts': [{'collectionId': 'RCMImageProducts', 
                    'fieldId': 'RCM.ORBIT_DIRECTION', 
                    'uiField': 'Orbit Direction', 
                    'rapiField': 'Orbit Direction'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'RCM.INCIDENCE_ANGLE', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Incidence Angle'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'RCM.BEAM_MNEMONIC', 
                    'uiField': 'Beam Mnemonic', 
                    'rapiField': 'Beam Mnemonic'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'SENSOR_BEAM_CONFIG.BEAM_MODE_QUALIFIER', 
                    'uiField': 'Beam Mode Qualifier', 
                    'rapiField': 'Beam Mode Qualifier'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'RCM.SBEAM', 
                    'uiField': 'Beam Mode Type', 
                    'rapiField': 'Beam Mode Type'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'RCM.DOWNLINK_SEGMENT_ID', 
                    'uiField': 'Downlink segment ID', 
                    'rapiField': 'Downlink segment ID'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'LUTApplied', 
                    'uiField': 'LUT Applied', 
                    'rapiField': 'LUT Applied'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'CATALOG_IMAGE.OPEN_DATA', 
                    'uiField': 'Open Data', 
                    'rapiField': 'Open Data'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'RCM.POLARIZATION', 
                    'uiField': 'Polarization', 
                    'rapiField': 'Polarization'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'PRODUCT_FORMAT.FORMAT_NAME_E', 
                    'uiField': 'Product Format', 
                    'rapiField': 'Product Format'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'ARCHIVE_IMAGE.PRODUCT_TYPE', 
                    'uiField': 'Product Type', 
                    'rapiField': 'Product Type'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'RCM.ORBIT_REL', 
                    'uiField': 'Relative Orbit', 
                    'rapiField': 'Relative Orbit'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'RCM.WITHIN_ORBIT_TUBE', 
                    'uiField': 'Within Orbital Tube', 
                    'rapiField': 'Within Orbital Tube'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'ARCHIVE_IMAGE.ORDER_KEY', 
                    'uiField': 'Order Key', 
                    'rapiField': 'Order Key'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'CATALOG_IMAGE.SEQUENCE_ID', 
                    'uiField': 'Sequence Id', 
                    'rapiField': 'Sequence Id'}, 
                 {'collectionId': 'RCMImageProducts', 
                    'fieldId': 'RCM.SPECIAL_HANDLING_REQUIRED', 
                    'uiField': 'Special Handling Required', 
                    'rapiField': 'Special Handling Required'}], 
            'RCMScienceData': [{'collectionId': 'RCMScienceData', 
                    'fieldId': 'RCM.ORBIT_DIRECTION', 
                    'uiField': 'Orbit Direction', 
                    'rapiField': 'Orbit Direction'}, 
                 {'collectionId': 'RCMScienceData', 
                    'fieldId': 'RCM.INCIDENCE_ANGLE', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Incidence Angle'}, 
                 {'collectionId': 'RCMScienceData', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'RCMScienceData', 
                    'fieldId': 'RCM.SBEAM', 
                    'uiField': 'Beam Mode', 
                    'rapiField': 'Beam Mode Type'}, 
                 {'collectionId': 'RCMScienceData', 
                    'fieldId': 'RCM.BEAM_MNEMONIC', 
                    'uiField': 'Beam Mnemonic', 
                    'rapiField': 'Beam Mnemonic'}, 
                 {'collectionId': 'RCMScienceData', 
                    'fieldId': 'CUF_RCM.TR_POL', 
                    'uiField': 'Transmit Polarization', 
                    'rapiField': 'Transmit Polarization'}, 
                 {'collectionId': 'RCMScienceData', 
                    'fieldId': 'CUF_RCM.REC_POL', 
                    'uiField': 'Receive Polarization', 
                    'rapiField': 'Receive Polarization'}, 
                 {'collectionId': 'RCMScienceData', 
                    'fieldId': 'RCM.DOWNLINK_SEGMENT_ID', 
                    'uiField': 'Downlink Segment ID', 
                    'rapiField': 'Downlink Segment ID'}], 
            'SPOT': [{'collectionId': 'SPOT', 
                    'fieldId': 'SPOT.CLOUD_PERCENT', 
                    'uiField': 'Maximum Cloud Cover (Not all vendors supply cloud cover data)', 
                    'rapiField': 'Cloud Cover'}, 
                 {'collectionId': 'SPOT', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'SPOT', 
                    'fieldId': 'SPOT.SENS_INC', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Sensor Incidence Angle'}], 
            'TerraSarX': [{'collectionId': 'TerraSarX', 
                    'fieldId': 'TSX1.ORBIT_DIRECTION', 
                    'uiField': 'Orbit Direction', 
                    'rapiField': 'Orbit Direction'}, 
                 {'collectionId': 'TerraSarX', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'TerraSarX', 
                    'fieldId': 'INCIDENCE_ANGLE', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Incidence Angle'}], 
            'VASP': [{'collectionId': 'VASP', 
                    'fieldId': 'CATALOG_SERIES.CEOID', 
                    'uiField': 'Value-added Satellite Product Options', 
                    'rapiField': 'Sequence Id'}], 
            'WorldView-1': [{'collectionId': 'WorldView-1', 
                    'fieldId': 'WV1.CLOUD_PERCENT', 
                    'uiField': 'Maximum Cloud Cover', 
                    'rapiField': 'Cloud Cover'}, 
                 {'collectionId': 'WorldView-1', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'WorldView-1', 
                    'fieldId': 'WV1.SENS_INC', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Sensor Incidence Angle'}, 
                 {'collectionId': 'WorldView-1', 
                    'fieldId': 'WV1.SBEAM', 
                    'uiField': 'Sensor Mode', 
                    'rapiField': 'Sensor Mode'}], 
            'WorldView-2': [{'collectionId': 'WorldView-2', 
                    'fieldId': 'WV2.CLOUD_PERCENT', 
                    'uiField': 'Maximum Cloud Cover', 
                    'rapiField': 'Cloud Cover'}, 
                 {'collectionId': 'WorldView-2', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId': 'WorldView-2', 
                    'fieldId': 'WV2.SENS_INC', 
                    'uiField': 'Incidence Angle (Decimal Degrees)', 
                    'rapiField': 'Sensor Incidence Angle'}, 
                 {'collectionId': 'WorldView-2', 
                    'fieldId': 'WV2.SBEAM', 
                    'uiField': 'Sensor Mode', 
                    'rapiField': 'Sensor Mode'}], 
            'WorldView-3': [{'collectionId': 'WorldView-3', 
                    'fieldId': 'WV3.CLOUD_PERCENT', 
                    'uiField': 'Maximum Cloud Cover', 
                    'rapiField': 'Cloud Cover'}, 
                 {'collectionId': 'WorldView-3', 
                    'fieldId': 'SENSOR_BEAM.SPATIAL_RESOLUTION', 
                    'uiField': 'Pixel Spacing (Metres)', 
                    'rapiField': 'Spatial Resolution'}, 
                 {'collectionId', 'WorldView-3', 
                    'fieldId', 'WV3.SENS_INC', 
                    'uiField', 'Incidence Angle (Decimal Degrees)', 
                    'rapiField', 'Sensor Incidence Angle'}, 
                 {'collectionId', 'WorldView-3', 
                    'fieldId', 'WV3.SBEAM', 
                    'uiField', 'Sensor Mode', 
                    'rapiField', 'Sensor Mode'}]}
        
        # self.field_map = {}
        # csv_fn = '%s/data/field_mapping.csv' % \
                # os.path.dirname(os.path.realpath(__file__))
        
        # #print("csv_fn: %s" % csv_fn)
        # with open(csv_fn) as csvfile:
            # reader = csv.DictReader(csvfile)
            # for row in reader:
                # coll_id = row['collectionId']
                # coll_lst = []
                # if coll_id in self.field_map.keys():
                    # coll_lst = self.field_map[coll_id]
                # coll_lst.append(row)
                # self.field_map[coll_id] = coll_lst
    
    def _parse_range(self, field, start, end):
        return '(%s>=%s AND %s<=%s)' % (field, start, field, end)
        
    def _parse_query(self, query=None, aoi=None, dates=None):
        
        query_lst = []
        
        if not self.rapi_collections:
            self.get_collections()
        
        srch_fields = self.rapi_collections[self.collection]['fields']\
                        ['search']
        
        # print("Search Fields: %s" % srch_fields)
        
        # print("Search Field Keys: %s" % srch_fields.keys())
        
        # print("dates: %s" % dates)
        
        if dates is not None and not str(dates).strip() == '':
            self.dates = dates
        # print("self.dates: %s" % self.dates)
        
        if self.dates is not None:
            
            if 'Acquisition Start Date' in srch_fields.keys():
                field_id = srch_fields['Acquisition Start Date']['id']
            else:
                field_id = srch_fields['Start Date']['id']
            
            #parsed_dates = self._get_dates()
            
            date_queries = []
            for rng in self.dates:
                if 'start' not in rng.keys():
                    break
                # print("rng: %s" % rng)
                start = self._convert_date(rng['start'], "%Y%m%d_%H%M%S", \
                                out_form="%Y-%m-%dT%H:%M:%SZ")
                end = self._convert_date(rng['end'], "%Y%m%d_%H%M%S", \
                                out_form="%Y-%m-%dT%H:%M:%SZ")
                                
                if start is None or end is None:
                    continue
                                
                # print("start: %s" % start)
                # print("end: %s" % end)
                
                date_queries.append("%s>='%s' AND %s<='%s'" % \
                    (field_id, start, field_id, end))
            
            if len(date_queries) > 0:
                query_lst.append("(%s)" % ' OR '.join(date_queries))
            
            # print("query_lst: %s" % query_lst)
            
            #answer = input("Press enter...")
            #field_id = srch_fields[
        
        if aoi is None: aoi = self.aoi
        
        if aoi is not None:
            
            self.aoi = self.geo.set_aoi(aoi)
            
            # print("aoi type: %s" % type(self.aoi))
            if self.aoi is None or isinstance(self.aoi, SyntaxError):
                # print("\n%sWARNING: AOI is not a valid entry. " \
                        # "Ignoring AOI.\n" % self._header)
                msg = "The AOI either cannot be opened or the AOI " \
                        "is not a valid entry. Ignoring AOI."
                self._log_msg(msg, 'warning')
            else:                
                # print("AOI: %s" % self.aoi)
                
                field_id = srch_fields['Footprint']['id']
                # print("field_id: %s" % field_id)
                
                query_lst.append("%s INTERSECTS %s" % (field_id, self.aoi))
        
        if query is not None:
            # print("query: %s" % query)
            for field, values in query.items():
            
                # Convert field name to proper field
                # coll_fields = self.rapi_collections[self.collection]['fields']
                # print("coll_fields: %s" % coll_fields)
                
                # print("field: %s" % field)
                # print("values: %s" % str(values))
                
                # print("Search Fields:")
                field_id = None
                if not field in srch_fields.keys():
                    coll_fields = self.field_map[self.collection]
                    ui_fields = [f['uiField'] for f in coll_fields]
                    # print("coll_fields: %s" % coll_fields)
                    # print([f['uiField'] for f in coll_fields])
                    
                    for f in coll_fields:
                        if f['uiField'].find(field) > -1 or \
                            f['uiField'].upper().replace(' ', '_')\
                                .find(field) > -1 or \
                            f['fieldId'].find(field) > -1:
                            field_id = f['fieldId']
                            break
                    
                    if field_id is None:
                        msg = "No available field named '%s'." % field
                        # print("\n%sWARNING: %s" % (self._header, msg))
                        self._log_msg(msg, 'warning')
                else:
                    field_id = srch_fields[field]['id']
                d_type = self._get_fieldType(self.collection, field_id)
                
                op = values[0]
                val = values[1]
                
                if not any(c in op for c in '=><'):
                    op = ' %s ' % op
                
                # if field == 'Incidence Angle':
                    
                    # fields = [srch_fields['Incidence Angle (Low)']['id'], \
                                # srch_fields['Incidence Angle (High)']['id']]
                    # print("fields: %s" % fields)
                    # if isinstance(val, list) or isinstance(val, tuple):
                        # for v in val:
                            # query_lst.append(self._parse_angle(fields, op, v))
                        # continue
                    # else:
                        # val_query = self._parse_angle(fields, op, val)
                        
                if field == 'Incidence Angle' or field == 'Scale' or \
                    field == 'Spacial Resolution' or field == 'Absolute Orbit':
                    #(SENSOR_BEAM_CONFIG.INCIDENCE_LOW >= 10.0 AND SENSOR_BEAM_CONFIG.INCIDENCE_LOW < 20.0) OR 
                    # (SENSOR_BEAM_CONFIG.INCIDENCE_HIGH >= 10.0 AND SENSOR_BEAM_CONFIG.INCIDENCE_HIGH < 20.0)
                    if isinstance(val, list) or isinstance(val, tuple):
                        for v in val:
                            if v.find('-') > -1:
                                start, end = v.split('-')
                                val_query = self._parse_range(field_id, start, end)
                            else:
                                val_query = "%s%s%s" % (field_id, op, v)
                            query_lst.append(val_query)
                        continue
                    else:
                        if val.find('-') > -1:
                            start, end = val.split('-')
                            val_query = self._parse_range(field_id, start, end)
                        else:
                            val_query = "%s%s%s" % (field_id, op, val)
                else:
                    if isinstance(val, list) or isinstance(val, tuple):
                        val_query = self._build_or(field_id, op, val, d_type)
                    else:
                        if d_type == 'String':
                            val_query = "%s%s'%s'" % (field_id, op, val)
                        else:
                            val_query = "%s%s%s" % (field_id, op, val)
                
                # print("val_query: %s" % val_query)
                # print("val_query type: %s" % type(val_query))
                query_lst.append(val_query)
        
        # print("query_lst: %s" % query_lst)
        if len(query_lst) > 1:
            query_lst = ['(%s)' % q if q.find(' OR ') > -1 else q \
                        for q in query_lst]
            
        full_query = ' AND '.join(query_lst)
        
        #print("full_query: %s" % full_query)
        
        return full_query    
            
    def _submit_search(self):
        """
        Submit a search query to the desired EODMS collection

        Since there may be instances where the default maxResults is greater 
        than 150, this method should recursively call itself until the 
        correct number of results is retrieved.
        
        (Adapted from: eodms-api-client (https://pypi.org/project/eodms-api-client/)
            developed by Mike Brady)
        
        :rtype:  json
        :return: The search-query response JSON from the EODMS REST API          
        """
        
        # old_maxResults = int(re.search(r'&maxResults=([\d*]+)', \
                        # self._search_url).group(1))
                        
        # print("old_maxResults: %s" % old_maxResults)
        
        if self.max_results is not None:
            if len(self.results) >= self.max_results:
                self.results = self.results[:self.max_results]
                return self.results
        
        # Print status of search
        # print("self._search_url: %s" % self._search_url)
        start = len(self.results) + 1
        end = len(self.results) + self.limit_interval
        
        msg = "Querying records within %s to %s..." % (start, end)
        self._log_msg(msg)
        
        logger.debug("RAPI Query URL: %s" % self._search_url)
        r = self._submit(self._search_url, as_json=False)
        
        # some GETs are returning 104 ECONNRESET
        # - possibly due to geometry vertex count (failed with 734 but 73 was fine)
        if isinstance(r, QueryError):
            msg = 'Retrying in 3 seconds...'
            self._log_msg(msg, 'warning')
            time.sleep(3)
            return self._submit_search()
            
        if r.ok:
            data = r.json()
            # the data['moreResults'] response is unreliable
            # thus, we submit another query if the number of results 
            # matches our query's maxResults value
            
            # If the number of results has reached the max_results specified
            #   by the user, return results up to max_results
            # if self.max_results is not None:
                # if len(data['results']) >= self.max_results:
                    # self.results += 
                    # return data['results'][:self.max_results]
                
            
            tot_results = int(data['totalResults'])
            # print("tot_results: %s" % tot_results)
            if tot_results == 0:
                return self.results
            elif tot_results < self.limit_interval:
                self.results += data['results']
                return self.results
            
            # if data['totalResults'] == old_maxResults:
                # logger.warning('Number of search results (%d) equals query ' \
                    # 'limit (%d). Increasing limit and trying again...' % \
                    # (data['totalResults'], old_maxResults))
                # new_maxResults = old_maxResults + self.limit_interval
                # self._search_url = self._search_url.replace(
                    # '&maxResults=%d' % old_maxResults,
                    # '&maxResults=%d' % new_maxResults
                # )
            self.results += data['results']
            first_result = len(self.results) + 1
            if self._search_url.find('&firstResult') > -1:
                old_firstResult = int(re.search(
                                        r'&firstResult=([\d*]+)', \
                                        self._search_url
                                    ).group(1))
                # print("old_firstResult: %s" % old_firstResult)
                # print("first_result: %s" % first_result)
                # print("self._search_url: %s" % self._search_url)
                self._search_url = self._search_url.replace(
                                    '&firstResult=%d' % old_firstResult, 
                                    '&firstResult=%d' % first_result
                                   )
                # print("self._search_url: %s" % self._search_url)
            else:
                self._search_url += '&firstResult=%s' % first_result
            return self._submit_search()
            # else:
                # return data['results']
            # return data['results']
            
    def _submit(self, query_url, timeout=None, \
                record_name=None, quiet=True, as_json=True):
        """
        Send a query to the RAPI.
        
        :type  query_url:   str
        :param query_url:   The query URL.
        :type  timeout:     float
        :param timeout:     The length of the timeout in seconds.
        :type  record_name: str
        :param record_name: A string used to supply information for the record 
                            in a print statement.
        
        :rtype  request.Response
        :return The response returned from the RAPI.
        """
        
        # logger = logging.getLogger('eodms')
        
        # logger.debug("_submit: RAPI Query URL: %s" % query_url)
        
        if timeout is None:
            timeout = self.timeout_query
        
        verify = True
        # if query_url.find('www-pre-prod') > -1:
            # verify = False
            
        logger.debug("RAPI Query URL: %s" % query_url)
        
        res = None
        attempt = 1
        err = None
        # Get the entry records from the RAPI using the downlink segment ID
        while res is None and attempt <= self.attempts:
            # Continue to attempt if timeout occurs
            try:
                if record_name is None:
                    msg = "Sending request to the RAPI (attempt %s)..." \
                            % attempt
                    if not quiet and attempt > 1:
                        logger.debug("\n%s%s" % (self._header, msg))
                else:
                    msg = "Sending request to the RAPI for '%s' " \
                                "(attempt %s)..." % (record_name, attempt)
                    if not quiet and attempt > 1:
                        logger.debug("\n%s%s" % (self._header, msg))
                #start_time = datetime.datetime.now()
                if self._session is None:
                    res = requests.get(query_url, timeout=timeout, verify=verify)
                else:
                    res = self._session.get(query_url, timeout=timeout, verify=verify)
                res.raise_for_status()
                #end_time = datetime.datetime.now()
                #logger.info("RAPI request took %s to complete." % str(end_time - start_time))
            except requests.exceptions.HTTPError as errh:
                msg = "HTTP Error: %s" % errh
                
                if msg.find('Unauthorized') > -1:
                    err = msg
                    attempt = 4
                
                if attempt < self.attempts:
                    msg = "%s; attempting to connect again..." % msg
                    self._log_msg(msg, 'warning')
                    res = None
                else:
                    err = msg
                attempt += 1
            except (requests.exceptions.Timeout, 
                    requests.exceptions.ReadTimeout) as errt:
                msg = "Timeout Error: %s" % errt
                if attempt < self.attempts:
                    msg = "%s; increasing timeout by a minute and trying " \
                            "again..." % msg
                    self._log_msg(msg, 'warning')
                    res = None
                    timeout += 60.0
                    self.timeout_query = timeout
                else:
                    err = msg
                attempt += 1
            except (requests.exceptions.ConnectionError, 
                    requests.exceptions.RequestException) as req_err:
                # print("req_err type: %s" % type(req_err))
                msg = "%s Error: %s" % (req_err.__class__.__name__, req_err)
                if attempt < self.attempts:
                    msg = "%s; attempting to connect again..." % msg
                    self._log_msg(msg, 'warning')
                    res = None
                else:
                    err = msg
                attempt += 1
            # except requests.exceptions.RequestException as err:
                # msg = "Exception: %s" % err
                # if attempt < self.attempts:
                    # msg = "WARNING: %s; attempting to connect again..." % msg
                    # print('\n%s' % msg)
                    # logger.warning(msg)
                    # res = None
                # else:
                    # err = msg
                # attempt += 1
            except KeyboardInterrupt as err:
                msg = "Process ended by user."
                self._log_msg(msg, out_indent='\n')
                sys.exit(1)
            except:
                msg = "Unexpected error: %s" % traceback.format_exc()
                if attempt < self.attempts:
                    msg = "%s; attempting to connect again..." % msg
                    self._log_msg(msg, 'warning')
                    res = None
                else:
                    err = msg
                attempt += 1
                
        if err is not None:
            query_err = QueryError(err)
            return query_err
                
        # If no results from RAPI, return None
        if res is None: return None
        
        # Check for exceptions that weren't already caught
        except_err = self._get_exception(res)
        
        if isinstance(except_err, QueryError):
            err_msg = except_err._get_msg()
            if err_msg.find('401 - Unauthorized') > -1:
                # Inform the user if the error was caused by an authentication 
                #   issue.
                err_msg = "An authentication error has occurred while " \
                            "trying to access the EODMS RAPI. Please run this " \
                            "script again with your username and password."
                self._log_msg(err_msg, 'error')
                sys.exit(1)
                
            self._log_msg(msg, 'warning')
            return except_err
        
        if as_json:
            return res.json()
        else:
            return res
            
    def _get_fullCollId(self, coll, unsupported=False):
        """
        Gets the full collection ID using the input collection ID which can be a 
            substring of the collection ID.
        
        Args:
            coll_id (str):      The collection ID to check.
            unsupported (bool): Determines whether to check in the supported or 
                                unsupported collection lists.
        """
        
        # if unsupported:
            # print("self.unsupport_collections: %s" % self.unsupport_collections)
            # for k in self.unsupport_collections.keys():
                # if k.find(coll_id) > -1:
                    # return k
        
        # for k in self.rapi_collections.keys():
            # if k.find(coll_id) > -1:
                # return k
                
        if not self.rapi_collections:
            self.get_collections()
                
        for k, v in self.rapi_collections.items():
            if coll.lower() == k.lower():
                return k
            elif coll.lower() in v['aliases']:
                return k
        
    def set_queryTimeout(self, timeout):
        """
        Sets the timeout limit for a query to the RAPI.
        
        Args:
            timeout (float): The value of the timeout in seconds.
        
        """
        self.timeout_query = float(timeout)
        
    def set_orderTimeout(self, timeout):
        """
        Sets the timeout limit for an order to the RAPI.
        
        Args:
            timeout (float): The value of the timeout in seconds.
            
        """
        self.timeout_order = float(timeout)
        
    def set_attempts(self, number):
        """
        Sets number of attempts to be made to the RAPI before the script 
        ends.
        
        Args:
            number (int): The value for the number of attempts.
        """
        self.attempts = int(number)
        
    def download(self, items, dest, wait=10.0): #, wait=True):
        """
        Downloads a list of order items from the EODMS RAPI.
        
        Args:
            items (list or dict): A list of order items returned from the RAPI.
                
            Example:
                
                {'items': [{'recordId': '8023427', 'status': 'SUBMITTED', 'collectionId': 'RCMImageProducts', 'itemId': '346204', 'orderId': '50975'}, ...]}
            or
                [{'recordId': '8023427', 'status': 'SUBMITTED', 'collectionId': 'RCMImageProducts', 'itemId': '346204', 'orderId': '50975'}, ...]
            dest (str): The local download folder location.
            wait (float or int): Sets the time to wait before checking the status of all orders.
        """
        
        # print("\n%sDownloading image results." % self._header)
        
        msg = "Downloading images..."
        self._log_msg(msg, log_indent='\n\n\t', out_indent='\n')
        
        # for r in results['items']:
            # self.get_order(r['itemId'])
            
        if isinstance(items, dict):
            if 'items' in items.keys():
                items = items['items']
                
        if len(items) == 0:
            msg = "No images to download."
            self._log_msg(msg)
            return []
        
        complete_items = []
        while len(items) > len(complete_items):
            time.sleep(wait)
            orders = self.get_orders()
            
            new_count = len(complete_items)
            
            # print("orders: %s" % orders)
            # print(json.dumps(orders, sort_keys=True, indent=4))
            
            for itm in items:
                item_id = itm['itemId']
                # print("Item ID: %s" % item_id)
                cur_item = self._get_itemFromOrders(item_id, orders)
                status = cur_item['status']
                record_id = cur_item['recordId']
                
                # Check record is already complete
                if self._check_complete(complete_items, record_id):
                    continue
                
                if status in self.failed_status:
                    if status == 'FAILED':
                        # If the order has failed, inform user
                        status_mess = cur_item.get('statusMessage')
                        msg = "\n  The following Order Item has failed:"
                        if status_mess is None:
                            msg += "\n    Order Item Id: %s\n" \
                                    "    Record Id: %s" % \
                                    "    Collection: %s\n" \
                                    (cur_item['itemId'], \
                                    cur_item['recordId'], \
                                    cur_item['collectionId'])
                        else:
                            msg += "\n    Order Item Id: %s\n" \
                                    "    Record Id: %s\n" \
                                    "    Collection: %s\n" \
                                    "    Reason for Failure: %s" % \
                                    (cur_item['itemId'], cur_item['recordId'], \
                                    cur_item['collectionId'], \
                                    cur_item['statusMessage'])
                    else:
                        # If the order was unsuccessful with another status, 
                        #   inform user
                        msg = "\n  The following Order Item has status " \
                                "'%s' and will not be downloaded:" % status
                        msg += "\n    Order Item Id: %s\n" \
                                "    Record Id: %s" % \
                                "    Collection: %s\n" \
                                (cur_item['itemId'], \
                                cur_item['recordId'], \
                                cur_item['collectionId'])
                    
                    self._log_msg(msg)
                    
                    cur_item['orderStatus'] = status
                    cur_item['orderMessage'] = cur_item['statusMessage']
                    cur_item['downloaded'] = 'False'
                    complete_items.append(cur_item)
                    
                elif status == 'AVAILABLE_FOR_DOWNLOAD':
                    cur_item['downloaded'] = 'True'
                    
                    dests = cur_item['destinations']
                    manifest_key = list(cur_item['manifest'].keys()).pop()
                    fsize = int(cur_item['manifest'][manifest_key])
                    
                    download_paths = []
                    for d in dests:
                        
                        # Get the string value of the destination
                        str_val = d['stringValue']
                        str_val = str_val.replace('</br>', '')
                        
                        # Parse the HTML text of the destination string
                        root = ElementTree.fromstring(str_val)
                        url = root.text
                        fn = os.path.basename(url)
                        
                        # Download the image
                        msg = "Downloading image with " \
                                "Record Id %s (%s)." % (record_id, \
                                os.path.basename(url))
                        self._log_msg(msg)
                        
                        # # Save the image contents to the 'downloads' folder
                        out_fn = os.path.join(dest, fn)
                        full_path = os.path.realpath(out_fn)
                        
                        if not os.path.exists(dest):
                            os.mkdir(dest)
                        
                        #self._set_downloadSize(0)
                        self._download_image(url, out_fn, fsize)
                        print('')
                        #self._set_downloadSize(0)
                        
                        # Record the URL and downloaded file to a dictionary
                        dest_info = {}
                        dest_info['url'] = url
                        dest_info['local_destination'] = full_path
                        download_paths.append(dest_info)
                        
                    cur_item['orderStatus'] = status
                    cur_item['orderMessage'] = cur_item['statusMessage']
                    cur_item['downloadPaths'] = download_paths
                    
                    complete_items.append(cur_item)
            
            if new_count == 0 and len(complete_items) == 0:
                msg = "No items are ready for download yet."
                self._log_msg(msg)
            elif new_count == len(complete_items):
                msg = "No new items are ready for download yet."
                self._log_msg(msg)
            
            # print("length of items: %s" % len(items))
            # print("length of complete_items: %s" % len(complete_items))
        
        # answer = input("Press enter...")
        
        return complete_items
        
    def get_availableFields(self, collection=None):
        """
        Gets a dictionary of available fields for a collection from the RAPI.
        
        Args:
            collection (str): The Collection ID.
        
        Returns:
            dict: A dictionary containing the available fields for the given 
                collection.
        """
        
        if collection is None: collection = self.collection
        
        query_url = '%s/collections/%s' % (self.rapi_root, collection)
        
        # print("#1")
        # logger.info("Getting Fields for Collection %s (RAPI Query): %s" % \
                    # (collection, query_url))
        
        coll_res = self._submit(query_url, timeout=20.0)
        
        # If an error occurred
        if isinstance(coll_res, QueryError):
            self._log_msg(coll_res._get_msg(), 'warning')
            return coll_res
        
        # coll_json = coll_res.json()
        
        # Get a list of the searchFields
        fields = {}
        srch_fields = {}
        for r in coll_res['searchFields']:
            srch_fields[r['title']] = {'id': r['id'], \
                                        'datatype': r['datatype']}
        
        fields['search'] = srch_fields
        
        res_fields = {}
        for r in coll_res['resultFields']:
            res_fields[r['title']] = {'id': r['id'], \
                                        'datatype': r['datatype']}
        
        fields['results'] = res_fields
            
        return fields
        
    def get_collections(self, as_list=False, redo=False):
        """
        Gets a list of available collections for the current user.
        
        Args:
            as_list (bool): Determines the type of return. If False, a dictionary
                            will be returned. If True, only a list of collection
                            IDs will be returned.
        
        Returns:
            dict: Either a dictionary of collections or a list of collection IDs 
                    depending on the value of as_list.
        """
        
        # print("\nGetting a list of available collections for the script, please wait...")
        
        # logger = logging.getLogger('eodms')
        
        if self.rapi_collections and not redo:
            return self.rapi_collections
        
        # print("\n%sGetting Collection information, please wait..." % \
        #         self._header)
        
        # List of collections that are either commercial products or not available 
        #   to the general public
        # ignore_collNames = ['RCMScienceData', 'Radarsat2RawProducts', 
                            # 'Radarsat1RawProducts', 'COSMO-SkyMed1', '162', 
                            # '165', '164']
        
        # Create the query to get available collections for the current user
        query_url = "%s/collections" % self.rapi_root
        
        msg = "Getting Collection information, please wait..."
        self._log_msg(msg)
        logger.debug("RAPI URL: %s" % query_url)
        
        # Send the query URL
        coll_res = self._submit(query_url, timeout=20.0)
        
        # If an error occurred
        if isinstance(coll_res, QueryError):
            msg = "Could not get a list of collections due to '%s'.\nPlease try " \
                    "running the script again." % coll_res._get_msg()
            self._log_msg(msg, 'error')
            sys.exit(1)
        
        # If a list is returned from the query, return it
        # if isinstance(coll_res, list):
            # return coll_res
        
        # Convert query to JSON
        # coll_json = coll_res.json()
        
        # Create the collections dictionary
        for coll in coll_res:
            for child in coll['children']:                
                for c in child['children']:
                    coll_id = c['collectionId']
                    # Add aliases for specific collections allowing easier access for users
                    aliases = []
                    if coll_id == 'RCMImageProducts':
                        aliases = ['rcm']
                    elif coll_id == 'Radarsat1':
                        aliases = ['r1', 'rs1', 'radarsat', 'radarsat-1']
                    elif coll_id == 'Radarsat2':
                        aliases = ['r2', 'rs2', 'radarsat-2']
                    elif coll_id == 'PlanetScope':
                        aliases = ['planet']
                    fields = self.get_availableFields(coll_id)
                    self.rapi_collections[c['collectionId']] = {
                        'title': c['title'], 
                        'aliases': aliases, 
                        'fields': fields}
        
        # print("self.rapi_collections: %s" % self.rapi_collections)
        # for coll, info in self.rapi_collections.items():
            # print("\n%s:" % coll)
            # for k, v in info.items():
                # print("%s: %s" % (k, v))
        # answer = input("Press enter...")
        
        # If as_list is True, convert dictionary to list of collection IDs
        if as_list:
            collections = [i['title'] for i in self.rapi_collections.values()]
            return collections
        
        return self.rapi_collections
        
    # def get_collIdByName(self, in_title, unsupported=False):
        # """
        # Gets the Collection ID based on the tile/name of the collection.
        
        # @type  in_title:    str
        # @param in_title:    The title/name of the collection.
                            # (ex: 'RCM Image Products' for ID 'RCMImageProducts')
        # @type  unsupported: boolean
        # @param unsupported: Determines whether to check in the unsupported list 
                            # or not.
        # """
        
        # if isinstance(in_title, list):
            # in_title = in_title[0]
        
        # if unsupported:
            # for k, v in self.unsupport_collections.items():
                # if v.find(in_title) > -1 or in_title.find(v) > -1 \
                    # or in_title.find(k) > -1 or k.find(in_title) > -1:
                    # return k
        
        # for k, v in self.rapi_collections.items():
            # if v['title'].find(in_title) > -1:
                # return k
                
        # return self.get_fullCollId(in_title)
                
    # def get_collectionName(self, in_id):
        # """
        # Gets the collection name for a specified collection ID.
        
        # @type  in_id: str
        # @param in_id: The collection ID.
        # """
        
        # return self.rapi_collections[in_id]
                
    def get_orderItem(self, itemId):
        """
        Submits a query to the EODMS RAPI to get a specific order item.
        
        Args:
            itemId (str or int): The Order Item ID of the image to retrieve from the RAPI.
            
        Returns:
            dict: A dictionary containing the JSON format of the results from the RAPI. 
        """
        
        query = "%s/order?itemId=%s" % (self.rapi_root, itemId)
        log_msg = "Getting order item %s (RAPI query): %s" % (itemId, query)
        msg = "Getting order item %s..." % itemId
        
        messages = (log_msg, msg)
        self._log_msg(messages, log_indent='\n\n\t', out_indent='\n')
        
        res = self._submit(query, timeout=self.timeout_order)
                
        return res
        
    def get_order(self, orderId):
        """
        Gets an specified order from the EODMS RAPI.
        
        Args:
            orderId (str or int): The Order ID of the specific order.
            
        Returns:
            dict: A JSON dictionary of the specific order.
        """
        
        orders = self.get_orders()
        
        order = []
        for item in order:
            if item['orderId'] == orderId:
                order.append(item)
                
        return order
                
    def get_orders(self, dtstart=None, dtend=None, maxOrders=10000, 
                    format='json'):
        """
        Sends a query to retrieve orders from the RAPI.
        
        Args:
            dtstart (datetime.datetime): The start date for the date range of the query.
            dtend (datetime.datetime): The end date for the date range of the query.
            maxOrders (int): The maximum number of orders to retrieve.
            format (str): The format of the results.
            
        Returns:
            dict: A JSON dictionary of the query results containing the orders.
        """
        
        # print("%sGetting list of your current orders..." % self._header)
        msg = "Getting list of current orders..."
        self._log_msg(msg)
        
        tm_frm = '%Y-%m-%dT%H:%M:%SZ'
        # end = datetime.datetime.now()
        params = {}
        if dtstart is not None:
            params['dtstart'] = dtstart.strftime(tm_frm)
            params['dtend'] = dtend.strftime(tm_frm)
        params['maxOrders'] = maxOrders
        param_str = urlencode(params)
        
        query_url = "%s/order?%s" % (self.rapi_root, param_str)
                    
        # logger.info("Searching for images (RAPI query)")
        logger.debug("RAPI URL:\n\n%s\n" % query_url)
        # Send the query to the RAPI
        res = self._submit(query_url, self.timeout_query, quiet=False)
            
        if 'items' in res.keys():
            return res['items']
        else:
            return res
            
    def get_ordersByRecords(self, records):
        """
        Gets a list of orders from the RAPI based on a list of records.
        
        Args:
            records (list): A list of records used to get the list of orders.
            
        Returns:
            list: A list of results from the RAPI.
        """
        
        orders = self.get_orders()
        
        # print("Number of records: %s" % len(records))
        
        msg = "Getting a list of order items..."
        self._log_msg(msg, log_indent='\n\n\t', out_indent='\n')
        
        found_orders = []
        unfound = []
        for r in records:
            # Go through each record
            rec_id = r['recordId']
            
            rec_orders = []
            
            for i in orders:
                # Go through each order item
                # i_date = datetime.datetime.strptime(i['dateSubmitted'], \
                        # '%Y-%m-%dT%H:%M:%SZ')
                
                if i['recordId'] == r['recordId']:
                    # Check in filt_orders for an older order item
                    #   and replace it
                    rec_orders.append(i)
                    # print("length of filt_orders: %s" % len(filt_orders))
                    # if len(filt_orders) == 0:
                        # filt_orders.append(i)
                    # else:
                        # filt_orders.append(i)
                        # for idx, o in enumerate(filt_orders):
                            # o_date = datetime.datetime.strptime(\
                                    # o['dateSubmitted'], \
                                    # '%Y-%m-%dT%H:%M:%SZ')
                            # print("i_date: %s" % i_date)
                            # print("o_date: %s" % o_date)
                            # print("o['recordId']: %s" % o['recordId'])
                            # print("i['recordId']: %s" % i['recordId'])
                            # if i_date > o_date and \
                                # o['recordId'] == i['recordId']:
                                # print("removing index: %s" % idx)
                                # del filt_orders[idx]
                                # #filt_orders.append(i)
                                # break
                                
            if len(rec_orders) == 0:
                unfound.append(rec_id)
                continue
        
            # Get the most recent order item with the given recordId
            order_item = max([r for r in rec_orders \
                        if r['recordId'] == rec_id], \
                        key=lambda x:x['dateSubmitted'])
                        
            found_orders.append(order_item)
        
        msg = "Found %s order items for the following records: %s" % \
                (len(found_orders), ', '.join([r['recordId'] \
                for r in found_orders]))
        self._log_msg(msg)
                    
        if len(unfound) > 0:
            msg = "No order items found for the following " \
                    "records: %s" % ', '.join(unfound)
            self._log_msg(msg)
        
        return found_orders
        
    def get_orderParameters(self, collection, recordId):
        """
        Gets the list of available Order parameters for a given image record.
        
        Args:
            collection (str): The Collection ID for the query.
            recordId (int or str): The Record ID for the image.
            
        Returns:
            dict: A JSON dictionary of the order parameters.
        """
        
        # Get the proper Collection ID for the RAPI
        collection = self._get_fullCollId(collection)
        
        msg = "\n\n\tGetting order parameters for image in " \
                "Collection %s with Record ID %s..." % \
                (collection, recordId)
        self._log_msg(msg, log_indent='\n\n\t', out_indent='\n')
        
        # Set the RAPI URL
        query_url = "%s/order/params/%s/%s" % (self.rapi_root, \
                    collection, recordId)
        
        # Send the JSON request to the RAPI
        try:
            # print("\n%sSubmitting orders..." % self._header)
            param_res = self._session.get(url=query_url)
            param_res.raise_for_status()
        except (requests.exceptions.HTTPError, 
                requests.exceptions.ConnectionError, 
                requests.exceptions.Timeout, 
                requests.exceptions.RequestException) as req_err:
            msg = "%s Error: %s" % (req_err.__class__.__name__, req_err)
            self._log_msg(msg, 'warning')
            return msg
        except KeyboardInterrupt as err:
            msg = "Process ended by user."
            self._log_msg(msg, out_indent='\n')
            print()
            sys.exit(1)
        
        if not param_res.ok:
            err = self._get_exception(param_res)
            if isinstance(err, list):
                msg = '; '.join(err)
                self._log_msg(msg, 'warning')
                return msg
                
        msg = "Order removed successfully."
        # print("\n%s%s" % (self._header, msg))
        self._log_msg(msg)
        #logger.info("\n\n\t%s" % msg)
                
        return param_res.json()
        
    def query(self, collection, aoi=None, dates=None, query=None, 
                resultField=[], maxResults=None):
        """
        Sends a query to the RAPI to search for image results.
        
        Args:
            collection (str): The Collection ID for the query.
            aoi (str, dict or list): The AOI used in the query. The AOI can either be:
                
                - a filename (ESRI Shapefile, KML, GML or GeoJSON)
                - a WKT format string
                - the 'geometry' entry from a GeoJSON Feature
                - a list of coordinates (ex: ```[(x1, y1), (x2, y2), ...]```)
                    
            dates (list): A list of date range dictionaries with keys "start" and "end".
                The values of the "start" and "end" can either be a string in format
                "yyyymmdd_hhmmss" or a datetime.datetime object.
                
                Example:
                    ```[{"start": "20201013_120000", "end": "20201013_150000"}]```
                
            query (dict): A dictionary of query parameters and values in 
                    the following format:
                    
                {"|parameter title|": ("|operator|", ["value1", "value2", ...]), ...}
                
                Example: ```{"Beam Mnemonic": {'=': []}}```
                
            resultField (str): A name of a parameter to include in the query results.
            maxResults (str or int): The maximum number of results to return from the query.
        """
                
        # Query: {"Beam Mnemonic": {'=': []}}
        
        # Get the proper Collection ID for the RAPI
        self.collection = self._get_fullCollId(collection)
        
        # print("collection: %s" % self.collection)
        
        params = {'collection': self.collection}
        
        # print("query: %s" % query)
        
        if query is not None or aoi is not None or dates is not None:
            params['query'] = self._parse_query(query, aoi, dates)
            # full_query = query.get_query()
            # full_queryEnc = urllib.parse.quote(full_query)
            # params['query'] = full_query
            
        # print("full query: %s" % params['query'])
        # answer = input("Press enter...")
        
        if isinstance(resultField, str):
            resultField = [resultField]
        
        # Get the geometry field and add it to resultField
        footprint_id = self._get_fieldId('Footprint', collection)
        if footprint_id is not None:
            resultField.append(footprint_id)
                
        # Get the pixel spacing field and add it to resultField
        pixspace_id = self._get_fieldId('Spatial Resolution', \
                        collection)
        if pixspace_id is not None:
            resultField.append(pixspace_id)
        
        params['resultField'] = ','.join(resultField)
        
        params['maxResults'] = self.limit_interval
        if maxResults is None or maxResults == '':
            self.max_results = None
        else:
            self.max_results = int(maxResults)
            
            if self.max_results is not None:
                params['maxResults'] = self.max_results \
                        if int(self.max_results) < int(self.limit_interval) \
                        else self.limit_interval
        
        # print("params['maxResults']: %s" % params['maxResults'])
        
        params['format'] = "json"
        
        query_str = urlencode(params)
        self._search_url = "%s/search?%s" % (self.rapi_root, query_str)
        
        # Clear self.results
        self.results = []
        
        # print("\n%sSearching for images..." % self._header)
        #logger.info('\n')
        msg = "Searching for %s images on RAPI" % self.collection
        self._log_msg(msg, log_indent='\n\n\t', out_indent='\n')
        logger.debug("RAPI URL:\n\n%s\n" % self._search_url)
        # Send the query to the RAPI
        #self.results = self._submit_search()
        self._submit_search()
        
        self.res_mdata = None
        
        msg = "Number of %s images returned from RAPI: %s" % \
                (self.collection, len(self.results))
        self._log_msg(msg)
        # print("%s%s" % (self._header, msg))
                
        # return self.results
        
    def get_results(self, form='raw'):
        """
        Gets the self.results in a given format
        
        Args:
            form (str): The type of format to return.
                Available options:
                
                - ```'raw'```: Returns the JSON results straight from the RAPI.
                - ```'full'```: Returns a JSON with full metadata information.
                - ```'geojson'```: Returns a FeatureCollection of the results
                            (requires geojson package).
                            
        Returns:
            dict: A dictionary of the results from self.results variable.
        """
        
        if self.results is None or isinstance(self.results, QueryError):
            msg = "No results exist. Please use query() to run a query on " \
                    "the RAPI."
            self._log_msg(msg, 'warning')
            # print("%s%s" % (self._header, msg))
            return None
            
        self.res_format = form
            
        if self.res_format == 'full':
            if self.res_mdata is None:
                self.res_mdata = self._fetch_metadata()
            return self.res_mdata
        elif self.res_format == 'geojson':
            self.name_conv = 'camel'
            if self.res_mdata is None:
                self.res_mdata = self._fetch_metadata()
            return self.geo.convert_toGeoJSON(self.res_mdata)
        else:
            return self.results
        
    def order(self, results, priority="Medium", parameter=None):
        """
        Sends an order to EODMS using the RAPI.
        
        Args:
            results (list): A list of JSON results from the RAPI.
                            
                The results list must contain a ```collectionId``` key and 
                a ```recordId``` key for each image.
                            
            priority (str or list): Determines the priority of the order.
                
                If you'd like to specify a separate priority for each image,
                pass a list of dictionaries containing the ```recordId``` (matching 
                the IDs in results) and ```priority```, such as:
                
                ```[{"recordId": 7627902, "priority": "Low"}, ...]```
                        
                Priority options: "Low", "Medium", "High" or "Urgent"
                
            parameter (list): Either a list of parameters or a list of record items.
                
                Use the get_orderParameters method to get a list of available parameters.
                
                Parameter list:
                    
                  [{"|internalName|": "|value|"}, ...]
                
                  ```[{"packagingFormat": "TARGZ"}, {"NOTIFICATION_EMAIL_ADDRESS": "kevin.ballantyne@canada.ca"}, ...]```
                
                Parameters for each record:
                    
                  [{"recordId": |recordId|, "parameters": [{"|internalName|": "|value|"}, ...]}]
                  
                  ```[{"recordId": 7627902, "parameters": [{"packagingFormat": "TARGZ"}, ...]}]```
        """
        
        msg = "Submitting order items..."
        self._log_msg(msg, log_indent='\n\n\t', out_indent='\n')
        
        # Add the 'Content-Type' option to the header
        self._session.headers.update({'Content-Type': 'application/json'})
        
        # Create the items from the list of results
        items = [{'collectionId': item['collectionId'], \
                'recordId': item['recordId']} \
                for item in results]
        
        items = []
        for r in results:
            item = {'collectionId': r['collectionId'], \
                    'recordId': r['recordId']}
            item['priority'] = priority
            if 'priority' in r.keys():
                item['priority'] == r['priority']
            items.append(item)
                
        #print("items: %s" % items)
        
        # Create the dictionary for the POST request JSON
        post_dict = {"destinations": [], 
                    "items": items}
                    
        # Dump the dictionary into a JSON object
        post_json = json.dumps(post_dict)
        
        # print("post_json: %s" % post_json)
        # answer = input("Press enter...")
        
        # Set the RAPI URL
        order_url = "%s/order" % self.rapi_root
        
        # Send the JSON request to the RAPI
        try:
            # print("\n%sSubmitting orders..." % self._header)
            order_res = self._session.post(url=order_url, data=post_json)
            order_res.raise_for_status()
        except (requests.exceptions.HTTPError, 
                requests.exceptions.ConnectionError, 
                requests.exceptions.Timeout, 
                requests.exceptions.RequestException) as req_err:
            msg = "%s Error: %s" % (req_err.__class__.__name__, req_err)
            self._log_msg(msg, 'warning')
            return msg
        except KeyboardInterrupt as err:
            msg = "Process ended by user."
            self._log_msg(msg, out_indent='\n')
            print()
            sys.exit(1)
        
        if not order_res.ok:
            err = self._get_exception(order_res)
            if isinstance(err, list):
                msg = '; '.join(err)
                self._log_msg(msg, 'warning')
                return msg
                
        msg = "Order submitted successfully."
        # print("\n%s%s" % (self._header, msg))
        self._log_msg(msg)
        #logger.info("\n\n\t%s" % msg)
                
        return order_res.json()
        
    def remove_orderItem(self, orderId, itemId):
        
        """
        Removes an Order Item from the EODMS using the RAPI.
        
        Args:
            orderId (int or str): The Order ID of the Order Item to remove.
            itemId (int or str): The Order Item ID of the Order Item to remove.
            
        Returns:
            byte str: Returns the contents of the Delete request (always empty).
        """
        
        msg = "Removing order item %s..." % itemId
        self._log_msg(msg, log_indent='\n\n\t', out_indent='\n')
        
        # Set the RAPI URL
        order_url = "%s/order/%s/%s" % (self.rapi_root, orderId, itemId)
        
        # Send the JSON request to the RAPI
        try:
            # print("\n%sSubmitting orders..." % self._header)
            delete_res = self._session.delete(url=order_url)
            delete_res.raise_for_status()
        except (requests.exceptions.HTTPError, 
                requests.exceptions.ConnectionError, 
                requests.exceptions.Timeout, 
                requests.exceptions.RequestException) as req_err:
            msg = "%s Error: %s" % (req_err.__class__.__name__, req_err)
            self._log_msg(msg, 'warning')
            return msg
        except KeyboardInterrupt as err:
            msg = "Process ended by user."
            self._log_msg(msg, out_indent='\n')
            print()
            sys.exit(1)
        
        if not delete_res.ok:
            err = self._get_exception(delete_res)
            if isinstance(err, list):
                msg = '; '.join(err)
                self._log_msg(msg, 'warning')
                return msg
                
        msg = "Order removed successfully."
        # print("\n%s%s" % (self._header, msg))
        self._log_msg(msg)
        #logger.info("\n\n\t%s" % msg)
                
        return delete_res.content
