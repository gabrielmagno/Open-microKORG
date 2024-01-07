use crate::{
    synthesizer::Program,
    filetype::FileType
};

fn decode_8to7(data_encoded: &[u8]) -> Vec<u8> {
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

pub struct Base;

impl FileType for Base {
    fn decode(data: &[u8]) -> Program {
        return Program { 
            data: decode_8to7(data)
        };
    }
    fn encode(program: Program) -> Vec<u8> {
        return Vec::new();
    }
}