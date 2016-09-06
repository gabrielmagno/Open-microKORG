from . import FileType

LAYOUT_PROGRAM = [
    ("Name",       "name"),
    ("Voice Mode", "voice_mode"),
    ("KBD Octave", "kbd_octave"),
    ("MOD FX", [ 
        ("Type", "modfx_type"),
        ("LFO Speed", "modfx_lfo_speed"),
        ("Effect Depth", "modfx_depth")
     ]),
    ("DELAY FX", [
        ("Type", "delayfx_type"),
        ("Tempo Sync", "delayfx_sync"),
        ("Sync Note", "delayfx_time_base"), # delayfx_sync.value == "On"
        ("Delay", "delayfx_delay_time"),    # delayfx_sync.value == "Off"
        ("Effect Depth", "delayfx_depth"),
     ]),
    ("EQ", [
        ("Low Freq.", "eq_low_freq"),
        ("Low Gain", "eq_low_gain"),
        ("High Freq.", "eq_hi_freq"),
        ("High Gain", "eq_hi_gain"),
     ]),
    ("Arpeggio", [
        ("Tempo", "arpeggio_tempo"),
        ("Arpeggiator", "arpeggio_onoff"),
        ("Latch", "arpeggio_latch"),
        ("Type", "arpeggio_type"),
        ("Resolution", "arpeggio_resolution"),
        ("Key Sync", "arpeggio_key_sync"),
        ("Range", "arpeggio_range"),
        ("Gate", "arpeggio_gate_time"),
        ("Swing", "arpeggio_swing"),
        ("Target", "arpeggio_target"),
        ("Last Step", "arpeggio_trigger_length"),
        ("Step Key", "arpeggio_trigger_pattern"),
     ]),
]

LAYOUT_TIMBRE = [
    ("Voice", [ 
        ("Voice Assign", "assign_mode"),
        ("Trigger Mode", "trigger_mode"),  # assign_mode.value in ["Mono", "Unison"]
        ("Unison Detune", "unison_detune") # assign_mode.value == "Unison"
     ]),
    ("Pitch", [
        ("Transpose", "pitch_transpose"),
        ("Tune", "pitch_tune"),
        ("Vibrato Intensity", "pitch_vibrato_int"),
        ("Portamento", "pitch_portamento_time"),
        ("Bend Range", "pitch_bend_range"),
     ]),
    ("OSC 1", [
        ("Wave", "osc1_wave"),
        ("Waveform CTRL1", "osc1_waveform_ctrl1"),
        ("Waveform CTRL2", "osc1_waveform_ctrl2"),
        ("DWGS Wave", "osc1_dwgs_wave"), # osc1_wave == "DWGS"
     ]),
    ("OSC 2", [
        ("Wave", "osc2_wave"),
        ("Osc Modulation", "osc2_mod_select"),
        ("Semitone", "osc2_semitone"),
        ("Tune", "osc2_tune"),
     ]),
    ("Mixer", [
        ("OSC 1 Level", "mixer_osc1_level"),
        ("OSC 2 Level", "mixer_osc2_level"),
        ("Noise Level", "mixer_noise_level"),
     ]),
    ("Filter", [
        ("Type", "filter_type"),
        ("Cutoff", "filter_cutoff"),
        ("Resonance", "filter_resonance"),
        ("Intensity", "filter_eg1_intensity"),
        ("Key Track", "filter_keyboard_track"),
     ]),
    ("Filter EG", [
        ("Attack", "eg1_attack"),
        ("Decay", "eg1_decay"),
        ("Sustain", "eg1_sustain"),
        ("Release", "eg1_release"),
        ("Reset", "eg1_reset"),
     ]),
    ("AMP", [
        ("Level", "amp_level"),
        ("Panpot", "amp_panpot"),
        ("Distortion", "amp_distortion"),
        ("Key Track", "amp_keyboard_track"),
     ]),
    ("AMP EG", [
        ("Attack", "eg2_attack"),
        ("Decay", "eg2_decay"),
        ("Sustain", "eg2_sustain"),
        ("Release", "eg2_release"),
        ("Reset", "eg2_reset"),
     ]),
    ("LFO1", [
        ("Wave", "lfo1_wave"),
        ("Key Sync", "lfo1_key_sync"),
        ("Tempo Sync", "lfo1_tempo_sync"),
        ("Frequency", "lfo1_frequency"), # lfo1_tempo_sync.value == "Off"
        ("Sync Note", "lfo1_sync_note"), # lfo1_tempo_sync.value == "On"
     ]),
    ("LFO2", [
        ("Wave", "lfo2_wave"),
        ("Key Sync", "lfo2_key_sync"),
        ("Tempo Sync", "lfo2_tempo_sync"),
        ("Frequency", "lfo2_frequency"), # lfo1_tempo_sync.value == "Off" 
        ("Sync Note", "lfo2_sync_note"), # lfo1_tempo_sync.value == "On"  
     ]),
]

LAYOUT_PATCH = [
    ("Source", "source"),
    ("Destination", "destination"),
    ("Intensity", "intensity")
]

LAYOUT_VOCODER = [
    ("Voice", [ 
        ("Voice Assign", "assign_mode"),
        ("Trigger Mode", "trigger_mode"),  # assign_mode.value in ["Mono", "Unison"]
        ("Unison Detune", "unison_detune") # assign_mode.value == "Unison"
     ]),
    ("Pitch", [
        ("Transpose", "pitch_transpose"),
        ("Tune", "pitch_tune"),
        ("Vibrato Intensity", "pitch_vibrato_int"),
        ("Portamento", "pitch_portamento_time"),
        ("Bend Range", "pitch_bend_range"),
     ]),
    ("OSC", [
        ("Wave", "osc1_wave"),
        ("Waveform CTRL1", "osc1_waveform_ctrl1"),
        ("Waveform CTRL2", "osc1_waveform_ctrl2"),
        ("DWGS Wave", "osc1_dwgs_wave"), # osc1_wave == "DWGS"
     ]),
    ("Mixer", [
        ("OSC1 Level", "mixer_osc1_level"),
        ("Ext1 Level", "mixer_ext1_level"),
        ("Noise Level", "mixer_noise_level"),
     ]),
    ("Filter", [
        ("Shift", "filter_shift"),
        ("Cutoff", "filter_cutoff"),
        ("Resonance", "filter_resonance"),
        ("Mod Source", "filter_mod_source"),
        ("Intensity", "filter_intensity"),
        ("E.F.Sense", "filter_efsense"),
     ]),
    ("AMP", [
        ("Level", "amp_level"),
        ("Direct Level", "amp_direct_level"),
        ("Distortion", "amp_distortion"),
        ("Key Track", "amp_key_track"),
     ]),
    ("LFO1", [
        ("Wave", "lfo1_wave"),
        ("Key Sync", "lfo1_key_sync"),
        ("Tempo Sync", "lfo1_tempo_sync"),
        ("Frequency", "lfo1_frequency"), # lfo1_tempo_sync.value == "Off"
        ("Sync Note", "lfo1_sync_note"), # lfo1_tempo_sync.value == "On"
     ]),
    ("LFO2", [
        ("Wave", "lfo2_wave"),
        ("Key Sync", "lfo2_key_sync"),
        ("Tempo Sync", "lfo2_tempo_sync"),
        ("Frequency", "lfo2_frequency"), # lfo1_tempo_sync.value == "Off" 
        ("Sync Note", "lfo2_sync_note"), # lfo1_tempo_sync.value == "On"  
     ]),
]

LAYOUT_CHANNEL = [
    ("Level", "level"),
    ("Pan", "pan")
]

def txt_encode_field(obj, field, indent=0):
    text_indent = "  "*indent

    if isinstance(field, tuple):

        field_text, field_name = field

        if isinstance(field_name, str):
            field_value = getattr(obj, field_name)
            return "{}- {:<20} : {}\n".format(text_indent, field_text, field_value)

        if isinstance(field_name, list):
            text = "{}+ {}\n".format(text_indent, field_text)
            for next_field in field_name:
                next_field_text = txt_encode_field(obj, next_field, indent+1)
                text += next_field_text
            return text

    elif isinstance(field, list):
        text = ""
        for next_field in field:
            next_field_text = txt_encode_field(obj, next_field, indent)
            text += next_field_text
            #text += "\n"
        return text

    else:
        return "ERROR"


class Text(FileType):
    
    def encode(self, prog):
        s = "\n"
        s += txt_encode_field(prog, LAYOUT_PROGRAM)
        if prog.voice_mode.value in ["Single", "Layer"]:
            for i in range(2):
                if prog.timbres[i]:
                    s += "+ Timbre {}\n".format(i+1)
                    s += txt_encode_field(prog.timbres[i], LAYOUT_TIMBRE, 1)
                    for j in range(4):
                        s += "  + Patch {}\n".format(j+1)
                        s += txt_encode_field(prog.timbres[i].patches[j], LAYOUT_PATCH, 2)
        elif prog.voice_mode.value == "Vocoder":
            s += "+ Vocoder\n"
            s += txt_encode_field(prog.vocoder, LAYOUT_VOCODER, 1)
            for j in range(16):
                s += "  + Channel {}\n".format(j+1)
                s += txt_encode_field(prog.vocoder.channels[j], LAYOUT_CHANNEL, 2)
        return s
  
