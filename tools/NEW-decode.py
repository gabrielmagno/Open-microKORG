import json
import collections
import bitstring

import lookup as lkp

def h2i(hex_str):
    return int(hex_str, 0)

def i2b(x):
    return "{0:08b}".format(x)

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

#with open("dumps/original-p_a11.syx", "rb") as infile:
with open("dumps/init_prog.prg", "rb") as infile:
    data_raw = infile.read()
    #data_encoded = data_raw[5:296]
    data_encoded = data_raw[30:296]
    data = decode_8to7(data_encoded)
    mydata = bitstring.BitStream(data)
    print(data)
    print(mydata)

#print(len(data_raw))
#print(len(data_encoded))
#print(len(data))



# Load information


## Generic

def collect_generics(data_full):

    data = data_full

    info = collections.defaultdict(dict)
    
    info["name"] = data[0:11].decode("ascii").rstrip()
    
    info["Arp. Pattern"] = [ not extract_bits(data[15], i, i) for i in range(8) ]
    info["Arp. State"] =  bool(extract_bits(data[32], 7, 7))
    info["KBD Octave"] =  data[37]
    
    info["MOD FX"]["TYPE"]         = lkp.modfx_types[data[25]]
    info["MOD FX"]["LFO SPEED"]    = data[23]
    info["MOD FX"]["EFFECT DEPTH"] = data[24]
    
    info["DELAY"]["TYPE"]           = lkp.delay_types[data[22]]
    info["DELAY"]["TEMPO SYNC"]     = bool(extract_bits(data[19], 7, 7))
    if info["DELAY"]["TEMPO SYNC"]:
        info["DELAY"]["SYNC NOTE"]  = lkp.time_base[extract_bits(data[19], 0, 3)]
    else:
        info["DELAY"]["DELAY TIME"] = data[20]
    info["DELAY"]["DELAY DEPTH"]    = data[21]
    
    info["EQ"]["LOW EQ FREQ."] = lkp.loF[data[28]]
    info["EQ"]["LOW EQ GAIN"]  = lkp.re_range(data[29], 12)    
    info["EQ"]["HI EQ FREQ."]  = lkp.hiF[data[26]]
    info["EQ"]["HI EQ GAIN"]   = lkp.re_range(data[27], 12) 
    
    info["ARPEG. A"]["TEMPO"]      = 256*data[30] + data[31]
    info["ARPEG. A"]["RESOLUTION"] = lkp.arp_resolution[data[35]]
    info["ARPEG. A"]["GATE"]       = max(data[34], 100)
    info["ARPEG. A"]["TYPE"]       = lkp.arp_types[extract_bits(data[33], 0, 3)]
    info["ARPEG. A"]["RANGE"]      = 1 + extract_bits(data[33], 4, 7)
    
    info["ARPEG. B"]["LATCH"]         = bool(extract_bits(data[32], 6, 6))
    info["ARPEG. B"]["SWING"]         = data[36] if data[36] <= 100 else (data[36] - 256)
    #info["ARPEG. B"]["SWING"]         = lkp.re_range(data[36], 100, 0)
    info["ARPEG. B"]["KEY SYNC"]      = bool(extract_bits(data[32], 0, 0))
    info["ARPEG. B"]["LAST STEP"]     = 1 + extract_bits(data[14], 0, 2)
    info["ARPEG. B"]["TARGET TIMBRE"] = lkp.arp_target_timbre[extract_bits(data[32], 4, 5)] 
    
    return info


def collect_timbre(data_full, start):

    data = data_full[start:]

    info = collections.defaultdict(dict)

    voice = lkp.voice_mode[extract_bits(data_full[16], 4, 5)]
    info["VOICE"]["SYNTH/VOCODER"] = "Vocoder" if voice == "Vocoder" else "Synthesizer"
    if voice in ["Single", "Layer"]:
        info["VOICE"]["SINGLE/LAYER"] = voice
    info["VOICE"]["VOICE ASSIGN"] = lkp.voice_mode_types[extract_bits(data[1], 6, 7)]
    if info["VOICE"]["VOICE ASSIGN"] in ["Mono", "Unison"]:
        info["VOICE"]["TRIGGER MODE"] = lkp.trigger_mode[extract_bits(data[1], 3, 3)]
    if info["VOICE"]["VOICE ASSIGN"] == "Unison":
        info["VOICE"]["UNISON DETUNE"] = data[2]

    info["PITCH"]["TRANSPOSE"] = lkp.re_range(data[5], 24)
    info["PITCH"]["TUNE"] = lkp.re_range(data[3], 50)
    info["PITCH"]["PORTAMENTO"] = extract_bits(data[15], 0, 6) 
    info["PITCH"]["BEND RANGE"] = lkp.re_range(data[4], 12)
    info["PITCH"]["VIBRATO INT"] = lkp.re_range(data[6], 63)
    
    info["OSC1"]["WAVE"] = lkp.osc1_waves[extract_bits(data[7], 0, 2)]
    info["OSC1"]["CONTROL 1"] = data[8] 
    info["OSC1"]["CONTROL 2"] = data[9]
    if info["OSC1"]["WAVE"] == "DWGS":
        info["OSC1"]["CONTROL 2"] = data[10] + 1
    
    info["OSC2"]["WAVE"] = lkp.osc2_waves[extract_bits(data[12], 0, 1)]
    info["OSC2"]["OSC MOD"] = lkp.osc2_mod[extract_bits(data[12], 4, 5)]
    info["OSC2"]["SEMITONE"] = lkp.re_range(data[13], 24) 
    info["OSC2"]["TUNE"] = lkp.re_range(data[13], 63)
    
    #info["MIXER"]["OSC 1 LEVEL"] = 
    #info["MIXER"]["OSC 2 LEVEL"] = 
    #info["MIXER"]["NOISE LEVEL"] = 
    
    #info["FILTER"]["TYPE"] = 
    #info["FILTER"]["CUTOFF"] = 
    #info["FILTER"]["RESONANCE"] = 
    #info["FILTER"]["FILTER EG INT"] = 
    #info["FILTER"]["FILTER KEY TRACK"] = 
    
    #info["FILTER EG"]["ATTACK"] = 
    #info["FILTER EG"]["DECAY"] = 
    #info["FILTER EG"]["SUSTAIN"] = 
    #info["FILTER EG"]["RELEASE"] = 
    info["FILTER EG"]["EG RESET"] = bool(extract_bits(data[1], 4, 4)) 
    
    #info["AMP"]["LEVEL"] = 
    #info["AMP"]["PANPOT"] = 
    #info["AMP"]["DISTORTION"] = 
    #info["AMP"]["KBD TRACK"] = 
    
    #info["AMP EG"]["ATTACK"] = 
    #info["AMP EG"]["DECAY"] = 
    #info["AMP EG"]["SUSTAIN"] = 
    #info["AMP EG"]["RELEASE"] = 
    info["AMP EG"]["EG RESET"] = bool(extract_bits(data[1], 5, 5)) 
    
    #info["LFO 1"]["WAVE"] = 
    #info["LFO 1"]["KEY SYNC"] = 
    #info["LFO 1"]["TEMPO SYNC"] = 
    #info["LFO 1"]["FREQUENCY/SYNC NOTE"] = 
    
    #info["LFO 2"]["WAVE"] = 
    #info["LFO 2"]["KEY SYNC"] = 
    #info["LFO 2"]["TEMPO SYNC"] = 
    #info["LFO 2"]["FREQUENCY/SYNC NOTE"] = 
    
    #info["PATCH"]["SOURCE"] = 
    #info["PATCH"]["DEST"] = 
    #info["PATCH"]["MOD INT"] = 

    return info


info = collect_generics(data)
timbre1 = collect_timbre(data, 38)


## Voices

#info["EXTRA"] = i2b(extract_bits(data[20], 0, 7))
#info["EXTRA"] = data[37]
#print(json.dumps(info, indent=4))
#import yaml
#print(yaml.dump(info))

timbre1["EXTRA"] = data[38:][0]
print(json.dumps(timbre1, indent=4))

