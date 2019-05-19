#!/usr/bin/env python

'''
localizes USGS Granule & products to product dir
'''
import os
import json
import subprocess as sub

DATASET_MAPPING = {'EO1_ALI': 'EO1_ALI_PUB', 'EO1_Hyperion': 'EO1_HYP_PUB'}
PRODUCT_MAPPING = {'STANDARD': 'zip', 'L1T': 'tif', 'L1R': 'zip', 'L1Gst': 'zip', 'FRB': 'jpg', 'GRB': 'zip'}

def retrieve(granule_id, short_name, product_id, filename_base):
    '''pulls the granule using the usgs cli'''
    dataset = DATASET_MAPPING.get(short_name)
    cmd = ['usgs', 'download-options', '--node', 'EE', dataset, granule_id]
    #print('running: {}'.format(' '.join(cmd)))
    result = json.loads(sub.check_output(cmd)).get('data', {})#.get('downloadOptions', False)
    for obj in result:
        options = obj.get('downloadOptions', False)
        for item in options:
            download_code = item.get('downloadCode', False)
            #print('download_code: {}'.format(download_code))
            if not download_code:
                continue
            # get the appropriate url
            cmd = ['usgs', 'download-url', dataset, granule_id, '--node', 'EE', '--product', download_code]
            #print('running: {}'.format(' '.join(cmd)))
            result2 = json.loads(sub.check_output(cmd))
            blob = result2.get('data', [])
            for subitem in blob:
                url = subitem.get('url', False)
                if not url:
                    continue
                # determine the path
                extension = PRODUCT_MAPPING.get(download_code)
                product_filename = filename_base.format(download_code, extension)
                if not os.path.exists(product_id):
                    os.mkdir(product_id)
                out_path = os.path.join(product_id, product_filename)
                #wget result as
                print('localizing product: {}'.format(product_filename))
                cmd = ['wget', '--timeout', '5', '-T', '5', '-O', out_path, url]
                #print('running: {}'.format(' '.join(cmd)))
                sub.check_output(cmd)
                if extension == 'zip':
                    sub.check_output(['unzip', out_path])
    
if __name__ == '__main__':
    #test
    retrieve('EO1A1981002004097110PZ_HGS_01', 'EO1_ALI', 'EO1_ALI-TEST_GRANULE-v1.0', 'EO1_ALI-{}-TEST_GRANULE-v1.0.{}')
