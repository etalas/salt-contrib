'''
Accessing libc's gethostname()/sethostname() 
and getdomainname()/setdomainname() from Salt.

:maintainer: <etalas@framentation.cc>
:maturity:  new
:depends:   ctypes
:platform:  POSIX?
'''
from ctypes import CDLL, c_char_p, c_size_t, byref, create_string_buffer

def getdomainname(max_len=255):
    '''
    Call libc's getdomainname() to get the current domainname.
    '''
    libc = CDLL('libc.so.6',use_errno=True)
    domainname_p = create_string_buffer(max_len)
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
    libc = CDLL('libc.so.6',use_errno=True)
    hostname_p = create_string_buffer(max_len)
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
    libc = CDLL('libc.so.6',use_errno=True)
    if (domainname isinstance unicode):
        domainname_p = c_char_p(domainname.encode('ascii','ignore'))
    elif (domainname isinstance str):
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
    libc = CDLL('libc.so.6',use_errno=True)
    if (hostname isinstance unicode):
        hostname_p = c_char_p(hostname.encode('ascii','ignore'))
    elif (hostname isinstance str):
        hostname_p = c_char_p(hostname)
    else:
        raise (ValueError, '<%s> is neither str or unicode' % hostname)
    max_len = c_size_t(len(hostname))
    c_ret = libc.sethostname(hostname_p, max_len)
    if c_ret == 0:
        return True
    else:
        return False

