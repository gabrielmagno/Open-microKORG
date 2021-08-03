trait Parameter {
    fn get_raw(&self) -> i8;
    fn get_value(&self) -> i8;
    fn set_raw(&self);
    fn set_value(&self);
}

struct ParamRange<offset, min, max> {
    raw: i8,
    value: i8
}

impl Parameter for ParamRange<offset, min, max> {
    fn get_raw(&self) -> i8 {

    }

    fn get_value(&self) -> i8 {c

    }

    fn set_raw(&self) {

    }

    fn set_value(&self) {
        
    }
}


struct Program {
    name: str,
    arpeggio_trigger_length: ParamRange<>,
    eq_hi_gain: ParamRange<>,
    eq_low_gain: ParamRange<>,
    arpeggio_range: ParamRange<>,
    arpeggio_gate_time: ParamRange<>,
    arpeggio_swing: ParamRange<>,
    kbd_octave: ParamRange<>,
}
