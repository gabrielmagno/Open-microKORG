use std::io::prelude::*;
use std::fs::File;
use std::cmp::*;
use std::convert::TryInto;
use std::collections::HashMap;

trait Parameter<T> {
    fn get_raw(&self) -> i8;
    fn get_value(&self) -> T;
    fn set_raw(&mut self, raw: i8);
    fn set_value(&mut self, value: T);
}

struct ParamSimple {
    raw: i8,
    value: i8
}

impl Parameter<i8> for ParamSimple {
    fn get_raw(&self) -> i8 { self.raw }
    fn get_value(&self) -> i8  { self.value }
    fn set_raw(&mut self, raw: i8) { self.raw = raw; self.value = raw; }
    fn set_value(&mut self, value: i8) { self.raw = value; self.value = value;}
}

#[derive(Copy, Clone)]
enum ParamOnOffValue {
    Off,
    On,
}

struct ParamOnOff {
    raw: i8,
    value: ParamOnOffValue
}

impl Parameter<ParamOnOffValue> for ParamOnOff {
    fn get_raw(&self) -> i8 { self.raw }
    fn get_value(&self) -> ParamOnOffValue  { self.value }
    fn set_raw(&mut self, raw: i8) { 
        self.raw = raw; 
        self.value = match raw {
            0 => ParamOnOffValue::Off,
            _ => ParamOnOffValue::On,
        };
    }
    fn set_value(&mut self, value: ParamOnOffValue) { 
        self.value = value;
        self.raw = match value {
            ParamOnOffValue::Off => 0,
            ParamOnOffValue::On  => 1,
        };
    }
}


#[derive(Debug)]
struct ParamRange<const OFFSET: i8, const MIN: i8, const MAX: i8> {
    raw: i8,
    value: i8
}

impl<const OFFSET: i8, const MIN: i8, const MAX: i8> Parameter<i8> for ParamRange<OFFSET, MIN, MAX> {

    fn get_raw(&self) -> i8 { self.raw }
    fn get_value(&self) -> i8  { self.value }

    fn set_raw(&mut self, raw: i8) {
        self.raw = raw;
        let value = raw + OFFSET;
        self.value = if value > 0 { min(value, MAX) } else { max(value, MIN) };
    }

    fn set_value(&mut self, value: i8) {
        self.value = if value > 0 { min(value, MAX) } else { max(value, MIN) };
        self.raw = value - OFFSET
    }
}

// trait TableValues {
//     fn set_table_values(&mut self, values: Vec<String>);
// }

// #[derive(Debug)]
// struct ParamTable {
//     table_decode: HashMap<i8, String>,
//     table_encode: HashMap<String, i8>,
//     raw: i8,
//     value: String
// }

// impl TableValues for ParamTable {
//     fn set_table_values(&mut self, values: Vec<String>) {
//         for (i, value) in values.iter().enumerate() {
//             self.table_decode.insert(i as i8, value.to_string());
//             self.table_encode.insert(value.to_string(), i as i8);
//         }
//     }
// }

// impl Parameter<String> for ParamTable {

//     fn get_raw(&self) -> i8 { self.raw }
//     fn get_value(&self) -> String  { self.value.to_string() }

//     fn set_raw(&mut self, raw: i8) {
//         self.raw = raw;
//         self.value = self.table_decode[&raw].to_string();
//     }

//     fn set_value(&mut self, value: String) {
//         self.raw = self.table_encode[&(value.to_string())];
//         self.value = value;
//     }
// }

// trait TableValues {
//     const VALUES: &'static [&'static str];
//     fn insert_decode(&mut self, i: i8, value: String);
//     fn insert_encode(&mut self, value: String, i: i8);
//     fn set_table_values(&mut self) {
//         for (i, value) in self.VALUES.iter().enumerate() {
//             self.insert_decode(i as i8, value.to_string());
//             self.insert_encode(value.to_string(), i as i8);
//         }
//     }
// }

trait TableValues {
    const VALUES: &'static [&'static str];
}

trait TableMod {
    const VALUES: &'static [&'static str];
    fn insert_decode(&mut self, i: i8, value: String);
    fn insert_encode(&mut self, value: String, i: i8);
    fn set_table_values(&mut self);
}

struct ParamTable {
    table_decode: HashMap<i8, String>,
    table_encode: HashMap<String, i8>,
    raw: i8,
    value: String
}

struct ParamVoiceMode;
impl TableMod for ParamVoiceMode {

    const VALUES: &'static [&'static str] = &["Single", "UNDEFINED", "Layer", "Vocoder"];

    fn insert_decode(&mut self, i: i8, value: String) {

    }
    
    fn insert_encode(&mut self, value: String, i: i8) {

    }
    
    fn set_table_values(&mut self) {

    }
}

struct Program {
    arpeggio_trigger_length: ParamRange<1, 1, 8>,
    eq_hi_gain: ParamRange<-64, -12, 12>,
    eq_low_gain: ParamRange<-64, -12, 12>,
    arpeggio_range: ParamRange<1, 1, 4>,
    arpeggio_gate_time: ParamRange<0, 0, 100>,
    arpeggio_swing: ParamRange<0, -100, 100>,
    kbd_octave: ParamRange<0, -3, -3>,
}


fn read_file(file_name: &str) -> Vec<u8> {

    let mut f = File::open(file_name)
        .expect(&format!("file not found: {}", file_name));

    let mut data_raw = Vec::new();
    f.read_to_end(&mut data_raw)
       .expect(&format!("cannot read file {}", file_name));

    return data_raw
}

fn frame_raw_data(data_raw: &Vec<u8>) -> (Vec<u8>, Vec<u8>) {

    let header = data_raw[..4].to_vec();
    let data_encoded = data_raw[5..296].to_vec();

    return (header, data_encoded)
}

fn decode_8to7(data_encoded: &Vec<u8>) -> Vec<u8> {
    let mut data = Vec::new();
    for bytes_chunk in data_encoded.chunks(8) {
        let mut bit7s = bytes_chunk[0];
        for byte8 in bytes_chunk.iter().skip(1) {
            let byte7 = byte8 | if (bit7s & 0x01) == 1 { 0x80 } else { 0x00 };
            data.push(byte7);
            bit7s = bit7s >> 1;
        }
    }
    return data
}

fn main() {

    let data_raw = read_file("data/original-p_a11.syx");

    let (header, data_encoded) = frame_raw_data(&data_raw);
    println!("\n\nHeader: {:02x?}", header);
    println!("Data ({}): {:02x?}", data_encoded.len(), data_encoded);

    let data = decode_8to7(&data_encoded);
    println!("Result ({}): {:02x?}", data.len(), data);

    let mut my_parameter: ParamRange<-64, -12, 12> = ParamRange { raw: 0, value: 33 };

    my_parameter.set_raw(64);
    println!("{:?}", my_parameter);

    my_parameter.set_raw(64 + 1);
    println!("{:?}", my_parameter);

    my_parameter.set_raw(64 + 2);
    println!("{:?}", my_parameter);

    my_parameter.set_raw(64 -1);
    println!("{:?}", my_parameter);

    // let mut my_table_parameter: ParamTable{};
    // //let table = !vec[ "Single".to_string(), "UNDEFINED".to_string(), "Layer".to_string(), "Vocoder".to_string()];
    // let table = ["Single", "UNDEFINED", "Layer", "Vocoder"].iter().map(|&s| s.into()).collect();
    // my_table_parameter.set_table_values(table);
    // my_table_parameter.set_raw(1);
    // println!("{:?}", my_table_parameter);
}