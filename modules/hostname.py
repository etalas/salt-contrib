'''
Accessing libc's gethostname()/sethostname() 
and getdomainname()/setdomainname() from Salt.

:maintainer: <etalas@framentation.cc>
:maturity:  new
:depends:   ctypes
:platform:  POSIX?
'''
from ctypes import CDLL as __CDLL__, c_char_p, c_size_t, create_string_buffer as __create_string_buffer__

__opts__ = {}

def __guess_libc_file__():
    '''
    Guess filename of libc for this OS...
    '''
    if __opts__.has_key('libc_filename'):
        return __opts__['libc_filename']
    elif __grains__['kernel'] == 'Linux':
      # Works on Debian 7 and Fedora 19:
      return 'libc.so.6'
    else:
      # Works on FreeBSD 9.1:
      return 'libc.so'

def getdomainname(max_len=255):
    '''
    Call libc's getdomainname() to get the current domainname.
    '''
    libc = __CDLL__(__guess_libc_file__(),use_errno=True)
    domainname_p = __create_string_buffer__(max_len)
    max_len = c_size_t(max_len)
    c_ret = libc.getdomainname(domainname_p, max_len)
    if c_ret == 0:
        return domainname_p.value
    else:
        return False

def gethostname(max_len=255):
    '''
    Call libc's gethostname() to get the current hostname.
    '''
    libc = __CDLL__(__guess_libc_file__(),use_errno=True)
    hostname_p = __create_string_buffer__(max_len)
    max_len = c_size_t(max_len)
    c_ret = libc.gethostname(hostname_p, max_len)
    if c_ret == 0:
        return hostname_p.value
    else:
        return False

def setdomainname(domainname):
    '''
    Call libc's setdomainname() to *set* the system's domainname.
    '''
    libc = __CDLL__(__guess_libc_file__(),use_errno=True)
    if isinstance(domainname,unicode):
        domainname_p = c_char_p(domainname.encode('ascii','ignore'))
    elif isinstance(domainname,str):
        domainname_p = c_char_p(domainname)
    else:
        raise (ValueError, '<%s> is neither str or unicode' % domainname)
    max_len = c_size_t(len(domainname))
    c_ret = libc.setdomainname(domainname_p, max_len)
    if c_ret == 0:
        return True
    else:
        return False

def sethostname(hostname):
    '''
    Call libc's sethostname() to *set* the system's hostname.
    '''
    libc = __CDLL__(__guess_libc_file__(),use_errno=True)
    if isinstance(hostname,unicode):
        hostname_p = c_char_p(hostname.encode('ascii','ignore'))
    elif isinstance(hostname,str):
        hostname_p = c_char_p(hostname)
    else:
        raise (ValueError, '<%s> is neither str or unicode' % hostname)
    max_len = c_size_t(len(hostname))
    c_ret = libc.sethostname(hostname_p, max_len)
    if c_ret == 0:
        return True
    else:
        return False

