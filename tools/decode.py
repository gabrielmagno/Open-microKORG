import json
import collections

import lookup as lkp

def extract_bits(word, i_f, i_t):
    return (word >> i_f) & ((1 << (i_t - i_f + 1)) - 1)

def decode_8to7(data_encoded):
    data = bytearray()
    for ptr in range(0, len(data_encoded), 8):
        chunk = data_encoded[ptr : (ptr + 8)]
        bit7s = chunk[0]
        for byte8 in chunk[1:]:
            byte7 = byte8 | (0x80 if (bit7s & 0x01) else 0x00)
            data.append(byte7)
            bit7s = bit7s >> 1
    return data


# Load information

def collect_generics(data_full):

    data = data_full

    info = collections.defaultdict(dict)
    
    info["NAME"] = data[0:11].decode("ascii").rstrip()
   
    voice = lkp.voice_mode[extract_bits(data[16], 4, 5)]
    info["EXTRA"]["Voice Mode"] = "Vocoder" if voice == "Vocoder" else "Synthesizer"
    if voice in ["Single", "Layer"]:
        info["EXTRA"]["Voice Synth. Type"] = voice
    info["EXTRA"]["Arp. Pattern"] = [ not extract_bits(data[15], i, i) for i in range(8) ]
    info["EXTRA"]["Arp. State"] =  bool(extract_bits(data[32], 7, 7))
    info["EXTRA"]["KBD Octave"] =  data[37]
    
    info["MOD FX"] = {
      "TYPE"         : lkp.modfx_types[data[25]],
      "LFO SPEED"    : data[23],
      "EFFECT DEPTH" : data[24]
    }
    
    info["DELAY"]["TYPE"]           = lkp.delay_types[data[22]]
    info["DELAY"]["TEMPO SYNC"]     = bool(extract_bits(data[19], 7, 7))
    if info["DELAY"]["TEMPO SYNC"]:
        info["DELAY"]["SYNC NOTE"]  = lkp.time_base[extract_bits(data[19], 0, 3)]
    else:
        info["DELAY"]["DELAY TIME"] = data[20]
    info["DELAY"]["DELAY DEPTH"]    = data[21]
    
    info["EQ"] = {
      "LOW EQ FREQ." : lkp.loF[data[28]],
      "LOW EQ GAIN"  : lkp.re_range(data[29], 12),
      "HI EQ FREQ."  : lkp.hiF[data[26]],
      "HI EQ GAIN"   : lkp.re_range(data[27], 12) 
    }
    
    info["ARPEG. A"] = {
      "TEMPO"      : 256*data[30] + data[31],
      "RESOLUTION" : lkp.arp_resolution[data[35]],
      "GATE"       : max(data[34], 100),
      "TYPE"       : lkp.arp_types[extract_bits(data[33], 0, 3)],
      "RANGE"      : 1 + extract_bits(data[33], 4, 7)
    }
    
    info["ARPEG. B"] = {
      "LATCH"         : bool(extract_bits(data[32], 6, 6)),
      "SWING"         : data[36] if data[36] <= 100 else (data[36] - 256),
      "KEY SYNC"      : bool(extract_bits(data[32], 0, 0)),
      "LAST STEP"     : 1 + extract_bits(data[14], 0, 2),
      "TARGET TIMBRE" : lkp.arp_target_timbre[extract_bits(data[32], 4, 5)] 
    }
    
    return info


def collect_timbre(data_full, start):

    data = data_full[start:]

    info = collections.defaultdict(dict)

    voice                               =  lkp.voice_mode[extract_bits(data_full[16], 4, 5)]
    info["VOICE"]["SYNTH/VOCODER"]      =  "Vocoder" if voice == "Vocoder" else "Synthesizer"
    if voice in ["Single", "Layer"]:
        info["VOICE"]["SINGLE/LAYER"]   =  voice
    info["VOICE"]["VOICE ASSIGN"]       =  lkp.voice_mode_types[extract_bits(data[1], 6, 7)]
    if info["VOICE"]["VOICE ASSIGN"] in ["Mono", "Unison"]:
        info["VOICE"]["TRIGGER MODE"]   =  lkp.trigger_mode[extract_bits(data[1], 3, 3)]
    if info["VOICE"]["VOICE ASSIGN"] == "Unison":
        info["VOICE"]["UNISON DETUNE"]  =  data[2]

    info["PITCH"] = { 
      "TRANSPOSE"   : lkp.re_range(data[5], 24),
      "TUNE"        : lkp.re_range(data[3], 50),
      "PORTAMENTO"  : extract_bits(data[15], 0, 6),
      "BEND RANGE"  : lkp.re_range(data[4], 12),
      "VIBRATO INT" : lkp.re_range(data[6], 63)
    }

    info["OSC1"]["WAVE"]                =  lkp.osc1_waves[extract_bits(data[7], 0, 2)]
    info["OSC1"]["CONTROL 1"]           =  data[8]
    info["OSC1"]["CONTROL 2"]           =  data[9]
    if info["OSC1"]["WAVE"] == "DWGS":
        info["OSC1"]["CONTROL 2"]       =  data[10] + 1

    info["OSC2"] = {
      "WAVE"     : lkp.osc2_waves[extract_bits(data[12], 0, 1)],
      "OSC MOD"  : lkp.osc2_mod[extract_bits(data[12], 4, 5)],
      "SEMITONE" : lkp.re_range(data[13], 24),
      "TUNE"     : lkp.re_range(data[14], 63)
    }

    info["MIXER"] = {
      "OSC 1 LEVEL" : data[16],
      "OSC 2 LEVEL" : data[17],
      "NOISE LEVEL" : data[18]
    }

    info["FILTER"] = {
      "TYPE"             : lkp.filter_type[data[19]],
      "CUTOFF"           : data[20],
      "RESONANCE"        : data[21],
      "FILTER EG INT"    : lkp.re_range(data[22], 63),
      "FILTER KEY TRACK" : lkp.re_range(data[24], 63)
    }

    info["FILTER EG"] = {
      "ATTACK"   : data[30],
      "DECAY"    : data[31],
      "SUSTAIN"  : data[32],
      "RELEASE"  : data[33],
      "EG RESET" : bool(extract_bits(data[1], 4, 4))
    }

    info["AMP"] = {
      "LEVEL"      : data[25],
      "PANPOT"     : lkp.decode_pan(data[26]),
      "DISTORTION" : bool(extract_bits(data[27], 0, 0)),
      "KBD TRACK"  : lkp.re_range(data[29], 63)
    }

    info["AMP EG"] = {
      "ATTACK"   : data[34],
      "DECAY"    : data[35],
      "SUSTAIN"  : data[36],
      "RELEASE"  : data[37],
      "EG RESET" : bool(extract_bits(data[1], 5, 5))
    }

    info["LFO 1"]["WAVE"]            =  lkp.lfo1_waves[extract_bits(data[38], 0, 1)]
    info["LFO 1"]["KEY SYNC"]        =  lkp.lfo_sync[extract_bits(data[38], 4, 5)]
    info["LFO 1"]["TEMPO SYNC"]      =  bool(extract_bits(data[40], 7, 7))
    if info["LFO 1"]["TEMPO SYNC"]:
        info["LFO 1"]["SYNC NOTE"]   =  lkp.lfo_sync_note[extract_bits(data[40], 0, 4)]
    else:
        info["LFO 1"]["FREQUENCY"]   =  data[39]

    info["LFO 2"]["WAVE"]            =  lkp.lfo2_waves[extract_bits(data[41], 0, 1)]
    info["LFO 2"]["KEY SYNC"]        =  lkp.lfo_sync[extract_bits(data[41], 4, 5)]
    info["LFO 2"]["TEMPO SYNC"]      =  bool(extract_bits(data[43], 7, 7))
    if info["LFO 2"]["TEMPO SYNC"]:
        info["LFO 2"]["SYNC NOTE"]   =  lkp.lfo_sync_note[extract_bits(data[43], 0, 4)]
    else:
        info["LFO 2"]["FREQUENCY"]   =  data[42]

    info["PATCHES"] = [ { 
        "SOURCE"  : lkp.patch_source[extract_bits(data[44+(i*2)], 0, 3)],
        "DEST"    : lkp.patch_destination[extract_bits(data[44+(i*2)], 4, 7)],
        "MOD INT" : lkp.re_range(data[45+(i*2)], 63) 
      } for i in range(4) 
    ]

    return info


def collect_vocoder(data_full, start):

    data = data_full[start:]

    info = collections.defaultdict(dict)

    voice                               =  lkp.voice_mode[extract_bits(data_full[16], 4, 5)]
    info["VOICE"]["SYNTH/VOCODER"]      =  "Vocoder" if voice == "Vocoder" else "Synthesizer"
    if voice in ["Single", "Layer"]:
        info["VOICE"]["SINGLE/LAYER"]   =  voice
    info["VOICE"]["VOICE ASSIGN"]       =  lkp.voice_mode_types[extract_bits(data[1], 6, 7)]
    if info["VOICE"]["VOICE ASSIGN"] in ["Mono", "Unison"]:
        info["VOICE"]["TRIGGER MODE"]   =  lkp.trigger_mode[extract_bits(data[1], 3, 3)]
    if info["VOICE"]["VOICE ASSIGN"] == "Unison":
        info["VOICE"]["UNISON DETUNE"]  =  data[2]

    info["PITCH"] = {
      "TRANSPOSE"   : lkp.re_range(data[5], 24),
      "TUNE"        : lkp.re_range(data[3], 50),
      "PORTAMENTO"  : extract_bits(data[14], 0, 6),
      "BEND RANGE"  : lkp.re_range(data[4], 12),
      "VIBRATO INT" : lkp.re_range(data[6], 63)
    }

    info["OSC"]["WAVE"]                =  lkp.osc1_waves[extract_bits(data[7], 0, 2)]
    info["OSC"]["CONTROL 1"]           =  data[8]
    info["OSC"]["CONTROL 2"]           =  data[9]
    if info["OSC"]["WAVE"] == "DWGS":
        info["OSC"]["CONTROL 2"]       =  data[10] + 1

    info["AUDIO IN1"] = {
      "GATE SENSE" : data[19],
      "THRESHOLD"  : data[20],
      "HPF LEVEL"  : data[18],
      "HPF GATE"   : bool(extract_bits(data[12], 0, 0))
    }
    
    info["MIXER"] = {
      "OSC 1 LEVEL" : data[15],
      "INST LEVEL"  : data[16],
      "NOISE LEVEL" : data[17]
    }
    
    info["FILTER"] = {
      "FORMANT SHIFT" : lkp.formant_shift[data[21]],
      "CUTOFF"        : lkp.re_range(data[22], 63),
      "RESONANCE"     : data[23],
      "E.F.SENSE"     : "{}".format(data[26]) if data[26] < 127 else "Hold"
    }
     
    info["FC MOD"] = {
      "SOURCE"    : lkp.fcmod_source[data[24]],
      "INTENSITY" : lkp.re_range(data[25], 63)
    }
     
    info["AMP"] = {
      "LEVEL"        : data[27],
      "DIRECT LEVEL" : data[28],
      "DISTORTION"   : bool(extract_bits(data[29], 0, 0)),
      "KBD TRACK"    : lkp.re_range(data[31], 63)
    }

    info["AMP EG"] = {
      "ATTACK"   : data[36],
      "DECAY"    : data[37],
      "SUSTAIN"  : data[38],
      "RELEASE"  : data[39]
    }

    info["LFO 1"]["WAVE"]            =  lkp.lfo1_waves[extract_bits(data[40], 0, 1)]
    info["LFO 1"]["KEY SYNC"]        =  lkp.lfo_sync[extract_bits(data[40], 4, 5)]
    info["LFO 1"]["TEMPO SYNC"]      =  bool(extract_bits(data[42], 7, 7))
    if info["LFO 1"]["TEMPO SYNC"]:
        info["LFO 1"]["SYNC NOTE"]   =  lkp.lfo_sync_note[extract_bits(data[42], 0, 4)]
    else:
        info["LFO 1"]["FREQUENCY"]   =  data[41]

    info["LFO 2"]["WAVE"]            =  lkp.lfo2_waves[extract_bits(data[43], 0, 1)]
    info["LFO 2"]["KEY SYNC"]        =  lkp.lfo_sync[extract_bits(data[43], 4, 5)]
    info["LFO 2"]["TEMPO SYNC"]      =  bool(extract_bits(data[45], 7, 7))
    if info["LFO 2"]["TEMPO SYNC"]:
        info["LFO 2"]["SYNC NOTE"]   =  lkp.lfo_sync_note[extract_bits(data[45], 0, 4)]
    else:
        info["LFO 2"]["FREQUENCY"]   =  data[44]

    info["CHANNELS LEVEL"] = [ data[46+i] for i in range(16) ]
    info["CHANNELS PAN"] = [ lkp.decode_pan(data[62+i]) for i in range(16) ]

    return info


def collect_all(data):

    info = collect_generics(data)

    if info["EXTRA"]["Voice Mode"] == "Synthesizer":
        info["TIMBRES"] = [
            collect_timbre(data, 38)
        ]

        if info["EXTRA"]["Voice Mode"] == "Layer":
            info["TIMBRES"].append(collect_timbre(data, 146))

    else:
        info["VOCODER"] = collect_vocoder(data, 38)

    return info

if __name__ == "__main__":

    import sys

    #with open("dumps/original-p_a11.syx", "rb") as infile:
    #with open("dumps/init_prog.prg", "rb") as infile:
    with open(sys.argv[1], "rb") as infile:
        data_raw = infile.read()
        #data_encoded = data_raw[5:296]
        data_encoded = data_raw[30:296]
        data = decode_8to7(data_encoded)

    info = collect_all(data)
    
    print(json.dumps(info, indent=4))
    
