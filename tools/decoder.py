import bitstring

from . import synthesizer

PATTERNS_PROGRAM = [
    #(None                      , "uint:16", 0),
    (None                      , "uint:8", 0),
    (None                      , "uint:8", 0),

    (None                      , "uint:5" , 0),
    ("arpeggio_trigger_length" , "uint:3" , None),
    ("arpeggio_trigger_pattern", "uint:8" , None),
    
    (None                      , "uint:2" , 1),
    ("voice_mode"              , "uint:2" , None),
    (None                      , "uint:4" , 0),
    
    (None                      , "uint:4" , 0),
    (None                      , "uint:4" , 0),
    (None                      , "uint:8" , 60),
    
    ("delayfx_sync"            , "uint:1" , None),
    (None                      , "uint:3" , 0),
    ("delayfx_time_base"       , "uint:4" , None),
    ("delayfx_delay_time"      , "uint:8" , None),
    ("delayfx_depth"           , "uint:8" , None),
    ("delayfx_type"            , "uint:8" , None),
    
    ("modfx_lfo_speed"         , "uint:8" , None),
    ("modfx_depth"             , "uint:8" , None),
    ("modfx_type"              , "uint:8" , None),
    
    ("eq_hi_freq"              , "uint:8" , None),
    ("eq_hi_gain"              , "uint:8" , None),
    ("eq_low_freq"             , "uint:8" , None),
    ("eq_low_gain"             , "uint:8" , None),
    
    ("arpeggio_tempo"          , "uint:16", None),
    ("arpeggio_onoff"          , "uint:1" , None),
    ("arpeggio_latch"          , "uint:1" , None),
    ("arpeggio_target"         , "uint:2" , None),
    (None                      , "uint:3" , 0),
    ("arpeggio_key_sync"       , "uint:1" , None),
    ("arpeggio_type"           , "uint:4" , None),
    ("arpeggio_range"          , "uint:4" , None),
    ("arpeggio_gate_time"      , "uint:8" , None),
    ("arpeggio_resolution"     , "uint:8" , None),
    ("arpeggio_swing"          , "int:8"  , None),
    
    ("kbd_octave"              , "int:8"  , None)
]

PATTERNS_TIMBRE = [
    (None                    , "int:8"  , -1),
    ("assign_mode"           , "uint:2" , None),
    ("eg2_reset"             , "uint:1" , None),
    ("eg1_reset"             , "uint:1" , None),
    ("trigger_mode"          , "uint:1" , None),
    (None                    , "uint:3" , 0)   ,
    ("unison_detune"         , "uint:8" , None),
    
    ("pitch_tune"            , "uint:8" , None),
    ("pitch_bend_range"      , "uint:8" , None),
    ("pitch_transpose"       , "uint:8" , None),
    ("pitch_vibrato_int"     , "uint:8" , None),
    
    ("osc1_wave"             , "uint:8" , None),
    ("osc1_waveform_ctrl1"   , "uint:8" , None),
    ("osc1_waveform_ctrl2"   , "uint:8" , None),
    ("osc1_dwgs_wave"        , "uint:8" , None),
    (None                    , "uint:8" , 0),
    
    (None                    , "uint:2" , 0),
    ("osc2_mod_select"       , "uint:2" , None),
    (None                    , "uint:2" , 0),
    ("osc2_wave"             , "uint:2" , None),
    ("osc2_semitone"         , "uint:8" , None),
    ("osc2_tune"             , "uint:8" , None),
    
    (None                    , "uint:1" , 0),
    ("pitch_portamento_time" , "uint:7" , None),
    
    ("mixer_osc1_level"      , "uint:8" , None),
    ("mixer_osc2_level"      , "uint:8" , None),
    ("mixer_noise_level"     , "uint:8" , None),
    
    ("filter_type"           , "uint:8"  , None),
    ("filter_cutoff"         , "uint:8"  , None),
    ("filter_resonance"      , "uint:8"  , None),
    ("filter_eg1_intensity"  , "uint:8"  , None),
    (None                    , "uint:8"  , 64),
    ("filter_keyboard_track" , "uint:8"  , None),
    
    ("amp_level"             , "uint:8"  , None),
    ("amp_panpot"            , "uint:8"  , None),
    (None                    , "uint:1"  , 0),
    (None                    , "uint:1"  , 0),
    (None                    , "uint:5"  , 0),
    ("amp_distortion"        , "uint:1"  , None),
    (None                    , "uint:8"  , 64),
    ("amp_keyboard_track"    , "uint:8"  , None),
    
    ("eg1_attack"            , "uint:8"  , None),
    ("eg1_decay"             , "uint:8"  , None),
    ("eg1_sustain"           , "uint:8"  , None),
    ("eg1_release"           , "uint:8"  , None),
    
    ("eg2_attack"            , "uint:8"  , None),
    ("eg2_decay"             , "uint:8"  , None),
    ("eg2_sustain"           , "uint:8"  , None),
    ("eg2_release"           , "uint:8"  , None),
    
    (None                    , "uint:2"  , 0),
    ("lfo1_key_sync"         , "uint:2"  , None),
    (None                    , "uint:2"  , 0),
    ("lfo1_wave"             , "uint:2"  , None),
    ("lfo1_frequency"        , "uint:8"  , None),
    ("lfo1_tempo_sync"       , "uint:1"  , None),
    (None                    , "uint:2"  , 0),
    ("lfo1_sync_note"        , "uint:5"  , None),
    
    (None                    , "uint:2"  , 0),
    ("lfo2_key_sync"         , "uint:2"  , None),
    (None                    , "uint:2"  , 0),
    ("lfo2_wave"             , "uint:2"  , None),
    ("lfo2_frequency"        , "uint:8"  , None),
    ("lfo2_tempo_sync"       , "uint:1"  , None),
    (None                    , "uint:2"  , 0),
    ("lfo2_sync_note"        , "uint:5"  , None)
]

PATTERNS_PATCH = [
    ("destination" , "uint:4" , None),
    ("source"      , "uint:4" , None),
    ("intensity"   , "uint:8" , None)
]

PATTERNS_VOCODER = [
    (None                    , "int:8"  , -1),
    ("assign_mode"           , "uint:2" , None),
    ("eg2_reset"             , "uint:1" , None),
    (None                    , "uint:1" , 0),
    ("trigger_mode"          , "uint:1" , None),
    (None                    , "uint:3" , 0)   ,
    ("unison_detune"         , "uint:8" , None),
    
    ("pitch_tune"            , "uint:8" , None),
    ("pitch_bend_range"      , "uint:8" , None),
    ("pitch_transpose"       , "uint:8" , None),
    ("pitch_vibrato_int"     , "uint:8" , None),
    
    ("osc1_wave"             , "uint:8" , None),
    ("osc1_waveform_ctrl1"   , "uint:8" , None),
    ("osc1_waveform_ctrl2"   , "uint:8" , None),
    ("osc1_dwgs_wave"        , "uint:8" , None),
    (None                    , "uint:8" , 0),
    
    (None                    , "uint:7" , 0),
    ("audioin1_hpf_gate"     , "uint:1" , None),

    (None                    , "uint:1" , 0),
    ("pitch_portamento_time" , "uint:7" , None),
    (None                    , "uint:8" , 0),
    
    ("mixer_osc1_level"      , "uint:8" , None),
    ("mixer_ext1_level"      , "uint:8" , None),
    ("mixer_noise_level"     , "uint:8" , None),

    ("audioin1_hpf_gate"     , "uint:8" , None),
    ("audioin1_gate_sense"   , "uint:8" , None),
    ("audioin1_threshold"    , "uint:8" , None),

    ("filter_shift"          , "uint:8" , None),
    ("filter_cutoff"         , "uint:8" , None),
    ("filter_resonance"      , "uint:8" , None),
    ("filter_mod_source"     , "uint:8" , None),
    ("filter_intensity"      , "uint:8" , None),
    ("filter_efsense"        , "uint:8" , None),
    
    ("amp_level"             , "uint:8" , None),
    ("amp_direct_level"      , "uint:8" , None),
    (None                    , "uint:7" , 0),
    ("amp_distortion"        , "uint:1" , None),
    (None                    , "uint:8" , 64),
    ("amp_key_track"         , "uint:8" , None),

    (None                    , "uint:8"  , 0),
    (None                    , "uint:8"  , 0),
    (None                    , "uint:8"  , 127),
    (None                    , "uint:8"  , 0),
    
    ("eg2_attack"            , "uint:8"  , None),
    ("eg2_decay"             , "uint:8"  , None),
    ("eg2_sustain"           , "uint:8"  , None),
    ("eg2_release"           , "uint:8"  , None),
    
    (None                    , "uint:2"  , 0),
    ("lfo1_key_sync"         , "uint:2"  , None),
    (None                    , "uint:2"  , 0),
    ("lfo1_wave"             , "uint:2"  , None),
    ("lfo1_frequency"        , "uint:8"  , None),
    ("lfo1_tempo_sync"       , "uint:1"  , None),
    (None                    , "uint:2"  , 0),
    ("lfo1_sync_note"        , "uint:5"  , None),
    
    (None                    , "uint:2"  , 0),
    ("lfo2_key_sync"         , "uint:2"  , None),
    (None                    , "uint:2"  , 0),
    ("lfo2_wave"             , "uint:2"  , None),
    ("lfo2_frequency"        , "uint:8"  , None),
    ("lfo2_tempo_sync"       , "uint:1"  , None),
    (None                    , "uint:2"  , 0),
    ("lfo2_sync_note"        , "uint:5"  , None),
]

PATTERNS_CHANNEL_LEVEL = [
    ("level"      , "uint:8", None)
]

PATTERNS_CHANNEL_PAN = [
    ("pan"        , "uint:8", None) 
]

def decode_patterns(obj, data, patterns):
    for element in patterns:
        if isinstance(element, tuple):
            field, pattern, value = element
            if field:
                print("OK: {}".format(field))
                getattr(obj, field).set_raw(data.read(pattern))
            else:
                temp = data.read(pattern)
                if temp == value:
                    print("OK: {} == {}".format(temp, value))
                    pass
                else:
                    print("WARNING: {} != {}".format(temp, value))
        else:
            n, (field, pattern, value) = element
            for i in range(n):
                getattr(obj, field)[i].set_raw(data.read(pattern))
                print("*** {}".format(getattr(obj, field)[i].raw))

def decode_8to7(data_encoded):
    data = bytearray()
    for ptr in range(0, len(data_encoded), 8):
        chunk = data_encoded[ptr : (ptr + 8)]
        bit7s = chunk[0]
        for byte8 in chunk[1:]:
            byte7 = byte8 | (0x80 if (bit7s & 0x01) else 0x00)
            data.append(byte7)
            bit7s = bit7s >> 1
    data = bitstring.ConstBitStream(data)
    return data


def _decode_patch(data):
    patch = synthesizer.Patch()
    decode_patterns(patch, data, PATTERNS_PATCH)
    return patch

def _decode_timbre(data):
    timbre = synthesizer.Timbre()
    decode_patterns(timbre, data, PATTERNS_TIMBRE)
    timbre.patches = [_decode_patch(data) for i in range(4)]
    data.read("bytes:56")
    return timbre

def _decode_channels(data):
    channels = [ synthesizer.Channel() for i in range(16) ]
    for i in range(16):
        decode_patterns(channels[i], data, PATTERNS_CHANNEL_LEVEL)
    for i in range(16):
        decode_patterns(channels[i], data, PATTERNS_CHANNEL_PAN)
    return channels

def _decode_vocoder(data):
    vocoder = synthesizer.Vocoder()
    decode_patterns(vocoder, data, PATTERNS_VOCODER)
    vocoder.channels = _decode_channels(data)
    data.read("bytes:112")
    return vocoder

def decode(data_encoded):

    data = decode_8to7(data_encoded) 

    prog = synthesizer.Program()
    prog.name = data.read("bytes:12").decode("ascii").rstrip()
    decode_patterns(prog, data, PATTERNS_PROGRAM)
    
    if prog.voice_mode.value in ["Single", "Layer"]:
        prog.timbres[0] = _decode_timbre(data)

        if prog.voice_mode.value == "Layer":
            prog.timbres[1] = _decode_timbre(data)

    elif prog.voice_mode.value == "Vocoder":
        prog.vocoder = _decode_vocoder(data)

    return prog

