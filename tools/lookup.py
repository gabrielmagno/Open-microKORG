# Lookup

voice_mode        = ["Single", "Undefined", "Layer", "Vocoder"]

time_base         = ["1/32", "1/24", "1/16", "1/12", "3/32", "1/8", "1/6", 
                     "3/16", "1/4", "1/3", "3/8", "1/2", "2/3", "3/4", "1/1"]

delay_types       = ["Stereo", "Cross", "L-R"]

modfx_types       = ["Cho/Flg", "Ensemble", "Phaser"]

hiF               = ["1kHz", "1.25kHz", "1.5kHz", "1.75kHz", "2kHz", "2.25kHz", 
                     "2.5kHz", "2.75kHz", "3kHz", "3.25kHz", "3.5kHz", "3.75kHz", 
                     "4kHz", "4.25kHz", "4.5kHz", "4.75kHz", "5kHz", "5.25kHz", 
                     "5.5kHz", "5.75kHz", "6kHz", "7kHz", "8kHz", "9kHz", "10kHz", 
                     "11kHz", "12kHz", "14kHz", "16kHz", "18kHz"]

loF               = ["40Hz", "50Hz", "60Hz", "80Hz", "100Hz", "120Hz", "140Hz", 
                     "160Hz", "180Hz", "200Hz", "220Hz", "240Hz", "260Hz", 
                     "280Hz", "300Hz", "320Hz", "340Hz", "360Hz", "380Hz", 
                     "400Hz", "420Hz", "440Hz", "460Hz", "480Hz", "500Hz", 
                     "600Hz", "700Hz", "800Hz", "900Hz", "1000Hz"]

arp_target_timbre = ["Both", "Timbre1", "Timbre2"]

arp_types         = ["Up", "Down", "Alt1", "Alt2", "Random", "Trigger"]

arp_resolution    = ["1/24", "1/16", "1/12", "1/8", "1/6", "1/4"]

voice_mode_types  = ["Mono", "Poly", "Unison"]

trigger_mode      = ["Single", "Multi"]

osc1_waves        = ["Saw", "Square", "Triangle", "Sine", "Vox Wave", 
                     "DWGS", "Noise", "Audio In"]

osc2_mod          = ["OFF", "Ring", "Sync", "RingSync"]

osc2_waves        = ["Saw", "Square", "Triangle"]

filter_type       = ["-24dB LP", "-12dB LP",  "-12dB BP",  "-12dB HP"]

lfo_sync          = ["OFF", "Timbre", "Voice"]

lfo1_waves        = ["Saw", "Square", "Triangle", "S&H"]

lfo2_waves        = ["Saw", "Squ+", "Sine", "S&H"]

lfo_sync_note     = ["1/1", "3/4", "2/3", "1/2", "3/8", "1/3", "1/4", "3/16", 
                     "1/6", "1/8", "3/32", "1/12", "1/16", "1/24", "1/32"]

patch_source      = ["EG1", "EG2", "LFO1", "LFO2", "Velocity",
                     "Key Track", "Bend", "Mod Wheel"]

patch_destination = ["Pitch", "Osc2 Pitch", "Ctl1", "Noise", 
                     "Cutoff", "Amp", "Pan", "LFO2 Freq"]

formant_shift = ["0", "+1", "+2", "-1", "-2"]

fcmod_source = ["---", "Amp EG", "LFO 1", "LFO 2", "Velocity", 
                "Key Track", "Bend", "Mod Wheel"]

def re_range(raw_value, range_max, center=64):
    value = raw_value - center
    if value == 0:
        return 0
    elif value > 0:
        return min(value, range_max)
    else:
        return max(value, -range_max)

def re_range2(raw_value, range_max, center=64):
    return raw_value if raw_value <= range_max else (raw_value - (256-center))

def decode_pan(raw_value):
    value = re_range(raw_value, 64)
    if value == 0:
        return "CNT"
    elif value < 0:
        return "L{}".format(-value)
    else:
        return "R{}".format(value)

