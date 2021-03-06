from distutils.core import setup

setup(  name        = 'issm',
        version     = '4.12',
        description = 'Ice Sheet System Model',
        author      = 'UCI/JPL modified by Evan Cummings',
        url         = 'https://github.com/pf4d/issm_python',
        packages    = ['issm'],
        package_dir = {'issm' : 'issm'}  )
