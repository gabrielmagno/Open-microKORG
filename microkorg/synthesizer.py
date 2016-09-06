from .parameters import *

class Program:

    def __init__(self):

        self.name = None
        
        self.arpeggio_trigger_length   = ParamRange(1, 1, 8)
        self.arpeggio_trigger_pattern  = ParamBitArray(8, invert=True)

        self.voice_mode                = ParamTable(["Single", "UNDEFINED", "Layer", "Vocoder"])

        self.delayfx_sync              = ParamOnOff()
        self.delayfx_time_base         = ParamTable(["1/32", "1/24", "1/16", "1/12", "3/32", "1/8", "1/6",
                                                "3/16", "1/4", "1/3", "3/8", "1/2", "2/3", "3/4", "1/1"])
        self.delayfx_delay_time        = ParamSimple()
        self.delayfx_depth             = ParamSimple()
        self.delayfx_type              = ParamTable(["StereoDelay", "CrossDelay", "L/R Delay"])

        self.modfx_lfo_speed           = ParamSimple()
        self.modfx_depth               = ParamSimple()
        self.modfx_type                = ParamTable(["Cho/Flg", "Ensemble", "Phaser"])

        self.eq_hi_freq                = ParamTable(["1kHz", "1.25kHz", "1.5kHz", "1.75kHz", "2kHz", "2.25kHz",
                                                     "2.5kHz", "2.75kHz", "3kHz", "3.25kHz", "3.5kHz", "3.75kHz",
                                                     "4kHz", "4.25kHz", "4.5kHz", "4.75kHz", "5kHz", "5.25kHz",
                                                     "5.5kHz", "5.75kHz", "6kHz", "7kHz", "8kHz", "9kHz", "10kHz",
                                                     "11kHz", "12kHz", "14kHz", "16kHz", "18kHz"])
        self.eq_hi_gain                = ParamRange(-64, -12, 12)
        self.eq_low_freq               = ParamTable(["40Hz", "50Hz", "60Hz", "80Hz", "100Hz", "120Hz", "140Hz",
                                                     "160Hz", "180Hz", "200Hz", "220Hz", "240Hz", "260Hz",
                                                     "280Hz", "300Hz", "320Hz", "340Hz", "360Hz", "380Hz",
                                                     "400Hz", "420Hz", "440Hz", "460Hz", "480Hz", "500Hz",
                                                     "600Hz", "700Hz", "800Hz", "900Hz", "1000Hz"])
        self.eq_low_gain               = ParamRange(-64, -12, 12)

        self.arpeggio_tempo            = ParamSimple()
        self.arpeggio_onoff            = ParamOnOff()
        self.arpeggio_latch            = ParamOnOff()
        self.arpeggio_target           = ParamTable(["Both", "Timb1", "Timb2"])
        self.arpeggio_key_sync         = ParamOnOff()
        self.arpeggio_type             = ParamTable(["Up", "Down", "Alt1", "Alt2", "Random", "Trigger"])
        self.arpeggio_range            = ParamRange(1, 1, 4)
        self.arpeggio_gate_time        = ParamRange(0, 0, 100)
        self.arpeggio_resolution       = ParamTable(["1/24", "1/16", "1/12", "1/8", "1/6", "1/4"])
        self.arpeggio_swing            = ParamRange(0, -100, 100)

        self.kbd_octave                = ParamRange(0, -3, 3)
        
        self.timbres = [None for i in range(2)]
        self.vocoder = None


class SynthBase: 
    
    def __init__(self):

        self.assign_mode           = ParamTable(["Mono", "Poly", "Unison"])
        self.eg2_reset             = ParamOnOff()
        self.trigger_mode          = ParamTable(["Single", "Multi"])
        self.unison_detune         = ParamRange(0, 0, 99)

        self.pitch_tune            = ParamRange(-64, -50, 50)
        self.pitch_bend_range      = ParamRange(-64, -12, 12)
        self.pitch_transpose       = ParamRange(-64, -24, 24)
        self.pitch_vibrato_int     = ParamRange(-64, -63, 63)
        self.pitch_portamento_time = ParamSimple()

        self.osc1_wave             = ParamTable(["Saw", "Square", "Tri", "Sin", 
                                                 "Vox Wave", "DWGS", "Noise", "Audio In"])
        self.osc1_waveform_ctrl1   = ParamSimple()
        self.osc1_waveform_ctrl2   = ParamSimple()
        self.osc1_dwgs_wave        = ParamRange(1, 1, 64)

        self.eg2_attack            = ParamSimple()
        self.eg2_decay             = ParamSimple()
        self.eg2_sustain           = ParamSimple()
        self.eg2_release           = ParamSimple()

        self.lfo1_key_sync         = ParamTable(["OFF", "Timbre", "Voice"])
        self.lfo1_wave             = ParamTable(["Saw", "Squ", "Tri", "S/H"])
        self.lfo1_frequency        = ParamSimple()
        self.lfo1_tempo_sync       = ParamOnOff()
        self.lfo1_sync_note        = ParamTable(["1/1", "3/4", "2/3", "1/2", "3/8", "1/3", "1/4", "3/16", 
                                                 "1/6", "1/8", "3/32", "1/12", "1/16", "1/24", "1/32"])

        self.lfo2_key_sync         = ParamTable(["OFF", "Timbre", "Voice"])
        self.lfo2_wave             = ParamTable(["Saw", "Squ+", "Sine", "S/H"])
        self.lfo2_frequency        = ParamSimple()
        self.lfo2_tempo_sync       = ParamOnOff()
        self.lfo2_sync_note        = ParamTable(["1/1", "3/4", "2/3", "1/2", "3/8", "1/3", "1/4", "3/16", 
                                                 "1/6", "1/8", "3/32", "1/12", "1/16", "1/24", "1/32"])


class Patch:

    def __init__(self):

        self.destination = ParamTable(["PITCH", "OSC2 PITCH", "OSC1 CNTL1", "NOISE LEVEL", 
                                       "CUTOFF", "AMP", "PAN", "LFO2 FREQ"])

        self.source      = ParamTable(["EG1", "EG2", "LFO1", "LFO2", "VELOCITY",
                                       "KBD TRACK", "P.Bend", "Mod"])

        self.intensity   = ParamRange(-64, -63, 63)


class Timbre(SynthBase):

    def __init__(self):

        super().__init__()

        self.eg1_reset             = ParamOnOff()

        self.osc2_mod_select       = ParamTable(["Off", "Ring", "Sync", "RingSync"])
        self.osc2_wave             = ParamTable(["Saw", "Square", "Tri"])
        self.osc2_semitone         = ParamRange(-64, -24, 24)
        self.osc2_tune             = ParamRange(-64, -63, 63)

        self.mixer_osc1_level      = ParamSimple()
        self.mixer_osc2_level      = ParamSimple()
        self.mixer_noise_level     = ParamSimple()

        self.filter_type           = ParamTable(["24LPF", "12LPF",  "12BPF",  "12HPF"])
        self.filter_cutoff         = ParamSimple()
        self.filter_resonance      = ParamSimple()
        self.filter_eg1_intensity  = ParamRange(-64, -63, 63)
        self.filter_keyboard_track = ParamRange(-64, -63, 63)

        self.amp_level             = ParamSimple()
        self.amp_panpot            = ParamPan(-64, -64, 63)
        self.amp_distortion        = ParamOnOff()
        self.amp_keyboard_track    = ParamRange(-64, -63, 63)

        self.eg1_attack            = ParamSimple()
        self.eg1_decay             = ParamSimple()
        self.eg1_sustain           = ParamSimple()
        self.eg1_release           = ParamSimple()

        #self.patches = [Patch() for i in range(4)]
        self.patches = [None for i in range(4)]


class Channel:

    def __init__(self):
        self.level = ParamSimple()
        self.pan   = ParamPan(-64, -63, 63)


class Vocoder(SynthBase):

    def __init__(self):

        super().__init__()

        self.audioin1_hpf_gate   = ParamTable(["Dis", "Ena"])
        self.audioin1_hpf_level  = ParamSimple()
        self.audioin1_gate_sense = ParamSimple()
        self.audioin1_threshold  = ParamSimple()

        self.mixer_osc1_level    = ParamSimple()
        self.mixer_ext1_level    = ParamSimple()
        self.mixer_noise_level   = ParamSimple()

        self.filter_shift        = ParamTable(["0", "+1", "+2", "-1", "-2"])
        self.filter_cutoff       = ParamRange(-64, -63, 63)
        self.filter_resonance    = ParamSimple()
        self.filter_mod_source   = ParamTable(["---", "AEG", "LFO1", "LFO2", 
                                               "VELOCITY", "KBD TRACK", "P.Bend", "Mod"])
        self.filter_intensity    = ParamRange(-64, -63, 63)
        self.filter_efsense      = ParamEFSense()

        self.amp_level           = ParamSimple()
        self.amp_direct_level    = ParamSimple()
        self.amp_distortion      = ParamOnOff()
        self.amp_key_track       = ParamRange(-64, -63, 63)

        self.channels            = [ None for i in range(16) ]

        self.ef_hold_level       = [] # TODO

