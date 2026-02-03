from __future__ import absolute_import
from sound_lib.external import pybass
from sound_lib.effects import effect


class Chorus(effect.SoundEffect):
    """ """
    effect_type = pybass.BASS_FX_DX8_CHORUS
    struct = pybass.BASS_DX8_CHORUS


class Echo(effect.SoundEffect):
    """ """
    effect_type = pybass.BASS_FX_DX8_ECHO
    struct = pybass.BASS_DX8_ECHO


class Compressor(effect.SoundEffect):
    """ """
    effect_type = pybass.BASS_FX_DX8_COMPRESSOR
    struct = pybass.BASS_DX8_COMPRESSOR


class Reverb(effect.SoundEffect):
 effect_type = pybass.BASS_FX_DX8_REVERB
 struct = pybass.BASS_DX8_REVERB


class Distortion(effect.SoundEffect):
    """ """
    effect_type = pybass.BASS_FX_DX8_DISTORTION
    struct = pybass.BASS_DX8_DISTORTION


class Flanger(effect.SoundEffect):
    """ """
    effect_type = pybass.BASS_FX_DX8_FLANGER
    struct = pybass.BASS_DX8_FLANGER


class Gargle(effect.SoundEffect):
    """ """
    effect_type = pybass.BASS_FX_DX8_GARGLE
    struct = pybass.BASS_DX8_GARGLE


class I3DL2Reverb(effect.SoundEffect):
    """ """
    effect_type = pybass.BASS_FX_DX8_I3DL2REVERB
    struct = pybass.BASS_DX8_I3DL2REVERB


class ParamEq(effect.SoundEffect):
    """ """
    effect_type = pybass.BASS_FX_DX8_PARAMEQ
    struct = pybass.BASS_DX8_PARAMEQ
